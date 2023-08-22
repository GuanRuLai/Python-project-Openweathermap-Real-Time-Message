import requests, time, json
import pandas as pd

# make a location reference before the code starts running
se1 = pd.Series({"新北市": 25.012, "台北市": 25.0478, "桃園市": 24.9896, "台中市": 24.1469, "台南市": 22.9908, "高雄市": 22.6163})
se2 = pd.Series({"新北市": 121.4657, "台北市": 121.5319, "桃園市": 121.3187, "台中市": 120.6839, "台南市": 120.2133, "高雄市": 120.3133})
# 以相同的 key 進行左右合併
df = pd.concat([se1, se2], axis = 1)
df.columns = ["lat", "lon"]
print("Location_referrence:")
print(df)

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

input_location_chinese_name = input("Please input location's chinese name: ")

# 自訂發送 Line Notify 通知內容
def sendLine(mode, real_humidity, counter_line, token):
    print(f"目前{input_location_chinese_name}濕度：" + str(real_humidity) + "%")
    if mode == 1: # 濕度 >= 70
        message = f"現在{input_location_chinese_name}濕度為" + str(real_humidity) + "%" + ", 一定要帶傘，不然等著變成落湯雞！"
    elif mode == 2: # 40 <= 濕度 < 70
        message = f"現在{input_location_chinese_name}濕度為" + str(real_humidity) + "%" + ", 帶把傘出門比較安心！"
    else: # 濕度 < 40        
        message = f"現在{input_location_chinese_name}濕度為" + str(real_humidity) + "%" + ", 可以安心出門！"
    code = lineNotify(token, message)
    if code == 200:
        counter_line += 1
        print("第" + str(counter_line) + "次發送訊息。")
    else:
        print("發送訊息失敗！")
    return counter_line

input_location_lat = input("Please input location lat: ")
input_location_lon = input("Please input location lon: ")

# connect openweathermap api
# json: https://api.openweathermap.org/data/2.5/weather?lat=25.105497&lon=121.597366&appid=d004968ab5800e8d6cfed0b96a46c59e
url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=d004968ab5800e8d6cfed0b96a46c59e".format(input_location_lat, input_location_lon)
weather_api = "d004968ab5800e8d6cfed0b96a46c59e"
payload = {
    "appid": weather_api,
    "units": "metric",
    "exclude": "current,minutely,daily",
    "lang": "zh_tw"
}
response = requests.get(url, data = payload)
# 檢查 API 請求是否成功。若收到的響應是錯誤的，則引發一 HTTP 錯誤以停止程式運行。
response.raise_for_status()

print("Ensure you make a key and also plus @linenotify to your line friend!!")
input_line_api = input("Please input your line notify api keys: ")
my_token = f"{input_line_api}"
counter_line = 0
counter_error = 0

while True:
    try:
        weather_data = json.loads(response.text)
        real_humidity = weather_data["main"]["humidity"]
        if int(real_humidity) >= 70:
            counter_line = sendLine(1, real_humidity, counter_line, my_token)
        elif 40 <= int(real_humidity) < 70:
            counter_line = sendLine(2, real_humidity, counter_line, my_token)
        else:
            counter_line = sendLine(3, real_humidity, counter_line, my_token)
        # 發送3次訊息即結束
        if counter_line >= 3:
            print("程式結束，歡迎再使用！")
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
