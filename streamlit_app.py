import streamlit as st

st.title("Ví dụ Popup với Modal")

if st.button("Hiện popup"):
    with st.modal("Thông báo"):
        st.write("Đây là nội dung popup.")
        if st.button("Đóng"):
            st.rerun()
