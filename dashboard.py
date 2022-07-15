import streamlit as st
import pandas as pd
import numpy as np
import cumulativeflowdiagram
# import cumulativeflowdiagram
import schedule
import datetime
import time   

# Schedules
boardId = 'fC64YwSb7Ry4YrvNt'
schedule.every(60).seconds.do(cumulativeflowdiagram.job)
# schedule.every().day.at("00:10").do(job)

# schedule.every(70).seconds.do(plot_cfd)
# schedule.every().day.at("00:12").do(plot_cfd)

st.title("Dashboard")

st.dataframe(cumulativeflowdiagram.cfd_to_csv())

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.area_chart(chart_data)

st.area_chart(cumulativeflowdiagram.cfd_to_csv())

while True:
    schedule.run_pending()
    time.sleep(1)

