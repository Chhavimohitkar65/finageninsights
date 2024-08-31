import streamlit as st
import openai
import pandas as pd
from datetime import datetime
import os

# Initialize OpenAI API client
class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def get_response(self, prompt, model="gpt-3.5-turbo", max_tokens=150):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content']

# Initialize OpenAI client
openai_client = OpenAIClient()

def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'], utc=True)
    return data

def filter_data_by_company(data, company_name):
    return data[data['Company'].str.contains(company_name, case=False, na=False)]

def filter_data_by_years(data, start_year, end_year):
    data['Year'] = data['Date'].dt.year
    return data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

def display_metrics(data):
    st.markdown(
        """
        <style>
        .metric-container {
            display: flex;
            justify-content: space-between;
            gap: 10px;
        }
        .metric-box {
            flex: 1;
            padding: 15px;
            background-color: #f0f2f6;
            border-radius: 5px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .metric-box:nth-child(1) {
            background-color: #FFA07A;
        }
        .metric-box:nth-child(2) {
            background-color: #87CEFA;
        }
        .metric-box:nth-child(3) {
            background-color: #90EE90;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box">Avg Close<br>${data['Close'].mean():.2f}</div>
        <div class="metric-box">Total Volume<br>{data['Volume'].sum():,.0f}</div>
        <div class="metric-box">Highest Close<br>${data['Close'].max():.2f}</div>
    </div>
    """, unsafe_allow_html=True)

def get_growth_analysis(company_name):
    prompt = f"Provide 3 key points for {company_name} growth analysis in 3-4 words each."
    response = openai_client.get_response(prompt)
    return response.split("\n")

def get_history_and_advice(company_name):
    history_prompt = f"Summarize {company_name}'s trend in 15 words max."
    advice_prompt = f"Give investment advice for {company_name} in 10 words max."
    
    history = openai_client.get_response(history_prompt)
    advice = openai_client.get_response(advice_prompt)
    
    return history, advice

def get_news_summary(company_name, start_date, end_date):
    prompt = f"Provide a summary of the top 3 news articles affecting {company_name} between {start_date} and {end_date}. Include the headline and a brief description."
    response = openai_client.get_response(prompt, max_tokens=300)
    return response

def main():
    st.title("FinAgent Insight")

    file_path = "updated_file.csv"
    data = load_data(file_path)

    company_name = st.text_input("Company Name:")

    if company_name:
        company_data = filter_data_by_company(data, company_name)

        st.subheader("Company Overview")
        display_metrics(company_data)

        st.subheader("Stock Trend")
        start_year, end_year = st.slider(
            "Select Year Range", min_value=2000, max_value=2024, value=(2010, 2024)
        )

        filtered_data = filter_data_by_years(company_data, start_year, end_year)
        st.line_chart(filtered_data.set_index('Date')['Close'])

        st.subheader("AI Insights")

        # Displaying buttons adjacently and colorfully
        st.markdown(
            """
            <style>
            .button-container {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 10px;
            }
            .button-container button {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
                flex: 1;
            }
            .button-container button:nth-child(1) {
                background-color: #FFA07A;
            }
            .button-container button:nth-child(2) {
                background-color: #87CEFA;
            }
            .button-container button:nth-child(3) {
                background-color: #90EE90;
            }
            </style>
            """, unsafe_allow_html=True
        )

        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("Growth Analysis"):
            growth_points = get_growth_analysis(company_name)
            st.write(f"**Growth Points:**")
            for point in growth_points:
                st.write(f"- {point}")
        if st.button("History & Advice"):
            history, advice = get_history_and_advice(company_name)
            st.write(f"**History:** {history}")
            st.write(f"**Advice:** {advice}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("Top News")
        
        # Convert year range to date format
        start_date = datetime(start_year, 1, 1).strftime('%Y-%m-%d')
        end_date = datetime(end_year, 12, 31).strftime('%Y-%m-%d')
        news_summary = get_news_summary(company_name, start_date, end_date)
        
        # Apply CSS for responsive and justified content with pastel colors
        st.markdown(
            """
            <style>
            .news-container {
                display: flex;
                flex-direction: column;
                gap: 10px;
                text-align: justify;
            }
            .news-item {
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                color: #333;
            }
            .news-item:nth-of-type(1) {
                background-color: #E6E6FA; /* Lavender */
            }
            .news-item:nth-of-type(2) {
                background-color: #D3F9D8; /* Pastel Green */
            }
            .news-item:nth-of-type(3) {
                background-color: #B3E5FC; /* Pastel Blue */
            }
            </style>
            """, unsafe_allow_html=True
        )
        
        if news_summary:
            st.markdown('<div class="news-container">', unsafe_allow_html=True)
            news_items = news_summary.split("\n")
            for article in news_items[:3]:
                st.markdown(f'<div class="news-item">{article.strip()}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No news articles found for the selected period.")

    else:
        st.warning("Please enter a company name.")

if __name__ == "__main__":
    main()
