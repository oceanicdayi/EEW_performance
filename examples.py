#!/usr/bin/env python
"""
Quick Examples and Tutorial for EEWS Analyzer
Demonstrates various usage patterns
"""

from eews_analyzer import EEWSAnalyzer
from eews_plotter import EEWSPlotter
import pandas as pd


def example_basic_analysis():
    """Example 1: Basic analysis workflow"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Analysis")
    print("="*70)
    
    # Initialize and load data
    analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
    analyzer.load_data()
    
    # Calculate errors and statistics
    analyzer.calculate_errors()
    stats = analyzer.get_statistics()
    
    # Print summary
    analyzer.print_summary()
    
    # Access specific statistics
    print(f"\nKey Metrics:")
    print(f"  Detection Rate: {stats['detection_rate']:.1f}%")
    print(f"  Mean Epicenter Error: {stats['epicenter_error_mean_km']:.2f} km")
    print(f"  Mean Processing Time: {stats['processing_time_mean_s']:.2f} s")


def example_filtered_analysis():
    """Example 2: Filtered analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Filtered Analysis (M >= 5.0, Depth <= 40 km)")
    print("="*70)
    
    analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
    analyzer.load_data()
    
    # Apply filters
    print(f"\nOriginal dataset: {len(analyzer.df)} events")
    
    analyzer.df = analyzer.filter_by_magnitude(min_mag=5.0)
    print(f"After magnitude filter (M >= 5.0): {len(analyzer.df)} events")
    
    analyzer.df = analyzer.filter_by_depth(max_depth=40.0)
    print(f"After depth filter (depth <= 40 km): {len(analyzer.df)} events")
    
    # Analyze filtered data
    analyzer.calculate_errors()
    analyzer.get_statistics()
    analyzer.print_summary()


def example_regional_analysis():
    """Example 3: Regional analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Regional Analysis (Central Taiwan)")
    print("="*70)
    
    analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
    analyzer.load_data()
    
    # Filter by region (central Taiwan)
    lon_range = (120.5, 121.5)
    lat_range = (23.0, 24.5)
    
    analyzer.df = analyzer.filter_by_region(lon_range, lat_range)
    print(f"\nEvents in central Taiwan: {len(analyzer.df)}")
    
    # Analyze regional data
    analyzer.calculate_errors()
    stats = analyzer.get_statistics()
    
    print(f"\nRegional Performance:")
    print(f"  Detection Rate: {stats['detection_rate']:.1f}%")
    print(f"  Mean Epicenter Error: {stats['epicenter_error_mean_km']:.2f} km")
    print(f"  Mean Processing Time: {stats['processing_time_mean_s']:.2f} s")


def example_detection_comparison():
    """Example 4: Compare detected vs missed events"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Detected vs Missed Events Comparison")
    print("="*70)
    
    analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
    analyzer.load_data()
    
    # Get detected and missed events
    detected = analyzer.get_detected_events()
    missed = analyzer.get_missed_events()
    
    print(f"\nDetected Events: {len(detected)}")
    print(f"Missed Events: {len(missed)}")
    print(f"Detection Rate: {len(detected)/(len(detected)+len(missed))*100:.1f}%")
    
    # Statistics for missed events
    print(f"\nMissed Events Characteristics:")
    print(f"  Mean Magnitude: {missed['Cat_Mag'].mean():.2f}")
    print(f"  Mean Depth: {missed['Cat_Depth'].mean():.2f} km")
    print(f"  Magnitude Range: {missed['Cat_Mag'].min():.2f} - {missed['Cat_Mag'].max():.2f}")
    print(f"  Depth Range: {missed['Cat_Depth'].min():.2f} - {missed['Cat_Depth'].max():.2f} km")


def example_custom_visualization():
    """Example 5: Create custom visualizations"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Custom Visualizations")
    print("="*70)
    
    analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
    analyzer.load_data()
    analyzer.calculate_errors()
    
    # Create plotter
    plotter = EEWSPlotter(analyzer)
    
    # Create individual plots
    print("\nCreating custom plots...")
    
    plotter.plot_epicenter_errors("custom_epicenter_map.png")
    plotter.plot_magnitude_comparison("custom_magnitude_plot.png")
    plotter.plot_processing_time_histogram("custom_time_histogram.png")
    
    print("\nCustom plots saved!")


def example_data_export():
    """Example 6: Export analyzed data"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Data Export")
    print("="*70)
    
    analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
    analyzer.load_data()
    analyzer.calculate_errors()
    
    # Save full analysis results
    analyzer.save_results("full_analysis.csv")
    
    # Export specific subsets
    detected = analyzer.get_detected_events()
    detected.to_csv("detected_events.csv", index=False)
    
    missed = analyzer.get_missed_events()
    missed.to_csv("missed_events.csv", index=False)
    
    # Export filtered data
    high_mag = analyzer.filter_by_magnitude(min_mag=6.0)
    high_mag.to_csv("high_magnitude_events.csv", index=False)
    
    print("\nData exported to CSV files!")


def example_processing_time_analysis():
    """Example 7: Detailed processing time analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Processing Time Analysis")
    print("="*70)
    
    analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
    analyzer.load_data()
    analyzer.calculate_errors()
    
    df = analyzer.df_analyzed
    
    # Categorize by processing time
    fast = df[df['Processing_Time'] <= 10]
    medium = df[(df['Processing_Time'] > 10) & (df['Processing_Time'] <= 20)]
    slow = df[df['Processing_Time'] > 20]
    
    print(f"\nProcessing Time Categories:")
    print(f"  Fast (≤ 10s):   {len(fast)} events ({len(fast)/len(df)*100:.1f}%)")
    print(f"  Medium (10-20s): {len(medium)} events ({len(medium)/len(df)*100:.1f}%)")
    print(f"  Slow (> 20s):    {len(slow)} events ({len(slow)/len(df)*100:.1f}%)")
    
    print(f"\nAccuracy by Processing Time:")
    print(f"  Fast - Mean Epicenter Error: {fast['Epicenter_Error_km'].mean():.2f} km")
    print(f"  Medium - Mean Epicenter Error: {medium['Epicenter_Error_km'].mean():.2f} km")
    print(f"  Slow - Mean Epicenter Error: {slow['Epicenter_Error_km'].mean():.2f} km")


def example_magnitude_accuracy():
    """Example 8: Magnitude accuracy by magnitude range"""
    print("\n" + "="*70)
    print("EXAMPLE 8: Magnitude Accuracy by Magnitude Range")
    print("="*70)
    
    analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
    analyzer.load_data()
    analyzer.calculate_errors()
    
    df = analyzer.df_analyzed
    
    # Analyze by magnitude bins
    mag_bins = [(4, 5), (5, 6), (6, 7), (7, 10)]
    
    print("\nMagnitude Error by Magnitude Range:")
    for mag_min, mag_max in mag_bins:
        subset = df[(df['Cat_Mag'] >= mag_min) & (df['Cat_Mag'] < mag_max)]
        if len(subset) > 0:
            print(f"\n  M {mag_min}-{mag_max}:")
            print(f"    Count: {len(subset)}")
            print(f"    Mean Error: {subset['Magnitude_Error'].mean():.3f}")
            print(f"    Std Dev: {subset['Magnitude_Error'].std():.3f}")
            print(f"    RMS Error: {(subset['Magnitude_Error']**2).mean()**0.5:.3f}")


def run_all_examples():
    """Run all examples"""
    examples = [
        example_basic_analysis,
        example_filtered_analysis,
        example_regional_analysis,
        example_detection_comparison,
        example_custom_visualization,
        example_data_export,
        example_processing_time_analysis,
        example_magnitude_accuracy
    ]
    
    print("\n" + "#"*70)
    print("# EEWS ANALYZER - EXAMPLES AND TUTORIALS")
    print("#"*70)
    
    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"\nExample {i} encountered an error: {e}")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n" + "#"*70)
    print("# ALL EXAMPLES COMPLETED!")
    print("#"*70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example_num = int(sys.argv[1])
        examples = [
            example_basic_analysis,
            example_filtered_analysis,
            example_regional_analysis,
            example_detection_comparison,
            example_custom_visualization,
            example_data_export,
            example_processing_time_analysis,
            example_magnitude_accuracy
        ]
        
        if 1 <= example_num <= len(examples):
            examples[example_num - 1]()
        else:
            print(f"Invalid example number. Choose 1-{len(examples)}")
    else:
        # Run all examples interactively
        run_all_examples()
