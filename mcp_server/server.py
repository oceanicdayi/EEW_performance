#!/usr/bin/env python3
"""
EEWS Analyzer MCP Server
Provides earthquake early warning system analysis capabilities via Model Context Protocol
"""

import sys
import json
from pathlib import Path
from typing import Any, Sequence
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from eews_analyzer import EEWSAnalyzer
from eews_plotter import EEWSPlotter

# Configure logging to stderr (not stdout, which is used for MCP messages)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("eews-mcp-server")

# Initialize MCP server
server = Server("eews-analyzer-server")

# Global analyzer instance (will be initialized when needed)
_analyzer_cache = {}


def get_analyzer(data_file: str) -> EEWSAnalyzer:
    """Get or create analyzer instance for a data file"""
    if data_file not in _analyzer_cache:
        logger.info(f"Initializing analyzer for {data_file}")
        analyzer = EEWSAnalyzer(data_file)
        analyzer.load_data()
        analyzer.calculate_errors()
        _analyzer_cache[data_file] = analyzer
    return _analyzer_cache[data_file]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available EEWS analysis tools"""
    return [
        Tool(
            name="analyze_eews_data",
            description="Analyze EEWS performance data file and return comprehensive statistics including detection rate, epicenter errors, magnitude errors, and processing times",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_file": {
                        "type": "string",
                        "description": "Path to EEW_ALL data file (e.g., EEW_ALL-2014-2025.txt)"
                    },
                    "min_magnitude": {
                        "type": "number",
                        "description": "Minimum magnitude filter (optional)",
                        "default": 0.0
                    },
                    "max_magnitude": {
                        "type": "number",
                        "description": "Maximum magnitude filter (optional)",
                        "default": 10.0
                    },
                    "max_depth": {
                        "type": "number",
                        "description": "Maximum depth filter in km (optional)",
                        "default": 1000.0
                    }
                },
                "required": ["data_file"]
            }
        ),
        Tool(
            name="get_detection_statistics",
            description="Get detection statistics including total events, detected events, missed events, and detection rate",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_file": {
                        "type": "string",
                        "description": "Path to EEW_ALL data file"
                    }
                },
                "required": ["data_file"]
            }
        ),
        Tool(
            name="get_epicenter_error_statistics",
            description="Get detailed epicenter location error statistics including mean, std dev, median, min, and max errors in kilometers",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_file": {
                        "type": "string",
                        "description": "Path to EEW_ALL data file"
                    }
                },
                "required": ["data_file"]
            }
        ),
        Tool(
            name="get_magnitude_error_statistics",
            description="Get magnitude estimation error statistics including mean, std dev, and RMS error",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_file": {
                        "type": "string",
                        "description": "Path to EEW_ALL data file"
                    }
                },
                "required": ["data_file"]
            }
        ),
        Tool(
            name="get_processing_time_statistics",
            description="Get EEWS processing time statistics showing how quickly warnings are issued after earthquake occurrence",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_file": {
                        "type": "string",
                        "description": "Path to EEW_ALL data file"
                    }
                },
                "required": ["data_file"]
            }
        ),
        Tool(
            name="create_visualization",
            description="Generate visualization plots for EEWS performance analysis (epicenter errors, magnitude comparison, processing times, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_file": {
                        "type": "string",
                        "description": "Path to EEW_ALL data file"
                    },
                    "plot_type": {
                        "type": "string",
                        "description": "Type of plot to generate",
                        "enum": [
                            "epicenter_errors",
                            "magnitude_comparison",
                            "processing_time_map",
                            "missed_events",
                            "processing_time_histogram",
                            "error_distributions",
                            "all"
                        ]
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Output directory for figures (default: figures)",
                        "default": "figures"
                    }
                },
                "required": ["data_file", "plot_type"]
            }
        ),
        Tool(
            name="export_analysis_results",
            description="Export analyzed EEWS data to CSV file with all calculated errors and metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_file": {
                        "type": "string",
                        "description": "Path to EEW_ALL data file"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Output CSV file path",
                        "default": "eews_analysis_results.csv"
                    }
                },
                "required": ["data_file"]
            }
        ),
        Tool(
            name="compare_regions",
            description="Compare EEWS performance between different geographic regions",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_file": {
                        "type": "string",
                        "description": "Path to EEW_ALL data file"
                    },
                    "region1_lon_range": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Region 1 longitude range [min, max]",
                        "minItems": 2,
                        "maxItems": 2
                    },
                    "region1_lat_range": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Region 1 latitude range [min, max]",
                        "minItems": 2,
                        "maxItems": 2
                    },
                    "region2_lon_range": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Region 2 longitude range [min, max]",
                        "minItems": 2,
                        "maxItems": 2
                    },
                    "region2_lat_range": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Region 2 latitude range [min, max]",
                        "minItems": 2,
                        "maxItems": 2
                    }
                },
                "required": ["data_file", "region1_lon_range", "region1_lat_range", "region2_lon_range", "region2_lat_range"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""
    try:
        if name == "analyze_eews_data":
            data_file = arguments["data_file"]
            analyzer = get_analyzer(data_file)
            
            # Apply filters if provided
            if "min_magnitude" in arguments or "max_magnitude" in arguments:
                min_mag = arguments.get("min_magnitude", 0.0)
                max_mag = arguments.get("max_magnitude", 10.0)
                analyzer.df = analyzer.filter_by_magnitude(min_mag, max_mag)
                analyzer.calculate_errors()
            
            if "max_depth" in arguments:
                max_depth = arguments["max_depth"]
                analyzer.df = analyzer.filter_by_depth(max_depth)
                analyzer.calculate_errors()
            
            stats = analyzer.get_statistics()
            
            # Format response
            response = f"""EEWS Performance Analysis Results
{'='*60}

DETECTION STATISTICS:
- Total Earthquakes: {stats['total_earthquakes']}
- Successfully Detected: {stats['eew_detected']}
- Missed Events: {stats['missed_events']}
- Detection Rate: {stats['detection_rate']:.2f}%

EPICENTER ERROR (km):
- Mean: {stats['epicenter_error_mean_km']:.2f}
- Std Dev: {stats['epicenter_error_std_km']:.2f}
- Median: {stats['epicenter_error_median_km']:.2f}
- Range: {stats['epicenter_error_min_km']:.2f} - {stats['epicenter_error_max_km']:.2f}

MAGNITUDE ERROR:
- Mean: {stats['magnitude_error_mean']:.3f}
- Std Dev: {stats['magnitude_error_std']:.3f}
- RMS: {stats['magnitude_error_rms']:.3f}

DEPTH ERROR (km):
- Mean: {stats['depth_error_mean_km']:.2f}
- Std Dev: {stats['depth_error_std_km']:.2f}

PROCESSING TIME (seconds):
- Mean: {stats['processing_time_mean_s']:.2f}
- Std Dev: {stats['processing_time_std_s']:.2f}
- Median: {stats['processing_time_median_s']:.2f}
- Range: {stats['processing_time_min_s']:.2f} - {stats['processing_time_max_s']:.2f}
"""
            return [TextContent(type="text", text=response)]
        
        elif name == "get_detection_statistics":
            data_file = arguments["data_file"]
            analyzer = get_analyzer(data_file)
            stats = analyzer.get_statistics()
            
            response = f"""Detection Statistics:
- Total Earthquakes: {stats['total_earthquakes']}
- Successfully Detected: {stats['eew_detected']}
- Missed Events: {stats['missed_events']}
- Detection Rate: {stats['detection_rate']:.2f}%
"""
            return [TextContent(type="text", text=response)]
        
        elif name == "get_epicenter_error_statistics":
            data_file = arguments["data_file"]
            analyzer = get_analyzer(data_file)
            stats = analyzer.get_statistics()
            
            response = f"""Epicenter Error Statistics (km):
- Mean Error: {stats['epicenter_error_mean_km']:.2f}
- Standard Deviation: {stats['epicenter_error_std_km']:.2f}
- Median Error: {stats['epicenter_error_median_km']:.2f}
- Minimum Error: {stats['epicenter_error_min_km']:.2f}
- Maximum Error: {stats['epicenter_error_max_km']:.2f}
"""
            return [TextContent(type="text", text=response)]
        
        elif name == "get_magnitude_error_statistics":
            data_file = arguments["data_file"]
            analyzer = get_analyzer(data_file)
            stats = analyzer.get_statistics()
            
            response = f"""Magnitude Error Statistics:
- Mean Error: {stats['magnitude_error_mean']:.3f}
- Standard Deviation: {stats['magnitude_error_std']:.3f}
- RMS Error: {stats['magnitude_error_rms']:.3f}
"""
            return [TextContent(type="text", text=response)]
        
        elif name == "get_processing_time_statistics":
            data_file = arguments["data_file"]
            analyzer = get_analyzer(data_file)
            stats = analyzer.get_statistics()
            
            response = f"""Processing Time Statistics (seconds):
- Mean Time: {stats['processing_time_mean_s']:.2f}
- Standard Deviation: {stats['processing_time_std_s']:.2f}
- Median Time: {stats['processing_time_median_s']:.2f}
- Minimum Time: {stats['processing_time_min_s']:.2f}
- Maximum Time: {stats['processing_time_max_s']:.2f}
"""
            return [TextContent(type="text", text=response)]
        
        elif name == "create_visualization":
            data_file = arguments["data_file"]
            plot_type = arguments["plot_type"]
            output_dir = arguments.get("output_dir", "figures")
            
            analyzer = get_analyzer(data_file)
            plotter = EEWSPlotter(analyzer)
            
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            if plot_type == "all":
                plotter.create_all_plots(output_dir)
                response = f"All visualization plots created successfully in {output_dir}/"
            else:
                plot_map = {
                    "epicenter_errors": ("epicenter_error_map.png", plotter.plot_epicenter_errors),
                    "magnitude_comparison": ("magnitude_comparison.png", plotter.plot_magnitude_comparison),
                    "processing_time_map": ("processing_time_map.png", plotter.plot_processing_time_map),
                    "missed_events": ("missed_events_map.png", plotter.plot_missed_events),
                    "processing_time_histogram": ("processing_time_hist.png", plotter.plot_processing_time_histogram),
                    "error_distributions": ("error_distributions.png", plotter.plot_error_distributions)
                }
                
                filename, plot_func = plot_map[plot_type]
                output_file = str(output_path / filename)
                plot_func(output_file)
                response = f"Plot created successfully: {output_file}"
            
            return [TextContent(type="text", text=response)]
        
        elif name == "export_analysis_results":
            data_file = arguments["data_file"]
            output_file = arguments.get("output_file", "eews_analysis_results.csv")
            
            analyzer = get_analyzer(data_file)
            analyzer.save_results(output_file)
            
            response = f"Analysis results exported to: {output_file}"
            return [TextContent(type="text", text=response)]
        
        elif name == "compare_regions":
            data_file = arguments["data_file"]
            analyzer = EEWSAnalyzer(data_file)
            analyzer.load_data()
            
            # Region 1
            region1_lon = tuple(arguments["region1_lon_range"])
            region1_lat = tuple(arguments["region1_lat_range"])
            df1 = analyzer.filter_by_region(region1_lon, region1_lat)
            
            # Calculate stats for region 1
            analyzer.df = df1
            analyzer.calculate_errors()
            stats1 = analyzer.get_statistics()
            
            # Region 2
            analyzer = EEWSAnalyzer(data_file)
            analyzer.load_data()
            region2_lon = tuple(arguments["region2_lon_range"])
            region2_lat = tuple(arguments["region2_lat_range"])
            df2 = analyzer.filter_by_region(region2_lon, region2_lat)
            
            # Calculate stats for region 2
            analyzer.df = df2
            analyzer.calculate_errors()
            stats2 = analyzer.get_statistics()
            
            response = f"""Regional Comparison Analysis
{'='*60}

REGION 1: Lon {region1_lon}, Lat {region1_lat}
- Events: {stats1['total_earthquakes']}
- Detection Rate: {stats1['detection_rate']:.2f}%
- Mean Epicenter Error: {stats1['epicenter_error_mean_km']:.2f} km
- Mean Processing Time: {stats1['processing_time_mean_s']:.2f} s

REGION 2: Lon {region2_lon}, Lat {region2_lat}
- Events: {stats2['total_earthquakes']}
- Detection Rate: {stats2['detection_rate']:.2f}%
- Mean Epicenter Error: {stats2['epicenter_error_mean_km']:.2f} km
- Mean Processing Time: {stats2['processing_time_mean_s']:.2f} s

COMPARISON:
- Detection Rate Difference: {stats1['detection_rate'] - stats2['detection_rate']:.2f}%
- Epicenter Error Difference: {stats1['epicenter_error_mean_km'] - stats2['epicenter_error_mean_km']:.2f} km
- Processing Time Difference: {stats1['processing_time_mean_s'] - stats2['processing_time_mean_s']:.2f} s
"""
            return [TextContent(type="text", text=response)]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server"""
    logger.info("Starting EEWS Analyzer MCP Server")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
