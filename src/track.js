import React, { useState } from 'react';
import Header from './header'; // Import the shared Header component
import './track.css';

const Track = () => {
  const [activeTab, setActiveTab] = useState('track');
  const [selectedOption, setSelectedOption] = useState('Track Options'); // Default text for the button
  const [dropdownVisible, setDropdownVisible] = useState(false); // Track dropdown visibility

  // Handle selection of dropdown options
  const handleOptionClick = (option) => {
    setSelectedOption(option); // Update selected option
    setDropdownVisible(false); // Hide the dropdown menu
  };

  // Toggle dropdown visibility
  const toggleDropdown = () => {
    setDropdownVisible(!dropdownVisible);
  };

  return (
    <div className="track-container">
      {/* Header with navigation buttons */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Dropdown menu */}
      <div className="dropdown-container">
        <button className="dropdown-button" onClick={toggleDropdown}>
          {selectedOption}
        </button>
        {dropdownVisible && (
          <div className="dropdown-content">
            <div
              className={`dropdown-item ${selectedOption === 'Screen Time' ? 'dropdown-active' : ''}`}
              onClick={() => handleOptionClick('Screen Time')}
            >
              Screen Time
            </div>
            <div
              className={`dropdown-item ${selectedOption === 'Away' ? 'dropdown-active' : ''}`}
              onClick={() => handleOptionClick('Away')}
            >
              Away
            </div>
            <div
              className={`dropdown-item ${selectedOption === 'Productivity' ? 'dropdown-active' : ''}`}
              onClick={() => handleOptionClick('Productivity')}
            >
              Productivity
            </div>
            <div
              className={`dropdown-item ${selectedOption === 'Unfocused' ? 'dropdown-active' : ''}`}
              onClick={() => handleOptionClick('Unfocused')}
            >
              Unfocused
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Track;
