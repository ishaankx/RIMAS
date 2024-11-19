import React, { useState, useEffect } from 'react';
import { jsPDF } from 'jspdf';
import Header from './header'; // Import the shared Header component
import './feedback.css';

const Feedback = () => {
  const [activeTab, setActiveTab] = useState('feedback');
  const [displayedText, setDisplayedText] = useState(''); // Text that appears with typing effect
  const exampleText = `Activity Report for Today

  On-Call: 2 hours  
  Using Phone: 3 hours  
  Away from Desk: 1.5 hours  
  Idle: 2 hours  
  
  Analysis:
  
  - **On-Call (2 hours)**: While being on calls is important for communication, prolonged calls without productive outcomes can drain energy and reduce focus. It's important to evaluate the efficiency of these calls to ensure they contribute to your goals.  
  - **Using Phone (3 hours)**: Excessive phone usage, especially for social media or entertainment, can negatively affect focus and productivity. The constant switching between tasks leads to cognitive overload, making it harder to stay on task.  
  - **Away from Desk (1.5 hours)**: Time away from the desk can be necessary for breaks, but long periods spent away from productive tasks can cause delays in project completion and a lack of focus.  
  - **Idle (2 hours)**: Idle time suggests that you were not actively engaging with tasks. While rest is important, excessive idle time can lead to unproductive hours that could be better spent on focused work.  
  
  Overall Impact on Productivity:  
  Your total "unfocused" time today was 8.5 hours, which is a significant portion of the day. This indicates a large amount of wasted potential time, which could have been used more effectively for task completion and goal achievement.  
  
  Tips for Boosting Productivity:  
  
  1. **Set Specific Time Limits**: Try setting time limits for activities like phone use or on-call meetings. Use apps that track screen time and alert you when you’ve hit your daily limit.  
  2. **Prioritize Tasks**: Identify key tasks for the day and ensure that you're not spending too much time on activities that aren’t directly aligned with your goals.  
  3. **Time Blocking**: Schedule specific blocks of time for focused work, and avoid distractions during those periods. Block off time for breaks and relaxation, but ensure you’re not away from work for long stretches.  
  4. **Use the Pomodoro Technique**: Break your work into intervals of 25 minutes, followed by a 5-minute break. This helps maintain focus while still providing regular rest.  
  5. **Minimize Idle Time**: Whenever you feel yourself drifting into idle time, remind yourself to take action – whether it’s a small task, a quick check-in on goals, or even a short burst of exercise.  
  
  By aligning your activities with these tips, you can reduce unproductive time and increase your overall effectiveness throughout the day.`;
  

  useEffect(() => {
    let index = 0;

    const typingInterval = setInterval(() => {
      if (index < exampleText.length) {
        setDisplayedText((prev) => prev + exampleText[index]);
        index++;
      } else {
        clearInterval(typingInterval);
      }
    }, 10); // Adjust typing speed in milliseconds

    return () => clearInterval(typingInterval); // Cleanup on unmount
  }, []);

  // Function to download the text content as a PDF
  const downloadReport = () => {
    const doc = new jsPDF({
      format: 'a4', // Set A4 paper size
      unit: 'mm',   // Use millimeters as the unit
    });
  
    const margin = 15; // Margin from the edges
    const pageWidth = doc.internal.pageSize.getWidth(); // Get page width
    const usableWidth = pageWidth - margin * 2; // Usable width inside margins
  
    const fontSize = 12; // Font size for the document
    doc.setFontSize(fontSize);
    doc.setFont('Times', 'normal');
  
    // Split text into lines that fit within the usable width
    const lines = doc.splitTextToSize(displayedText, usableWidth);
  
    let cursorY = margin; // Start text at the top margin
  
    lines.forEach((line, index) => {
      if (cursorY + fontSize > doc.internal.pageSize.getHeight() - margin) {
        // Add a new page when nearing the bottom margin
        doc.addPage();
        cursorY = margin; // Reset cursor to the top margin
      }
      doc.text(line, margin, cursorY); // Write text line by line
      cursorY += fontSize * 1.2; // Increment Y position (line height = font size * 1.2)
    });
  
    // Save the generated PDF
    doc.save('report.pdf');
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
