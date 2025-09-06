import streamlit as st

popup_html = """
<div id="popup" style="
    position: fixed; top:0; left:0; width:100%; height:100%;
    background-color: rgba(0,0,0,0.6); display:flex; 
    align-items:center; justify-content:center; z-index:9999;">
  <div style="background:white; padding:30px; border-radius:12px; max-width:400px; text-align:center;">
    <h3 style="color:red;">⚠️ Thông báo</h3>
    <p>Trang web đang trong quá trình hoàn thiện.<br>Dữ liệu hiện tại chỉ là thử nghiệm.</p>
    <button onclick="document.getElementById('popup').style.display='none'" 
      style="margin-top:20px; padding:10px 20px; background:#f00; color:white; border:none; border-radius:8px; cursor:pointer;">
      Đóng
    </button>
  </div>
</div>
"""

st.components.v1.html(popup_html, height=300)
