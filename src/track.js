import React, { useState } from 'react';
import Header from './header'; // Import the shared Header component
import './track.css';
import { Bar } from 'react-chartjs-2'; // Assuming you're using Chart.js
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Track = () => {
  const [activeTab, setActiveTab] = useState('track');
  const [selectedOption, setSelectedOption] = useState('Track Options');
  const [dropdownVisible, setDropdownVisible] = useState(false);

  // Dummy data for each option
  const data = {
    'Screen Time': {
      labels: ['Social Media', 'Work', 'Entertainment', 'Other'],
      datasets: [
        {
          label: 'Time Spent (hours)',
          data: [2, 7, 3, 1],
          backgroundColor: ['blue', 'red', 'cyan', 'yellow'],
        },
      ],
    },
    Away: {
      labels: ['Lunch', 'Break', 'Meeting'],
      datasets: [
        {
          label: 'Time Spent (hours)',
          data: [1, 1, 2],
          backgroundColor: ['orange', 'green', 'purple'],
        },
      ],
    },
    Productivity: {
      labels: ['Coding', 'Design', 'Testing', 'Studying'],
      datasets: [
        {
          label: 'Time Spent (hours)',
          data: [3, 3, 4, 2],
          backgroundColor: ['#FF5733', '#33FF57', '#5733FF', 'pink'],
        },
      ],
    },
    Unfocused: {
      labels: ['Browsing', 'Idle'],
      datasets: [
        {
          label: 'Time Spent (hours)',
          data: [4, 2],
          backgroundColor: ['#FFC300', '#C70039'],
        },
      ],
    },
  };

  const [graphData, setGraphData] = useState(null);

  const handleOptionClick = (option) => {
    setSelectedOption(option);
    setGraphData(data[option]);
    setDropdownVisible(false);
  };

  return (
    <div className="track-container">
      {/* Fixed Header */}
      <div className="header-container">
        <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      </div>

      {/* Dropdown menu */}
      <div className={`dropdown-container ${graphData ? 'dropdown-active' : ''}`}>
        <button className={`dropdown-button ${dropdownVisible ? 'dropdown-active' : ''}`} onClick={() => setDropdownVisible(!dropdownVisible)}>
          {selectedOption}
        </button>
        {dropdownVisible && (
          <div className="dropdown-content">
            {Object.keys(data).map((option) => (
              <div
                key={option}
                className={`dropdown-item ${selectedOption === option ? 'dropdown-active' : ''}`}
                onClick={() => handleOptionClick(option)}
              >
                {option}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Graphical and statistical representation */}
      {graphData && (
        <div className="graph-container">
          <h2>{selectedOption}</h2>
          <div className="statistics">Total Time Spent: {graphData.datasets[0].data.reduce((a, b) => a + b, 0)} hours</div>
          <Bar data={graphData} options={{ responsive: true, maintainAspectRatio: false }} />
          
        </div>
      )}
    </div>
  );
};

export default Track;
