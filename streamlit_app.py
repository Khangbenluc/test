import streamlit as st

st.title("💰 Giá vàng & Biểu đồ Kitco")

st.header("📊 Giá vàng hiện tại")
st.components.v1.html("""
<iframe src="https://www.kitco.com/charts/gold" 
    width="100%" height="500" style="border:none;"></iframe>
""", height=520)

st.header("📈 Biểu đồ giá vàng 24h")
st.components.v1.html("""
<iframe src="https://www.kitco.com/charts/gold" 
    width="100%" height="500" style="border:none;"></iframe>
""", height=520)
