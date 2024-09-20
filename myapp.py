import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Set the title of the app
st.title('📈 Stock Price App')

st.markdown("""
This app retrieves the stock **closing price** and **volume** of any company!
""")

# Sidebar for user inputs
st.sidebar.header('User Input Parameters')

def get_input():
    # Get ticker symbol from the user
    ticker_symbol = st.sidebar.text_input("Ticker Symbol", value='GOOGL', max_chars=10)

    # Get date range from the user
    start_date = st.sidebar.date_input("Start Date", datetime(2010, 1, 1))
    end_date = st.sidebar.date_input("End Date", datetime.today())

    # Ensure start date is before end date
    if start_date > end_date:
        st.sidebar.error('Error: End date must fall after start date.')
    
    return ticker_symbol.upper(), start_date, end_date

@st.cache_data
def get_data(ticker_symbol, start_date, end_date):
    try:
        # Retrieve data for the given ticker symbol and date range
        ticker_data = yf.Ticker(ticker_symbol)
        ticker_df = ticker_data.history(start=start_date, end=end_date)
        if ticker_df.empty:
            return None
        else:
            return ticker_df
    except Exception as e:
        return None

def plot_data(ticker_df, ticker_symbol):
    # Plot Closing Price
    fig_close = px.line(
        ticker_df, x=ticker_df.index, y='Close',
        title=f'Closing Price of {ticker_symbol}',
        labels={'x': 'Date', 'Close': 'Closing Price'}
    )
    st.plotly_chart(fig_close, use_container_width=True)

    # Plot Volume
    fig_volume = px.line(
        ticker_df, x=ticker_df.index, y='Volume',
        title=f'Trading Volume of {ticker_symbol}',
        labels={'x': 'Date', 'Volume': 'Volume'}
    )
    st.plotly_chart(fig_volume, use_container_width=True)

def main():
    ticker_symbol, start_date, end_date = get_input()
    ticker_df = get_data(ticker_symbol, start_date, end_date)

    if ticker_df is not None:
        st.header(f"Showing data for **{ticker_symbol}** from **{start_date}** to **{end_date}**")
        st.write(ticker_df)

        # Visualization
        plot_data(ticker_df, ticker_symbol)
    else:
        st.error(f"Unable to retrieve data for ticker symbol '{ticker_symbol}'. Please check the symbol and try again.")

if __name__ == "__main__":
    main()
