import plotly.graph_objs as go
import streamlit as st

def plot_stock_data(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=f'Close Price of {symbol}', line=dict(color='cyan')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Open'], mode='lines', name=f'Open Price of {symbol}', line=dict(color='green')))
    fig.update_layout(
        title=f'Stock Price of {symbol} Over Time',
        xaxis_title='Date',
        yaxis_title='Price',
        hovermode='x',
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig)
