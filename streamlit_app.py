import streamlit as st

popup_html = """
<style>
#popup {
  position: fixed; top: 0; left: 0;
  width: 100vw; height: 100vh;
  background-color: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999;
}
.popup-box {
  background: white; padding: 30px; border-radius: 12px;
  max-width: 400px; text-align: center;
}
.close-btn {
  margin-top: 20px; padding: 10px 20px;
  background: #f00; color: white; border: none;
  border-radius: 8px; cursor: pointer;
}
</style>

<div id="popup">
  <div class="popup-box">
    <h3 style="color:red;">⚠️ Thông báo</h3>
    <p>Trang web đang trong quá trình hoàn thiện.<br>Dữ liệu hiện tại chỉ là thử nghiệm.</p>
    <button class="close-btn" onclick="document.getElementById('popup').style.display='none'">
      Đóng
    </button>
  </div>
</div>
"""

# Chiều cao để lớn hơn viewport → overlay che toàn bộ
st.components.v1.html(popup_html, height=700, width=None)
