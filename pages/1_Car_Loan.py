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

def sideVariables():
    global monthlyPayment, upFront, totalPaid, totalLoan , addedCost, interestPaid
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
        upFront = down
        totalPaid = (monthlyPayment * month)+taxRate
        totalLoan = (price - down) + taxRate

    else:
        upFront = taxRate + down
        totalPaid = monthlyPayment * month
        totalLoan = price - down


    interestPaid = totalPaid - totalLoan 
    
    
    if rate == 0:
        interestPaid = 0
    else:
        interestPaid = totalPaid - totalLoan 
    
    
    addedCost = total + interestPaid
sideVariables()



source = pd.DataFrame({"Breakdown": ["Principal", "Interest"], "Dollars": [total, interestPaid], "Percentages":["P","I"]})
pie = alt.Chart(source).mark_arc().encode(
        theta=alt.Theta(field="Dollars", type="quantitative"),
        color=alt.Color(field="Breakdown", type="nominal"),    
        tooltip=['Breakdown', alt.Tooltip('Dollars:Q',  format="$,.2f")]
    ).interactive(

    ).configure_legend(
     labelFontWeight = 100,
     labelFontSize = 12,
     titleFontSize = 15,
     titleFontWeight = 100
    )

def sidePage():        
    with topCols[1]:
        html_str = f"""
        <style>
        .a {{
        font: 24px sans-serif;
        font-weight: bold;
        }}

        .top{{
            margin-top:1.5em;

        }}
        </style>
        <h3 class="a top">Monthly: $ {(str("{:,}".format(round(float(monthlyPayment), 2))))}</h3>
        <h3 class="a">Sales Tax: $ {(str("{:,}".format(round(float(taxRate), 2))))}</h3>
        <h3 class="a">Upfront: $ {(str("{:,}".format(round(float(upFront), 2))))}</h3>
        <h3 class="a"> Loan Cost: $ {(str("{:,}".format(round(float(totalLoan), 2))))}</h3>
        <h3 class="a top">{month} month total: $ {(str("{:,}".format(round(float(totalPaid), 2))))}</h3>
        <h3 class="a">Total Interest: $ {(str("{:,}".format(round(float(interestPaid), 2))))}</h3>
        <h3 class="a">Total Cost: $ {(str("{:,}".format(round(float(addedCost), 2))))}</h3>
        """
        st.markdown(html_str, unsafe_allow_html=True)
sidePage()

def data():
  global x, y
  y = [totalPaid]
  x = list(range(0,int(month)+1))
data()

def chartCalculation():
    global totalPaid
    for i in range(1, int(month + 1)):
        totalPaid = totalPaid - monthlyPayment
        y.append(round((totalPaid),2))
chartCalculation()


def plotChart():
    global monthlyChart, df
    df = pd.DataFrame({
    'Dollars': y,
    'Months': x
    })
    monthlyChart = alt.Chart(df).mark_line().encode(
    x = alt.X('Months:Q', axis = alt.Axis(
        grid = False,
    )),
    y ='Dollars'
    ).configure_view(
    strokeOpacity=0
    ).configure_axis(
    labelFontSize=15,
    titleFontSize=18,
    titleFontWeight = 100
    )
plotChart()


def dataFrame2():
    global df2, yearlyChart
    df2 = df.iloc[::12,:]
    del df2["Months"]
    df2['Years'] = (df['Months'] / 12).round(2)
    yearlyChart = alt.Chart(df2).mark_bar().encode(
    x = alt.X('Years:Q', axis = alt.Axis(
        grid = False,
    )),
    y ='Dollars'
    ).configure_view(
    strokeOpacity=0
    ).configure_axis(
    labelFontSize=15,
    titleFontSize=18,
    titleFontWeight = 100
    )
dataFrame2()



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
        header = st.empty()
        agree = st.checkbox('Yearly') 
        chart = st.empty()
        if agree:
            header.subheader('Yearly Chart')
            chart.altair_chart(yearlyChart, use_container_width = True)
        else:
            header.subheader('Monthly Chart')
            chart.altair_chart(monthlyChart, use_container_width = True)
  #Data
  with tab_data:
        st.subheader('Data')
        agree = st.checkbox('Monthly Loan Total') 
        data = st.empty()
        if agree:
            data.table(df)
        else:
            data.table(df2)
tabs()


def style(): 
  hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
  st.markdown(hide_table_row_index, unsafe_allow_html=True)
style()


