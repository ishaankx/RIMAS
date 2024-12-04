R.I.M.A.S. (Real-Time Intelligent Monitoring Advanced System)
R.I.M.A.S. is a desktop application designed to enhance productivity and focus by leveraging cutting-edge technologies like computer vision and machine learning. It tracks user activity, detects distractions, and provides real-time feedback and voice-based interactions, making it ideal for individuals with attention challenges or those aiming to improve their work habits.

Features
Real-Time Activity Monitoring: Uses YOLOv8 and OpenCV to detect user behavior such as phone usage and idle time.
Voice Feedback: Provides productivity suggestions and reminders using speech recognition and TTS.
Cross-Device Alerts: Sends notifications to mobile devices when the desktop is idle.
Privacy Focused: All data is processed locally, ensuring user privacy.
Requirements
Software
Operating System: Windows 11 or higher
Python: 3.8 or higher
Node.js: 16 or higher
Frameworks & Libraries:
PyTorch
OpenCV
YOLOv8
Text-to-Speech (TTS) library
SQLite
Hardware
Camera: A functional webcam
Memory: Minimum 8GB RAM
Processor: Intel i5 or higher
Installation
Step 1: Clone the Repository
bash
Copy code
git clone https://github.com/ishaankx/RIMAS.git
cd RIMAS
Step 2: Install Dependencies
bash
Copy code
# For backend (Python)
pip install -r requirements.txt

# For frontend (Node.js and Tauri)
npm install
Step 3: Run the Application
Backend (Python)
bash
Copy code
python src/backend.py
Frontend (Tauri)
bash
Copy code
npm start
Step 4: Access the Application
Open http://localhost:3000 in your browser to interact with the R.I.M.A.S. interface.

Contributing
Feel free to submit issues or pull requests to enhance the functionality of R.I.M.A.S.

License
This project is licensed under the MIT License.

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
