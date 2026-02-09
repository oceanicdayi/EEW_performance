# EEWS Performance Analyzer - Quick Start Guide

## Installation (5 minutes)

```bash
# 1. Install required packages
pip install -r requirements.txt

# Or install individually:
pip install numpy pandas matplotlib pygmt
```

## Quick Analysis (30 seconds)

```bash
# Run complete analysis with all visualizations
python analyze_eews.py
```

This will:
- Load and analyze the EEWS data
- Print performance statistics
- Create 6 publication-quality figures in `figures/` directory

## View Results

Check the `figures/` directory for:
- `epicenter_error_map.png` - Location accuracy map
- `magnitude_comparison.png` - Magnitude accuracy plot
- `processing_time_map.png` - Processing time distribution
- `missed_events_map.png` - Detection coverage
- `processing_time_hist.png` - Timing histogram
- `error_distributions.png` - Comprehensive error analysis

## Common Use Cases

### 1. Filter by magnitude (M ≥ 5.0 only)
```bash
python analyze_eews.py --min-mag 5.0
```

### 2. Shallow earthquakes only (depth ≤ 30 km)
```bash
python analyze_eews.py --max-depth 30
```

### 3. Specific time period
```bash
python analyze_eews.py EEW_ALL-2020-2022.txt
```

### 4. Save data to CSV
```bash
python analyze_eews.py --save-csv
```

### 5. Just statistics (no plots)
```bash
python analyze_eews.py --no-plots
```

## Python API Quick Examples

### Basic usage
```python
from eews_analyzer import EEWSAnalyzer

analyzer = EEWSAnalyzer("EEW_ALL-2014-2025.txt")
analyzer.load_data()
analyzer.calculate_errors()
analyzer.print_summary()
```

### Create specific plots
```python
from eews_plotter import EEWSPlotter

plotter = EEWSPlotter(analyzer)
plotter.plot_epicenter_errors("my_map.png")
plotter.plot_magnitude_comparison("my_plot.png")
```

### Filter data
```python
# Magnitude filter
filtered = analyzer.filter_by_magnitude(min_mag=5.0, max_mag=7.0)

# Depth filter
shallow = analyzer.filter_by_depth(max_depth=40.0)

# Regional filter (Taiwan region)
regional = analyzer.filter_by_region(
    lon_range=(120.0, 122.0), 
    lat_range=(23.0, 25.0)
)
```

### Get event statistics
```python
# Get detected vs missed
detected = analyzer.get_detected_events()
missed = analyzer.get_missed_events()

print(f"Detection rate: {len(detected)/(len(detected)+len(missed))*100:.1f}%")
```

## Interactive Examples

```bash
# Run all tutorial examples
python examples.py

# Run specific example (1-8)
python examples.py 1  # Basic analysis
python examples.py 5  # Custom visualizations
python examples.py 7  # Processing time analysis
```

## Troubleshooting

### PyGMT not installing?
```bash
conda install -c conda-forge pygmt
```

### File not found error?
Make sure you're in the correct directory:
```bash
cd d:\WORK\EEW_performance
python analyze_eews.py
```

### No figures generated?
Check if PyGMT is properly installed:
```python
import pygmt
print(pygmt.__version__)
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore [examples.py](examples.py) for advanced usage patterns
3. Modify plotting functions in [eews_plotter.py](eews_plotter.py) for custom visualizations
4. Extend analysis in [eews_analyzer.py](eews_analyzer.py) for new metrics

## Key Performance Metrics

The analysis automatically calculates:

✅ **Detection Rate** - Percentage of earthquakes detected  
✅ **Epicenter Error** - Location accuracy in km  
✅ **Magnitude Error** - Magnitude estimation accuracy  
✅ **Depth Error** - Depth estimation accuracy in km  
✅ **Processing Time** - Speed of warning issuance in seconds  

All metrics include: mean, median, standard deviation, min/max

## Support

For issues or questions:
- Check existing examples in `examples.py`
- Review detailed documentation in `README.md`
- Examine the source code (well-documented)

---

**Total setup time:** < 5 minutes  
**First analysis:** < 30 seconds  
**Learning curve:** Minimal - just run `python analyze_eews.py`
