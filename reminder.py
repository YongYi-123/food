import os
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# 從環境變數讀取（這些在 GitHub secrets 中設定）
EMAIL = os.environ["EMAIL"]
TO = os.environ["TO"]
APP_PASSWORD = os.environ["APP_PASSWORD"]

def load_food():
    with open("food.json", "r") as f:
        return json.load(f)

def get_expiring_items(food_list):
    today = datetime.now().date()
    result = []
    for item in food_list:
        expire_date = datetime.strptime(item["expire_date"], "%Y-%m-%d").date()
        days_left = (expire_date - today).days
        if 0 <= days_left <= 2:
            result.append((item["name"], days_left))
    return result

def send_email(expiring_items):
    if not expiring_items:
        return

    content = "以下食物即將到期：\n\n"
    for name, days in expiring_items:
        if days == 0:
            content += f"- {name}：今天到期\n"
        else:
            content += f"- {name}：剩下 {days} 天\n"

    msg = MIMEText(content)
    msg["Subject"] = "📦 食物保存提醒"
    msg["From"] = EMAIL
    msg["To"] = TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    food_list = load_food()
    expiring = get_expiring_items(food_list)
    send_email(expiring)
