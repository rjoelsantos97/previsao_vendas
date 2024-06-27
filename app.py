import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import io
from datetime import datetime, date

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
    df = df[['ds', 'y']].sort_values('ds').set_index('ds')
    return df

def train_model_and_forecast(df, forecast_period):
    model = ExponentialSmoothing(df, seasonal_periods=12, trend='add', seasonal='add')
    fitted_model = model.fit()
    forecast = fitted_model.forecast(forecast_period)
    return fitted_model, forecast

def plot_forecast(df, forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['y'], mode='lines', name='Dados históricos'))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast, mode='lines', name='Previsão'))
    fig.update_layout(title='Previsão de Vendas', xaxis_title='Data', yaxis_title='Vendas')
    return fig

def main():
    st.title('Previsão de Vendas com Statsmodels')

    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            st.write("Primeiras linhas do dataset:")
            st.write(df.head())

            date_column = st.selectbox("Selecione a coluna de data", df.columns)
            target_column = st.selectbox("Selecione a coluna alvo (vendas)", df.columns)

            # Converter as datas para o formato correto
            df[date_column] = pd.to_datetime(df[date_column])
            min_date = df[date_column].min().date()
            max_date = df[date_column].max().date()

            start_date = st.date_input("Data de início para previsão", min_date)
            end_date = st.date_input("Data de fim para previsão", max_date)

            if start_date and end_date:
                if start_date > end_date:
                    st.error("A data de início deve ser anterior à data de fim.")
                else:
                    df_processed = preprocess_data(df, date_column, target_column)
                    forecast_period = (end_date - start_date).days

                    if st.button("Realizar Previsão"):
                        model, forecast = train_model_and_forecast(df_processed, forecast_period)

                        st.subheader("Gráfico de Previsão")
                        fig = plot_forecast(df_processed, forecast)
                        st.plotly_chart(fig)

                        st.subheader("Dados da Previsão")
                        st.write(forecast.tail())

                        csv = forecast.to_csv(index=True)
                        st.download_button(
                            label="Download da previsão como CSV",
                            data=csv,
                            file_name="previsao_vendas.csv",
                            mime="text/csv"
                        )

if __name__ == "__main__":
    main()
