import streamlit as st

# Khởi tạo trạng thái popup
if "show_notice" not in st.session_state:
    st.session_state.show_notice = True

# Nếu popup đang bật thì hiển thị cảnh báo nổi bật
if st.session_state.show_notice:
    st.markdown(
        """
        <div style="
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.6); 
            display: flex; align-items: center; justify-content: center;
            z-index: 9999;">
            <div style="
                background: white; padding: 30px; border-radius: 12px; 
                max-width: 400px; text-align: center;">
                <h3 style="color: red;">⚠️ Thông báo</h3>
                <p>Trang web đang trong quá trình hoàn thiện.<br>
                Dữ liệu hiện tại chỉ là thử nghiệm.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Đóng"):
        st.session_state.show_notice = False
