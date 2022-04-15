import pandas as pd
import streamlit as st
import requests
from currency_converter import CurrencyConverter

converter = CurrencyConverter(fallback_on_missing_rate=True,
                              fallback_on_wrong_date=True)
st.header('Bitcoin Price Tracker')
days = st.slider('No of days', 1, 365)
currency = st.radio('Currency', ('CAD', 'USD', 'EUR','INR'))
payload = {'vs_currency': currency, 'days': days, 'interval': 'daily'}
req = requests.get(
    'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart', params=payload)
if req.status_code == 200:
    r = req.json()
df = pd.DataFrame(r['prices'], columns=['date', currency])
df['date'] = pd.to_datetime(df['date'],unit='ms')
df = df.tail(days)
if currency == 'USD':
    df[currency] = df.apply(lambda row: converter.convert(row[currency], 'CAD', 'USD', date=row["date"]), axis=1)
elif currency=='EUR':
    df[currency] = df.apply(lambda row: converter.convert(row[currency], 'CAD', 'EUR', date=row["date"]), axis=1)
elif currency=='INR':
    df[currency] = df.apply(lambda row: converter.convert(row[currency], 'CAD', 'INR', date=row["date"]), axis=1)
df = df.set_index('date')
mean_price = df[currency].mean()
st.line_chart(df[currency])
st.write('Average Price during this time was  {} {:.2f}'.format(currency, mean_price))
st.subheader('Assignment by Mayuresh Sawant (A00442519)')
