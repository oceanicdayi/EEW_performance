# EEWS Analyzer MCP Server

A Model Context Protocol (MCP) server that provides earthquake early warning system (EEWS) performance analysis capabilities. This server can be used by any MCP-compatible client (Claude Desktop, VS Code, etc.) to analyze EEWS data anywhere, anytime.

## Features

The EEWS Analyzer MCP server exposes 8 powerful tools for earthquake early warning analysis:

### 1. **analyze_eews_data**
Comprehensive analysis of EEWS performance with filtering capabilities.
- Inputs: data file path, optional magnitude/depth filters
- Returns: Complete statistics including detection rate, location errors, magnitude errors, and processing times

### 2. **get_detection_statistics**
Quick overview of detection performance.
- Returns: Total events, detected events, missed events, detection rate

### 3. **get_epicenter_error_statistics**
Detailed epicenter location error analysis.
- Returns: Mean, std dev, median, min, max errors in kilometers

### 4. **get_magnitude_error_statistics**
Magnitude estimation accuracy metrics.
- Returns: Mean error, std dev, RMS error

### 5. **get_processing_time_statistics**
EEWS response time analysis.
- Returns: Mean, std dev, median, min, max processing times

### 6. **create_visualization**
Generate PyGMT-based visualizations.
- Plot types: epicenter errors, magnitude comparison, processing time maps, missed events, histograms, error distributions
- Outputs: High-quality geographic maps and statistical plots

### 7. **export_analysis_results**
Export analyzed data to CSV for further processing.
- Includes all calculated errors and metrics

### 8. **compare_regions**
Compare EEWS performance between different geographic regions.
- Inputs: Two regions defined by lon/lat ranges
- Returns: Side-by-side comparison of all metrics

## Installation

### Prerequisites
- Python 3.8 or higher
- MCP-compatible client (VS Code with Copilot, Claude Desktop, etc.)

### Setup Steps

1. **Install Python dependencies:**
```bash
cd d:\WORK\EEW_performance
pip install -r mcp_server/requirements.txt
```

2. **Configure VS Code (if using VS Code):**
   
   The `.vscode/mcp.json` file is already configured. VS Code will automatically detect and connect to the MCP server.

3. **Configure Claude Desktop (if using Claude Desktop):**
   
   Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):
   
   ```json
   {
     "mcpServers": {
       "eews-analyzer": {
         "command": "python",
         "args": ["-u", "d:\\WORK\\EEW_performance\\mcp_server\\server.py"]
       }
     }
   }
   ```

4. **Restart your MCP client** to load the server.

## Usage Examples

Once the MCP server is running and connected to your client, you can use natural language to interact with it:

### Example 1: Basic Analysis
```
"Analyze the EEWS data in EEW_ALL-2014-2025.txt and give me the detection statistics"
```

### Example 2: Filtered Analysis
```
"Analyze earthquakes with magnitude >= 5.0 in EEW_ALL-2014-2025.txt and show epicenter error statistics"
```

### Example 3: Create Visualizations
```
"Create an epicenter error map from EEW_ALL-2014-2025.txt"
```

### Example 4: Regional Comparison
```
"Compare EEWS performance between northern Taiwan (120-122E, 24-26N) and southern Taiwan (120-122E, 22-24N) using EEW_ALL-2014-2025.txt"
```

### Example 5: Export Results
```
"Export the analysis results to CSV file"
```

## Data Format

The server expects EEWS data files in the following tab-separated format:

```
EQ_ID   Year Month Day Hour Min Sec Lat Lon Depth Mag EEW_Lat EEW_Lon EEW_Depth EEW_Mag Origin_Time EEW_Time
```

Where:
- **EQ_ID**: Unique earthquake identifier
- **Year, Month, Day, Hour, Min, Sec**: Earthquake origin time
- **Lat, Lon**: Epicenter coordinates (catalog values)
- **Depth**: Focal depth in km (catalog value)
- **Mag**: Magnitude (catalog value)
- **EEW_Lat, EEW_Lon**: EEWS estimated epicenter
- **EEW_Depth**: EEWS estimated depth
- **EEW_Mag**: EEWS estimated magnitude
- **Origin_Time**: Earthquake origin timestamp
- **EEW_Time**: EEWS alert timestamp

## Architecture

The MCP server is built using:
- **Python MCP SDK**: Official Python implementation of Model Context Protocol
- **stdio transport**: Local communication between client and server
- **EEWSAnalyzer**: Core analysis engine (from `eews_analyzer.py`)
- **EEWSPlotter**: Visualization engine (from `eews_plotter.py`)

## Troubleshooting

### Server not connecting
1. Check that Python is installed and accessible from PATH
2. Verify all dependencies are installed: `pip install -r mcp_server/requirements.txt`
3. Check the MCP client logs for error messages

### Import errors
- Ensure `eews_analyzer.py` and `eews_plotter.py` are in the workspace root
- Verify the working directory in `mcp.json` is set correctly

### PyGMT errors
- Install GMT first: https://www.generic-mapping-tools.org/download/
- Ensure PyGMT can find GMT: `python -c "import pygmt; pygmt.show_versions()"`

## License

This MCP server wraps the EEWS analysis toolkit developed for earthquake early warning system performance evaluation.
