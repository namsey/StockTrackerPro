import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Stock Data Visualization", layout="wide")

# Function to fetch stock data
def fetch_stock_data(symbol, start_date, end_date):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date)
        return df, stock.info
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None, None

# Function to create price history chart
def create_price_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Price'
    ))
    fig.update_layout(
        title="Stock Price History",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )
    return fig

# Main app
def main():
    st.title("Stock Data Visualization App")

    # User input
    col1, col2, col3 = st.columns(3)
    with col1:
        symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)").upper()
    with col2:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        start_date = st.date_input("Start Date", value=start_date)
    with col3:
        end_date = st.date_input("End Date", value=end_date)

    if symbol and start_date and end_date:
        # Fetch stock data
        df, info = fetch_stock_data(symbol, start_date, end_date)

        if df is not None and info is not None:
            # Display key financial information
            st.subheader(f"Key Financial Information for {symbol}")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Price", f"${info.get('currentPrice', 'N/A'):.2f}")
            col2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.2f}B")
            col3.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A'):.2f}")
            col4.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A'):.2f}")

            # Display price history chart
            st.plotly_chart(create_price_chart(df), use_container_width=True)

            # Display financial data table
            st.subheader("Financial Data Table")
            st.dataframe(df)

            # Download CSV button
            csv = df.to_csv(index=True)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{symbol}_stock_data.csv",
                mime="text/csv",
            )
        else:
            st.warning("Unable to fetch stock data. Please check the symbol and try again.")
    else:
        st.info("Please enter a stock symbol and select date range to view data.")

if __name__ == "__main__":
    main()
