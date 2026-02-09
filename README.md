# 🌍 地震預警系統性能分析 (EEWS Performance Analysis)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyGMT](https://img.shields.io/badge/PyGMT-Visualization-orange.svg)](https://www.pygmt.org/)

台灣地震預警系統（Earthquake Early Warning System, EEWS）2014-2025年性能統計分析工具。提供完整的地震預警數據分析、視覺化和互動式網頁展示。

> 🌐 **互動式網頁**: [GitHub Pages展示](https://oceanicdayi.github.io/EEW_performance/)

## ✨ 主要功能

### 📊 統計分析
- ✅ **發布率分析**：計算預警發布成功率（97.8%+）
- ✅ **處理時效統計**：平均處理時間、標準差分析
- ✅ **震央定位誤差**：計算預警震央與實際震央距離
- ✅ **規模誤差分析**：預警規模與目錄規模對比（含RMS）
- ✅ **島內/外海分類**：基於台灣邊界自動分類地震位置
- ✅ **空間範圍篩選**：經度119-123°E，緯度21-26°N

### 🗺️ 地圖視覺化 (PyGMT)
- 🎨 **處理時效著色地圖**：用顏色梯度展示處理速度（藍色=快，紅色=慢）
- 📍 **震央分布圖**：顯示所有地震位置與台灣邊界
- ⭕ **規模圓圈**：圓圈大小代表地震規模
- 📊 **統計圖表**：誤差分布、時效統計等

### 🌐 互動式網頁
- 💻 **Streamlit網頁介面**：即時調整篩選條件
- 🔧 **動態參數調整**：規模、深度、時間範圍可調
- 📈 **即時統計更新**：條件改變時即時重新計算
- 📥 **結果下載**：CSV格式匯出分析結果

## 📦 安裝

### 環境需求
```bash
Python 3.8+
```

### 快速安裝
```bash
# 複製專案
git clone https://github.com/oceanicdayi/EEW_performance.git
cd EEW_performance

# 建立虛擬環境（建議）
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安裝套件
pip install -r requirements.txt

# 安裝網頁套件（選用）
pip install -r requirements_web.txt
```

### 主要套件
- `numpy` - 數值計算
- `pandas` - 數據處理
- `matplotlib` - 基礎繪圖
- `pygmt` - 專業地球科學視覺化
- `streamlit` - 互動式網頁（選用）

## 🚀 使用方式

### 1. 基本統計分析

```bash
# 執行2014-2025年統計分析
python analyze_2014_2024_summary.py
```

輸出結果：
- `outputs/eews_summary_2014_2025.csv` - 統計摘要
- `outputs/earthquake_list_2014_2025.csv` - 詳細地震列表

### 2. 繪製地圖

```bash
# 繪製處理時效著色地圖
python plot_earthquakes_pygmt.py
```

輸出結果：
- `outputs/earthquake_distribution_gmt_2014_2025.png` - 高解析度地圖

### 3. 啟動互動式網頁

```bash
# 啟動Streamlit網頁
streamlit run app.py
```

然後在瀏覽器開啟 `http://localhost:8501`

## 📊 統計結果 (2014-2025)

### 整體表現
| 指標 | 數值 |
|------|------|
| **總地震數** | 272筆 |
| **發布預警** | 267筆 |
| **發布率** | 98.2% |
| **平均處理時效** | 16.27秒 |
| **平均震央誤差** | 10.09公里 |
| **規模誤差RMS** | 0.361 |

### 島內 vs 外海
| 類別 | 發布次數 | 平均時效 | 震央誤差 | 規模誤差RMS |
|------|---------|---------|---------|-----------|
| **島內** | 99 | 12.79秒 | 4.62公里 | 0.342 |
| **外海** | 168 | 18.32秒 | 13.32公里 | 0.372 |

**結論**：島內地震預警表現優於外海，處理速度快30.5%，定位準確度高74.4%。

## 📁 專案結構

```
EEW_performance/
├── 📄 analyze_2014_2024_summary.py  # 主分析腳本
├── 📄 eews_analyzer.py              # 分析核心引擎
├── 📄 plot_earthquakes_pygmt.py     # PyGMT繪圖
├── 📄 app.py                        # Streamlit網頁
├── 📊 EEW_ALL-2014-2025.txt         # 地震資料
├── 🗺️ taiwan.txt                    # 台灣邊界座標
├── 📦 requirements.txt              # Python套件需求
└── 📂 outputs/                      # 輸出結果目錄
    ├── eews_summary_2014_2025.csv
    ├── earthquake_list_2014_2025.csv
    └── earthquake_distribution_gmt_2014_2025.png
```

## 📖 資料格式

輸入檔案格式（tab/space分隔）：

```
Type	ID	Time	Lon	Lat	Mag	Depth	EEW_Lon	EEW_Lat	EEW_Mag	EEW_Dep	Processing_Time
xY	1	201401141838012	121.081	22.893	5.05	8.29	121.07	22.88	5.3	10	16
xN	2	201404100238005	123.068	23.737	5.35	38.26
```

### Type代碼說明：
- `xY` / `oY` - 成功發布預警（x=島內, o=外海）
- `xN` / `oN` - 未發布預警
- `xL` / `oL` - 延遲發布

## 🔧 進階使用

### 自訂篩選條件

編輯 `analyze_2014_2024_summary.py`：

```python
# 修改篩選條件
min_mag = 5.0      # 最小規模
max_depth = 40.0   # 最大深度(km)
min_lon = 119.0    # 最小經度
max_lon = 123.0    # 最大經度
min_lat = 21.0     # 最小緯度
max_lat = 26.0     # 最大緯度
```

### 客製化地圖樣式

編輯 `plot_earthquakes_pygmt.py`：

```python
# 修改色彩配置
pygmt.makecpt(cmap="polar", series=[min_time, max_time])

# 調整圓圈大小
def mag_to_size(mag):
    return 0.05 * (mag ** 2) * 0.3  # 調整係數
```

## 🤝 貢獻指南

歡迎提交Issue和Pull Request！

1. Fork專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟Pull Request

## 📝 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

**Oceanic Dayi**
- GitHub: [@oceanicdayi](https://github.com/oceanicdayi)

## 🙏 致謝

- 台灣中央氣象署地震預警資料
- PyGMT開發團隊
- Streamlit社群

## 📮 聯絡方式

有任何問題或建議，歡迎：
- 開啟 [Issue](https://github.com/oceanicdayi/EEW_performance/issues)
- 提交 Pull Request

---

⭐ 如果這個專案對您有幫助，請給個星星！