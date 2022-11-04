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

def values():
    global initial, interest, time, intitializeChart
    st.title("Compund Interest Calculator 📈")
    initial = st.number_input("Initial Value:")
    interest = st.number_input("Interest Rate: ")
    time = st.number_input("Over how many years: ")
    intitializeChart = initial
values()

def totalCalculation():
    global initial
    for i in range(1, int(time + 1)):
      initial = (float(initial)) * (1 + float(interest * 0.01))
    total = (str("{:,}".format(round(float(initial), 2))))
    years = round(int(time), 2)
    st.subheader("The total in " + str(years) +  " years is: " + "$ " + total)
totalCalculation()

def chart():
  #Plotting the chart
  global intitializeChart, df
  arr = [intitializeChart]
  for i in range(1, int(time + 1)):
    intitializeChart = (float(intitializeChart)) * (1 + float(interest * 0.01))
    arr.append((round(float(intitializeChart), 2)))      
  df = pd.DataFrame(arr, columns =['                                           Dollars'])
  st.line_chart(df)
chart()

def sidebar():
  with st.sidebar:
    st.sidebar.success("Select Page Above")
    st.subheader("Increase Per Year Chart 💸")
    df
sidebar()




