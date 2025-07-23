import streamlit as st
from datetime import datetime, timedelta
import json
import os

DATA_FILE = 'food.json'

# === 資料處理函式 ===
def load_food():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_food(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# === 頁面基本設定 ===
st.set_page_config(page_title="食物保存追蹤", layout="centered")
st.title("🥫 食物保存追蹤器")

# === 新增食物表單 ===
with st.form("add_food_form"):
    name = st.text_input("食物名稱")
    purchase_date = st.date_input("購買日期", value=datetime.today())

    input_method = st.radio("選擇輸入方式", ["保存天數", "輸入到期日"])

    expire_date = None

    if input_method == "保存天數":
        days = st.number_input("保存天數", min_value=1, step=1, value=7)
        expire_date = purchase_date + timedelta(days=days)
    elif input_method == "輸入到期日":
        expire_date = st.date_input("到期日", min_value=purchase_date)

    submitted = st.form_submit_button("新增")

    if submitted:
        if not name:
            st.warning("⚠️ 請輸入食物名稱")
        elif not expire_date:
            st.warning("⚠️ 請確認保存天數或到期日已正確填寫")
        else:
            food = load_food()
            food.append({
                "id": datetime.now().timestamp(),
                "name": name,
                "date": purchase_date.strftime("%Y-%m-%d"),
                "expire_date": expire_date.strftime("%Y-%m-%d")
            })
            save_food(food)
            st.success(f"✅ 新增 {name} 成功！")
            st.rerun()

# === 顯示食物清單 ===
st.subheader("📦 食物清單")
food_list = load_food()

if not food_list:
    st.info("目前還沒有食物喔～快來新增吧！")
else:
    for item in food_list:
        expire = datetime.strptime(item["expire_date"], "%Y-%m-%d").date()
        today = datetime.now().date()
        diff = (expire - today).days

        color = "red" if diff < 0 else "black"
        status = f"❗已過期 {-diff} 天" if diff < 0 else f"剩下 {diff} 天"

        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"<span style='color:{color}'><b>{item['name']}</b></span>", unsafe_allow_html=True)
            st.caption(f"購買日：{item['date']}｜到期日：{item['expire_date']}")
        with col2:
            st.markdown(f"<span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
        with col3:
            if st.button("🗑️ 刪除", key=item["id"]):
                food_list = [f for f in food_list if f["id"] != item["id"]]
                save_food(food_list)
                st.rerun()
