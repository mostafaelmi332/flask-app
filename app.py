from flask import Flask, render_template_string
import requests
import threading
import time

app = Flask(__name__)

# آدرس جدید API
URL = "https://cdn.tsetmc.com/api/Instrument/GetInstrumentOptionMarketWatch/0"

# کش داده‌ها
data_cache = []

# تابع برای دریافت داده‌ها
def fetch_data():
    global data_cache
    while True:
        try:
            response = requests.get(URL)
            print("وضعیت پاسخ:", response.status_code)
            if response.status_code == 200:
                data = response.json()
                if "instrumentOptMarketWatch" in data:   # ✅ کلید درست
                    data_cache = data["instrumentOptMarketWatch"]
                else:
                    data_cache = []
        except Exception as e:
            print("خطا:", e)
        time.sleep(30)   # هر ۳۰ ثانیه یک بار آپدیت

# اجرا در رشته جداگانه
threading.Thread(target=fetch_data, daemon=True).start()

# قالب HTML
TEMPLATE = """
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>نمایش داده‌های آپشن</title>
    <style>
        body { font-family: Tahoma, sans-serif; direction: rtl; background: #f9f9f9; padding: 20px; }
        h2 { text-align: center; color: #333; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; font-size: 14px; }
        th { background: #4CAF50; color: white; }
        tr:nth-child(even) { background: #f2f2f2; }
    </style>
</head>
<body>
    <h2>داده‌های بازار آپشن</h2>
    <table>
        <thead>
            <tr>
                <th>نماد پایه</th>
                <th>قیمت اعمال</th>
                <th>تاریخ سررسید</th>
                <th>آخرین قیمت (Put)</th>
                <th>آخرین قیمت (Call)</th>
                <th>تعداد معاملات Put</th>
                <th>تعداد معاملات Call</th>
            </tr>
        </thead>
        <tbody>
            {% for item in data %}
            <tr>
                <td>{{ item.get('lval30_UA','') }}</td>
                <td>{{ item.get('strikePrice','') }}</td>
                <td>{{ item.get('endDate','') }}</td>
                <td>{{ item.get('pClosing_P','') }}</td>
                <td>{{ item.get('pClosing_C','') }}</td>
                <td>{{ item.get('zTotTran_P','') }}</td>
                <td>{{ item.get('zTotTran_C','') }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(TEMPLATE, data=data_cache)

if __name__ == "__main__":
    app.run(debug=True)