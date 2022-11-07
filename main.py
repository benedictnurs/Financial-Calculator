import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt
import yfinance as yf

#streamlit run main.py
def configPage():
  st.set_page_config(
    page_title = "Financial Calculator",
    page_icon="📈",
    initial_sidebar_state="collapsed"
)
configPage()

def sidebar():
  with st.sidebar:
    st.sidebar.success("Select Page Above")
sidebar()

st.title("Welcome")


x = np.arange(100)
source = pd.DataFrame({
  'x': [1,2,3],
  'f(x)': [2,3,4]
})


df = pd.DataFrame({
    'bin': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5,
            1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0],
    'count': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 7, 14, 13, 29, 47,
              59, 59, 75, 72, 103, 96, 119, 76, 93, 68, 70, 44, 49]
})

c = alt.Chart(df).mark_line().encode(
    x=alt.X('bin:Q', axis=alt.Axis(
        tickCount=df.shape[0],
        grid=False,
        labelExpr="datum.value % 1 ? null : datum.label"
    )),
    y=alt.Y('count:Q')
)
st.altair_chart(c, use_container_width=True)
