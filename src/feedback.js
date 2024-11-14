import React, { useState, useEffect } from 'react';
import { jsPDF } from 'jspdf';
import Header from './header'; // Import the shared Header component
import './feedback.css';

const Feedback = () => {
  const [activeTab, setActiveTab] = useState('feedback');
  const [displayedText, setDisplayedText] = useState(''); // Text that appears with typing effect
  const exampleText = "This is an example of a report. Here are the details:\n- User engagement is high.\n- Productivity has improved.\n- Focus duration is consistent.\n";

  useEffect(() => {
    let index = 0;

    const typingInterval = setInterval(() => {
      if (index < exampleText.length) {
        setDisplayedText((prev) => prev + exampleText[index]);
        index++;
      } else {
        clearInterval(typingInterval);
      }
    }, 70); // Adjust typing speed in milliseconds

    return () => clearInterval(typingInterval); // Cleanup on unmount
  }, []);

  // Function to download the text content as a PDF
  const downloadReport = () => {
    const doc = new jsPDF();
    doc.setFontSize(12);
    doc.setFont("Times New Roman");
    doc.text(displayedText, 10, 10); // Add the text content at position (10, 10)
    doc.save("report.pdf"); // Save the generated PDF with a file name
  };

  return (
    <div className="feedback-container">
      {/* Header with navigation buttons */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Feedback content */}
      <div className="content">
        <h1>Daily Report</h1> {/* Centered heading */}
        <div className="feedback-box">
          <textarea 
            placeholder="Enter your feedback here..." 
            value={displayedText} 
            readOnly // Makes the text area read-only to show generated text
          />
          <button className="download-btn" onClick={downloadReport}>Download Report</button>
        </div>
      </div>
    </div>
  );
};

export default Feedback;
