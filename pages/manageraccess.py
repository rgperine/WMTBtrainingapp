import streamlit as st

import sqlite3

conn = sqlite3.connect('radio.db')
cursor = conn.cursor()

djid = st.session_state.id

cursor.execute("select admin from djs where dj_id =?",(djid,))
admin = cursor.fetchall()[0][0]

st.subheader("Current Users")

cursor.execute("select dj_id, first_name, last_name, manager, admin from djs")
results = cursor.fetchall()
for i in results:
    dj_id,first_name,last_name,manager,admins = i[0],i[1],i[2],i[3],i[4]
    label = first_name+" "+last_name
    with st.popover(label):
        label2 = "remove "+label
        label3 = "give "+label+" manager access"
        label4 = "remove manager access for "+label
        if st.button(label2):
            if admins == 1:
                st.warning("you cannot remove a current admin",icon ="⚠️")
            else:
                cursor.execute("delete from djs where dj_id = ?",(dj_id,))

                conn.commit()
                st.success("this user will be removed")

            
            st.write
        if admin == 1:
            if manager == 0:
                if st.button(label3):
                    cursor.execute("update djs set manager=? where dj_id=?",(1,dj_id))
                    conn.commit()
                    st.success("this user will be given access")

            else:
                if st.button(label4):
                    cursor.execute("update djs set manager=? where dj_id=?",(0,dj_id))
                    conn.commit()
                    st.success("this user's access will be removed")

if st.button("return to dashboard"):
    st.switch_page("pages/managerdashboard.py")