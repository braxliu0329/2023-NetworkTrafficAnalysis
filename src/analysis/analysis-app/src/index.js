import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Import your global styles
import App from './App'; // Import your root component
import reportWebVitals from './reportWebVitals'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();

