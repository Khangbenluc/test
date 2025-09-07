"""
Streamlit App: Xem giá vàng Kitco + Biểu đồ
-------------------------------------------
- Lấy giá vàng mới nhất từ trang Kitco (web scraping).
- Hiển thị biểu đồ giá vàng Kitco bằng iframe.
- Không dùng API key.
"""

# ------------------------
# IMPORTS
# ------------------------
import streamlit as st
import requests
from bs4 import BeautifulSoup
import logging

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
    Trả về dict {'label':..., 'value':...}
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
                if "Gold" in label:
                    prices.append({"label": label, "value": value})
        return prices
    except Exception as e:
        logger.error(f"Lỗi khi lấy giá vàng: {e}")
        return []

# ------------------------
# UI LAYOUT
# ------------------------
st.title("💰 Giá vàng Kitco & Biểu đồ")

st.sidebar.title("Tùy chọn")
if st.sidebar.button("Làm mới dữ liệu"):
    st.experimental_rerun()

# --- Giá vàng ---
st.header("Giá vàng mới nhất")
gold_prices = fetch_kitco_gold()
if not gold_prices:
    st.error("Không lấy được giá vàng từ Kitco.")
else:
    for p in gold_prices:
        st.markdown(
            f"<div style='font-size:18px; font-weight:600;'>{p['label']}: "
            f"<span style='color:#b91c1c'>{p['value']}</span></div>",
            unsafe_allow_html=True,
        )

# --- Biểu đồ ---
st.header("Biểu đồ giá vàng 24h (Kitco)")
try:
    st.components.v1.html(
        """
        <iframe src="https://www.kitco.com/charts/gold"
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
