"""
EEWS Performance Analyzer
Analyzes Earthquake Early Warning System performance by comparing 
catalog data with EEW results.

Usage:
    python eews_analyzer.py [data_file] [min_magnitude] [max_depth] [year]
    
    If no arguments provided, interactive mode will prompt for values.
    
Examples:
    python eews_analyzer.py EEW_ALL-2014-2025.txt 5.0 40.0 2025    # Specify file and filters
    python eews_analyzer.py                                    # Interactive mode
"""

import numpy as np
import pandas as pd
from datetime import datetime
import math
import sys
from typing import Tuple, Dict, List


class EEWSAnalyzer:
    """Analyzes EEWS performance data"""
    
    def __init__(self, data_file: str, boundary_file: str = "taiwan.txt"):
        """
        Initialize analyzer with data file.
        
        Args:
            data_file: Path to EEW_ALL-[year1]-[year2].txt file
            boundary_file: Path to boundary coordinates file (default: taiwan.txt)
        """
        self.data_file = data_file
        self.boundary_file = boundary_file
        self.df = None
        self.results = {}
        self.boundary_lons = []
        self.boundary_lats = []
        self.near_coast_line_dis = 1.0  # km
        
        # Load boundary data if file exists
        self._load_boundary_data()
    
    def _load_boundary_data(self):
        """Load Taiwan boundary coordinates from file"""
        try:
            with open(self.boundary_file, 'r') as f:
                for line in f:
                    data = line.split()
                    if len(data) >= 2:
                        self.boundary_lons.append(float(data[0]))
                        self.boundary_lats.append(float(data[1]))
        except FileNotFoundError:
            print(f"Warning: Boundary file '{self.boundary_file}' not found. Inland/offshore analysis will be skipped.")
    
    def check_inland(self, lon: float, lat: float) -> bool:
        """
        Check if earthquake location is inland (within Taiwan boundary).
        Uses the same algorithm as ana_forplot.py check_seis_r function.
        
        The algorithm checks if the earthquake location is surrounded by boundary points
        in all four quadrants, or if it's very close to any boundary point.
        
        Args:
            lon: Longitude of earthquake
            lat: Latitude of earthquake
            
        Returns:
            True if inland, False if offshore
        """
        if not self.boundary_lons:
            return None  # No boundary data available
        
        # Following ana_forplot.py logic: accumulate quadrant information
        # across all boundary points
        sta = [0, 0, 0, 0, 0]
        result = 0
        
        for i in range(len(self.boundary_lons)):
            x = self.boundary_lons[i] - lon
            y = self.boundary_lats[i] - lat
            dist = self.calculate_distance(lat, lon, self.boundary_lats[i], self.boundary_lons[i])
            
            # Check and accumulate quadrants (cumulative across all boundary points)
            if x > 0 and y > 0:
                sta[0] = 1
            if x < 0 and y < 0:
                sta[1] = 1
            if x > 0 and y < 0:
                sta[2] = 1
            if x < 0 and y > 0:
                sta[3] = 1
            if dist < self.near_coast_line_dis:
                sta[4] = 1
            
            # Check if all quadrants are covered or very close to any boundary point
            check = sta[0] * sta[1] * sta[2] * sta[3]
            
            if check == 1 or sta[4] == 1:
                result = 1
                break
        
        return result == 1
        
    def load_data(self) -> pd.DataFrame:
        """Load and parse the EEWS data file"""
        # Read the data file
        data = []
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Skip header
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 7:  # At least catalog data
                    row = {
                        'Type': parts[0],
                        'ID': parts[1],
                        'Origin_Time': parts[2],
                        'Cat_Lon': float(parts[3]),
                        'Cat_Lat': float(parts[4]),
                        'Cat_Mag': float(parts[5]),
                        'Cat_Depth': float(parts[6])
                    }
                    
                    # Add EEW data if available (Type contains 'Y')
                    if 'Y' in parts[0] and len(parts) >= 12:
                        row['EEW_Lon'] = float(parts[7])
                        row['EEW_Lat'] = float(parts[8])
                        row['EEW_Mag'] = float(parts[9])
                        row['EEW_Depth'] = float(parts[10])
                        row['Processing_Time'] = float(parts[11])
                    else:
                        row['EEW_Lon'] = np.nan
                        row['EEW_Lat'] = np.nan
                        row['EEW_Mag'] = np.nan
                        row['EEW_Depth'] = np.nan
                        row['Processing_Time'] = np.nan
                    
                    data.append(row)
        
        self.df = pd.DataFrame(data)
        
        # Add inland/offshore classification
        if self.boundary_lons:
            self.df['Is_Inland'] = self.df.apply(
                lambda row: self.check_inland(row['Cat_Lon'], row['Cat_Lat']),
                axis=1
            )
        
        return self.df
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate epicentral distance in km using simplified method.
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in km
        """
        avlat = 0.5 * (lat1 + lat2)
        a = 1.840708 + avlat * (0.0015269 + avlat * (-0.00034 + avlat * 1.02337e-6))
        b = 1.843404 + avlat * (-6.93799e-5 + avlat * (8.79993e-6 + avlat * (-6.47527e-8)))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        dx = a * dlon * 60.0
        dy = b * dlat * 60.0
        delta = math.sqrt(dx * dx + dy * dy)
        return delta
    
    def calculate_errors(self) -> pd.DataFrame:
        """Calculate all error metrics"""
        if self.df is None:
            self.load_data()
        
        # Filter for successful EEW detections (Type contains 'Y')
        eew_detected = self.df[self.df['Type'].str.contains('Y', na=False)].copy()
        
        # Calculate epicenter error
        eew_detected['Epicenter_Error_km'] = eew_detected.apply(
            lambda row: self.calculate_distance(
                row['Cat_Lat'], row['Cat_Lon'],
                row['EEW_Lat'], row['EEW_Lon']
            ) if not np.isnan(row['EEW_Lat']) else np.nan,
            axis=1
        )
        
        # Calculate magnitude error
        eew_detected['Magnitude_Error'] = abs(
            eew_detected['Cat_Mag'] - eew_detected['EEW_Mag']
        )
        
        # Calculate depth error
        eew_detected['Depth_Error_km'] = abs(
            eew_detected['Cat_Depth'] - eew_detected['EEW_Depth']
        )
        
        self.df_analyzed = eew_detected
        return eew_detected
    
    def get_statistics(self) -> Dict:
        """Calculate comprehensive statistics"""
        if not hasattr(self, 'df_analyzed'):
            self.calculate_errors()
        
        df = self.df_analyzed.dropna(subset=['Epicenter_Error_km'])
        
        stats = {
            'total_earthquakes': len(self.df),
            'eew_detected': len(df),
            'missed_events': len(self.df) - len(df),
            'detection_rate': len(df) / len(self.df) * 100,
            
            # Epicenter error statistics
            'epicenter_error_mean_km': df['Epicenter_Error_km'].mean(),
            'epicenter_error_std_km': df['Epicenter_Error_km'].std(),
            'epicenter_error_median_km': df['Epicenter_Error_km'].median(),
            'epicenter_error_max_km': df['Epicenter_Error_km'].max(),
            'epicenter_error_min_km': df['Epicenter_Error_km'].min(),
            
            # Magnitude error statistics
            'magnitude_error_mean': df['Magnitude_Error'].mean(),
            'magnitude_error_std': df['Magnitude_Error'].std(),
            'magnitude_error_rms': np.sqrt(np.mean(df['Magnitude_Error']**2)),
            
            # Depth error statistics
            'depth_error_mean_km': df['Depth_Error_km'].mean(),
            'depth_error_std_km': df['Depth_Error_km'].std(),
            
            # Processing time statistics
            'processing_time_mean_s': df['Processing_Time'].mean(),
            'processing_time_std_s': df['Processing_Time'].std(),
            'processing_time_median_s': df['Processing_Time'].median(),
            'processing_time_max_s': df['Processing_Time'].max(),
            'processing_time_min_s': df['Processing_Time'].min(),
        }
        
        # Add inland/offshore statistics if available
        if 'Is_Inland' in df.columns and df['Is_Inland'].notna().any():
            df_inland = df[df['Is_Inland'] == True]
            df_offshore = df[df['Is_Inland'] == False]
            
            stats['inland_count'] = len(df_inland)
            stats['offshore_count'] = len(df_offshore)
            
            # Inland statistics
            if len(df_inland) > 0:
                stats['inland_epicenter_error_mean_km'] = df_inland['Epicenter_Error_km'].mean()
                stats['inland_epicenter_error_std_km'] = df_inland['Epicenter_Error_km'].std()
                stats['inland_magnitude_error_rms'] = np.sqrt(np.mean(df_inland['Magnitude_Error']**2))
                stats['inland_processing_time_mean_s'] = df_inland['Processing_Time'].mean()
                stats['inland_processing_time_std_s'] = df_inland['Processing_Time'].std()
            
            # Offshore statistics
            if len(df_offshore) > 0:
                stats['offshore_epicenter_error_mean_km'] = df_offshore['Epicenter_Error_km'].mean()
                stats['offshore_epicenter_error_std_km'] = df_offshore['Epicenter_Error_km'].std()
                stats['offshore_magnitude_error_rms'] = np.sqrt(np.mean(df_offshore['Magnitude_Error']**2))
                stats['offshore_processing_time_mean_s'] = df_offshore['Processing_Time'].mean()
                stats['offshore_processing_time_std_s'] = df_offshore['Processing_Time'].std()
        
        self.results = stats
        return stats
    
    def filter_by_magnitude(self, min_mag: float = 4.0, max_mag: float = 10.0) -> pd.DataFrame:
        """Filter events by magnitude range"""
        if self.df is None:
            self.load_data()
        return self.df[(self.df['Cat_Mag'] >= min_mag) & (self.df['Cat_Mag'] <= max_mag)]
    
    def filter_by_depth(self, max_depth: float = 40.0) -> pd.DataFrame:
        """Filter events by maximum depth"""
        if self.df is None:
            self.load_data()
        return self.df[self.df['Cat_Depth'] <= max_depth]
    
    def filter_by_region(self, lon_range: Tuple[float, float], 
                         lat_range: Tuple[float, float]) -> pd.DataFrame:
        """Filter events by geographic region"""
        if self.df is None:
            self.load_data()
        return self.df[
            (self.df['Cat_Lon'] >= lon_range[0]) & (self.df['Cat_Lon'] <= lon_range[1]) &
            (self.df['Cat_Lat'] >= lat_range[0]) & (self.df['Cat_Lat'] <= lat_range[1])
        ]
    
    def get_missed_events(self) -> pd.DataFrame:
        """Get events that were missed by EEWS"""
        if self.df is None:
            self.load_data()
        return self.df[self.df['Type'].str.contains('N|L', na=False)]
    
    def get_detected_events(self) -> pd.DataFrame:
        """Get events that were detected by EEWS"""
        if self.df is None:
            self.load_data()
        return self.df[self.df['Type'].str.contains('Y', na=False)]
    
    def print_summary(self):
        """Print a summary of the analysis"""
        if not self.results:
            self.get_statistics()
        
        print("\n" + "="*70)
        print("EARTHQUAKE EARLY WARNING SYSTEM (EEWS) PERFORMANCE SUMMARY")
        print("="*70)
        
        print(f"\n📊 DETECTION STATISTICS:")
        print(f"  Total Earthquakes:        {self.results['total_earthquakes']:>6}")
        print(f"  Successfully Detected:    {self.results['eew_detected']:>6}")
        print(f"  Missed Events:            {self.results['missed_events']:>6}")
        print(f"  Detection Rate:           {self.results['detection_rate']:>6.2f}%")
        
        print(f"\n📍 EPICENTER ERROR (km):")
        print(f"  Mean:                     {self.results['epicenter_error_mean_km']:>6.2f}")
        print(f"  Std Dev:                  {self.results['epicenter_error_std_km']:>6.2f}")
        print(f"  Median:                   {self.results['epicenter_error_median_km']:>6.2f}")
        print(f"  Range:                    {self.results['epicenter_error_min_km']:>6.2f} - {self.results['epicenter_error_max_km']:>6.2f}")
        
        print(f"\n📏 MAGNITUDE ERROR:")
        print(f"  Mean:                     {self.results['magnitude_error_mean']:>6.3f}")
        print(f"  Std Dev:                  {self.results['magnitude_error_std']:>6.3f}")
        print(f"  RMS:                      {self.results['magnitude_error_rms']:>6.3f}")
        
        print(f"\n⬇️  DEPTH ERROR (km):")
        print(f"  Mean:                     {self.results['depth_error_mean_km']:>6.2f}")
        print(f"  Std Dev:                  {self.results['depth_error_std_km']:>6.2f}")
        
        print(f"\n⏱️  PROCESSING TIME (seconds):")
        print(f"  Mean:                     {self.results['processing_time_mean_s']:>6.2f}")
        print(f"  Std Dev:                  {self.results['processing_time_std_s']:>6.2f}")
        print(f"  Median:                   {self.results['processing_time_median_s']:>6.2f}")
        print(f"  Range:                    {self.results['processing_time_min_s']:>6.2f} - {self.results['processing_time_max_s']:>6.2f}")
        
        # Print inland/offshore statistics if available
        if 'inland_count' in self.results:
            print(f"\n🏝️  INLAND vs OFFSHORE ANALYSIS:")
            print(f"  Inland Events:            {self.results['inland_count']:>6}")
            print(f"  Offshore Events:          {self.results['offshore_count']:>6}")
            
            if 'inland_epicenter_error_mean_km' in self.results:
                print(f"\n  📍 INLAND - Epicenter Error:")
                print(f"     Mean ± Std:            {self.results['inland_epicenter_error_mean_km']:>6.2f} ± {self.results['inland_epicenter_error_std_km']:>6.2f} km")
                print(f"     Magnitude RMS:         {self.results['inland_magnitude_error_rms']:>6.3f}")
                print(f"     Processing Time:       {self.results['inland_processing_time_mean_s']:>6.1f} ± {self.results['inland_processing_time_std_s']:>6.1f} sec")
            
            if 'offshore_epicenter_error_mean_km' in self.results:
                print(f"\n  🌊 OFFSHORE - Epicenter Error:")
                print(f"     Mean ± Std:            {self.results['offshore_epicenter_error_mean_km']:>6.2f} ± {self.results['offshore_epicenter_error_std_km']:>6.2f} km")
                print(f"     Magnitude RMS:         {self.results['offshore_magnitude_error_rms']:>6.3f}")
                print(f"     Processing Time:       {self.results['offshore_processing_time_mean_s']:>6.1f} ± {self.results['offshore_processing_time_std_s']:>6.1f} sec")
        
        print("\n" + "="*70 + "\n")
    
    def save_results(self, output_file: str = "outputs/eews_analysis_results.csv"):
        """Save analyzed data to CSV"""
        if not hasattr(self, 'df_analyzed'):
            self.calculate_errors()
        
        # Ensure outputs directory exists
        import os
        os.makedirs("outputs", exist_ok=True)
        
        self.df_analyzed.to_csv(output_file, index=False)
        print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) == 5:
        # Use command-line arguments
        try:
            data_file = sys.argv[1]
            min_mag = float(sys.argv[2])
            max_depth = float(sys.argv[3])
            target_year = int(sys.argv[4])
            print("\n" + "="*70)
            print("EEWS PERFORMANCE ANALYZER - Command-Line Mode")
            print("="*70)
        except ValueError:
            print("Error: Invalid arguments. Usage: python eews_analyzer.py [data_file] [min_magnitude] [max_depth] [year]")
            sys.exit(1)
    else:
        # Interactive mode
        print("\n" + "="*70)
        print("EEWS PERFORMANCE ANALYZER - Filter Configuration")
        print("="*70)
        
        # Get data file
        while True:
            data_file_input = input("\nEnter data file name (default=EEW_ALL-2014-2025.txt, press Enter to use default): ").strip()
            data_file = data_file_input if data_file_input else "EEW_ALL-2014-2025.txt"
            
            # Check if file exists
            import os
            if not os.path.exists(data_file):
                print(f"Warning: File '{data_file}' not found. Please check the filename.")
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != 'y':
                    print("Exiting.")
                    sys.exit(0)
                continue
            break
        
        # Get minimum magnitude
        while True:
            try:
                min_mag_input = input("\nEnter minimum catalog magnitude (default=5.0, press Enter to use default): ").strip()
                min_mag = float(min_mag_input) if min_mag_input else 5.0
                if min_mag < 0:
                    print("Magnitude must be non-negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        
        # Get maximum depth
        while True:
            try:
                max_depth_input = input("Enter maximum catalog depth in km (default=40.0, press Enter to use default): ").strip()
                max_depth = float(max_depth_input) if max_depth_input else 40.0
                if max_depth < 0:
                    print("Depth must be non-negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        # Get target year
        while True:
            try:
                year_input = input("Enter target year (default=2025, press Enter to use default): ").strip()
                target_year = int(year_input) if year_input else 2025
                if target_year < 0:
                    print("Year must be non-negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric year.")
    
    print(f"\n📋 Configuration:")
    print(f"   Data File: {data_file}")
    print(f"   Magnitude >= {min_mag}")
    print(f"   Depth <= {max_depth} km")
    print(f"   Year == {target_year}")
    print("="*70 + "\n")
    
    # Load and analyze data
    analyzer = EEWSAnalyzer(data_file)
    analyzer.load_data()
    
    # Apply filters
    original_count = len(analyzer.df)
    analyzer.df['Origin_Time'] = pd.to_datetime(analyzer.df['Origin_Time'], errors='coerce')
    analyzer.df = analyzer.df[analyzer.df['Origin_Time'].dt.year == target_year]
    analyzer.df = analyzer.df[
        (analyzer.df['Cat_Mag'] >= min_mag) & 
        (analyzer.df['Cat_Depth'] <= max_depth)
    ]
    filtered_count = len(analyzer.df)
    
    if filtered_count == 0:
        print("⚠️  No events match the specified criteria. Please adjust your filters.")
    else:
        print(f"✅ Filtered {filtered_count} events from {original_count} total events\n")
        analyzer.calculate_errors()
        analyzer.get_statistics()
        analyzer.print_summary()
        analyzer.save_results()
