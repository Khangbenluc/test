import streamlit as st
import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime

st.title("💰 Giá vàng Kitco")

# Thời gian VN
vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
now_vn = datetime.now(vn_tz).strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"⏰ Thời gian (Việt Nam): {now_vn}")

# --- PHẦN GIÁ VÀNG ---
st.header("📊 Giá vàng mới nhất")
def fetch_kitco_gold():
    url = "https://www.kitco.com/price/precious-metals/"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.select("ul.chart-data li")
        prices = []
        for row in rows:
            label_el = row.select_one("div.price-label")
            value_el = row.select_one("div.price-value")
            if label_el and value_el:
                label = label_el.get_text(strip=True)
                value = value_el.get_text(strip=True)
                if "Gold" in label:
                    prices.append({"label": label, "value": value})
        return prices
    except:
        return []

gold_prices = fetch_kitco_gold()
if not gold_prices:
    st.error("⚠️ Không lấy được giá vàng")
else:
    for p in gold_prices:
        st.markdown(f"**{p['label']}**: {p['value']}")

# --- PHẦN BIỂU ĐỒ ---
st.header("📈 Biểu đồ giá vàng 24h")
st.components.v1.html(
    """
    <iframe src="https://www.kitco.com/charts/livegold.html"
        width="100%" height="500" style="border:none;"></iframe>
    """,
    height=520
)
