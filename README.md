## 專案介紹
本專案是一個透過 OpenWeatherMap API 獲取指定地點天氣濕度，並透過 LINE Notify 發送通知的 Python 腳本。使用者可指定地點，當濕度達到特定門檻時，自動推送通知。

## 主要功能
- 取得台灣六都的經緯度參考
- 自訂查詢任意地點的濕度資訊
- 依據濕度等級自動發送 LINE Notify 通知
- 程式自動運行，達到指定次數後停止

## 使用技術
- Python
- requests
- pandas
- OpenWeatherMap API
- LINE Notify API

## 安裝與使用
### 1. 安裝必要套件
請確保已安裝 Python，並使用 pip 安裝所需套件：
```bash
pip install requests pandas
```

### 2. 取得 API 金鑰
- **OpenWeatherMap API**: [申請 API Key](https://home.openweathermap.org/api_keys)
- **LINE Notify API**: [申請 Access Token](https://notify-bot.line.me/en/)

### 3. 執行腳本
```bash
python script.py
```

### 4. 輸入相關資訊
執行程式後，依序輸入：
1. 查詢地點名稱（如台北市）
2. 查詢地點的經緯度
3. LINE Notify API Key

## 濕度通知等級
| 濕度範圍 | 提示內容 |
|----------|---------|
| ≧ 70% | 一定要帶傘，不然等著變成落湯雞！ |
| 40% ~ 70% | 帶把傘出門比較安心！ |
| < 40% | 可以安心出門！ |

## 程式邏輯
1. 透過 OpenWeatherMap API 取得天氣數據
2. 判斷濕度範圍
3. 透過 LINE Notify 發送對應的訊息
4. 每 5 分鐘檢查一次，最多發送 3 次通知

## 注意事項
- 需確保 API Key 正確
- 執行時請確認 LINE Notify 已加為好友
- 需提供正確的經緯度以獲取準確資訊

## 授權
本專案採用 MIT 授權條款，歡迎自由使用與修改！
