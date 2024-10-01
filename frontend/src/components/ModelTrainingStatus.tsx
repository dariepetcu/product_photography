import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from "src/components/ui/card";
import { Loader2, CheckCircle, XCircle, Clock } from "lucide-react";

const ModelTrainingStatus = () => {
  const [status, setStatus] = useState('processing');
  const { model_name } = useParams();

  useEffect(() => {
    const fetchStatus = async () => {
      if (model_name) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/training/status/${model_name}`);
          if (!response.ok) {
            throw new Error('Failed to fetch status');
          }
          const data = await response.json();
          setStatus(data.status);
        } catch (error) {
          console.error('Error fetching status:', error);
          setStatus('failed');
        }
      }
    };

    const intervalId = setInterval(fetchStatus, 5000); // Poll every 5 seconds

    return () => clearInterval(intervalId); // Clean up on unmount
  }, [model_name]);

  const renderStatusIcon = () => {
    switch (status) {
      case 'processing':
        return <Loader2 className="h-16 w-16 animate-spin text-blue-500" />;
      case 'succeeded':
        return <CheckCircle className="h-16 w-16 text-green-500" />;
      case 'failed':
        return <XCircle className="h-16 w-16 text-red-500" />;
      case 'queued':
        return <Clock className="h-16 w-16 text-yellow-500" />;
      default:
        return null;
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Model Training Status</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center">
        {renderStatusIcon()}
        <p className="mt-4 text-lg font-semibold">{status.charAt(0).toUpperCase() + status.slice(1)}</p>
      </CardContent>
    </Card>
  );
};

export default ModelTrainingStatus;