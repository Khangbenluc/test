import streamlit as st

if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

if st.button("Hiện thông báo"):
    st.session_state.show_popup = True

if st.session_state.show_popup:
    with st.expander("🔔 Thông báo (bấm để đóng)"):
        st.write("Đây là thông báo giả lập popup.")
        if st.button("Đóng"):
            st.session_state.show_popup = False
