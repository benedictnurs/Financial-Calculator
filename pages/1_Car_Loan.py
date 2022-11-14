import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt

#streamlit run main.py
def configPage():
  st.set_page_config(
    page_title = "Auto Loan Calculator",
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
    global price, down, interest, tax, monthly, topCols
    st.title("Car Loan Calculator")
    topCols = st.columns(2)
    with topCols[0]:
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
    global monthlyPayment, upfront
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
    if agree:
        upfront = taxRate + down
    else:
        upfront = taxRate + down
selection()



interestPaid = round((total - (monthlyPayment * month)),2)



source = pd.DataFrame({"Loan Breakdown": ["Principal", "Interest"], "Dollars": [total, interestPaid]})
pie = alt.Chart(source).mark_arc().encode(
        theta=alt.Theta(field="Dollars", type="quantitative"),
        color=alt.Color(field="Loan Breakdown", type="nominal"),    
        tooltip=['Loan Breakdown', alt.Tooltip('Dollars:Q',  format="$,.2f")]
    ).interactive()


with topCols[1]:
    html_str = f"""
    <style>
    p.a {{
    font: 20vw sans-serif;
    }}
    </style>
    <p></p>
    <h3 class="a">Monthly Pay: $ {(str("{:,}".format(round(float(monthlyPayment), 2))))}</h3>
    <h3 class="a">Sale Tax: $ {(str("{:,}".format(round(float(taxRate), 2))))}</h3>
    <h3 class="a">Upfront: $ {(str("{:,}".format(round(float(upfront), 2))))}</h3>
    <h3 class="a">Total Interest: $ {(str("{:,}".format(round(float(interestPaid), 2))))}</h3>
    <h3 class="a">Total Cost: $ {(str("{:,}".format(round(float(monthlyPayment), 2))))}</h3>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def tabs():
  tabs = st.tabs(["Chart", "Table",])
  #Chart
  tab_chart = tabs[0]
  tab_data = tabs[1]
  
  with tab_chart:
        cols = st.columns(2)
  with cols[0]:
        st.subheader("Loan Breakdown")
        st.altair_chart(pie, use_container_width=True)
  with cols[1]:
        st.subheader("Loan By Year")
  
  #Data
  with tab_data:
        st.subheader('Data')
tabs()






