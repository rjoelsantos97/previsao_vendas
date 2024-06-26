from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime
import joblib

app = Flask(__name__)

model = None
scaler = None

def train_model(data):
    global model, scaler
    
    # Converter datas para formato datetime
    data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%y')

    # Extrair características das datas
    data['DayOfWeek'] = data['Date'].dt.dayofweek
    data['DayOfMonth'] = data['Date'].dt.day
    data['Month'] = data['Date'].dt.month

    # Preparar features e target
    X = data[['DayOfWeek', 'DayOfMonth', 'Month']]
    y = data['Valor']

    # Dividir dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalizar os dados
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Criar e treinar o modelo
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Avaliar o modelo
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    
    return mse

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        # Ler o arquivo CSV
        data = pd.read_csv(file, parse_dates=['Date'])
        
        # Treinar o modelo
        mse = train_model(data)
        
        return jsonify({'message': 'Model trained successfully', 'mse': mse}), 200

@app.route('/predict', methods=['POST'])
def predict():
    global model, scaler
    if model is None or scaler is None:
        return jsonify({'error': 'Model not trained'}), 400
    
    date = request.json['date']
    date = pd.to_datetime(date)
    features = np.array([[date.dayofweek, date.day, date.month]])
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)
    
    return jsonify({'prediction': prediction[0]}), 200

if __name__ == '__main__':
    app.run(debug=True)
