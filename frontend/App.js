import React, { useState } from 'react';

// Importe os componentes necessários do shadcn/ui
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';

// Importe os componentes necessários do recharts
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Substitua esta URL pela URL real do seu backend no Render
const API_URL = 'https://sales-prediction-backend.onrender.com';

const SalesPredictionApp = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [predictions, setPredictions] = useState([]);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handlePredict = async () => {
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start_date: startDate, end_date: endDate }),
      });
      const data = await response.json();
      if (response.ok) {
        setPredictions(data.predictions);
      } else {
        setMessage(data.error || 'Erro ao fazer previsão');
      }
    } catch (error) {
      setMessage('Erro ao conectar com o servidor');
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Por favor, selecione um arquivo');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(`Modelo treinado com sucesso. MSE: ${data.mse}`);
      } else {
        setMessage(data.error || 'Erro ao treinar modelo');
      }
    } catch (error) {
      setMessage('Erro ao conectar com o servidor');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card className="w-full max-w-4xl mx-auto">
        <CardHeader>
          <h2 className="text-2xl font-bold">Previsão de Vendas</h2>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <Input type="file" onChange={handleFileChange} accept=".csv" />
              <Button onClick={handleUpload} className="mt-2 w-full">
                Enviar Arquivo e Treinar Modelo
              </Button>
            </div>
            <div className="flex space-x-2">
              <Input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                placeholder="Data Inicial"
              />
              <Input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                placeholder="Data Final"
              />
            </div>
            <Button onClick={handlePredict} className="w-full">
              Prever Vendas
            </Button>
            {predictions.length > 0 && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold">Previsões de Vendas:</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={predictions}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="prediction" stroke="#8884d8" activeDot={{ r: 8 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
            {message && (
              <Alert>
                <AlertDescription>{message}</AlertDescription>
              </Alert>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SalesPredictionApp;
