import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './dashboard';
import Track from './track';
import Feedback from './feedback';
import axios from 'axios';

import './App.css';

const App = () => {
  const [alertMessage, setAlertMessage] = useState("");
  

  useEffect(() => {
    const startMonitoring = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:8000/start_monitoring/');
        console.log(response.data.status);
      } catch (error) {
        console.error("Error starting monitoring:", error);
      }
    };

    // Polling for alerts
    const fetchAlerts = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/get_alert/");
        setAlertMessage(response.data.alert || "");  // Update alert message
      } catch (error) {
        console.error("Error fetching alert:", error);
      }
    };

    startMonitoring();
    const interval = setInterval(fetchAlerts, 5000);

    return () => clearInterval(interval);
  }, []);

  // Send user response
  const sendResponse = async (label, timeInSeconds) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/receive_response/", {
        label: label,
        time_in_seconds: timeInSeconds,
      });
      console.log(response.data.status);
    } catch (error) {
      console.error("Error sending response:", error);
    }
  };

  return (
    <Router>
      <div>
        {alertMessage && (
          <div className="alert-message">
            {alertMessage}
            <button onClick={() => sendResponse("phone", 120)}>Respond</button>
          </div>
        )}
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/track" element={<Track />} />
          <Route path="/feedback" element={<Feedback />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App; 
