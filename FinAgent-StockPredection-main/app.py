import streamlit as st
import http.client
import pandas as pd
import plotly.graph_objs as go
from prophet import Prophet
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# RapidAPI credentials
RAPIDAPI_KEY = "af4b7ada73msh7333fb00c727f70p195232jsne091685d1739"

# Expanded company name to stock symbol mapping
company_symbol_mapping = {
    "Netflix": "NFLX",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Facebook": "META",
    "Tesla": "TSLA",
    "Nvidia": "NVDA",
    "Intel": "INTC",
    "IBM": "IBM",
    "Twitter": "TWTR",
    "Salesforce": "CRM",
    "Adobe": "ADBE",
    "Zoom": "ZM",
    "PayPal": "PYPL",
    "Snap": "SNAP",
    "Uber": "UBER",
    "Airbnb": "ABNB",
    "Spotify": "SPOT",
    "Slack": "WORK",
    "Shopify": "SHOP",
    "Alibaba": "BABA",
    "Tencent": "TCEHY",
    "Baidu": "BIDU",
    "JD.com": "JD",
    "Sina": "SINA",
    "Etsy": "ETSY",
    "Square": "SQ",
    "Palantir": "PLTR",
    "Roku": "ROKU",
    "DocuSign": "DOCU",
    "Twilio": "TWLO",
    "Atlassian": "TEAM",
    "Zillow": "Z",
    "DraftKings": "DKNG",
    "Pinterest": "PINS",
    "Alibaba": "BABA",
    "Alibaba": "BABA",
    "Xiaomi": "XIACF",
    "Lyft": "LYFT",
    "Uber": "UBER",
    "Moderna": "MRNA",
    "Johnson & Johnson": "JNJ",
    "Pfizer": "PFE",
    "Merck": "MRK",
    "Roche": "RHHBY",
    "Novartis": "NVS",
    "AstraZeneca": "AZN",
    "Gilead": "GILD",
    "Bristol-Myers Squibb": "BMY",
    "Amgen": "AMGN",
    "Eli Lilly": "LLY",
    "GlaxoSmithKline": "GSK",
    "Sanofi": "SNY",
    "Abbott": "ABT",
    "Thermo Fisher": "TMO",
    "GE Healthcare": "GEHC",
    "Siemens Healthineers": "SMMNY",
    "Medtronic": "MDT",
    "Boston Scientific": "BSX",
    "Stryker": "SYK",
    "Zimmer Biomet": "ZBH",
    "Dexcom": "DXCM",
    "Intuitive Surgical": "ISRG",
    "Align Technology": "ALGN",
    "Edwards Lifesciences": "EW",
    "Hologic": "HOLX",
    "Varian": "VAR",
    "Illumina": "ILMN",
    "NantKwest": "NK",
    "Bluebird Bio": "BLUE",
    "Sarepta Therapeutics": "SRPT",
    "CRISPR Therapeutics": "CRSP",
    "Docusign": "DOCU",
    "CrowdStrike": "CRWD",
    "Nutanix": "NTNX",
    "Elastic": "ESTC",
    "Snowflake": "SNOW",
    "HashiCorp": "HCP",
    "Okta": "OKTA",
    "ServiceNow": "NOW",
}
# Function to fetch stock data from RapidAPI
def fetch_stock_data(symbol, time_series_type, interval=None):
    conn = http.client.HTTPSConnection("alpha-vantage.p.rapidapi.com")
    
    if time_series_type == "Intraday":
        endpoint = f"/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize=compact&datatype=json"
    elif time_series_type == "Weekly":
        endpoint = f"/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&outputsize=compact&datatype=json"
    elif time_series_type == "Monthly":
        endpoint = f"/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&outputsize=compact&datatype=json"
    
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
    }
    
    conn.request("GET", endpoint, headers=headers)
    
    response = conn.getresponse()
    data = response.read()
    
    if response.status != 200:
        st.error("Failed to fetch data from RapidAPI. Please try again later.")
        return None
    
    data_json = json.loads(data.decode("utf-8"))
    
    if "Time Series" not in str(data_json.keys()):
        if "Error Message" in data_json:
            st.error(f"API Error: {data_json['Error Message']}")
        elif "Note" in data_json:
            st.error(f"API Note: {data_json['Note']}")
        else:
            st.error("Unexpected error. Please try again later.")
        return None
    
    if time_series_type == "Intraday":
        time_series_key = f"Time Series ({interval})"
    elif time_series_type == "Weekly":
        time_series_key = "Weekly Time Series"
    elif time_series_type == "Monthly":
        time_series_key = "Monthly Time Series"
    
    time_series = data_json.get(time_series_key)
    return time_series

# Function to convert fetched data into a DataFrame
def convert_to_dataframe(time_series):
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close',
        '5. volume': 'Volume'
    })
    df = df.astype(float)
    return df

# Function to train a model and predict stock trend
# Function to train a model and predict stock trend
def predict_trend(df, period, freq):
    df_prophet = df.reset_index().rename(columns={"index": "ds", "Close": "y"})
    
    model = Prophet(daily_seasonality=True)
    model.fit(df_prophet)

    # Use lowercase 'h', 'w', 'm' instead of 'H', 'W', 'M'
    future = model.make_future_dataframe(periods=period, freq=freq.lower())
    forecast = model.predict(future)

    fig = model.plot(forecast)
    st.pyplot(fig)

    forecast['trend_diff'] = forecast['yhat'].diff()

    last_trend = forecast['trend_diff'].iloc[-1]
    if last_trend > 0:
        return "Up"
    elif last_trend < 0:
        return "Down"
    else:
        return "Neutral"


# Function to plot the stock data
def plot_stock_data(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=f'Close Price of {symbol}', line=dict(color='cyan')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Open'], mode='lines', name=f'Open Price of {symbol}', line=dict(color='green')))
    fig.update_layout(
        title=f'Stock Price of {symbol} Over Time',
        xaxis_title='Date',
        yaxis_title='Price',
        hovermode='x',
        template='plotly_dark'
    )
    st.plotly_chart(fig)

# Streamlit app
def main():
    st.title("FinAgent Stock Prediction")
    st.markdown("""
    <style>
    .reportview-container {
        background-color: #f5f5f5;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    search_term = st.text_input("Search for a Company", "")
    
    if search_term:
        # Filter company names based on the search term
        filtered_companies = {name: symbol for name, symbol in company_symbol_mapping.items() if search_term.lower() in name.lower()}
        
        if filtered_companies:
            for company_name, stock_symbol in filtered_companies.items():
                st.markdown(f"### {company_name} ({stock_symbol})")
                
                time_series_type = st.selectbox("Select Time Series Type", ["Intraday", "Weekly", "Monthly"], key=company_name)
                
                interval = None
                if time_series_type == "Intraday":
                    interval = st.selectbox("Select Interval", ["1min", "5min", "15min", "30min", "60min"], key=f'{company_name}_interval')
                
                if st.button(f"Fetch Data for {company_name}"):
                    with st.spinner(f"Fetching data for {company_name}..."):
                        time_series = fetch_stock_data(stock_symbol, time_series_type, interval)
                    
                    if time_series:
                        df = convert_to_dataframe(time_series)
                        
                        st.write(f"Showing {time_series_type.lower()} data for: **{company_name} ({stock_symbol})**")
                        st.dataframe(df.head())
                        
                        plot_stock_data(df, company_name)
                        
                        if time_series_type == "Intraday":
                            trend = predict_trend(df, period=1, freq='H')  # Hourly prediction
                        elif time_series_type == "Weekly":
                            trend = predict_trend(df, period=1, freq='W')  # Weekly prediction
                        elif time_series_type == "Monthly":
                            trend = predict_trend(df, period=1, freq='M')  # Monthly prediction
                        
                        st.markdown(f"### Predicted Trend for next {time_series_type.lower()}: **{trend}**")
                    else:
                        st.error("Error fetching data. Please try again later.")
        else:
            st.warning("No companies match your search term. Please try another term.")
    else:
        st.write("Start typing the company name to see suggestions...")

if __name__ == "__main__":
    main()
