# GitHub Pages 設定指南

## 🌐 啟用 GitHub Pages

### 方法 1: 從 docs/ 目錄發布（推薦）

1. 前往你的 GitHub repository：  
   https://github.com/oceanicdayi/EEW_performance

2. 點擊 **Settings**（設定）

3. 在左側選單找到 **Pages**

4. 在 **Source** 下：
   - Branch: 選擇 `main`
   - Folder: 選擇 `/docs`
   - 點擊 **Save**

5. 等待約 1-2 分鐘，頁面會顯示：
   ```
   Your site is published at https://oceanicdayi.github.io/EEW_performance/
   ```

### 方法 2: 從根目錄發布

如果想使用 README.md 作為首頁：

1. 前往 **Settings** → **Pages**
2. Branch: `main` → Folder: `/ (root)`
3. 點擊 **Save**

> ⚠️ **注意**：根目錄模式會將 README.md 轉為網頁首頁

---

## 📱 網站連結

設定完成後，你的網站將在以下網址：

- **主要網站**：https://oceanicdayi.github.io/EEW_performance/
- **互動式首頁**：自動顯示 docs/index.html
- **README 文件**：https://oceanicdayi.github.io/EEW_performance/README.html

---

## 🎨 已包含的功能

### 網站首頁 (docs/index.html)
- ✅ 響應式設計 (手機、平板、桌面自適應)
- ✅ 即時統計數據展示
- ✅ 島內 vs 外海性能比較表
- ✅ 視覺化圖片展示
- ✅ 快速安裝指南
- ✅ 直接連結到 GitHub repository

### README.md
- ✅ 完整專案說明
- ✅ 安裝與使用教學
- ✅ 統計結果表格
- ✅ 專案結構說明
- ✅ 進階使用範例

---

## 🔄 更新網站內容

### 修改首頁
```bash
# 編輯首頁內容
code docs/index.html

# 提交變更
git add docs/index.html
git commit -m "docs: Update landing page"
git push origin main
```

### 修改 README
```bash
# 編輯 README
code README.md

# 提交變更
git add README.md
git commit -m "docs: Update README"
git push origin main
```

> 💡 **提示**：每次推送後，GitHub Pages 會自動重新建置（約 1-2 分鐘）

---

## 🚀 部署 Streamlit 互動網頁

GitHub Pages 只能托管靜態 HTML，無法直接運行 Python Streamlit。  
建議使用以下服務部署互動式應用：

### Streamlit Community Cloud（免費）

1. 前往 https://share.streamlit.io/
2. 使用 GitHub 帳號登入
3. 點擊 "New app"
4. 選擇：
   - Repository: `oceanicdayi/EEW_performance`
   - Branch: `main`
   - Main file path: `app.py`
5. 點擊 "Deploy"

部署成功後，你會得到類似連結：
```
https://oceanicdayi-eew-performance.streamlit.app/
```

### 其他選項

- **Hugging Face Spaces**（免費）  
  https://huggingface.co/spaces

- **Railway**（付費，有免費額度）  
  https://railway.app/

---

## 📊 網站分析（選用）

### 添加 Google Analytics

1. 取得 Google Analytics tracking ID (例如: `G-XXXXXXXXXX`)

2. 編輯 `_config.yml`：
   ```yaml
   google_analytics: G-XXXXXXXXXX
   ```

3. 提交變更：
   ```bash
   git add _config.yml
   git commit -m "feat: Add Google Analytics"
   git push origin main
   ```

---

## 🎯 驗證設定

設定完成後，檢查以下項目：

- [ ] GitHub Pages 顯示為 "published"
- [ ] 網站可以在瀏覽器正常開啟
- [ ] 首頁樣式正確顯示
- [ ] 圖片能正常載入
- [ ] 所有連結可以點擊

---

## ❓ 常見問題

### 1. 網站顯示 404 錯誤
- 確認 GitHub Pages 已啟用
- 檢查分支和資料夾設定
- 等待約 5-10 分鐘讓 GitHub 完成建置

### 2. 圖片無法顯示
- 確認 outputs/ 目錄的圖片已上傳
- 檢查 index.html 中的圖片路徑
- 相對路徑範例：`../outputs/earthquake_distribution_gmt_2014_2025.png`

### 3. 樣式跑版
- 檢查 index.html 的 CSS 語法
- 使用瀏覽器開發者工具 (F12) 查看錯誤

### 4. README.md 在 GitHub Pages 無法顯示
- GitHub Pages 會將 markdown 轉為 HTML
- 預設主題由 `_config.yml` 控制
- 如需自訂樣式，可使用 Jekyll 主題

---

## 📚 進階設定

### 自訂網域

1. 在 repository 根目錄建立 `CNAME` 文件
2. 內容填入你的網域：`www.example.com`
3. 在網域服務商設定 DNS CNAME 記錄指向 `oceanicdayi.github.io`

### 使用 Jekyll 主題

編輯 `_config.yml`：
```yaml
theme: jekyll-theme-cayman
# 或其他主題：minima, slate, minimal, etc.
```

更多主題：https://pages.github.com/themes/

---

## ✅ 完成清單

設定完成後，你將擁有：

- [x] 專業的 GitHub README.md
- [x] 響應式互動首頁 (docs/index.html)
- [x] GitHub Pages 網站發布
- [ ] Streamlit Cloud 互動應用（選用）
- [ ] Google Analytics 追蹤（選用）
- [ ] 自訂網域（選用）

---

## 🎉 成功範例

設定完成後，在 README.md 中更新連結：

```markdown
> 🌐 **互動式網頁**: [GitHub Pages展示](https://oceanicdayi.github.io/EEW_performance/)
> 📊 **即時分析工具**: [Streamlit App](https://your-app.streamlit.app/)
```

---

需要協助？歡迎在 [Issues](https://github.com/oceanicdayi/EEW_performance/issues) 提問！
