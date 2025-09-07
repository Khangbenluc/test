import streamlit as st

st.title("💰 Giá vàng & Biểu đồ Kitco")

st.header("📊 Giá vàng hiện tại (Top Kitco)")
st.components.v1.html("""
<iframe src="https://www.kitco.com/charts/livegold.html" 
    width="100%" height="500" style="border:none; overflow:hidden;"></iframe>
""", height=500)

st.header("📈 Biểu đồ giá vàng (bắt đầu từ biểu đồ Kitco)")
st.components.v1.html("""
<iframe src="https://www.kitco.com/charts/livegold.html" 
    width="100%" height="500" style="border:none; overflow:hidden;"></iframe>
""", height=500)
