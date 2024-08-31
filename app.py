import streamlit as st
import openai
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API client
class OpenAIClient:
    def __init__(self):
        self.api_key = st.secrets["OPENAI_API_KEY"]
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

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'], utc=True)
    return data

def filter_data_by_company(data, company_name):
    return data[data['Company'].str.contains(company_name, case=False, na=False)]

def filter_data_by_years(data, start_year, end_year):
    data['Year'] = data['Date'].dt.year
    return data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

# ... (rest of the functions remain the same)

def main():
    st.title("FinAgent Insight")

    file_path = "updated_file.csv"
    data = load_data(file_path)

    company_name = st.text_input("Company Name:")

    if company_name:
        company_data = filter_data_by_company(data, company_name)

        if company_data.empty:
            st.warning(f"No data found for {company_name}. Please check the company name and try again.")
        else:
            st.subheader("Company Overview")
            display_metrics(company_data)

            st.subheader("Stock Trend")
            min_year = company_data['Date'].dt.year.min()
            max_year = company_data['Date'].dt.year.max()
            start_year, end_year = st.slider(
                "Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year)
            )

            filtered_data = filter_data_by_years(company_data, start_year, end_year)
            st.line_chart(filtered_data.set_index('Date')['Close'])

            # ... (rest of the main function remains the same)

if __name__ == "__main__":
    main()
