import streamlit as st
import pandas as pd
from prophet.forecaster import Prophet
import base64
import io

st.title('Time Series Forecasting with Prophet')

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)
    
    st.write("Data Preview:")
    st.write(data.head())
    
    columns = data.columns
    target_column = st.selectbox("Select the target column for prediction", columns)
    date_column = st.selectbox("Select the date column", columns)
    
    if st.button('Train Model'):
        df = data[[date_column, target_column]].rename(columns={date_column: 'ds', target_column: 'y'})
        
        model = Prophet()
        model.fit(df)
        
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)
        
        st.write("Forecast Data:")
        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        
        fig = model.plot(forecast)
        st.pyplot(fig)
        
        # Provide download link for forecast
        csv = forecast.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        href = f'<a href="data:file/csv;base64,{b64}" download="forecast.csv">Download Forecast CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
