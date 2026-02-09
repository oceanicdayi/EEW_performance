"""
Plot epicenter error map with proportional circles (publication style)
Creates a black and white map with circle sizes representing epicenter error magnitude
"""

import pygmt
import pandas as pd
import numpy as np
from eews_analyzer import EEWSAnalyzer


def plot_epicenter_error_circles(analyzer, output_file="outputs/epicenter_error_circles.png", dpi=300):
    """
    Create map with circles sized by epicenter error (publication style).
    
    Args:
        analyzer: EEWSAnalyzer instance with loaded data
        output_file: Output filename
        dpi: Resolution in dots per inch
    """
    if not hasattr(analyzer, 'df_analyzed'):
        analyzer.calculate_errors()
    
    df = analyzer.df_analyzed.dropna(subset=['Epicenter_Error_km'])
    
    # Taiwan region
    region = [119.85, 123.1, 21.2, 25.7]
    
    fig = pygmt.Figure()
    
    # Setup map with simple frame
    fig.basemap(
        region=region,
        projection="M15c",
        frame=["WSne", "xa1f0.5", "ya1f0.5"]
    )
    
    # Draw coastline - simple black outline
    fig.coast(
        region=region,
        projection="M15c",
        shorelines="1p,black",
        land="white",
        water="white"
    )
    
    # Scale circles by epicenter error (km to cm conversion)
    # Use a scaling factor to make circles visible
    scale_factor = 0.015  # Adjust this to control circle sizes
    
    print(f"Plotting {len(df)} circles...")
    
    # Calculate circle sizes for all points
    circle_sizes = df['Epicenter_Error_km'].values * scale_factor
    
    # Plot all circles at once
    fig.plot(
        x=df['Cat_Lon'].values,
        y=df['Cat_Lat'].values,
        size=circle_sizes,
        style="c",
        pen="0.5p,black",
        fill="white"
    )
    
    # Add scale bar
    fig.basemap(
        map_scale="jBR+w100k+o0.5c/0.5c+f+l"
    )
    
    # Save figure
    fig.savefig(output_file, dpi=dpi)
    print(f"Epicenter error circles map saved to: {output_file}")


if __name__ == "__main__":
    import sys
    
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
    
    print("\n" + "="*70)
    print("EPICENTER ERROR CIRCLES PLOTTER")
    print("="*70)
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
    
    # Create plot
    plot_epicenter_error_circles(analyzer)
    print("\nDone!")
