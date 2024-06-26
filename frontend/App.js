import React, { useState } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_URL = 'https://sales-prediction-backend.onrender.com'; // Substitua pela URL do seu backend no Render

const SalesPredictionApp = () => {
  // ... (resto do código permanece o mesmo)

  const handlePredict = async () => {
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start_date: startDate, end_date: endDate }),
      });
      // ... (resto do código permanece o mesmo)
    } catch (error) {
      setMessage('Erro ao conectar com o servidor');
    }
  };

  const handleUpload = async () => {
    // ... (código anterior)
    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      // ... (resto do código permanece o mesmo)
    } catch (error) {
      setMessage('Erro ao conectar com o servidor');
    }
  };

  // ... (resto do componente permanece o mesmo)
};

export default SalesPredictionApp;
