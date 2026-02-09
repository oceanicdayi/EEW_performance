#!/usr/bin/env python
"""
EEWS Performance Analysis - Main Script
Comprehensive analysis and visualization of Earthquake Early Warning System performance

Usage:
    python analyze_eews.py [data_file]
    
Example:
    python analyze_eews.py EEW_ALL-2014-2025.txt
"""

import sys
import argparse
from pathlib import Path
from eews_analyzer import EEWSAnalyzer
from eews_plotter import EEWSPlotter


def main():
    """Main execution function"""
    
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Analyze EEWS performance data and create visualizations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze default data file
  python analyze_eews.py
  
  # Analyze specific data file
  python analyze_eews.py EEW_ALL-2020-2022.txt
  
  # Specify output directory
  python analyze_eews.py --output-dir results
  
  # Apply filters
  python analyze_eews.py --min-mag 5.0 --max-depth 30
        """
    )
    
    parser.add_argument(
        'data_file',
        nargs='?',
        default='EEW_ALL-2014-2025.txt',
        help='Path to EEWS data file (default: EEW_ALL-2014-2025.txt)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='figures',
        help='Output directory for figures (default: figures)'
    )
    
    parser.add_argument(
        '--min-mag',
        type=float,
        default=None,
        help='Minimum magnitude filter'
    )
    
    parser.add_argument(
        '--max-mag',
        type=float,
        default=None,
        help='Maximum magnitude filter'
    )
    
    parser.add_argument(
        '--max-depth',
        type=float,
        default=None,
        help='Maximum depth filter (km)'
    )
    
    parser.add_argument(
        '--no-plots',
        action='store_true',
        help='Skip generating plots (only perform analysis)'
    )
    
    parser.add_argument(
        '--save-csv',
        action='store_true',
        help='Save analysis results to CSV file'
    )
    
    args = parser.parse_args()
    
    # Check if data file exists
    if not Path(args.data_file).exists():
        print(f"Error: Data file '{args.data_file}' not found!")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("EARTHQUAKE EARLY WARNING SYSTEM (EEWS) PERFORMANCE ANALYZER")
    print("="*70)
    print(f"\nData File: {args.data_file}")
    print(f"Output Directory: {args.output_dir}\n")
    
    # Initialize analyzer
    print("Loading data...")
    analyzer = EEWSAnalyzer(args.data_file)
    analyzer.load_data()
    print(f"Loaded {len(analyzer.df)} earthquake events")
    
    # Apply filters if specified
    if args.min_mag is not None or args.max_mag is not None:
        min_mag = args.min_mag if args.min_mag is not None else 0
        max_mag = args.max_mag if args.max_mag is not None else 10
        print(f"\nApplying magnitude filter: {min_mag} <= M <= {max_mag}")
        analyzer.df = analyzer.filter_by_magnitude(min_mag, max_mag)
        print(f"Filtered to {len(analyzer.df)} events")
    
    if args.max_depth is not None:
        print(f"\nApplying depth filter: depth <= {args.max_depth} km")
        analyzer.df = analyzer.filter_by_depth(args.max_depth)
        print(f"Filtered to {len(analyzer.df)} events")
    
    # Perform analysis
    print("\nCalculating errors and statistics...")
    analyzer.calculate_errors()
    analyzer.get_statistics()
    analyzer.print_summary()
    
    # Save results to CSV if requested
    if args.save_csv:
        output_csv = Path(args.output_dir) / "eews_analysis_results.csv"
        Path(args.output_dir).mkdir(exist_ok=True)
        analyzer.save_results(str(output_csv))
    
    # Generate plots
    if not args.no_plots:
        print("\nGenerating visualizations...")
        plotter = EEWSPlotter(analyzer)
        plotter.create_all_plots(args.output_dir)
    
    print("\n" + "="*70)
    print("Analysis complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
