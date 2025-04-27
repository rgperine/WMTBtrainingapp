import streamlit as st
import sqlite3
from dateutil import parser



style = """
    <style>
        /* Hide the sidebar container */
        div[data-testid="stSidebarContent"] {
            display: none;
        }

    </style>
"""

st.markdown(style, unsafe_allow_html=True)


conn = sqlite3.connect('radio.db')
cursor = conn.cursor()

st.subheader("Add an available time")
st.divider()


timeAvailable = True


with st.form("my_form"):

    d = st.date_input("Date")
    t = st.time_input("Time")
    

    d_str = d.strftime('%Y-%m-%d')  
    t_str = t.strftime('%H:%M:%S')  
    

    cursor.execute('SELECT dj_id FROM manager_times WHERE available_time = ? AND available_date = ?', (t_str, d_str))
    result = cursor.fetchall()
    cursor.execute('SELECT start, end,day from schedule')
    result2 = cursor.fetchall()
    for i in result2:
        start = i[0]
        startTime = parser.parse(start).time()
        end = i[1]
        endTime = parser.parse(end).time()
        day = i[2]
        if startTime<=t<=endTime and d.strftime('%A')==day:
            timeAvailable = False

        if timeAvailable == False:
            st.warning("There is a radio show at this time.", icon="⏰")
            break
        


    if result: 
        st.warning("That time is already booked.", icon="⏰")
        timeAvailable = False
    

    submitted = st.form_submit_button("Submit")


    if submitted:
        if timeAvailable:
            cursor.execute('INSERT INTO manager_times (dj_id, available_time, available_date) VALUES (?, ?, ?)', (st.session_state.id, t_str, d_str))
            conn.commit()
            st.success("Time has been successfully added!")
            st.switch_page("pages/managerdashboard.py")


conn.close()
