import requests, time, json

# 自訂發送 Line Notify 通知形式
def lineNotify(token, msg):
    headers = {
        "Authorization": "Bearer " + token,  
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {"message": msg}
    url = "https://notify-api.line.me/api/notify"
    notify = requests.post(url, headers = headers, data = payload)
    return notify.status_code

# 自訂發送 Line Notify 通知內容
def sendLine(mode, real_humidity, counter_line, token):
    print("目前台北濕度：" + str(real_humidity) + "%")
    if mode == 1: # 濕度 >= 50
        message = "現在濕度為" + str(real_humidity) + "%" + ", 帶支雨傘出門吧！"
    else: # 濕度 < 50
        message = "現在濕度為" + str(real_humidity) + "%" + ", 可以放心出門！"

    code = lineNotify(token, message)
    if code == 200:
        counter_line += 1
        print("第" + str(counter_line) + "次發送訊息。")
    else:
        print("發送訊息失敗！")
    return counter_line

# connect openweathermap api
# json: https://api.openweathermap.org/data/2.5/weather?lat=25.105497&lon=121.597366&appid=d004968ab5800e8d6cfed0b96a46c59e
url = "https://api.openweathermap.org/data/2.5/weather?lat=25.105497&lon=121.597366&appid=d004968ab5800e8d6cfed0b96a46c59e"
weather_api = "d004968ab5800e8d6cfed0b96a46c59e"
payload = {
    "lat": 25.1055,
    "lon": 121.5974,
    "appid": weather_api,
    "units": "metric",
    "exclude": "current,minutely,daily",
    "lang": "zh_tw"
}
response = requests.get(url, data = payload)
# 檢查 API 請求是否成功。若收到的響應是錯誤的，則引發一 HTTP 錯誤以停止程式運行。
response.raise_for_status()

my_token = "coxRioVBGKBlBdGwdCqlg2QWfb1hipWxgjbn2lvD6hi"
counter_line = 0
counter_error = 0

print("程式開始執行！")
while True:
    try:
        weather_data = json.loads(response.text)
        real_humidity = weather_data["main"]["humidity"]
        if int(real_humidity) >= 50:
            counter_line = sendLine(1, real_humidity, counter_line, my_token)
        elif int(real_humidity) < 50:
            counter_line = sendLine(2, real_humidity, counter_line, my_token)
        # 發送3次訊息即結束
        if counter_line >= 3:
            print("程式結束！")
            break
        # 每5分鐘讀取一次資料並發送訊息
        for i in range(300):
            time.sleep(1)
    except:
        print("資料讀取錯誤！")
        counter_error += 1
        # 最多發送3次錯誤訊息
        if counter_error >= 3:
            print("程式結束！")
            break



