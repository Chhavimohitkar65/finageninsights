import pandas as pd
from prophet import Prophet

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

def predict_trend(df, period, freq):
    df_prophet = df.reset_index().rename(columns={"index": "ds", "Close": "y"})
    
    model = Prophet(daily_seasonality=True)
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=period, freq=freq.lower())
    forecast = model.predict(future)

    fig = model.plot(forecast)
    return fig, forecast

    forecast['trend_diff'] = forecast['yhat'].diff()
    last_trend = forecast['trend_diff'].iloc[-1]
    
    if last_trend > 0:
        return "Up"
    elif last_trend < 0:
        return "Down"
    else:
        return "Neutral"
