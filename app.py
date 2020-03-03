import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('King County House Sales in 2014')

def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/bmcgarry194/knn_workshop/master/data/kc-house-data.zip")

    data = df.rename(columns={'long': 'lon'})
    data['month_sold'] = pd.to_datetime(data['date']).dt.month
    return data

data = load_data()

multi = st.multiselect("Zipcodes", list(data['zipcode'].unique()), default=list(data['zipcode'].unique()))

min_price = data['price'].min()
max_price = data['price'].max()
low, high = st.sidebar.slider('Price Range', min_value=int(min_price), max_value=int(max_price), value=(int(min_price), int(max_price)))

month_data = data.loc[(data['price'] >= low) &
                         (data['price'] <= high) &
                         (data['zipcode'].isin(multi)), :]

st.deck_gl_chart(viewport={'latitude': 47.6062,
                           'longitude': -122.3321,
                           'zoom': 10,},
                layers=[{'type': 'ScatterplotLayer',
                         'data': month_data,
                         'opacity': .5,
                         'radiusScale': .2}])

st.sidebar.subheader('Histogram of House Prices')
hist_values = np.histogram(month_data['price'], bins=24)[0]
st.sidebar.bar_chart(hist_values)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(month_data)
