import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go
import io

# Substituir np.float_ por np.float64
np.float_ = np.float64

def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            st.error("Formato de arquivo não suportado. Por favor, use CSV ou Excel.")
            return None
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

def preprocess_data(df, date_column, target_column):
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.rename(columns={date_column: 'ds', target_column: 'y'})
    df = df[['ds', 'y']].sort_values('ds')
    return df

def train_model(df, forecast_period):
    model = Prophet()
    model.fit(df)
    future_dates = model.make_future_dataframe(periods=forecast_period)
    forecast = model.predict(future_dates)
    return model, forecast

def main():
    st.title('Previsão de Vendas com Prophet')

    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            st.write("Primeiras linhas do dataset:")
            st.write(df.head())

            date_column = st.selectbox("Selecione a coluna de data", df.columns)
            target_column = st.selectbox("Selecione a coluna alvo (vendas)", df.columns)

            start_date = st.date_input("Data de início para previsão", df[date_column].min())
            end_date = st.date_input("Data de fim para previsão", df[date_column].max())

            if start_date and end_date:
                if start_date > end_date:
                    st.error("A data de início deve ser anterior à data de fim.")
                else:
                    df_processed = preprocess_data(df, date_column, target_column)
                    df_forecast = df_processed[(df_processed['ds'].dt.date >= start_date) & (df_processed['ds'].dt.date <= end_date)]

                    forecast_period = (end_date - start_date).days

                    if st.button("Realizar Previsão"):
                        model, forecast = train_model(df_processed, forecast_period)

                        st.subheader("Gráfico de Previsão")
                        fig = plot_plotly(model, forecast)
                        st.plotly_chart(fig)

                        st.subheader("Dados da Previsão")
                        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

                        csv = forecast.to_csv(index=False)
                        st.download_button(
                            label="Download da previsão como CSV",
                            data=csv,
                            file_name="previsao_vendas.csv",
                            mime="text/csv"
                        )

if __name__ == "__main__":
    main()
