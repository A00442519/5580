import pandas as pd
import streamlit as st
import requests

st.header('Bitcoin Price Tracker')

days = st.slider('No of days', 1, 365)
currency = st.radio('Currency', ('🇨🇦 CAD', '🇺🇸 USD', '🇪🇺 EUR','🇮🇳 INR'))

payload = {'vs_currency': currency.split(' ')[-1], 'days': days, 'interval': 'daily'}
req = requests.get(
    'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart', params=payload)

if req.status_code == 200:
    r = req.json()
else:
    st.write(req.status_code)

df = pd.DataFrame(r['prices'], columns=['Date', currency])
df['Date'] = pd.to_datetime(df['Date'], unit='ms')
df = df.set_index('Date')
mean_price = df[currency].mean()

st.line_chart(df[currency])
st.write('Average Price during the last {} days time was  {} {:,.2f}'.format(
    days, currency, mean_price))
st.subheader('Assignment by Mayuresh Sawant (A00442519)')
