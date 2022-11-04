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
st.title("Welcome")


def sidebar():
  with st.sidebar:
    st.sidebar.success("Select Page Above")
sidebar()




