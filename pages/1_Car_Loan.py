import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt

#streamlit run main.py
def configPage():
  st.set_page_config(
    page_title = "Car Loan",
    page_icon="📈",
    initial_sidebar_state="collapsed"
)
configPage()

def sidebar():
  with st.sidebar:
    st.sidebar.success("Select Page Above")
sidebar()

#Get the user input values
def values():
    global price, down, interest, tax, monthly
    st.title("Car Loan Calculator")
    price = st.number_input("Car Total")
    down = st.number_input("Down Payment")
    interest = st.number_input("Interest Rate")
    tax = st.number_input("Sales Tax")
    monthly = st.selectbox(
    'How many months will the loan be?',
    ('12', '24', '48','60','72','84'))
values()

taxRate = price * tax/100
total = (taxRate + price)  
rate = (interest / 100)/12

def years():
    global month, year
    if monthly == '12':
        month = 12
    elif monthly == '24':
        month = 24
    elif monthly == '48':
        month = 48
    elif monthly == '60':
        month = 60
    elif monthly == '72':
        month = 72     
    else:
        month = 84
    year = month/12
years()

def selection():
    global monthlyPayment
    agree = st.checkbox('Include All Fees in Loan')
    if agree:
        if rate == 0 :
            monthlyPayment =  (price - down)/month 
        else:
            monthlyPayment = (total - down) * (rate*(1+rate)**month)/((1+rate)**month-1)
    else:
        if rate == 0 :
            monthlyPayment =  (total - down)/month 
        else:
            monthlyPayment = (price - down) * (rate*(1+rate)**month)/((1+rate)**month-1)    
selection()

st.subheader("Monthly Payment: $" + (str("{:,}".format(round(float(monthlyPayment), 2)))))

def tabs():
  tab1, tab2 , tab3 = st.tabs(["Chart","Data", "Table",])
  #Chart
  tab1.subheader('Increase Per Year Chart')
  #Data
  tab2.subheader('Increase Per Year Data')
  #Table
  tab3.subheader('Increase Per Year Table')
tabs()

interestPaid = (monthlyPayment * month) - total
source = pd.DataFrame({"Loan Breakdown": ["Principal", "Interest"], "Dollars": [total, interestPaid]})

plot = alt.Chart(source).mark_arc().encode(
    theta=alt.Theta(field="Dollars", type="quantitative"),
    color=alt.Color(field="Loan Breakdown", type="nominal"),    
    tooltip=['Loan Breakdown', 'Dollars']
).interactive()

st.altair_chart(plot, use_container_width=False)