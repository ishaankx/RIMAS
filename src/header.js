// Header.js
import React from 'react';
import { Link } from 'react-router-dom';
import './header.css'; // Add your styles
import '@fortawesome/fontawesome-free/css/all.min.css';


const Header = ({ activeTab, setActiveTab }) => {
  const handleTabClick = (tabName) => {
    setActiveTab(tabName); // Set the active tab
  };

  return (
    <div className="header">
      <div className="tab-container">
        <Link to="/">
          <button
            className={`tab ${activeTab === 'rimas' ? 'tab-active' : ''}`}
            onClick={() => handleTabClick('rimas')}
          >
            R.I.M.A.S
          </button>
        </Link>
        <Link to="/track">
          <button
            className={`tab ${activeTab === 'track' ? 'tab-active' : ''}`}
            onClick={() => handleTabClick('track')}
          >
            Track
          </button>
        </Link>
        <Link to="/feedback">
          <button
            className={`tab ${activeTab === 'feedback' ? 'tab-active' : ''}`}
            onClick={() => handleTabClick('feedback')}
          >
            Feedback
          </button>
        </Link>
      </div>
      <div className="profile-icon">
        <i className="fas fa-user" style={{ fontSize: '24px' }}></i>
      </div>
    </div>
  );
};

export default Header;
