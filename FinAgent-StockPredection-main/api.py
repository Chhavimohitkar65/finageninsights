import streamlit as st
from api import fetch_stock_data
from data_processing import convert_to_dataframe, predict_trend
from visualization import plot_stock_data

# Expanded company name to stock symbol mapping
company_symbol_mapping = {
    "Netflix": "NFLX", "Apple": "AAPL", "Microsoft": "MSFT", "Amazon": "AMZN",
    "Google": "GOOGL", "Facebook": "META", "Tesla": "TSLA", "Nvidia": "NVDA",
    "Intel": "INTC", "IBM": "IBM", "Twitter": "TWTR", "Salesforce": "CRM",
    "Adobe": "ADBE", "Zoom": "ZM", "PayPal": "PYPL", "Snap": "SNAP",
    "Uber": "UBER", "Airbnb": "ABNB", "Spotify": "SPOT", "Slack": "WORK",
    "Shopify": "SHOP", "Alibaba": "BABA", "Tencent": "TCEHY", "Baidu": "BIDU",
    "JD.com": "JD", "Sina": "SINA", "Etsy": "ETSY", "Square": "SQ",
    "Palantir": "PLTR", "Roku": "ROKU", "DocuSign": "DOCU", "Twilio": "TWLO",
    "Atlassian": "TEAM", "Zillow": "Z", "DraftKings": "DKNG", "Pinterest": "PINS",
    "Xiaomi": "XIACF", "Lyft": "LYFT", "Moderna": "MRNA", "Johnson & Johnson": "JNJ",
    "Pfizer": "PFE", "Merck": "MRK", "Roche": "RHHBY", "Novartis": "NVS",
    "AstraZeneca": "AZN", "Gilead": "GILD", "Bristol-Myers Squibb": "BMY",
    "Amgen": "AMGN", "Eli Lilly": "LLY", "GlaxoSmithKline": "GSK", "Sanofi": "SNY",
    "Abbott": "ABT", "Thermo Fisher": "TMO", "GE Healthcare": "GEHC",
    "Siemens Healthineers": "SMMNY", "Medtronic": "MDT", "Boston Scientific": "BSX",
    "Stryker": "SYK", "Zimmer Biomet": "ZBH", "Dexcom": "DXCM", "Intuitive Surgical": "ISRG",
    "Align Technology": "ALGN", "Edwards Lifesciences": "EW", "Hologic": "HOLX",
    "Varian": "VAR", "Illumina": "ILMN", "NantKwest": "NK", "Bluebird Bio": "BLUE",
    "Sarepta Therapeutics": "SRPT", "CRISPR Therapeutics": "CRSP", "CrowdStrike": "CRWD",
    "Nutanix": "NTNX", "Elastic": "ESTC", "Snowflake": "SNOW", "HashiCorp": "HCP",
    "Okta": "OKTA", "ServiceNow": "NOW"
}

def main():
    st.title("Stock Prediction App")

    company = st.selectbox("Select Company", list(company_symbol_mapping.keys()))
    symbol = company_symbol_mapping[company]

    time_series_type = st.selectbox("Select Time Series Type", ["Intraday", "Weekly", "Monthly"])
    
    if time_series_type == "Intraday":
        interval = st.selectbox("Select Interval", ["1min", "5min", "15min", "30min", "60min"])
    else:
        interval = None
    
    time_series = fetch_stock_data(symbol, time_series_type, interval)
    
    if time_series:
        df = convert_to_dataframe(time_series)
        
        plot_stock_data(df, symbol)
        
        period = st.slider("Select Forecast Period (days)", min_value=1, max_value=365, value=30)
        freq = st.selectbox("Select Forecast Frequency", ["D", "W", "M"])
        
        trend = predict_trend(df, period, freq)
        st.write(f"The predicted trend for the next {period} {freq} is: {trend}")

if __name__ == "__main__":
    main()
