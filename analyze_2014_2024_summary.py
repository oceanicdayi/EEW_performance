#!/usr/bin/env python
"""
EEWS Performance Analysis 2014-2024
分析2014年至2024年12月的地震预警系统性能
规模 > 5.0 且深度 < 40 km
分别统计岛内和外海地震
"""

import pandas as pd
import numpy as np
from eews_analyzer import EEWSAnalyzer


def main():
    print("\n" + "="*80)
    print("地震预警系统性能统计分析 (2014-2025)")
    print("Earthquake Early Warning System Performance Analysis (2014-2025)")
    print("="*80)
    
    # Initialize analyzer
    data_file = "EEW_ALL-2014-2025.txt"
    analyzer = EEWSAnalyzer(data_file, boundary_file="taiwan.txt")
    
    # Load data
    print("\n正在加载数据...")
    print("Loading data...")
    analyzer.load_data()
    
    # Apply filters: magnitude > 5.0 and depth < 40 km
    min_mag = 5.0
    max_depth = 40.0
    min_lon = 119.0
    max_lon = 123.0
    min_lat = 21.0
    max_lat = 26.0
    
    print(f"\n筛选条件 (Filter criteria):")
    print(f"  规模 (Magnitude):  > {min_mag}")
    print(f"  深度 (Depth):      < {max_depth} km")
    print(f"  经度范围 (Longitude):  {min_lon} ~ {max_lon}")
    print(f"  纬度范围 (Latitude):   {min_lat} ~ {max_lat}")
    print(f"  时间范围 (Period): 2014-2025年")
    print("-"*80)
    
    original_count = len(analyzer.df)
    analyzer.df = analyzer.df[
        (analyzer.df['Cat_Mag'] > min_mag) & 
        (analyzer.df['Cat_Depth'] < max_depth) &
        (analyzer.df['Cat_Lon'] >= min_lon) & 
        (analyzer.df['Cat_Lon'] <= max_lon) &
        (analyzer.df['Cat_Lat'] >= min_lat) & 
        (analyzer.df['Cat_Lat'] <= max_lat)
    ]
    filtered_count = len(analyzer.df)
    
    print(f"\n符合条件的地震总数: {filtered_count} (筛选前: {original_count})")
    print(f"Total eligible earthquakes: {filtered_count} (before filtering: {original_count})")
    
    if filtered_count == 0:
        print("\n警告: 没有符合条件的地震事件!")
        return
    
    # Calculate errors for all events
    analyzer.calculate_errors()
    
    # Get detected events with EEW data
    df_detected = analyzer.df_analyzed
    
    # Separate inland and offshore events
    if 'Is_Inland' in df_detected.columns:
        df_inland = df_detected[df_detected['Is_Inland'] == True].copy()
        df_offshore = df_detected[df_detected['Is_Inland'] == False].copy()
    else:
        print("\n警告: 无法分类岛内/外海地震，缺少边界数据文件!")
        df_inland = pd.DataFrame()
        df_offshore = pd.DataFrame()
    
    # Print comprehensive statistics
    print("\n" + "="*80)
    print("统计结果 (Statistical Results)")
    print("="*80)
    
    # Overall statistics
    print("\n【整体统计 Overall Statistics】")
    print(f"  符合条件的地震总数 (Total earthquakes):           {filtered_count}")
    print(f"  成功发布预警次数 (Alerts issued):                 {len(df_detected)}")
    print(f"  未能发布次数 (Missed):                            {filtered_count - len(df_detected)}")
    print(f"  发布率 (Alert rate):                              {len(df_detected)/filtered_count*100:.1f}%")
    
    if len(df_detected) > 0:
        print(f"\n  平均处理时效 (Avg processing time):               {df_detected['Processing_Time'].mean():.2f} 秒 (seconds)")
        print(f"  平均震央误差 (Avg epicenter error):               {df_detected['Epicenter_Error_km'].mean():.2f} 公里 (km)")
        print(f"  平均规模误差 (Avg magnitude error):               {df_detected['Magnitude_Error'].mean():.3f}")
        print(f"  规模误差RMS (Magnitude error RMS):                {np.sqrt(np.mean(df_detected['Magnitude_Error']**2)):.3f}")
    
    # Inland statistics
    if len(df_inland) > 0:
        print("\n" + "-"*80)
        print("【岛内地震统计 Inland Earthquakes】")
        print(f"  发布次数 (Number of alerts):                      {len(df_inland)}")
        print(f"  平均处理时效 (Avg processing time):               {df_inland['Processing_Time'].mean():.2f} 秒 (seconds)")
        print(f"                                                     标准差 (±{df_inland['Processing_Time'].std():.2f} s)")
        print(f"  平均震央误差 (Avg epicenter error):               {df_inland['Epicenter_Error_km'].mean():.2f} 公里 (km)")
        print(f"                                                     标准差 (±{df_inland['Epicenter_Error_km'].std():.2f} km)")
        print(f"  平均规模误差 (Avg magnitude error):               {df_inland['Magnitude_Error'].mean():.3f}")
        print(f"                                                     标准差 (±{df_inland['Magnitude_Error'].std():.3f})")
        print(f"  规模误差RMS (Magnitude error RMS):                {np.sqrt(np.mean(df_inland['Magnitude_Error']**2)):.3f}")
    else:
        print("\n【岛内地震统计 Inland Earthquakes】")
        print("  无数据 (No data)")
    
    # Offshore statistics
    if len(df_offshore) > 0:
        print("\n" + "-"*80)
        print("【外海地震统计 Offshore Earthquakes】")
        print(f"  发布次数 (Number of alerts):                      {len(df_offshore)}")
        print(f"  平均处理时效 (Avg processing time):               {df_offshore['Processing_Time'].mean():.2f} 秒 (seconds)")
        print(f"                                                     标准差 (±{df_offshore['Processing_Time'].std():.2f} s)")
        print(f"  平均震央误差 (Avg epicenter error):               {df_offshore['Epicenter_Error_km'].mean():.2f} 公里 (km)")
        print(f"                                                     标准差 (±{df_offshore['Epicenter_Error_km'].std():.2f} km)")
        print(f"  平均规模误差 (Avg magnitude error):               {df_offshore['Magnitude_Error'].mean():.3f}")
        print(f"                                                     标准差 (±{df_offshore['Magnitude_Error'].std():.3f})")
        print(f"  规模误差RMS (Magnitude error RMS):                {np.sqrt(np.mean(df_offshore['Magnitude_Error']**2)):.3f}")
    else:
        print("\n【外海地震统计 Offshore Earthquakes】")
        print("  无数据 (No data)")
    
    # Create summary table
    print("\n" + "="*80)
    print("汇总表 (Summary Table)")
    print("="*80)
    print(f"\n{'类别 Category':<20} {'发布次数':<12} {'平均时效(秒)':<16} {'平均震央误差(km)':<18} {'平均规模误差':<12}")
    print(f"{'':20} {'Alerts':<12} {'Proc.Time(s)':<16} {'Epi.Error(km)':<18} {'Mag.Error':<12}")
    print("-"*80)
    
    if len(df_detected) > 0:
        print(f"{'整体 Overall':<20} {len(df_detected):<12} {df_detected['Processing_Time'].mean():<16.2f} "
              f"{df_detected['Epicenter_Error_km'].mean():<18.2f} {df_detected['Magnitude_Error'].mean():<12.3f}")
    
    if len(df_inland) > 0:
        print(f"{'岛内 Inland':<20} {len(df_inland):<12} {df_inland['Processing_Time'].mean():<16.2f} "
              f"{df_inland['Epicenter_Error_km'].mean():<18.2f} {df_inland['Magnitude_Error'].mean():<12.3f}")
    
    if len(df_offshore) > 0:
        print(f"{'外海 Offshore':<20} {len(df_offshore):<12} {df_offshore['Processing_Time'].mean():<16.2f} "
              f"{df_offshore['Epicenter_Error_km'].mean():<18.2f} {df_offshore['Magnitude_Error'].mean():<12.3f}")
    
    print("\n" + "="*80)
    
    # Save detailed results to CSV
    output_file = "outputs/eews_summary_2014_2025.csv"
    import os
    os.makedirs("outputs", exist_ok=True)
    
    # Create summary dataframe
    summary_data = []
    
    if len(df_detected) > 0:
        summary_data.append({
            '类别': '整体 Overall',
            '发布次数': len(df_detected),
            '平均处理时效(秒)': f"{df_detected['Processing_Time'].mean():.2f}",
            '处理时效标准差': f"{df_detected['Processing_Time'].std():.2f}",
            '平均震央误差(km)': f"{df_detected['Epicenter_Error_km'].mean():.2f}",
            '震央误差标准差': f"{df_detected['Epicenter_Error_km'].std():.2f}",
            '平均规模误差': f"{df_detected['Magnitude_Error'].mean():.3f}",
            '规模误差标准差': f"{df_detected['Magnitude_Error'].std():.3f}",
            '规模误差RMS': f"{np.sqrt(np.mean(df_detected['Magnitude_Error']**2)):.3f}"
        })
    
    if len(df_inland) > 0:
        summary_data.append({
            '类别': '岛内 Inland',
            '发布次数': len(df_inland),
            '平均处理时效(秒)': f"{df_inland['Processing_Time'].mean():.2f}",
            '处理时效标准差': f"{df_inland['Processing_Time'].std():.2f}",
            '平均震央误差(km)': f"{df_inland['Epicenter_Error_km'].mean():.2f}",
            '震央误差标准差': f"{df_inland['Epicenter_Error_km'].std():.2f}",
            '平均规模误差': f"{df_inland['Magnitude_Error'].mean():.3f}",
            '规模误差标准差': f"{df_inland['Magnitude_Error'].std():.3f}",
            '规模误差RMS': f"{np.sqrt(np.mean(df_inland['Magnitude_Error']**2)):.3f}"
        })
    
    if len(df_offshore) > 0:
        summary_data.append({
            '类别': '外海 Offshore',
            '发布次数': len(df_offshore),
            '平均处理时效(秒)': f"{df_offshore['Processing_Time'].mean():.2f}",
            '处理时效标准差': f"{df_offshore['Processing_Time'].std():.2f}",
            '平均震央误差(km)': f"{df_offshore['Epicenter_Error_km'].mean():.2f}",
            '震央误差标准差': f"{df_offshore['Epicenter_Error_km'].std():.2f}",
            '平均规模误差': f"{df_offshore['Magnitude_Error'].mean():.3f}",
            '规模误差标准差': f"{df_offshore['Magnitude_Error'].std():.3f}",
            '规模误差RMS': f"{np.sqrt(np.mean(df_offshore['Magnitude_Error']**2)):.3f}"
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n结果已保存至: {output_file}")
    print(f"Results saved to: {output_file}")
    
    # Save detailed earthquake list
    detail_file = "outputs/earthquake_list_2014_2025.csv"
    
    # Prepare detailed list with all filtered earthquakes
    earthquake_list = []
    for idx, row in analyzer.df.iterrows():
        # Check if EEW was issued
        has_eew = 'Y' in str(row['Type'])
        
        eq_info = {
            '序号': row['ID'],
            '类型': row['Type'],
            '发生时间': row['Origin_Time'],
            '经度': f"{row['Cat_Lon']:.4f}",
            '纬度': f"{row['Cat_Lat']:.4f}",
            '规模': f"{row['Cat_Mag']:.2f}",
            '深度(km)': f"{row['Cat_Depth']:.2f}",
            '岛内/外海': '岛内' if row.get('Is_Inland') == True else ('外海' if row.get('Is_Inland') == False else '未知'),
            '是否发布预警': '是' if has_eew else '否'
        }
        
        if has_eew and not pd.isna(row.get('EEW_Lon')):
            eq_info['预警经度'] = f"{row['EEW_Lon']:.4f}"
            eq_info['预警纬度'] = f"{row['EEW_Lat']:.4f}"
            eq_info['预警规模'] = f"{row['EEW_Mag']:.1f}"
            eq_info['预警深度(km)'] = f"{row['EEW_Depth']:.0f}"
            eq_info['处理时效(秒)'] = f"{row['Processing_Time']:.0f}"
        else:
            eq_info['预警经度'] = ''
            eq_info['预警纬度'] = ''
            eq_info['预警规模'] = ''
            eq_info['预警深度(km)'] = ''
            eq_info['处理时效(秒)'] = ''
        
        earthquake_list.append(eq_info)
    
    eq_df = pd.DataFrame(earthquake_list)
    eq_df.to_csv(detail_file, index=False, encoding='utf-8-sig')
    
    print(f"\n地震详细列表已保存至: {detail_file}")
    print(f"Detailed earthquake list saved to: {detail_file}")
    
    # Display first 20 earthquakes
    print("\n" + "="*80)
    print("地震列表 (前20笔) Earthquake List (First 20)")
    print("="*80)
    print(f"\n{'序号':<6} {'发生时间':<16} {'经纬度':<20} {'规模':<6} {'深度':<8} {'类型':<8} {'预警':<6}")
    print(f"{'ID':<6} {'Time':<16} {'Lon/Lat':<20} {'Mag':<6} {'Depth':<8} {'Region':<8} {'Alert':<6}")
    print("-"*80)
    
    for i, eq in enumerate(earthquake_list[:20]):
        time_str = str(eq['发生时间'])[:15] if len(str(eq['发生时间'])) > 15 else str(eq['发生时间'])
        coord = f"{eq['经度'][:7]}/{eq['纬度'][:6]}"
        region = eq['岛内/外海'][:4]
        alert = eq['是否发布预警']
        
        print(f"{eq['序号']:<6} {time_str:<16} {coord:<20} {eq['规模']:<6} "
              f"{eq['深度(km)']:<8} {region:<8} {alert:<6}")
    
    if len(earthquake_list) > 20:
        print(f"\n... 共 {len(earthquake_list)} 笔地震记录 (Total {len(earthquake_list)} earthquakes)")
    
    print("\n完成! (Completed!)\n")


if __name__ == "__main__":
    main()
