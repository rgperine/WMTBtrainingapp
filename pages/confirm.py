import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from dotenv import load_dotenv
import os
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

managerid = st.session_state.managerid
dj_id = st.session_state.id
name = st.session_state.name
dj_email = cursor.execute("select email from djs where dj_id = ?",(dj_id,)).fetchall()[0][0]
manager_email = cursor.execute("select email from djs where dj_id = ?",(managerid,)).fetchall()[0][0]
st.markdown(style, unsafe_allow_html=True)
st.subheader("confirmation")
st.divider()
st.write("you selected a training session on "+st.session_state.selectdate+ " at "+st.session_state.selecttime+" with "+ st.session_state.managername)
# Email credentials
load_dotenv()
mailServer = "smtp.mailersend.net"
port = 587
email = os.getenv('email')
password = os.getenv('password')  


msg = MIMEMultipart()
msg["From"] = email
msg["To"] = dj_email
msg["Subject"] = "Training Session Confirmation"

body = "You scheduled a training session on "+st.session_state.selectdate+ " at "+st.session_state.selecttime+" with "+ st.session_state.managername
msg.attach(MIMEText(body, "plain"))

# Send email
server = smtplib.SMTP(mailServer, port)
server.starttls()  # Secure connection
server.login(email, password)
server.sendmail(email, dj_email, msg.as_string())
server.quit()
print("Email sent successfully!")


msg = MIMEMultipart()
msg["From"] = email
msg["To"] = manager_email
msg["Subject"] = "Training Session Notification"

body = "You have a training session on "+st.session_state.selectdate+ " at "+st.session_state.selecttime+" with "+ st.session_state.name
msg.attach(MIMEText(body, "plain"))


try:
    server = smtplib.SMTP(mailServer, port)
    server.starttls()  # Secure connection
    server.login(email, password)
    server.sendmail(email, dj_email, msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("Error:", e)


#pass: M0untR@di0


if st.button("return to dashboard"):
    st.switch_page("pages/home.py")