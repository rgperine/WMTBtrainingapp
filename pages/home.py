import streamlit as st
import sqlite3
from datetime import datetime
conn = sqlite3.connect('radio.db')
cursor = conn.cursor()


style = """
    <style>
        /* Hide the sidebar container */
        div[data-testid="stSidebarContent"] {
            display: none;
        }

    </style>
"""
st.session_state.manager = 0

st.markdown(style, unsafe_allow_html=True)
st.title("Welcome to the WMTB Training Portal")
st.divider()

with st.container():
    st.divider()
    st.subheader("Your current booked times")
    result = cursor.execute('SELECT date, time, manager FROM bookedtimes WHERE trainee = ?', (st.session_state.id,)).fetchall()

    for i in result:
            managername = cursor.execute('select first_name from djs where dj_id = ?',(i[2],)).fetchall()[0][0]

            dtstr = f"{i[0]} {i[1]}"

            datetime_obj = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')
            formatted = datetime_obj.strftime('%B %d at %I:%M %p')
            label = formatted+ " with "+ managername
            if st.button(label):
                pass
    st.divider()
    selection = st.pills("dj actions",options=["book a session","view schedule","log out"],label_visibility="hidden")

    if selection == "book a session":
        st.switch_page("pages/booksession.py")
    if selection == "log out":
        st.switch_page("sl1.py")
    if selection == "view schedule":
        st.switch_page("pages/schedule.py")
