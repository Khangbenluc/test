"""
Streamlit App: Xem giá vàng Kitco + Biểu đồ
-------------------------------------------
- Lấy giá vàng mới nhất từ trang Kitco (web scraping).
- Hiển thị biểu đồ giá vàng Kitco bằng iframe.
- Hiển thị giờ Việt Nam.
"""

# ------------------------
# IMPORTS
# ------------------------
import streamlit as st
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import pytz

# ------------------------
# LOGGING
# ------------------------
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("gold_app")
logger.setLevel(logging.INFO)

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(
    page_title="Giá vàng Kitco",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------
# SCRAPING FUNCTION
# ------------------------
def fetch_kitco_gold():
    """
    Lấy giá vàng từ trang Kitco Precious Metals.
    Trả về list dict [{'label':..., 'value':...}]
    """
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
                if "Gold" in label:  # chỉ lấy vàng
                    prices.append({"label": label, "value": value})
        return prices
    except Exception as e:
        logger.error(f"Lỗi khi lấy giá vàng: {e}")
        return []

# ------------------------
# UI LAYOUT
# ------------------------
st.title("💰 Giá vàng Kitco & Biểu đồ")

# Hiển thị thời gian VN
vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
now_vn = datetime.now(vn_tz).strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"⏰ Thời gian (Việt Nam): {now_vn}")

st.sidebar.title("Tùy chọn")
if st.sidebar.button("🔄 Làm mới dữ liệu"):
    st.rerun()

# --- Giá vàng ---
st.header("📊 Giá vàng mới nhất")
gold_prices = fetch_kitco_gold()
if not gold_prices:
    st.error("⚠️ Không lấy được giá vàng từ Kitco. Có thể do thay đổi giao diện website.")
else:
    for p in gold_prices:
        st.markdown(
            f"<div style='font-size:20px; font-weight:600; margin-bottom:8px;'>{p['label']}: "
            f"<span style='color:#b91c1c'>{p['value']}</span></div>",
            unsafe_allow_html=True,
        )

# --- Biểu đồ ---
st.header("📈 Biểu đồ giá vàng 24h (Kitco)")
try:
    st.components.v1.html(
        """
        <iframe src="https://www.kitco.com/charts/livegold.html"
            width="100%" height="500" style="border:none;">
        </iframe>
        """,
        height=520,
    )
except Exception as e:
    st.error(f"Không nhúng được biểu đồ: {e}")

st.markdown(
    "<div style='font-size:12px; color:#6b7280'>Nguồn dữ liệu: Kitco.com</div>",
    unsafe_allow_html=True,
)
