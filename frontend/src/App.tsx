import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ModelTrainingForm from './components/ModelTrainingForm';
import ModelTrainingStatusPage from './components/ModelTrainingStatusPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ModelTrainingForm />} />
        <Route path="/model-training-status/:model_name" element={<ModelTrainingStatusPage />} />
      </Routes>
    </Router>
  );
}

export default App;