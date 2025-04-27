from datetime import datetime
import streamlit as st

import pandas as pd

st.subheader("WMTB Air Schedule")
st.divider()
data_df = pd.DataFrame(
    {
        "appointment": [
            datetime(2024, 2, 5, 12, 30),
            datetime(2023, 11, 10, 18, 0),
            datetime(2024, 3, 11, 20, 10),
            datetime(2023, 9, 12, 3, 0),
        ]
    }
)

st.data_editor(
    data_df,
    column_config={
        "appointment": st.column_config.DatetimeColumn(
            "Appointment",
            minVal=datetime(2023, 6, 1),
            maxVal=datetime(2025, 1, 1),
            format="D MMM YYYY, h:mm a",
            step=60,
        ),
    },
    hide_index=True,
)