import streamlit as st
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
st.title("WMTB Training Portal")
st.divider()
st.header("Log in")

if "id" not in st.session_state:
    st.session_state.id = None
if "name" not in st.session_state:
    st.session_state.name = ""

options = ["I'm new", "I'm returning"]
selection = st.pills("", options,default="I'm new")

if selection == "I'm new":
    with st.form("my_form"):
        first = st.text_input("First Name")
        last = st.text_input("Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        st.write("Managers will have to be given access by admin upon account creation.")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            cursor.execute("SELECT email FROM djs WHERE first_name = ? AND last_name = ?", (first, last))
            result = cursor.fetchall()
            
            if not result:  
                cursor.execute("INSERT INTO djs (first_name, last_name, email, password) VALUES (?, ?, ?, ?)", (first, last, email, password))
                conn.commit()
                st.success("Account created successfully!")
                cursor.execute("SELECT dj_id FROM djs WHERE first_name = ? AND last_name = ? AND password = ?", (first, last, password))
                results = cursor.fetchall()
                dj_id = results[0][0]
                st.session_state.id = dj_id
                st.session_state.name = first
                st.session_state.manager = 0
                st.switch_page('pages/home.py')
            else:
                st.warning("This user already exists", icon="🔐")





if selection == "I'm returning":
    with st.form("my_form2"):
        first = st.text_input("First Name")
        last = st.text_input("Last Name")
        password = st.text_input("Password", type='password')
        
        cursor.execute("SELECT password FROM djs WHERE first_name = ? AND last_name = ?", (first, last))
        result = cursor.fetchall()
        
        if result:
            correctpass = result[0][0]
        else:
            correctpass = None
        submitted1 = st.form_submit_button("Submit")
        
        if submitted1:
            if correctpass == None or password != correctpass:
                st.warning("Incorrect login information", icon="🔐")
            else:
                cursor.execute("SELECT dj_id,manager FROM djs WHERE first_name = ? AND last_name = ? AND password = ?", (first, last, correctpass))
                results = cursor.fetchall()
                dj_id = results[0][0]
                manager = results[0][1]

                st.session_state.id = dj_id

                st.session_state.name = first
                st.session_state.manager = manager
                
                cursor.execute("SELECT manager FROM djs WHERE first_name = ? AND last_name = ? AND password = ?", (first, last, correctpass))
                manager = cursor.fetchall()[0][0]
                
                if manager == 1:
                    st.switch_page('pages/managerdashboard.py')
                else:
                    st.switch_page('pages/home.py')
