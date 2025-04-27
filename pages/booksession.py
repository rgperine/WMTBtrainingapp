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

st.markdown(style, unsafe_allow_html=True)

conn = sqlite3.connect('radio.db')
cursor = conn.cursor()
st.title("Book a training session")
st.subheader("select a time that works for you")
st.divider()
result = cursor.execute('SELECT available_date, available_time,dj_id from manager_times').fetchall()
print(result)
if result== "":
    st.write("there are no available times right now, please check back at a later time")
else:
    for i in result:


            dtstr = f"{i[0]} {i[1]}"

            datetime_obj = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')


            formatted = datetime_obj.strftime('%B %d at %I:%M %p')
            label = formatted
            
            cursor.execute("select first_name from djs where dj_id = ?",(i[2],))
            st.session_state.managerid=i[2]
            managername = cursor.fetchall()[0][0]
            if st.button(label):
                    if "selectdate" not in st.session_state:
                        st.session_state.selectdate = i[0]
                    if "selecttime" not in st.session_state:
                        st.session_state.selecttime = i[1]
                    if "managername" not in st.session_state:
                        st.session_state.managername = managername
                    cursor.execute('insert into bookedtimes (trainee,manager,date,time) values(?,?,?,?)',(st.session_state.id,i[2],i[0],i[1]))
                    conn.commit()
                    cursor.execute("Delete from manager_times where dj_id = ? and available_time =? and available_date =?",(i[2],i[1],i[0]))
                    conn.commit()
                    st.switch_page('pages/confirm.py')

st.divider()
if st.button("return to dashboard"):
    st.switch_page("pages/home.py")

                    
