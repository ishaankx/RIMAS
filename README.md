# R.I.M.A.S. (Real-Time Intelligent Monitoring Advanced System)

R.I.M.A.S. is a desktop application designed to enhance productivity and focus by leveraging cutting-edge technologies like computer vision and machine learning. It tracks user activity, detects distractions, and provides real-time feedback and voice-based interactions, making it ideal for individuals with attention challenges or those aiming to improve their work habits.

---

## 🚀 **Features**

- **Real-Time Activity Monitoring:** Uses YOLOv8 and OpenCV to detect user behavior, such as phone usage and idle time.
- **Voice Feedback:** Provides productivity suggestions and reminders using speech recognition and Text-to-Speech (TTS).
- **Cross-Device Alerts:** Sends notifications to mobile devices when the desktop is idle.
- **Privacy Focused:** All data is processed locally, ensuring user privacy.

---

## 📋 **Requirements**

### **Software**
- **Operating System:** Windows 11 or higher
- **Python:** 3.8 or higher
- **Node.js:** 16 or higher
- **Frameworks & Libraries:**
   - PyTorch
   - OpenCV
   - YOLOv8
   - Text-to-Speech (TTS) library
   - SQLite

### **Hardware**
- **Camera:** A functional webcam
- **Memory:** Minimum 8GB RAM
- **Processor:** Intel i5 or higher

---

## 🛠️ **Installation**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/ishaankx/RIMAS.git
cd RIMAS
```

### **Step 2: Install Dependencies**
#### Backend (Python)
```bash
pip install -r requirements.txt
```
#### Frontend (Node.js and Tauri)
```bash
npm install
```

### **Step 3: Run the Application**
#### Backend (Python)
```bash
python src/backend.py
```
#### Frontend (Tauri)
```bash
npm start
```

### **Step 4: Access the Application**
Open your browser and navigate to:
```
http://localhost:3000
```

---

## 🤝 **Contributing**
Feel free to submit issues or pull requests to enhance the functionality of R.I.M.A.S.

---

## 📄 **License**
This project is licensed under the MIT License.

---

## ⚠️ **Troubleshooting**
If `npm run build` fails to minify, refer to the following documentation:
[https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

---

Happy Monitoring! 🎯
