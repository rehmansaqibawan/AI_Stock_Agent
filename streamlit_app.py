#this file will be used to print the responce of the llm from the maain.py and we will build ui of this responce using streamlitS
import streamlit as st
from langchain.schema import HumanMessage
  # Import the agent executor from main.py
import sys
import os

st.write("Current Directory:", os.getcwd())  # Print current directory
st.write("Python Path:", sys.path)  # Print Python's search path

sys.path.append(os.path.dirname(__file__))  # Ensure Python recognizes the current directory

from main import finance_agent_executor


# Streamlit UI Setup
st.title("Finance Agent - Stock Information")
st.write("Enter a company name to get financial details.")

# User input for company name
company_name = st.text_input("Company Name", "Apple")

if st.button("Get Stock Info"):
    with st.spinner("Fetching stock details..."):
        # Fetch stock price
        response_price = finance_agent_executor.invoke(
            {"messages": [HumanMessage(content=f"What is the stock price of {company_name}?")]} )
        
        # Fetch last dividend date
        response_dividend = finance_agent_executor.invoke(
            {"messages": [HumanMessage(content=f"What is the last dividend date of {company_name}?")]} )
        
        # Display results
        st.subheader("Stock Price")
        st.write(response_price)
        
        st.subheader("Last Dividend Date")
        st.write(response_dividend)

if st.button("Get Stock Info", key="get_stock_info_button"):
    st.write("Fetching stock details...")
    
    try:
        with st.spinner("Fetching stock details..."):
            st.write("Calling `finance_agent_executor.invoke()`...")  # Debugging step
            
            # Fetch stock price
            response_price = finance_agent_executor.invoke(
                {"messages": [HumanMessage(content=f"What is the stock price of {company_name}?")]}
            )
            
            st.write("Stock price fetched.")  # Debugging step
            
            # Fetch last dividend date
            response_dividend = finance_agent_executor.invoke(
                {"messages": [HumanMessage(content=f"What is the last dividend date of {company_name}?")]}
            )
            
            st.write("Dividend info fetched.")  # Debugging step
            
            # Display results
            st.subheader("Stock Price")
            st.write(response_price)
            
            st.subheader("Last Dividend Date")
            st.write(response_dividend)

    except Exception as e:
        st.error(f"Error: {str(e)}")  # Show the exact error message in Streamlit
