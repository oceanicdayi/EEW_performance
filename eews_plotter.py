"""
EEWS Performance Visualization
Creates publication-quality figures for EEWS analysis
"""

try:
    import pygmt
    HAS_PYGMT = True
except (ImportError, Exception) as e:
    HAS_PYGMT = False
    print(f"Warning: PyGMT not available ({type(e).__name__}). Using matplotlib for basic plots.")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.patches as mpatches


class EEWSPlotter:
    """Create visualizations for EEWS performance analysis"""
    
    def __init__(self, analyzer, city_boundary_file: str = "city_2016.gmt"):
        """
        Initialize plotter with an EEWSAnalyzer instance.
        
        Args:
            analyzer: EEWSAnalyzer instance with loaded data
            city_boundary_file: Path to GMT format city boundary file
        """
        self.analyzer = analyzer
        self.taiwan_region = [119.85, 123.1, 21.2, 25.7]  # [lon_min, lon_max, lat_min, lat_max]
        self.city_boundary_file = city_boundary_file
        
    def plot_epicenter_errors(self, output_file: str = "outputs/epicenter_error_map.png", 
                              dpi: int = 300):
        """
        Create map showing epicenter location errors.
        
        Args:
            output_file: Output filename
            dpi: Resolution in dots per inch
        """
        if not hasattr(self.analyzer, 'df_analyzed'):
            self.analyzer.calculate_errors()
        
        df = self.analyzer.df_analyzed.dropna(subset=['Epicenter_Error_km'])
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(exist_ok=True, parents=True)
        
        if HAS_PYGMT:
            # Use PyGMT for publication-quality maps
            fig = pygmt.Figure()
            
            # Setup map projection and region
            region = self.taiwan_region
            projection = "M15c"
            
            # Draw basemap
            fig.basemap(region=region, projection=projection, frame=["af", "WSne"])
            fig.coast(region=region, projection=projection, 
                      land="lightgray", water="lightblue", 
                      shorelines="1/0.5p,black")
            
            # Draw city boundaries from GMT file
            try:
                fig.plot(self.city_boundary_file, pen="1p,black")
            except Exception as e:
                print(f"Warning: Could not load city boundaries: {e}")
            
            # Plot catalog epicenters (circles)
            if len(df) > 0:
                print(f"Plotting {len(df)} epicenter locations...")
                
                # Create colormap for epicenter error
                max_error = df['Epicenter_Error_km'].max()
                print(f"Epicenter error range: 0 - {max_error:.2f} km")
                pygmt.makecpt(cmap="hot", series=[0, max_error], reverse=True)
                
                # Plot catalog locations as filled circles colored by error
                fig.plot(
                    x=df['Cat_Lon'].values,
                    y=df['Cat_Lat'].values,
                    size=0.3,
                    fill=df['Epicenter_Error_km'].values,
                    cmap=True,
                    style="c",
                    pen="0.5p,black"
                )
                
                # Plot EEW locations as triangles (only where EEW data exists)
                df_with_eew = df.dropna(subset=['EEW_Lon', 'EEW_Lat'])
                print(f"Plotting {len(df_with_eew)} EEW locations...")
                if len(df_with_eew) > 0:
                    fig.plot(
                        x=df_with_eew['EEW_Lon'].values,
                        y=df_with_eew['EEW_Lat'].values,
                        size=0.25,
                        style="t",
                        fill="blue",
                        pen="0.5p,black"
                    )
            else:
                print("Warning: No data to plot after filtering!")
            
            # Add colorbar
            fig.colorbar(frame=["af", "x+lEpicenter Error (km)"], position="JMR+w10c/0.5c+o1c/0c")
            
            # Add legend
            legend_str = """S 0.3c c 0.3c yellow 0.5p,black 0.6c Catalog Location
S 0.3c t 0.25c blue 0.5p,black 0.6c EEW Location
S 0.3c - 0.5c red 1p,red 0.6c Location Error"""
            
            with open("legend_temp.txt", "w") as f:
                f.write(legend_str)
            
            fig.legend(
                spec="legend_temp.txt",
                position="jBL+w5c+o0.3c",
                box="+gwhite+p1p"
            )
            
            # Add title
            fig.text(
                text="EEWS Epicenter Location Performance",
                position="TC",
                offset="0/0.5c",
                font="16p,Helvetica-Bold"
            )
            
            # Save
            fig.savefig(output_file, dpi=dpi)
        else:
            # Fallback to matplotlib with Taiwan coastline outline
            fig = plt.figure(figsize=(10, 12))
            ax = plt.gca()
            
            # Add simplified Taiwan coastline (approximate outline)
            taiwan_coast_lon = [
                120.0, 120.1, 120.3, 120.5, 120.7, 121.0, 121.3, 121.6, 121.9, 122.0,
                121.95, 121.9, 121.8, 121.7, 121.6, 121.5, 121.4, 121.3, 121.2, 121.1,
                121.0, 120.9, 120.8, 120.7, 120.6, 120.5, 120.4, 120.3, 120.2, 120.1, 120.0
            ]
            taiwan_coast_lat = [
                22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 24.8, 25.0, 25.2, 25.3,
                25.2, 25.0, 24.8, 24.5, 24.2, 24.0, 23.7, 23.4, 23.1, 22.8,
                22.5, 22.3, 22.1, 22.0, 21.9, 21.9, 21.9, 22.0, 22.0, 22.0, 22.0
            ]
            ax.plot(taiwan_coast_lon, taiwan_coast_lat, 'k-', linewidth=1.5, 
                   label='Taiwan Coast', zorder=1)
            ax.fill(taiwan_coast_lon, taiwan_coast_lat, color='lightgray', 
                   alpha=0.3, zorder=0)
            
            # Draw lines connecting catalog to EEW locations
            for idx, row in df.iterrows():
                ax.plot([row['Cat_Lon'], row['EEW_Lon']],
                       [row['Cat_Lat'], row['EEW_Lat']],
                       'r-', alpha=0.3, linewidth=0.5, zorder=2)
            
            # Plot catalog locations
            scatter = ax.scatter(df['Cat_Lon'], df['Cat_Lat'], 
                                c=df['Epicenter_Error_km'], 
                                cmap='hot_r', s=100, alpha=0.7,
                                edgecolors='black', linewidth=0.5,
                                label='Catalog Location', zorder=3)
            
            # Plot EEW locations
            ax.scatter(df['EEW_Lon'], df['EEW_Lat'], 
                      marker='^', c='blue', s=80, alpha=0.7,
                      edgecolors='black', linewidth=0.5,
                      label='EEW Location', zorder=3)
            
            plt.colorbar(scatter, label='Epicenter Error (km)')
            ax.set_xlabel('Longitude (°E)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Latitude (°N)', fontsize=12, fontweight='bold')
            ax.set_title('EEWS Epicenter Location Performance', 
                       fontsize=14, fontweight='bold')
            ax.legend(loc='lower left', fontsize=10)
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
            ax.set_aspect('equal')
            ax.set_xlim(self.taiwan_region[0], self.taiwan_region[1])
            ax.set_ylim(self.taiwan_region[2], self.taiwan_region[3])
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
            plt.close()
        
        print(f"Epicenter error map saved to: {output_file}")
    
    def plot_magnitude_comparison(self, output_file: str = "outputs/magnitude_comparison.png",
                                   dpi: int = 300):
        """
        Create scatter plot comparing catalog vs EEW magnitudes.
        
        Args:
            output_file: Output filename
            dpi: Resolution
        """
        if not hasattr(self.analyzer, 'df_analyzed'):
            self.analyzer.calculate_errors()
        
        df = self.analyzer.df_analyzed.dropna(subset=['EEW_Mag'])
        
        fig = pygmt.Figure()
        
        # Define plot region (magnitude range)
        mag_min = min(df['Cat_Mag'].min(), df['EEW_Mag'].min()) - 0.5
        mag_max = max(df['Cat_Mag'].max(), df['EEW_Mag'].max()) + 0.5
        region = [mag_min, mag_max, mag_min, mag_max]
        
        # Create figure
        fig.basemap(
            region=region,
            projection="X15c/15c",
            frame=["af", "x+lCatalog Magnitude (ML)", "y+lEEW Magnitude", "WSne"]
        )
        
        # Plot 1:1 reference line
        fig.plot(x=[mag_min, mag_max], y=[mag_min, mag_max], 
                 pen="2p,black")
        
        # Calculate and plot standard deviation lines
        mag_std = df['Magnitude_Error'].std()
        fig.plot(x=[mag_min, mag_max], 
                 y=[mag_min + mag_std, mag_max + mag_std],
                 pen="1p,black,dashed")
        fig.plot(x=[mag_min, mag_max], 
                 y=[mag_min - mag_std, mag_max - mag_std],
                 pen="1p,black,dashed")
        
        # Plot data points
        fig.plot(
            x=df['Cat_Mag'],
            y=df['EEW_Mag'],
            style="c0.3c",
            fill="yellow",
            pen="1p,red"
        )
        
        # Add statistics text
        stats_text = f"Mean Error: {df['Magnitude_Error'].mean():.2f}\\nStd Dev: {mag_std:.2f}"
        fig.text(
            text=stats_text,
            position="TL",
            offset="0.5c/-0.5c",
            font="12p,Helvetica",
            fill="white",
            pen="1p,black"
        )
        
        # Add title
        fig.text(
            text="Magnitude Comparison: Catalog vs EEW",
            position="TC",
            offset="0/0.8c",
            font="16p,Helvetica-Bold"
        )
        
        fig.savefig(output_file, dpi=dpi)
        print(f"Magnitude comparison plot saved to: {output_file}")
    
    def plot_processing_time_map(self, output_file: str = "outputs/processing_time_map.png",
                                  dpi: int = 300):
        """
        Create map showing processing time distribution.
        
        Args:
            output_file: Output filename
            dpi: Resolution
        """
        if not hasattr(self.analyzer, 'df_analyzed'):
            self.analyzer.calculate_errors()
        
        df = self.analyzer.df_analyzed.dropna(subset=['Processing_Time'])
        
        fig = pygmt.Figure()
        
        # Setup map
        region = self.taiwan_region
        projection = "M15c"
        
        fig.basemap(region=region, projection=projection, frame=["af", "WSne"])
        fig.coast(region=region, projection=projection,
                  land="lightgray", water="lightblue",
                  shorelines="1/0.5p,black")
        
        # Draw city boundaries from GMT file
        try:
            fig.plot(self.city_boundary_file, pen="0.5p,black")
        except Exception as e:
            print(f"Warning: Could not plot city boundaries: {e}")
        
        # Create colormap for processing time
        pygmt.makecpt(cmap="jet", series=[df['Processing_Time'].min(), 
                                          df['Processing_Time'].max()],
                      reverse=True)
        
        # Scale point size by processing time (scaled for visualization)
        point_sizes = 0.2 + (df['Processing_Time'] / df['Processing_Time'].max()) * 0.4
        
        # Plot epicenters colored by processing time
        fig.plot(
            x=df['Cat_Lon'],
            y=df['Cat_Lat'],
            size=point_sizes,
            fill=df['Processing_Time'],
            cmap=True,
            style="cc",
            pen="0.5p,black"
        )
        
        # Add colorbar
        fig.colorbar(
            frame=["af", "x+lProcessing Time (seconds)"],
            position="JMR+w10c/0.5c+o1c/0c"
        )
        
        # Add title
        fig.text(
            text="EEWS Processing Time Distribution",
            position="TC",
            offset="0/0.5c",
            font="16p,Helvetica-Bold"
        )
        
        # Add statistics box
        stats_text = (f"Mean: {df['Processing_Time'].mean():.1f}s\\n"
                      f"Median: {df['Processing_Time'].median():.1f}s")
        fig.text(
            text=stats_text,
            position="BL",
            offset="0.5c/0.5c",
            font="11p,Helvetica",
            fill="white",
            pen="1p,black"
        )
        
        fig.savefig(output_file, dpi=dpi)
        print(f"Processing time map saved to: {output_file}")
    
    def plot_missed_events(self, output_file: str = "outputs/missed_events_map.png",
                           dpi: int = 300):
        """
        Create map showing missed vs detected events.
        
        Args:
            output_file: Output filename
            dpi: Resolution
        """
        detected = self.analyzer.get_detected_events()
        missed = self.analyzer.get_missed_events()
        
        fig = pygmt.Figure()
        
        # Setup map
        region = self.taiwan_region
        projection = "M15c"
        
        fig.basemap(region=region, projection=projection, frame=["af", "WSne"])
        fig.coast(region=region, projection=projection,
                  land="lightgray", water="lightblue",
                  shorelines="1/0.5p,black")
        
        # Draw city boundaries from GMT file
        try:
            fig.plot(self.city_boundary_file, pen="0.5p,black")
        except Exception as e:
            print(f"Warning: Could not plot city boundaries: {e}")
        
        # Plot detected events (circles, green)
        if len(detected) > 0:
            fig.plot(
                x=detected['Cat_Lon'],
                y=detected['Cat_Lat'],
                size=0.3,
                style="cc",
                fill="green",
                pen="0.5p,black"
            )
        
        # Plot missed events (triangles, red)
        if len(missed) > 0:
            fig.plot(
                x=missed['Cat_Lon'],
                y=missed['Cat_Lat'],
                size=0.35,
                style="t",
                fill="red",
                pen="0.5p,black"
            )
        
        # Add legend
        legend_str = f"""S 0.3c c 0.3c green 0.5p,black 0.8c Detected ({len(detected)})
S 0.3c t 0.35c red 0.5p,black 0.8c Missed ({len(missed)})"""
        
        with open("legend_temp_missed.txt", "w") as f:
            f.write(legend_str)
        
        fig.legend(
            spec="legend_temp_missed.txt",
            position="jBL+w5c+o0.3c",
            box="+gwhite+p1p"
        )
        
        # Add title
        detection_rate = len(detected) / (len(detected) + len(missed)) * 100
        fig.text(
            text=f"EEWS Detection Performance (Rate: {detection_rate:.1f}%)",
            position="TC",
            offset="0/0.5c",
            font="16p,Helvetica-Bold"
        )
        
        fig.savefig(output_file, dpi=dpi)
        print(f"Missed events map saved to: {output_file}")
    
    def plot_processing_time_histogram(self, output_file: str = "outputs/processing_time_hist.png",
                                        figsize: tuple = (10, 6)):
        """
        Create histogram of processing times using matplotlib.
        
        Args:
            output_file: Output filename
            figsize: Figure size (width, height)
        """
        if not hasattr(self.analyzer, 'df_analyzed'):
            self.analyzer.calculate_errors()
        
        df = self.analyzer.df_analyzed.dropna(subset=['Processing_Time'])
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create histogram
        n, bins, patches = ax.hist(df['Processing_Time'], bins=20, 
                                     color='skyblue', edgecolor='black', alpha=0.7)
        
        # Add vertical lines for mean and median
        mean_time = df['Processing_Time'].mean()
        median_time = df['Processing_Time'].median()
        
        ax.axvline(mean_time, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_time:.1f}s')
        ax.axvline(median_time, color='green', linestyle='--', linewidth=2,
                   label=f'Median: {median_time:.1f}s')
        
        ax.set_xlabel('Processing Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Events', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of EEWS Processing Times', 
                     fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Processing time histogram saved to: {output_file}")
    
    def plot_error_distributions(self, output_file: str = "outputs/error_distributions.png",
                                  figsize: tuple = (15, 10)):
        """
        Create comprehensive error distribution plots.
        
        Args:
            output_file: Output filename
            figsize: Figure size
        """
        if not hasattr(self.analyzer, 'df_analyzed'):
            self.analyzer.calculate_errors()
        
        df = self.analyzer.df_analyzed.dropna()
        
        fig, axes = plt.subplots(2, 3, figsize=figsize)
        
        # 1. Epicenter error histogram
        axes[0, 0].hist(df['Epicenter_Error_km'], bins=20, color='coral', 
                        edgecolor='black', alpha=0.7)
        axes[0, 0].axvline(df['Epicenter_Error_km'].mean(), color='red', 
                           linestyle='--', linewidth=2)
        axes[0, 0].set_xlabel('Epicenter Error (km)', fontweight='bold')
        axes[0, 0].set_ylabel('Count', fontweight='bold')
        axes[0, 0].set_title('Epicenter Error Distribution', fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Magnitude error histogram
        axes[0, 1].hist(df['Magnitude_Error'], bins=20, color='lightgreen',
                        edgecolor='black', alpha=0.7)
        axes[0, 1].axvline(df['Magnitude_Error'].mean(), color='red',
                           linestyle='--', linewidth=2)
        axes[0, 1].set_xlabel('Magnitude Error', fontweight='bold')
        axes[0, 1].set_ylabel('Count', fontweight='bold')
        axes[0, 1].set_title('Magnitude Error Distribution', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Depth error histogram
        axes[0, 2].hist(df['Depth_Error_km'], bins=20, color='skyblue',
                        edgecolor='black', alpha=0.7)
        axes[0, 2].axvline(df['Depth_Error_km'].mean(), color='red',
                           linestyle='--', linewidth=2)
        axes[0, 2].set_xlabel('Depth Error (km)', fontweight='bold')
        axes[0, 2].set_ylabel('Count', fontweight='bold')
        axes[0, 2].set_title('Depth Error Distribution', fontweight='bold')
        axes[0, 2].grid(True, alpha=0.3)
        
        # 4. Epicenter error vs magnitude
        scatter = axes[1, 0].scatter(df['Cat_Mag'], df['Epicenter_Error_km'],
                                      c=df['Processing_Time'], cmap='viridis',
                                      alpha=0.6, edgecolors='black')
        axes[1, 0].set_xlabel('Catalog Magnitude', fontweight='bold')
        axes[1, 0].set_ylabel('Epicenter Error (km)', fontweight='bold')
        axes[1, 0].set_title('Epicenter Error vs Magnitude', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[1, 0], label='Processing Time (s)')
        
        # 5. Processing time vs depth
        axes[1, 1].scatter(df['Cat_Depth'], df['Processing_Time'],
                          c=df['Cat_Mag'], cmap='hot', alpha=0.6, 
                          edgecolors='black')
        axes[1, 1].set_xlabel('Catalog Depth (km)', fontweight='bold')
        axes[1, 1].set_ylabel('Processing Time (s)', fontweight='bold')
        axes[1, 1].set_title('Processing Time vs Depth', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Summary statistics text
        axes[1, 2].axis('off')
        stats_text = f"""
        EEWS Performance Summary
        {'='*30}
        
        Detection Rate: {len(df)/len(self.analyzer.df)*100:.1f}%
        
        Epicenter Error:
          Mean: {df['Epicenter_Error_km'].mean():.2f} km
          Std:  {df['Epicenter_Error_km'].std():.2f} km
        
        Magnitude Error:
          Mean: {df['Magnitude_Error'].mean():.3f}
          RMS:  {np.sqrt((df['Magnitude_Error']**2).mean()):.3f}
        
        Processing Time:
          Mean:   {df['Processing_Time'].mean():.2f} s
          Median: {df['Processing_Time'].median():.2f} s
          Range:  {df['Processing_Time'].min():.1f} - {df['Processing_Time'].max():.1f} s
        """
        axes[1, 2].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                        verticalalignment='center')
        
        plt.suptitle('EEWS Performance Analysis - Error Distributions', 
                     fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Error distributions plot saved to: {output_file}")
    
    def create_all_plots(self, output_dir: str = "outputs"):
        """
        Create all visualization plots.
        
        Args:
            output_dir: Directory to save figures
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print("\n" + "="*70)
        print("Creating EEWS Performance Visualizations...")
        print("="*70 + "\n")
        
        try:
            self.plot_epicenter_errors(str(output_path / "epicenter_error_map.png"))
        except Exception as e:
            print(f"Warning: Could not create epicenter error map: {e}")
        
        try:
            self.plot_magnitude_comparison(str(output_path / "magnitude_comparison.png"))
        except Exception as e:
            print(f"Warning: Could not create magnitude comparison: {e}")
        
        try:
            self.plot_processing_time_map(str(output_path / "processing_time_map.png"))
        except Exception as e:
            print(f"Warning: Could not create processing time map: {e}")
        
        try:
            self.plot_missed_events(str(output_path / "missed_events_map.png"))
        except Exception as e:
            print(f"Warning: Could not create missed events map: {e}")
        
        try:
            self.plot_processing_time_histogram(str(output_path / "processing_time_hist.png"))
        except Exception as e:
            print(f"Warning: Could not create processing time histogram: {e}")
        
        try:
            self.plot_error_distributions(str(output_path / "error_distributions.png"))
        except Exception as e:
            print(f"Warning: Could not create error distributions: {e}")
        
        print("\n" + "="*70)
        print(f"All plots saved to: {output_path}")
        print("="*70 + "\n")


if __name__ == "__main__":
    from eews_analyzer import EEWSAnalyzer
    import sys
    
    # Load data
    print("\n" + "="*70)
    print("EEWS PERFORMANCE PLOTTER")
    print("="*70)
    
    # Use command-line arguments or defaults
    if len(sys.argv) == 5:
        data_file = sys.argv[1]
        min_mag = float(sys.argv[2])
        max_depth = float(sys.argv[3])
        target_year = int(sys.argv[4])
    else:
        data_file = "EEW_ALL-2014-2025.txt"
        min_mag = 5.0
        max_depth = 40.0
        target_year = 2025
    
    print(f"\nConfiguration:")
    print(f"   Data File: {data_file}")
    print(f"   Magnitude >= {min_mag}")
    print(f"   Depth <= {max_depth} km")
    print(f"   Year == {target_year}")
    print("="*70 + "\n")
    
    # Initialize analyzer
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
    
    print(f"Filtered {filtered_count} events from {original_count} total events\n")
    
    # Calculate errors
    analyzer.calculate_errors()
    analyzer.get_statistics()
    
    # Create plotter and generate all plots
    plotter = EEWSPlotter(analyzer)
    plotter.create_all_plots()
