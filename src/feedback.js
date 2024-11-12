import React, { useState } from 'react';
import Header from './header'; // Import the shared Header component
import './feedback.css';

const Feedback = () => {
  const [activeTab, setActiveTab] = useState('feedback');

  return (
    <div className="feedback-container">
      {/* Header with navigation buttons */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Feedback content */}
      <div className="content">
        <h1>Daily Report</h1> {/* Centered heading */}
        <div className="feedback-box">
          <textarea placeholder="Enter your feedback here..."></textarea>
          <button className="download-btn">Download Report</button>
        </div>
      </div>
    </div>
  );
};

export default Feedback;
