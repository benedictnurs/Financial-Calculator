import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt

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

source = pd.DataFrame({
    'a': [1, 2,3, 4, 5, 6, 7, 8, 9],
    'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
})

c = alt.Chart(source).mark_bar().encode(
    x='a',
    y='b'
)




st.altair_chart(c, use_container_width=False)