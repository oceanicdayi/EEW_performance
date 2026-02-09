#!/usr/bin/env python
"""
绘制2014-2024年地震分布图
Plot earthquake distribution map for 2014-2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_taiwan_boundary(boundary_file='taiwan.txt'):
    """加载台湾边界数据"""
    try:
        lons, lats = [], []
        with open(boundary_file, 'r') as f:
            for line in f:
                data = line.split()
                if len(data) >= 2:
                    lons.append(float(data[0]))
                    lats.append(float(data[1]))
        return lons, lats
    except FileNotFoundError:
        print(f"Warning: Boundary file '{boundary_file}' not found.")
        return [], []


def magnitude_to_size(magnitude, scale_factor=50):
    """将地震规模转换为圆圈大小"""
    # 使用指数函数使大地震更明显
    return scale_factor * (magnitude ** 2)


def plot_earthquakes():
    """绘制地震分布图"""
    
    # 读取地震数据
    print("正在读取地震数据...")
    eq_file = 'outputs/earthquake_list_2014_2024.csv'
    
    if not Path(eq_file).exists():
        print(f"错误: 找不到文件 {eq_file}")
        print("请先运行 analyze_2014_2024_summary.py 生成数据文件")
        return
    
    df = pd.read_csv(eq_file, encoding='utf-8-sig')
    
    # 转换数据类型
    df['经度'] = pd.to_numeric(df['经度'], errors='coerce')
    df['纬度'] = pd.to_numeric(df['纬度'], errors='coerce')
    df['规模'] = pd.to_numeric(df['规模'], errors='coerce')
    
    # 分类岛内和外海地震
    df_inland = df[df['岛内/外海'] == '岛内'].copy()
    df_offshore = df[df['岛内/外海'] == '外海'].copy()
    
    print(f"岛内地震: {len(df_inland)} 笔")
    print(f"外海地震: {len(df_offshore)} 笔")
    
    # 加载台湾边界
    boundary_lons, boundary_lats = load_taiwan_boundary()
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 14))
    
    # 绘制台湾边界
    if boundary_lons:
        ax.plot(boundary_lons, boundary_lats, 'k-', linewidth=1.5, 
                label='台湾边界', zorder=1, alpha=0.6)
    
    # 定义颜色和标记
    inland_color = '#FF6B6B'      # 红色 - 岛内地震
    offshore_color = '#4ECDC4'    # 青色 - 外海地震
    
    # 绘制外海地震（先画，使其在下层）
    if len(df_offshore) > 0:
        sizes_offshore = df_offshore['规模'].apply(magnitude_to_size)
        scatter_offshore = ax.scatter(
            df_offshore['经度'], 
            df_offshore['纬度'],
            s=sizes_offshore,
            c=offshore_color,
            alpha=0.6,
            edgecolors='darkblue',
            linewidths=1,
            marker='o',
            label=f'外海地震 (n={len(df_offshore)})',
            zorder=2
        )
    
    # 绘制岛内地震（后画，使其在上层）
    if len(df_inland) > 0:
        sizes_inland = df_inland['规模'].apply(magnitude_to_size)
        scatter_inland = ax.scatter(
            df_inland['经度'], 
            df_inland['纬度'],
            s=sizes_inland,
            c=inland_color,
            alpha=0.6,
            edgecolors='darkred',
            linewidths=1,
            marker='o',
            label=f'岛内地震 (n={len(df_inland)})',
            zorder=3
        )
    
    # 添加规模参考圆圈
    legend_mags = [5.0, 5.5, 6.0, 6.5]
    legend_elements = []
    
    # 添加主要图例（岛内/外海）
    legend_elements.append(mpatches.Patch(color=inland_color, label=f'岛内地震 (n={len(df_inland)})'))
    legend_elements.append(mpatches.Patch(color=offshore_color, label=f'外海地震 (n={len(df_offshore)})'))
    
    # 添加规模参考
    for mag in legend_mags:
        legend_elements.append(
            plt.scatter([], [], s=magnitude_to_size(mag), 
                       c='gray', alpha=0.5, edgecolors='black',
                       label=f'M = {mag}')
        )
    
    # 设置图例
    legend1 = ax.legend(handles=legend_elements[:2], 
                       loc='upper left', 
                       fontsize=11,
                       title='地震类型',
                       title_fontsize=12,
                       framealpha=0.9)
    
    legend2 = ax.legend(handles=legend_elements[2:], 
                       loc='lower left', 
                       fontsize=10,
                       title='规模参考',
                       title_fontsize=11,
                       framealpha=0.9)
    
    ax.add_artist(legend1)
    
    # 设置坐标轴
    ax.set_xlabel('经度 (Longitude)', fontsize=12, fontweight='bold')
    ax.set_ylabel('纬度 (Latitude)', fontsize=12, fontweight='bold')
    ax.set_title('2014-2024年地震分布图\n(规模 > 5.0, 深度 < 40 km)\n' + 
                 'Earthquake Distribution Map (M > 5.0, Depth < 40 km)',
                 fontsize=14, fontweight='bold', pad=20)
    
    # 设置合适的坐标范围
    ax.set_xlim(119.5, 124.5)
    ax.set_ylim(21.5, 26.0)
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.3, zorder=0)
    
    # 设置长宽比
    ax.set_aspect('equal', adjustable='box')
    
    # 添加统计信息文本框
    stats_text = (
        f'总计: {len(df)} 笔地震\n'
        f'岛内: {len(df_inland)} 笔 ({len(df_inland)/len(df)*100:.1f}%)\n'
        f'外海: {len(df_offshore)} 笔 ({len(df_offshore)/len(df)*100:.1f}%)\n'
        f'规模范围: {df["规模"].min():.1f} - {df["规模"].max():.1f}'
    )
    
    ax.text(0.98, 0.98, stats_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            zorder=10)
    
    # 保存图形
    plt.tight_layout()
    output_file = 'outputs/earthquake_distribution_map_2014_2024.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n图形已保存至: {output_file}")
    
    # 显示图形
    plt.show()
    
    print("\n完成!")


if __name__ == "__main__":
    plot_earthquakes()
