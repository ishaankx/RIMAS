# main.py - FastAPI Backend with WebSocket Support

from fastapi import FastAPI, WebSocket, BackgroundTasks
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pyautogui
import os
import requests
import cv2
import time
import threading

# Initialize FastAPI app and necessary libraries
app = FastAPI()
engine = pyttsx3.init('sapi5')
recognizer = sr.Recognizer()
OPENAI_API_KEY = ""
reminders = []  # List to store reminders


# Helper Functions
def speak(message):
    """Converts text to speech."""
    engine.say(message)
    engine.runAndWait()


def adjust_volume(level):
    """Adjusts system volume to the specified level (0-100)."""
    os.system(f"nircmd.exe setsysvolume {level * 655.35}")


def open_browser(url="https://www.google.com"):
    """Opens a browser with a specific URL."""
    webbrowser.open(url)


def close_browser():
    """Closes the browser."""
    os.system("taskkill /f /im msedge.exe")


def take_screenshot():
    """Takes a screenshot and saves it."""
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    screenshot_path = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(screenshot_path)
    return screenshot_path


def open_youtube(query=""):
    """Opens YouTube with a search query."""
    if query:
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    else:
        webbrowser.open("https://www.youtube.com")


def open_notepad():
    """Opens Notepad."""
    os.system("notepad.exe")


def open_camera():
    """Opens the default camera."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Could not open the camera."

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return "Camera closed."


def chat_with_openai(prompt):
    """Queries OpenAI's ChatGPT with a user prompt."""
    response = requests.post(
        "https://api.openai.com/v1/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": "text-davinci-003",
            "prompt": prompt,
            "max_tokens": 100
        }
    )
    return response.json()['choices'][0]['text'].strip()


def add_reminder(subject, reminder_time):
    """Adds a reminder to the reminders list."""
    reminders.append({"subject": subject, "time": reminder_time})
    speak(f"Reminder set for {subject} at {reminder_time.strftime('%I:%M %p')}.")


def check_reminders():
    """Continuously checks for reminders and notifies the user when they are due."""
    while True:
        current_time = datetime.datetime.now()
        for reminder in reminders[:]:
            if current_time >= reminder["time"]:
                speak(f"Reminder: {reminder['subject']}.")
                reminders.remove(reminder)
        time.sleep(60)  # Check every minute


# Start reminder checker in a background thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to Voice Assistant")

    while True:
        try:
            data = await websocket.receive_text()
            if "volume" in data:
                if "increase" in data:
                    adjust_volume(80)
                    await websocket.send_text("Volume increased.")
                elif "decrease" in data:
                    adjust_volume(20)
                    await websocket.send_text("Volume decreased.")

            elif "browser" in data:
                if "open" in data:
                    open_browser()
                    await websocket.send_text("Browser opened.")
                elif "close" in data:
                    close_browser()
                    await websocket.send_text("Browser closed.")

            elif "screenshot" in data:
                screenshot_path = take_screenshot()
                await websocket.send_text(f"Screenshot saved as {screenshot_path}.")

            elif "youtube" in data:
                query = data.replace("youtube", "").strip()
                open_youtube(query)
                await websocket.send_text(f"Opened YouTube with search: {query}")

            elif "notepad" in data:
                open_notepad()
                await websocket.send_text("Notepad opened.")

            elif "camera" in data:
                response = open_camera()
                await websocket.send_text(response)

            elif "chat" in data:
                response = chat_with_openai(data)
                speak(response)
                await websocket.send_text(f"ChatGPT says: {response}")

            elif "reminder" in data:
                await websocket.send_text("Please specify the reminder subject.")
                reminder_subject = await websocket.receive_text()
                await websocket.send_text("Please specify the reminder time in format 'hour:minute am/pm'")
                reminder_time_str = await websocket.receive_text()

                # Parse reminder time
                try:
                    reminder_time = datetime.datetime.strptime(reminder_time_str, '%I:%M %p')
                    add_reminder(reminder_subject, reminder_time)
                    await websocket.send_text(
                        f"Reminder set for {reminder_subject} at {reminder_time.strftime('%I:%M %p')}.")
                except ValueError:
                    await websocket.send_text("Invalid time format. Please try again.")

            else:
                await websocket.send_text("Command not recognized.")

        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
            break
