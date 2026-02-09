"""
Plot earthquake distribution map (2014-2024) with PyGMT
Distinguishes inland and offshore earthquakes with different colors
Circle sizes represent earthquake magnitude
"""

import pygmt
import pandas as pd
import numpy as np


def plot_earthquake_distribution_gmt(output_file="outputs/earthquake_distribution_gmt_2014_2025.png", dpi=300):
    """
    Create map with earthquakes colored by location (inland/offshore).
    Circle sizes represent earthquake magnitude.
    
    Args:
        output_file: Output filename
        dpi: Resolution in dots per inch
    """
    
    # Read earthquake data
    print("正在读取地震数据...")
    eq_file = 'outputs/earthquake_list_2014_2025.csv'
    
    try:
        df = pd.read_csv(eq_file, encoding='utf-8-sig')
    except FileNotFoundError:
        print(f"错误: 找不到文件 {eq_file}")
        print("请先运行 analyze_2014_2024_summary.py 生成数据文件")
        return
    
    # Convert data types
    df['经度'] = pd.to_numeric(df['经度'], errors='coerce')
    df['纬度'] = pd.to_numeric(df['纬度'], errors='coerce')
    df['规模'] = pd.to_numeric(df['规模'], errors='coerce')
    df['处理时效(秒)'] = pd.to_numeric(df['处理时效(秒)'], errors='coerce')
    
    # Filter only events with EEW (with processing time)
    df = df[df['是否发布预警'] == '是'].copy()
    df = df.dropna(subset=['处理时效(秒)']).copy()
    
    print(f"具有处理时效的地震: {len(df)} 笔")
    print(f"处理时效范围: {df['处理时效(秒)'].min():.0f} - {df['处理时效(秒)'].max():.0f} 秒")
    
    # Taiwan region (統計空間範圍: 119~123, 21~26)
    region = [119.0, 123.0, 21.0, 26.0]
    
    fig = pygmt.Figure()
    
    # Setup map with frame
    fig.basemap(
        region=region,
        projection="M15c",
        frame=["WSne+t2014-2025 EEW Performance (Processing Time)", 
               "xa1f0.5+lLongitude", 
               "ya1f0.5+lLatitude"]
    )
    
    # Draw coastline
    fig.coast(
        region=region,
        projection="M15c",
        shorelines="1p,black",
        land="lightgray",
        water="lightblue",
        borders="1/0.5p,black"
    )
    
    # Draw Taiwan boundary from taiwan.txt
    try:
        print("正在加载台湾边界...")
        boundary_data = pd.read_csv('taiwan.txt', sep=r'\s+', header=None, names=['lon', 'lat'])
        fig.plot(
            x=boundary_data['lon'],
            y=boundary_data['lat'],
            pen="1.5p,red,solid"
        )
        print("台湾边界已绘制")
    except FileNotFoundError:
        print("警告: 找不到 taiwan.txt 文件，跳过边界绘制")
    
    # Scale factor for magnitude to circle size
    # Using exponential scaling to make larger earthquakes more prominent
    def mag_to_size(mag):
        """Convert magnitude to circle size in cm"""
        return 0.05 * (mag ** 2) * 0.3  # Reduced to 0.3x original size
    
    # Calculate circle sizes
    circle_sizes = df['规模'].apply(mag_to_size).values
    
    # Get processing times for color mapping
    processing_times = df['处理时效(秒)'].values
    min_time = processing_times.min()
    max_time = processing_times.max()
    
    print(f"绘制 {len(df)} 個地震...")
    print(f"處理時效著色範圍: {min_time:.1f} - {max_time:.1f} 秒")
    
    # Define color range for processing time
    # Blue (cold) = fast, Red (hot) = slow
    pygmt.makecpt(cmap="polar", series=[min_time, max_time])
    
    # Plot earthquakes with color representing processing time
    # Use a color palette: blue (fast) to red (slow)
    fig.plot(
        x=df['经度'].values,
        y=df['纬度'].values,
        size=circle_sizes,
        style="c",
        fill=processing_times,  # Color by processing time
        cmap=True,  # Use the CPT created above
        pen="0.3p,black",
        transparency=20  # 20% transparency
    )
    
    # Add colorbar for processing time
    fig.colorbar(
        position="JMR+o0.5c/0c+w8c/0.5c+e",
        frame=[f"x+lProcessing Time (sec)", "y+ls"]
    )
    
    # Add scale bar
    fig.basemap(
        map_scale="jBR+w100k+o0.5c/0.5c+f+lkm"
    )
    
    # Save figure
    print(f"\n正在保存图形...")
    fig.savefig(output_file, dpi=dpi)
    print(f"地震分布图已保存至: {output_file}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("地震分布图绘制 (PyGMT)")
    print("Earthquake Distribution Map (PyGMT)")
    print("="*70 + "\n")
    
    # Create plot
    plot_earthquake_distribution_gmt()
    
    print("\n完成!")
    print("Done!\n")
