from fastapi import FastAPI, BackgroundTasks
import cv2
import time
import pyttsx3
import ctypes
from ultralytics import YOLO
import speech_recognition as sr
import threading

# Initialize FastAPI app and YOLO model
app = FastAPI()
model = YOLO('F:/rimas/rimas/runs/detect/train/weights/best.pt')

# Initialize TTS engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()
monitoring_active = False  # Flag to control monitoring

class_labels = ['away', 'focused', 'idle', 'oncall', 'phone', 'using-phone']
timers = {label: 0 for label in class_labels}


# Utility functions for TTS and volume control
def set_system_volume_to_max():
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x319, 0, 0x5000)  # Windows-specific


def voice_command(message):
    engine.say(message)
    engine.runAndWait()



recognizer = sr.Recognizer()

timers = {
    'focused': 0,
    'away': 0,
    'idle': 0,
    'oncall': 0,
    'phone': 0,
    'using-phone': 0
}

# Global flag to control monitoring
monitoring_paused = False
def get_reason_and_time(label):
    global monitoring_paused
    with sr.Microphone() as source:
        print("Listening for reason and time... Please state your reason and time (in seconds)...")
        try:
            audio = recognizer.listen(source, timeout=10)  # Set 10-second timeout for response
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

            # Extract the time in seconds from the spoken text
            if "minute" in text:
                time_in_seconds = int([int(s) for s in text.split() if s.isdigit()][0]) * 60
            elif "second" in text:
                time_in_seconds = int([int(s) for s in text.split() if s.isdigit()][0])
            else:
                time_in_seconds = 60  # Default to 60 seconds if no time is mentioned

            timers[label] = time.time() + time_in_seconds
            print(f"Monitoring will resume after {time_in_seconds} seconds.")
            monitoring_paused = True
            time.sleep(time_in_seconds)  # Pause for the user-defined time
        except sr.WaitTimeoutError:
            print("User did not respond within 10 seconds. Resuming monitoring.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            monitoring_paused = False
    # with sr.Microphone() as source:
    #     print("Listening for reason and time...")
    #     try:
    #         audio = recognizer.listen(source, timeout=10)
    #         text = recognizer.recognize_google(audio)
    #         if "minute" in text:
    #             timers[label] = time.time() + int([int(s) for s in text.split() if s.isdigit()][0]) * 60
    #         elif "second" in text:
    #             timers[label] = time.time() + int([int(s) for s in text.split() if s.isdigit()][0])
    #         else:
    #             timers[label] = time.time() + 60  # Default to 60 seconds
    #     except sr.WaitTimeoutError:
    #         print("No response detected. Continuing monitoring.")


# Monitoring function
def monitor():
    global monitoring_active
    monitoring_active = True
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while monitoring_active:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO model inference
        results = model(frame, conf=0.5)
        annotated_frame = results[0].plot()

        for result in results[0].boxes:
            label = class_labels[int(result.cls[0])]
            if timers[label] > time.time():
                continue
            if label in ["away", "using-phone"]:
                voice_command(f"Please provide a reason, you are detected as {label}")
                threading.Thread(target=get_reason_and_time, args=(label,)).start()

        cv2.imshow("YOLO Monitoring", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    monitoring_active = False


# API endpoint to start monitoring
@app.post("/start_monitoring/")
async def start_monitoring(background_tasks: BackgroundTasks):
    if not monitoring_active:
        background_tasks.add_task(monitor)
        return {"status": "Monitoring started"}
    return {"status": "Monitoring already active"}


# API endpoint to stop monitoring
@app.post("/stop_monitoring/")
async def stop_monitoring():
    global monitoring_active
    monitoring_active = False
    return {"status": "Monitoring stopped"}
