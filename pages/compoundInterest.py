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


#Get the user input values
def values():
    global initial, interest, time, intitializeChart
    st.title("Compund Interest Calculator 📈")
    initial = st.number_input("Initial Value:")
    interest = st.number_input("Interest Rate: ")
    time = st.number_input("Over how many years: ")
    intitializeChart = initial
values()


#calculate the interest and the years
def totalCalculation():
    global initial
    for i in range(1, int(time + 1)):
      initial = (float(initial)) * (1 + float(interest * 0.01))
    total = (str("{:,}".format(round(float(initial), 2))))
    years = round(int(time), 2)
    st.subheader("The total in " + str(years) +  " years is: " + "$ " + total)
totalCalculation()


#data for the chart
def data():
  global x, y 
  y = [intitializeChart]
  x = list(range(0,int(time)+1))
data()


#creating the data frame for the chart
def chart():
  global intitializeChart, df
  for i in range(1, int(time + 1)):
    intitializeChart = (float(intitializeChart)) * (1 + float(interest * 0.01))
    y.append((round(float(intitializeChart), 2)))      
  df = pd.DataFrame(y, columns =['                                           Dollars'])
chart()




#plotting the chart
def plotChart():
  source = pd.DataFrame({
  'Dollars': y,
  'Years': x
  })
  
  #Plotting the chart
  global plot
  plot = alt.Chart(source).mark_line().encode(
    x = alt.X('Years:Q', axis = alt.Axis(
        tickCount = df.shape[0],
        grid = False,
    )),
    y = alt.Y('Dollars:Q', axis = alt.Axis(
    ))
  ).configure_view(
    strokeOpacity=0
  ).configure_axis(
    labelFontSize=15,
    titleFontSize=18,
    titleFontWeight = 100
  )

plotChart()

def tabs():
  tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
  tab1.subheader('Increase Per Year Chart 💸')
  tab1.altair_chart(plot, use_container_width=True)
  tab2.subheader('Increase Per Year Table 💸')
  tab2.write(df)
tabs()


#the sidebar
def sidebar():
  with st.sidebar:
    st.sidebar.success("Select Page Above")
sidebar()
