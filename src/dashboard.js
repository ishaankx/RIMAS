import React, { useState } from 'react';
import Header from './header'; // Import the new Header component
import logo from './rimasLogo.png'; 
import './dashboard.css'; 


const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('rimas'); // Default to 'rimas'

  return (
    <div className="dashboard-container">
      {/* Header with navigation buttons */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main content */}
      <div className="content">
        <div className="App-logo">
          <img src={logo} alt="Logo" />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;




