from datetime import time
from array import array
import pandas as pd
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

names = []
titles = []
days = []
starts = []
end = []
results = cursor.execute("select * from schedule")

for i in results:
    names.append(str(i[0]))
    titles.append(str(i[1]))
    days.append(str(i[2]))
    starts.append(str(i[3]))
    end.append(str(i[4]))

data_df = pd.DataFrame(
    {
        "dj name":names,
        "show name":titles,
        "day of week":days,
        "start time":starts,
        "end time": end,
    }
)
st.dataframe(data_df)
st.page_link("https://onlineradiobox.com/us/wmtb/", label="listen to WMTB 89.9 FM", icon="📻")
st.divider()
if st.session_state.manager == 1:
    selection = st.pills("actions",label_visibility="hidden",options=["insert show time","return to dashboard"])
    if selection == "insert show time":
        st.switch_page("pages/addshow.py")
    if selection == "return to dashboard":
        st.switch_page("pages/managerdashboard.py")
else:
    if st.button("return to dashboard"):
        st.switch_page("pages/home.py")

