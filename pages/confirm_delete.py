import streamlit as st




st.write(st.session_state['deletedtime']," has been removed")
if st.button("return to dashboard"):
    st.switch_page("pages/managerdashboard.py")
