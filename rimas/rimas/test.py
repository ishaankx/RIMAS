import cv2
import time
import pyttsx3
import ctypes
from ultralytics import YOLO
import speech_recognition as sr
import threading

# Initialize Text-to-Speech engine
engine = pyttsx3.init()


# Function to set system volume to max
def set_system_volume_to_max():
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x319, 0, 0x5000)  # For Windows


# Function to give voice feedback
def voice_command(message):
    engine.say(message)
    engine.runAndWait()


# Initialize speech recognizer
recognizer = sr.Recognizer()


# Function to capture user's reason and time for delay using speech-to-text (in a separate thread)
def get_reason_and_time(timers, label):
    with sr.Microphone() as source:
        print("Listening for reason and time... Please state your reason and time (in seconds)...")
        audio = recognizer.listen(source)
        try:
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
        except:
            print("Sorry, I could not understand the command.")
            timers[label] = time.time() + 60  # Default delay to 60 seconds if recognition fails


# Function to handle speech recognition in a separate thread
def listen_for_reason(timers, label):
    listen_thread = threading.Thread(target=get_reason_and_time, args=(timers, label))
    listen_thread.start()


# Load the trained YOLOv8 model
model = YOLO('runs/detect/train/weights/best.pt')  # Path to your trained model's weights

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set FPS and frame interval
desired_fps = 5
frame_interval = int(1 / desired_fps * 1000)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Starting video capture...")

# Define labels for your custom classes
class_labels = ['away', 'focused', 'idle', 'oncall', 'phone', 'using-phone']
user_name = "Ishaan"  # Replace with actual user's name

# Timers for each category
timers = {
    'focused': 0,
    'away': 0,
    'idle': 0,
    'oncall': 0,
    'phone': 0,
    'using-phone': 0
}

while True:
    start_time = time.time()

    # Capture frame-by-frame from webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: Unable to read from webcam.")
        break

    # Run the YOLO model on the captured frame
    results = model(frame, conf=0.5)  # Adjust confidence threshold as needed

    # Process and annotate the results
    annotated_frame = results[0].plot()  # Annotate the frame with bounding boxes

    # Extract predicted class and confidence
    for result in results[0].boxes:
        class_id = int(result.cls[0])
        label = class_labels[class_id]  # Get the corresponding label for the detected class
        confidence = result.conf[0].item()  # Confidence score for detection

        # Check if a timer is running for this label, if so, skip giving commands
        if timers[label] > time.time():
            continue

        # Handle the voice commands based on the detected label
        if label == "away":
            # set_system_volume_to_max()
            # Keep calling user until they come back and give a reason
            while label == "away":
                voice_command(f"{user_name}, please come back to your desk!")

                # Continuously check if the user has returned by running YOLO again
                ret, frame = cap.read()
                if ret:
                    results = model(frame, conf=0.5)
                    for result in results[0].boxes:
                        class_id = int(result.cls[0])
                        label = class_labels[class_id]
                        if label != "away":
                            voice_command(f"Welcome back {user_name}.")
                            break  # Exit loop if user has returned

                # Run the speech recognition in a separate thread
                listen_for_reason(timers, label)

        elif label == "focused":
            pass  # No action if focused
        elif label == "idle":
            voice_command(f"{user_name}, why are you idle? Please do some work!")
        elif label == "oncall":
            voice_command(f"{user_name}, please put down the phone and get back to work!")
        elif label == "phone" or label == "using-phone":
            voice_command(f"{user_name}, stop using the phone and focus on work!")

            # Initiate a thread to listen for a reason while continuing monitoring
            listen_for_reason(timers, label)

    # Show the annotated frame in a window
    cv2.imshow("YOLOv8 Real-Time Webcam", annotated_frame)

    # Control the FPS
    time_spent = (time.time() - start_time) * 1000  # Convert to milliseconds
    if time_spent < frame_interval:
        cv2.waitKey(int(frame_interval - time_spent))

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
