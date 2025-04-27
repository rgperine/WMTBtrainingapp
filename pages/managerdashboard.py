import streamlit as st
from datetime import datetime 
import sqlite3

style = """
    <style>
        /* Hide the sidebar container */
        div[data-testid="stSidebarContent"] {
            display: none;
        }

    </style>
"""

conn = sqlite3.connect('radio.db')
cursor = conn.cursor()

st.markdown(style, unsafe_allow_html=True)
st.title("Manager Dashboard")
st.write("Welcome "+st.session_state.name+"!")
st.divider()
st.subheader("Your current available times")
djid = st.session_state.id
result = cursor.execute('SELECT available_date, available_time FROM manager_times WHERE dj_id = ?', (djid,)).fetchall()

print(result)
for i in result:



        dtstr = f"{i[0]} {i[1]}"

        datetime_obj = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')


        formatted = datetime_obj.strftime('%B %d at %I:%M %p')
        label = formatted

        with st.popover(label):
            label2 = "remove "+label
            if st.button(label2):
                cursor.execute("delete from manager_times where available_date = ? and available_time = ?",(i[0],i[1]))
                conn.commit()
                st.session_state['deletedtime'] = label
                st.switch_page("pages/confirm_delete.py")

st.divider()
st.subheader("Your current booked times")
result = cursor.execute('SELECT bt.date, bt.time, d.first_name FROM bookedtimes bt JOIN djs d ON bt.trainee = d.dj_id WHERE bt.manager = ?', (st.session_state.id,)).fetchall()
for i in result:

        dtstrng = f"{i[0]} {i[1]}"

        datetime = datetime.strptime(dtstrng, '%Y-%m-%d %H:%M:%S')

        formatted = datetime.strftime('%B %d at %I:%M %p')
        label = formatted+ " with "+ i[2]

        with st.popover(label):
            label2 = "remove "+label
            if st.button(label2):
                cursor.execute("delete from bookedtimes where date = ? and time = ?",(i[0],i[1]))
                conn.commit()
                st.session_state['deletedtime'] = label
                st.switch_page("pages/confirm_delete.py")
st.divider()

selection = st.pills("manager actions",options = ["view and edit member list","add available times","logout","view and edit schedule"],label_visibility="hidden")
if selection == "view and edit member list":
        st.switch_page("pages/manageraccess.py")
if selection == "add available times":
    st.switch_page("pages/add-time.py")
if selection == "logout":
    st.switch_page("sl1.py")
if selection == "view and edit schedule":
    st.switch_page("pages/schedule.py")