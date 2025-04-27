import streamlit as st
import sqlite3
from datetime import datetime
conn = sqlite3.connect('radio.db')
cursor = conn.cursor()
st.subheader("add a show to the schedule")
st.divider()
with st.container(border=True):
    with st.form("new show"):
        dj = st.text_input("dj name")
        title = st.text_input("show title")
        day = st.radio("day of the week",options=("Sunday", "Monday", "Tuesday", "Wednesday","Thursday","Friday"))
        start = st.time_input("Start Time", step=1800)
        end = st.time_input("End Time", step=1800)
        startformat = str(start.strftime("%I:%M %p"))
        endformat = str(end.strftime("%I:%M %p"))
        submitted = st.form_submit_button("Add")
        if submitted:
            cursor.execute("insert into schedule (name,title,day,start,end) values(?,?,?,?,?)",(dj,title,day,startformat,endformat))
            conn.commit()
            st.switch_page("pages/schedule.py")