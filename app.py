import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
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

def train_model_and_forecast(df, forecast_period, trend, seasonal, seasonal_periods):
    model = ExponentialSmoothing(df, seasonal_periods=seasonal_periods, trend=trend, seasonal=seasonal)
    fitted_model = model.fit()
    forecast = fitted_model.forecast(forecast_period)
    return fitted_model, forecast

def plot_forecast(df, forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['y'], mode='lines', name='Dados históricos'))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast, mode='lines', name='Previsão'))
    fig.update_layout(title='Previsão de Vendas', xaxis_title='Data', yaxis_title='Vendas')
    return fig

def plot_seasonality(df):
    df['month'] = df.index.month
    seasonality = df.groupby('month')['y'].mean()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=seasonality.index, y=seasonality.values))
    fig.update_layout(title='Sazonalidade Média por Mês', xaxis_title='Mês', yaxis_title='Vendas Médias')
    return fig

def plot_trend(df):
    df['year'] = df.index.year
    trend = df.groupby('year')['y'].mean()
    fig = go.Figure()
    fig.add_trace(go.Line(x=trend.index, y=trend.values))
    fig.update_layout(title='Tendência Média por Ano', xaxis_title='Ano', yaxis_title='Vendas Médias')
    return fig

def main():
    st.title('Previsão de Vendas com Statsmodels')

    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        with st.spinner('Carregando dados...'):
            df = load_data(uploaded_file)
        
        if df is not None:
            st.write("Primeiras linhas do dataset:")
            st.write(df.head())
            
            date_column = st.selectbox("Selecione a coluna de data", df.columns)
            target_column = st.selectbox("Selecione a coluna alvo (vendas)", df.columns)

            df[date_column] = pd.to_datetime(df[date_column])
            min_date = df[date_column].min().date()
            max_date = df[date_column].max().date()

            st.subheader("Resumo Estatístico")
            st.write(df.describe())

            st.subheader("Análise de Correlação")
            corr_matrix = df.corr()
            st.write(corr_matrix)

            start_date = st.date_input("Data de início para previsão", min_date)
            end_date = st.date_input("Data de fim para previsão", max_date)

            trend = st.selectbox("Selecione o tipo de tendência", ['add', 'mul', 'additive', 'multiplicative', None])
            seasonal = st.selectbox("Selecione o tipo de sazonalidade", ['add', 'mul', 'additive', 'multiplicative', None])
            seasonal_periods = st.slider("Selecione o número de períodos sazonais", 1, 24, 12)

            if start_date and end_date:
                if start_date > end_date:
                    st.error("A data de início deve ser anterior à data de fim.")
                else:
                    df_processed = preprocess_data(df, date_column, target_column)
                    forecast_period = (end_date - start_date).days

                    st.subheader("Análise de Tendências e Sazonalidades")
                    st.plotly_chart(plot_seasonality(df_processed))
                    st.plotly_chart(plot_trend(df_processed))

                    if st.button("Realizar Previsão"):
                        with st.spinner('Treinando modelo e gerando previsão...'):
                            try:
                                model, forecast = train_model_and_forecast(df_processed, forecast_period, trend, seasonal, seasonal_periods)
                                st.success('Previsão realizada com sucesso!')

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
                            except Exception as e:
                                st.error(f"Ocorreu um erro ao realizar a previsão: {e}")

if __name__ == "__main__":
    main()
