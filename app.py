from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
DATA_FILE = 'food.json'

def load_food():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_food(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        expire_date = None

        if request.form.get('expire_date'):  # 直接輸入到期日
            expire_date = datetime.strptime(request.form['expire_date'], "%Y-%m-%d")
        elif request.form.get('days'):
            days = int(request.form['days'])
            expire_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=days)

        food = load_food()
        food.append({
            "id": datetime.now().timestamp(),  # 加上唯一ID
            "name": name,
            "date": date,
            "expire_date": expire_date.strftime("%Y-%m-%d")
        })
        save_food(food)
        return redirect('/')

    food_list = []
    for item in load_food():
        expire_date = datetime.strptime(item["expire_date"], "%Y-%m-%d")
        now = datetime.now()
        diff = (expire_date - now).days
        item['status'] = f"剩下 {diff} 天" if diff >= 0 else f"❗已過期 {-diff} 天"
        item['color'] = "red" if diff < 0 else "black"
        food_list.append(item)

    return render_template('index.html', foods=food_list)

@app.route('/delete/<float:item_id>')
def delete(item_id):
    food = load_food()
    food = [f for f in food if f["id"] != item_id]
    save_food(food)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
