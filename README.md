DataScienceCourse

# Global Population & Geopolitical Risk Dashboard
作者：陳亭妤

## GitHub Pages
https://tinyuchen.github.io/DataScienceCourse_week01/

## GitHub Repo
https://github.com/tinyuchen/DataScienceCourse_week01

---

## 專案簡介
本專案是一個可公開瀏覽的單頁儀表板，內容包含：
1) 世界人口預測（2024、2030、2050、2100）
2) 伊朗地緣政治風險分析（至少 4 個風險因子，並區分「事實資料」與「推論」）
3) 方法論（我如何使用 AI、我如何驗證資料）

---

## 專案結構
- index.html / styles.css / script.js
- data/raw.txt（原始人口資料）
- data/cleaned.json（由 Python 產生）
- scripts/clean.py（清理＋計算：平均值／成長率／CAGR，並輸出 JSON）
- assets/population_sparkline.svg（由 Python 產生）
- report.pdf（1 頁 PDF 分析報告）

---

## 資料來源
### 人口資料（必須引用 UN WPP 或 Our World in Data）
- UN World Population Prospects (WPP)：
  https://population.un.org/wpp/
- Our World in Data（UN projections）：
  https://ourworldindata.org/grapher/population-with-un-projections

### 伊朗風險資料
- IAEA（核查/監督相關文件）：
  https://www.iaea.org/
- EIA（Hormuz chokepoint）：
  https://www.eia.gov/todayinenergy/detail.php?id=65504
- OFAC（Iran sanctions）：
  https://ofac.treasury.gov/sanctions-programs-and-country-information/iran-sanctions
- Brookings（proxy forces 脈絡）：
  https://www.brookings.edu/articles/the-path-forward-on-iran-and-its-proxy-forces/

---

## AI 使用聲明
我使用 AI 的範圍：
- 產出網站 HTML/CSS/JS 的初稿結構與文案草稿
- 協助整理「可能的」伊朗風險因子清單（僅作為初步 brainstorming）
- 協助摘要來源內容（摘要僅作理解用途）

我沒有把 AI 產生的內容當成事實證據：
- 任何「事實資料（Facts）」都必須可追溯到來源連結
- 沒有來源支撐的內容一律標為「推論（Inference）」或刪除

---

## Prompt 範例
（下面是我實際用過或等價的 prompt 範例）

1) 網站：
- 「請生成一個單頁儀表板（RWD），包含 Landing、人口區塊、Iran Risk Matrix、方法論，並提供簡潔的 HTML/CSS/JS。」

2) 人口資料處理：
- 「請用 Python 讀取 data/raw.txt，清理出 2024/2030/2050/2100 人口數（billion），計算平均值、成長率、CAGR，輸出成 data/cleaned.json，並產生一張簡單的折線圖 SVG。」

3) 伊朗風險：
- 「請列出至少 4 個伊朗地緣政治風險因子，每個因子用 Facts vs Inference 格式撰寫，並建議可用來驗證的主要資料來源（例如 IAEA/EIA/OFAC）。」

---

## 驗證流程
### 人口數據驗證
1) 以 UN WPP 或 Our World in Data（UN projections）作為優先依據。
2) 若不同 AI 給出不同人口數字：
   - 我不以 AI 回答為準
   - 回到 UN WPP / OWID 來源確認
   - 在本 README 記錄「AI 給的數字」與「我採用的數字」及原因（以可追溯來源為準）
3) 本專案最終採用的數字以 data/cleaned.json 為準，且由 scripts/clean.py 可重現產生。

### 伊朗風險驗證（Facts vs Inference）
1) Facts：必須附來源連結（IAEA/EIA/OFAC 等）。
2) Inference：必須明確標示為推論，不以「事實口吻」呈現。
3) 偏誤控管：
   - 優先引用一手/準一手資料
   - 對於容易引發立場偏誤的敘述，降低語氣、改成條件式推論
   - 不引用無法追溯來源的結論句

---

## 可重現性說明
- data/cleaned.json 與 assets/population_sparkline.svg 為程式產物
- 由 scripts/clean.py（GitHub Actions）自動生成，可追溯與重跑
