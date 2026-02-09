# EEWS Performance Analyzer

A comprehensive Python toolkit for analyzing Earthquake Early Warning System (EEWS) performance by comparing earthquake catalog data with EEWS detection results.

## Features

### Analysis Capabilities
- ✅ **Epicenter Error Analysis**: Calculate distance between catalog and EEWS epicenter locations
- ✅ **Magnitude Comparison**: Compare catalog vs EEWS magnitude estimates with RMS error
- ✅ **Depth Error Analysis**: Evaluate depth estimation accuracy
- ✅ **Processing Time Analysis**: Measure time from earthquake occurrence to alarm issuance
- ✅ **Detection Rate**: Calculate percentage of detected vs missed events
- ✅ **Statistical Summaries**: Mean, standard deviation, median, min/max for all metrics

### Visualization (PyGMT)
- 🗺️ **Epicenter Error Map**: Geographic distribution of location errors with color-coded accuracy
- 📊 **Magnitude Comparison Plot**: Scatter plot of catalog vs EEW magnitudes with error bounds
- ⏱️ **Processing Time Map**: Spatial distribution of processing times
- 🎯 **Detection Coverage Map**: Shows detected vs missed events geographically
- 📈 **Statistical Plots**: Histograms and distributions of all error metrics
- 📉 **Multi-panel Error Analysis**: Comprehensive error distribution dashboard

## Installation

### Requirements
```bash
# Create a virtual environment (recommended)
python -m venv eews_env
source eews_env/bin/activate  # On Windows: eews_env\Scripts\activate

# Install required packages
pip install numpy pandas matplotlib pygmt
```

### Package Dependencies
- `numpy` - Numerical computations
- `pandas` - Data manipulation and analysis
- `matplotlib` - Statistical plotting
- `pygmt` - Geographic mapping and visualization

## Data Format

The input file should be a tab/space-separated text file with the following format:

```
Type	ID	Earthquake_occurrenceTime	Epicenter_Lon	Epicenter_Lat	Epicenter_Mag	Epicenter_Depth	EEW_Lon	EEW_Lat	EEW_Mag	EEW_Dep	EEW_processing_time
xY	1	201401141644027	120.9843	23.8608	4.97	14.98	121.01	23.85	4.7	10	14
xN	2	201401162040019	123.3007	24.8333	5.23	130.98					
xL	3	201401061849040	122.9468	25.3803	5.78	226.55					
```

### Column Descriptions:
- **Type**: Event classification
  - `xY` or `oY`: Successfully detected by EEWS
  - `xN`: Missed detection (no warning issued)
  - `xL`: Late detection (too slow for early warning)
- **ID**: Event identifier
- **Earthquake_occurrenceTime**: Origin time (YYYYMMDDHHMMSSs)
- **Epicenter_Lon/Lat**: Catalog epicenter location (degrees)
- **Epicenter_Mag**: Catalog magnitude
- **Epicenter_Depth**: Catalog depth (km)
- **EEW_Lon/Lat**: EEWS-estimated epicenter (only for detected events)
- **EEW_Mag**: EEWS-estimated magnitude (only for detected events)
- **EEW_Dep**: EEWS-estimated depth (only for detected events)
- **EEW_processing_time**: Time from origin to alarm issuance (seconds)

## Usage

### Basic Analysis

```bash
# Analyze default data file (EEW_ALL-2014-2025.txt)
python analyze_eews.py

# Analyze specific data file
python analyze_eews.py EEW_ALL-2020-2022.txt

# Save results to CSV
python analyze_eews.py --save-csv
```

### Advanced Options

```bash
# Apply magnitude filter (M >= 5.0)
python analyze_eews.py --min-mag 5.0

# Apply depth filter (depth <= 40 km)
python analyze_eews.py --max-depth 40

# Combine filters
python analyze_eews.py --min-mag 5.0 --max-depth 30

# Specify output directory
python analyze_eews.py --output-dir results_2024

# Analysis only (no plots)
python analyze_eews.py --no-plots
```

### Python API

```python
from eews_analyzer import EEWSAnalyzer
from eews_plotter import EEWSPlotter

# Initialize analyzer
analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")

# Load and analyze data
analyzer.load_data()
analyzer.calculate_errors()
stats = analyzer.get_statistics()

# Print summary
analyzer.print_summary()

# Apply filters
filtered_df = analyzer.filter_by_magnitude(min_mag=5.0)
filtered_df = analyzer.filter_by_depth(max_depth=40)

# Get specific event types
detected = analyzer.get_detected_events()
missed = analyzer.get_missed_events()

# Create visualizations
plotter = EEWSPlotter(analyzer)
plotter.create_all_plots("output_figures")

# Or create individual plots
plotter.plot_epicenter_errors("epicenter_map.png")
plotter.plot_magnitude_comparison("magnitude_plot.png")
plotter.plot_processing_time_map("processing_time.png")
```

## Output Files

### Figures (in `figures/` directory):
1. **epicenter_error_map.png** - Map showing location errors with connecting lines
2. **magnitude_comparison.png** - Scatter plot of catalog vs EEW magnitudes
3. **processing_time_map.png** - Map colored by processing time
4. **missed_events_map.png** - Detected (green circles) vs missed (red triangles)
5. **processing_time_hist.png** - Histogram of processing time distribution
6. **error_distributions.png** - 6-panel comprehensive error analysis

### Data Output (optional):
- **eews_analysis_results.csv** - Full analyzed dataset with calculated errors

## Performance Metrics

The analysis calculates the following key metrics:

### Detection Performance
- Total number of earthquakes
- Number of detected events
- Number of missed events
- Detection rate (%)

### Location Accuracy
- Mean epicenter error (km)
- Standard deviation of epicenter error
- Median epicenter error
- Min/max epicenter error

### Magnitude Accuracy
- Mean magnitude error
- Standard deviation of magnitude error
- RMS magnitude error

### Depth Accuracy
- Mean depth error (km)
- Standard deviation of depth error

### Timing Performance
- Mean processing time (seconds)
- Median processing time
- Processing time range
- Standard deviation

## Example Output

```
======================================================================
EARTHQUAKE EARLY WARNING SYSTEM (EEWS) PERFORMANCE SUMMARY
======================================================================

📊 DETECTION STATISTICS:
  Total Earthquakes:            973
  Successfully Detected:        652
  Missed Events:                321
  Detection Rate:              67.01%

📍 EPICENTER ERROR (km):
  Mean:                        15.24
  Std Dev:                     12.87
  Median:                      12.45
  Range:                        0.85 - 78.32

📏 MAGNITUDE ERROR:
  Mean:                         0.287
  Std Dev:                      0.245
  RMS:                          0.376

⬇️  DEPTH ERROR (km):
  Mean:                        12.56
  Std Dev:                     15.23

⏱️  PROCESSING TIME (seconds):
  Mean:                        15.32
  Std Dev:                      6.87
  Median:                      14.00
  Range:                        6.60 - 34.00
======================================================================
```

## Comparison with Original GMT Scripts

This toolkit replaces the original GMT batch scripts with modern Python/PyGMT:

| Original GMT Script | New PyGMT Function | Description |
|---------------------|-------------------|-------------|
| `loc_err.bat` | `plot_epicenter_errors()` | Epicenter error map |
| `magplot.bat` | `plot_magnitude_comparison()` | Magnitude comparison |
| `pro_time.bat` | `plot_processing_time_map()` | Processing time map |
| `plot_miss.bat` | `plot_missed_events()` | Detection coverage |
| `plot_seismicity.bat` | Multiple functions | Seismicity visualization |

### Advantages over GMT scripts:
- ✅ Cross-platform (no Windows-specific paths)
- ✅ Easier to modify and extend
- ✅ Integrated analysis and visualization
- ✅ Better error handling
- ✅ Reproducible with version control
- ✅ No external GMT installation required
- ✅ Publication-quality output

## File Structure

```
EEW_performance/
├── analyze_eews.py          # Main analysis script
├── eews_analyzer.py         # Analysis class
├── eews_plotter.py          # Visualization class
├── EEW_ALL-2014-2025.txt    # Input data file
├── README.md                # This file
├── requirements.txt         # Package dependencies
└── figures/                 # Output directory (created automatically)
    ├── epicenter_error_map.png
    ├── magnitude_comparison.png
    ├── processing_time_map.png
    ├── missed_events_map.png
    ├── processing_time_hist.png
    └── error_distributions.png
```

## Troubleshooting

### PyGMT Installation Issues
If you encounter PyGMT installation problems:

```bash
# Try installing with conda (recommended for PyGMT)
conda install -c conda-forge pygmt

# Or use pip with specific version
pip install pygmt==0.10.0
```

### GMT Backend Issues
PyGMT requires GMT 6.3 or newer. Check your GMT version:
```python
import pygmt
print(pygmt.show_versions())
```

### Memory Issues with Large Datasets
For very large datasets (>10,000 events):
```python
# Process in chunks or filter data first
analyzer.df = analyzer.filter_by_magnitude(min_mag=4.5)
```

## Contributing

Suggestions and improvements welcome! Key areas for enhancement:
- Additional statistical tests
- Machine learning-based error prediction
- Real-time analysis capabilities
- Web-based dashboard
- Additional visualization types

## Citation

If you use this tool in research, please cite:
```
EEWS Performance Analyzer (2025)
https://github.com/[your-repo]/eews-analyzer
```

## License

MIT License - Feel free to use and modify as needed.

## Contact

For questions or issues, please open a GitHub issue or contact [your-email].

---

**Last Updated:** January 2025  
**Version:** 1.0.0  
**Python Version:** 3.8+
