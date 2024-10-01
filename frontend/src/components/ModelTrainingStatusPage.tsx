import React from 'react';
import ModelTrainingStatus from './ModelTrainingStatus';

const ModelTrainingStatusPage = () => {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="mb-8 text-4xl font-bold">Model Training Status</h1>
      <ModelTrainingStatus />
    </main>
  );
};

export default ModelTrainingStatusPage;