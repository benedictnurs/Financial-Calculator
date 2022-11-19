import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt

#streamlit run main.py
st.set_page_config(
    page_title = "Auto Loan Calculator",
    page_icon="📈",
    initial_sidebar_state="collapsed"
    )
with st.sidebar:
    st.sidebar.success("Select Page Above")

#Get the user input values
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

#Function styles the table so that there is no index
tableIndexHide = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(tableIndexHide, unsafe_allow_html=True)


#Creates the monthly values for calculations
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

def variables():
    global monthlyPayment, upFront, totalPaid, totalLoan , totalCost, totalInterest , salesTax, total, rate
    
    salesTax = price * tax/100
    total = (salesTax + price)  
    rate = (interest / 100)/12
    agree = st.checkbox('Include All Fees in Loan')
    
    #Calculates the monthly payments
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
    
    #Calculates the monthly payments with the upfront payment
    if agree:
        upFront = down
        totalPaid = (monthlyPayment * month) + salesTax
        totalLoan = (price - down) + salesTax
    else:
        upFront = salesTax + down
        totalPaid = monthlyPayment * month
        totalLoan = price - down

    #Interest total of the monthly payments
    totalInterest = totalPaid - totalLoan 
    
    #To prevent 0's from messing up with the total interest
    if rate == 0:
        totalInterest = 0
    else:
        totalInterest = totalPaid - totalLoan 
    
    #Total cost of the loans with the interest 
    totalCost = total + totalInterest
variables()


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
        <h3 class="a">Sales Tax: $ {(str("{:,}".format(round(float(salesTax), 2))))}</h3>
        <h3 class="a">Upfront: $ {(str("{:,}".format(round(float(upFront), 2))))}</h3>
        <h3 class="a"> Loan Cost: $ {(str("{:,}".format(round(float(totalLoan), 2))))}</h3>
        <h3 class="a top">{month} month total: $ {(str("{:,}".format(round(float(totalPaid), 2))))}</h3>
        <h3 class="a">Total Interest: $ {(str("{:,}".format(round(float(totalInterest), 2))))}</h3>
        <h3 class="a">Total Cost: $ {(str("{:,}".format(round(float(totalCost), 2))))}</h3>
        """
        st.markdown(html_str, unsafe_allow_html=True)


#Creates the monthlyData data frame
def chart_calculations():
    global totalPaid, x, y
    y = [totalPaid]
    x = list(range(0,int(month)+1))
    for i in range(1, int(month + 1)):
        totalPaid = totalPaid - monthlyPayment
        y.append(round((totalPaid),2))
chart_calculations()

#Creates the data frame for the pie chart
pie = pd.DataFrame({"Breakdown": ["Principal", "Interest"], "Dollars": [total, totalInterest], "Percentages":["P","I"]})


#Creates the data frame for the monthly payment chart
monthlyData = pd.DataFrame({
    'Dollars': y,
    'Months': x
    })


#Creates the data frame for the yearly payment chart
yearlyData = monthlyData.iloc[::12,:]
del yearlyData["Months"]
yearlyData['Years'] = (monthlyData['Months'] / 12).round(2)


def plot_charts():
    global monthlyChart , yearlyChart, pieChart


    #Plotting the monthly chart
    monthlyChart = alt.Chart(monthlyData).mark_line().encode(
    x = alt.X('Months:Q', axis = alt.Axis(
        grid = False,
    )),
    y ='Dollars'
    ).configure_view(
    strokeOpacity = 0
    ).configure_axis(
    labelFontSize = 15,
    titleFontSize = 18,
    titleFontWeight = 100
    )


    #Plotting the yearly chart
    yearlyChart = alt.Chart(yearlyData).mark_bar().encode(
    x = alt.X('Years:Q', axis = alt.Axis(
        grid = False,
    )),
    y ='Dollars'
    ).configure_view(
    strokeOpacity = 0
    ).configure_axis(
    labelFontSize = 15,
    titleFontSize = 18,
    titleFontWeight = 100
    )

    #Plotting the pie chart
    pieChart = alt.Chart(pie).mark_arc().encode(
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

plot_charts()

#Creates the 2 tabs of the chart
tabs = st.tabs(["Chart", "Table",])
tab_chart = tabs[0]
tab_data = tabs[1]
  
#First tab
with tab_chart:
#Creates 2 columns for the first tab
    cols = st.columns(2)
with cols[0]:
    st.subheader("Loan Breakdown")
    st.altair_chart(pieChart, use_container_width=True)
with cols[1]:
    header = st.empty()
    agree = st.checkbox('Monthly') 
    chart = st.empty()
    if agree:
        header.subheader('Monthly Chart')
        chart.altair_chart(monthlyChart, use_container_width = True)
    else:
        header.subheader('Yearly Chart')
        chart.altair_chart(yearlyChart, use_container_width = True)


#Second tab
with tab_data:
    st.subheader('Data')
    agree = st.checkbox('Monthly Loan Total') 
    data = st.empty()
    if agree:
        data.table(monthlyData)
    else:
        data.table(yearlyData)


