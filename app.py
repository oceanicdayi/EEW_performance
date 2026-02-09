"""
Interactive EEWS Performance Analysis Dashboard
互動式地震預警系統性能分析儀表板
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from eews_analyzer import EEWSAnalyzer
import os

# Page configuration
st.set_page_config(
    page_title="EEWS Performance Analysis",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🌏 地震預警系統性能分析<br>Earthquake Early Warning System Performance Analysis</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Filters
st.sidebar.header("📊 篩選條件 / Filter Criteria")

# Data file selection
data_file = st.sidebar.selectbox(
    "資料檔案 / Data File",
    ["EEW_ALL-2014-2025.txt", "EEW_ALL-2014-2024.txt"],
    index=0
)

# Magnitude filter
col1, col2 = st.sidebar.columns(2)
with col1:
    min_mag = st.number_input("最小規模 / Min Magnitude", 
                               min_value=3.0, max_value=8.0, 
                               value=5.0, step=0.1)
with col2:
    max_mag = st.number_input("最大規模 / Max Magnitude", 
                               min_value=3.0, max_value=9.0, 
                               value=9.0, step=0.1)

# Depth filter
max_depth = st.sidebar.slider(
    "最大深度 (km) / Max Depth (km)",
    min_value=10, max_value=100, value=40, step=5
)

# Spatial range
st.sidebar.subheader("空間範圍 / Spatial Range")
col3, col4 = st.sidebar.columns(2)
with col3:
    min_lon = st.number_input("最小經度 / Min Lon", 
                               min_value=118.0, max_value=124.0, 
                               value=119.0, step=0.1)
    min_lat = st.number_input("最小緯度 / Min Lat", 
                               min_value=20.0, max_value=27.0, 
                               value=21.0, step=0.1)
with col4:
    max_lon = st.number_input("最大經度 / Max Lon", 
                               min_value=118.0, max_value=124.0, 
                               value=123.0, step=0.1)
    max_lat = st.number_input("最大緯度 / Max Lat", 
                               min_value=20.0, max_value=27.0, 
                               value=26.0, step=0.1)

# Analyze button
analyze_button = st.sidebar.button("🔍 開始分析 / Analyze", type="primary")

# Load and cache data
@st.cache_data
def load_and_analyze_data(data_file, min_mag, max_mag, max_depth, 
                          min_lon, max_lon, min_lat, max_lat):
    """Load and analyze EEWS data"""
    if not os.path.exists(data_file):
        return None, None
    
    # Initialize analyzer
    analyzer = EEWSAnalyzer(data_file, boundary_file="taiwan.txt")
    analyzer.load_data()
    
    # Apply filters
    analyzer.df = analyzer.df[
        (analyzer.df['Cat_Mag'] >= min_mag) & 
        (analyzer.df['Cat_Mag'] <= max_mag) &
        (analyzer.df['Cat_Depth'] <= max_depth) &
        (analyzer.df['Cat_Lon'] >= min_lon) & 
        (analyzer.df['Cat_Lon'] <= max_lon) &
        (analyzer.df['Cat_Lat'] >= min_lat) & 
        (analyzer.df['Cat_Lat'] <= max_lat)
    ]
    
    # Calculate errors
    analyzer.calculate_errors()
    
    # Get statistics
    stats = analyzer.get_statistics()
    
    return analyzer, stats

# Main content
if analyze_button or 'analyzer' not in st.session_state:
    with st.spinner('正在分析數據... / Analyzing data...'):
        analyzer, stats = load_and_analyze_data(
            data_file, min_mag, max_mag, max_depth,
            min_lon, max_lon, min_lat, max_lat
        )
        
        if analyzer is None:
            st.error(f"❌ 找不到資料檔案: {data_file}")
            st.stop()
        
        st.session_state['analyzer'] = analyzer
        st.session_state['stats'] = stats

# Get data from session state
if 'analyzer' in st.session_state:
    analyzer = st.session_state['analyzer']
    stats = st.session_state['stats']
    
    # Check if data exists
    if len(analyzer.df) == 0:
        st.warning("⚠️ 沒有符合條件的地震資料 / No earthquakes match the criteria")
        st.stop()
    
    # Overview metrics
    st.header("📈 整體統計 / Overall Statistics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("總地震數 / Total", 
                  f"{stats['total_earthquakes']}")
    with col2:
        st.metric("發布預警 / Alerts", 
                  f"{stats['eew_detected']}", 
                  f"{stats['detection_rate']:.1f}%")
    with col3:
        st.metric("未發布 / Missed", 
                  f"{stats['missed_events']}")
    with col4:
        st.metric("島內 / Inland", 
                  f"{stats.get('inland_count', 0)}")
    with col5:
        st.metric("外海 / Offshore", 
                  f"{stats.get('offshore_count', 0)}")
    
    st.markdown("---")
    
    # Performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("⏱️ 處理時效 / Processing Time")
        st.metric("平均 / Mean", 
                  f"{stats['processing_time_mean_s']:.2f} 秒")
        st.metric("標準差 / Std Dev", 
                  f"±{stats['processing_time_std_s']:.2f} 秒")
        st.metric("範圍 / Range", 
                  f"{stats['processing_time_min_s']:.1f} - {stats['processing_time_max_s']:.1f} 秒")
    
    with col2:
        st.subheader("📍 震央誤差 / Epicenter Error")
        st.metric("平均 / Mean", 
                  f"{stats['epicenter_error_mean_km']:.2f} 公里")
        st.metric("標準差 / Std Dev", 
                  f"±{stats['epicenter_error_std_km']:.2f} 公里")
        st.metric("中位數 / Median", 
                  f"{stats['epicenter_error_median_km']:.2f} 公里")
    
    with col3:
        st.subheader("📏 規模誤差 / Magnitude Error")
        st.metric("平均 / Mean", 
                  f"{stats['magnitude_error_mean']:.3f}")
        st.metric("標準差 / Std Dev", 
                  f"±{stats['magnitude_error_std']:.3f}")
        st.metric("RMS", 
                  f"{stats['magnitude_error_rms']:.3f}")
    
    st.markdown("---")
    
    # Inland vs Offshore comparison
    if stats.get('inland_count', 0) > 0 and stats.get('offshore_count', 0) > 0:
        st.header("🏝️ 島內 vs 外海比較 / Inland vs Offshore Comparison")
        
        comparison_data = {
            '類別 / Category': ['島內 / Inland', '外海 / Offshore'],
            '數量 / Count': [stats['inland_count'], stats['offshore_count']],
            '平均處理時效 (秒) / Avg Time (s)': [
                stats.get('inland_processing_time_mean_s', 0),
                stats.get('offshore_processing_time_mean_s', 0)
            ],
            '平均震央誤差 (km) / Avg Epi Error (km)': [
                stats.get('inland_epicenter_error_mean_km', 0),
                stats.get('offshore_epicenter_error_mean_km', 0)
            ],
            '規模誤差 RMS / Mag Error RMS': [
                stats.get('inland_magnitude_error_rms', 0),
                stats.get('offshore_magnitude_error_rms', 0)
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
    
    st.markdown("---")
    
    # Interactive plots
    st.header("📊 互動式圖表 / Interactive Plots")
    
    # Prepare data for plotting
    df_plot = analyzer.df_analyzed.copy()
    df_plot['Is_Inland_Label'] = df_plot['Is_Inland'].map({
        True: '島內 / Inland', 
        False: '外海 / Offshore'
    })
    
    # Tab layout for different plots
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ 地震分布圖 / Distribution Map",
        "⏱️ 處理時效分析 / Processing Time",
        "📍 震央誤差分析 / Epicenter Error",
        "📏 規模誤差分析 / Magnitude Error"
    ])
    
    with tab1:
        st.subheader("地震分布圖 / Earthquake Distribution Map")
        
        # Color by selection
        color_by = st.selectbox(
            "著色依據 / Color by:",
            ["處理時效 / Processing Time", 
             "震央誤差 / Epicenter Error",
             "島內/外海 / Inland/Offshore"]
        )
        
        if "處理時效" in color_by:
            color_col = 'Processing_Time'
            color_label = '處理時效 (秒) / Processing Time (s)'
            color_scale = 'RdYlBu_r'
        elif "震央誤差" in color_by:
            color_col = 'Epicenter_Error_km'
            color_label = '震央誤差 (km) / Epicenter Error (km)'
            color_scale = 'Reds'
        else:
            color_col = 'Is_Inland_Label'
            color_label = '類型 / Type'
            color_scale = None
        
        # Create map
        fig_map = px.scatter_geo(
            df_plot,
            lat='Cat_Lat',
            lon='Cat_Lon',
            color=color_col,
            size='Cat_Mag',
            hover_data={
                'Cat_Lon': ':.4f',
                'Cat_Lat': ':.4f',
                'Cat_Mag': ':.2f',
                'Cat_Depth': ':.1f',
                'Processing_Time': ':.1f',
                'Epicenter_Error_km': ':.2f',
                'Is_Inland_Label': True
            },
            labels={
                'Cat_Lon': '經度 / Lon',
                'Cat_Lat': '緯度 / Lat',
                'Cat_Mag': '規模 / Mag',
                'Cat_Depth': '深度 (km) / Depth',
                'Processing_Time': '處理時效 (秒) / Proc Time',
                'Epicenter_Error_km': '震央誤差 (km) / Epi Error',
                'Is_Inland_Label': '類型 / Type'
            },
            color_continuous_scale=color_scale if color_scale else None,
            title=f"地震分布圖 (按{color_by}著色) / Distribution Map (colored by {color_by})"
        )
        
        fig_map.update_geos(
            projection_type="mercator",
            lataxis_range=[min_lat-0.5, max_lat+0.5],
            lonaxis_range=[min_lon-0.5, max_lon+0.5],
            showcountries=True,
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="lightblue"
        )
        
        fig_map.update_layout(height=600, margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
    
    with tab2:
        st.subheader("處理時效分析 / Processing Time Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig_hist = px.histogram(
                df_plot,
                x='Processing_Time',
                color='Is_Inland_Label',
                nbins=30,
                title='處理時效分布 / Processing Time Distribution',
                labels={
                    'Processing_Time': '處理時效 (秒) / Processing Time (s)',
                    'count': '數量 / Count',
                    'Is_Inland_Label': '類型 / Type'
                },
                barmode='overlay',
                opacity=0.7
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot
            fig_box = px.box(
                df_plot,
                x='Is_Inland_Label',
                y='Processing_Time',
                color='Is_Inland_Label',
                title='處理時效比較 / Processing Time Comparison',
                labels={
                    'Processing_Time': '處理時效 (秒) / Processing Time (s)',
                    'Is_Inland_Label': '類型 / Type'
                }
            )
            st.plotly_chart(fig_box, use_container_width=True)
    
    with tab3:
        st.subheader("震央誤差分析 / Epicenter Error Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig_hist = px.histogram(
                df_plot,
                x='Epicenter_Error_km',
                color='Is_Inland_Label',
                nbins=30,
                title='震央誤差分布 / Epicenter Error Distribution',
                labels={
                    'Epicenter_Error_km': '震央誤差 (km) / Epicenter Error (km)',
                    'count': '數量 / Count',
                    'Is_Inland_Label': '類型 / Type'
                },
                barmode='overlay',
                opacity=0.7
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Scatter plot
            fig_scatter = px.scatter(
                df_plot,
                x='Cat_Mag',
                y='Epicenter_Error_km',
                color='Is_Inland_Label',
                size='Processing_Time',
                title='震央誤差 vs 規模 / Epicenter Error vs Magnitude',
                labels={
                    'Cat_Mag': '規模 / Magnitude',
                    'Epicenter_Error_km': '震央誤差 (km) / Epi Error',
                    'Processing_Time': '處理時效 (秒) / Proc Time',
                    'Is_Inland_Label': '類型 / Type'
                },
                hover_data=['Cat_Depth']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab4:
        st.subheader("規模誤差分析 / Magnitude Error Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig_hist = px.histogram(
                df_plot,
                x='Magnitude_Error',
                color='Is_Inland_Label',
                nbins=30,
                title='規模誤差分布 / Magnitude Error Distribution',
                labels={
                    'Magnitude_Error': '規模誤差 / Magnitude Error',
                    'count': '數量 / Count',
                    'Is_Inland_Label': '類型 / Type'
                },
                barmode='overlay',
                opacity=0.7
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Scatter plot: Catalog vs EEW magnitude
            fig_scatter = px.scatter(
                df_plot,
                x='Cat_Mag',
                y='EEW_Mag',
                color='Is_Inland_Label',
                title='目錄規模 vs 預警規模 / Catalog vs EEW Magnitude',
                labels={
                    'Cat_Mag': '目錄規模 / Catalog Magnitude',
                    'EEW_Mag': '預警規模 / EEW Magnitude',
                    'Is_Inland_Label': '類型 / Type'
                },
                hover_data=['Magnitude_Error']
            )
            # Add 1:1 line
            fig_scatter.add_trace(
                go.Scatter(
                    x=[min_mag, max_mag],
                    y=[min_mag, max_mag],
                    mode='lines',
                    name='1:1 line',
                    line=dict(dash='dash', color='gray')
                )
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Data table
    st.header("📋 地震列表 / Earthquake List")
    
    # Select columns to display
    display_columns = ['ID', 'Origin_Time', 'Cat_Lon', 'Cat_Lat', 
                       'Cat_Mag', 'Cat_Depth', 'Processing_Time',
                       'Epicenter_Error_km', 'Magnitude_Error', 'Is_Inland_Label']
    
    # Filter available columns
    available_cols = [col for col in display_columns if col in df_plot.columns]
    
    # Display data
    st.dataframe(
        df_plot[available_cols].sort_values('Origin_Time', ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = df_plot[available_cols].to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 下載 CSV / Download CSV",
        data=csv,
        file_name=f"eews_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.info("👈 請在左側設定篩選條件，然後按「開始分析」按鈕 / Please set filter criteria in the sidebar and click 'Analyze' button")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>地震預警系統性能分析儀表板 / EEWS Performance Analysis Dashboard</p>
    <p>© 2025 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
