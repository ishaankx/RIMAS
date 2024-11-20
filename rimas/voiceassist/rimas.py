import datetime
import pyttsx3  # type: ignore
import speech_recognition as sr  # type: ignore
import wikipedia  # type: ignore
import webbrowser
import pywhatkit as wk
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL  # type: ignore
import threading
import time
import cv2
import operator
import pyautogui
import sys
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

# Global list to store reminders
reminders = []


def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    return current_volume


def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100, None)


def change_volume(delta):
    current_volume = get_volume()
    new_volume = current_volume + delta
    new_volume = max(0, min(100, new_volume))
    set_volume(new_volume)
    speak(f"Volume set to {int(new_volume)} percent")


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am ready. What can I do for you?")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = r.listen(source, timeout=5)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query


def close_browser_after_delay(delay):
    time.sleep(delay)
    os.system("taskkill /f /im msedge.exe")
    speak("I've closed the browser as you were watching content for 5 minutes.")


def check_reminders():
    """Function to continuously check and trigger reminders"""
    while True:
        current_time = datetime.datetime.now()
        for reminder in reminders[:]:  # Create a copy of the list to avoid modification during iteration
            if current_time >= reminder['time']:
                speak("Attention! Time for your reminder!")
                speak(
                    f"It's {current_time.strftime('%-I:%M %p')} and you asked me to remind you to: {reminder['subject']}")
                speak("Would you like me to dismiss this reminder?")
                response = takecommand().lower()
                if 'yes' in response or 'ok' in response:
                    reminders.remove(reminder)
                    speak("Reminder dismissed.")
                else:
                    speak("I'll remind you again in 5 minutes.")
                    reminder['time'] = current_time + datetime.timedelta(minutes=5)
        time.sleep(1)  # Check every second


def parse_time(time_str):
    """Convert user time format to datetime object
    Accepts formats:
    - "5 40 pm" (hour minute period)
    - "in 30 seconds"
    """
    current_time = datetime.datetime.now()
    try:
        # Handle "in X seconds" format
        if "in" in time_str.lower():
            parts = time_str.lower().split()
            if len(parts) >= 3 and parts[2].startswith("second"):
                seconds = int(parts[1])
                return current_time + datetime.timedelta(seconds=seconds)
            return None

        # Handle "hour minute period" format (e.g., "5 40 pm")
        else:
            parts = time_str.lower().split()
            if len(parts) != 3:
                return None

            hour = int(parts[0])
            minute = int(parts[1])
            period = parts[2]

            # Convert to 24-hour format
            if period == "pm" and hour != 12:
                hour += 12
            elif period == "am" and hour == 12:
                hour = 0

            reminder_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # If the time has already passed today, set it for tomorrow
            if reminder_time < current_time:
                reminder_time += datetime.timedelta(days=1)

            return reminder_time
    except:
        return None


def ask_chatgpt(prompt, max_retries=3, retry_delay=5):
    """
    Send a prompt to ChatGPT and get the response
    """
    retries = 0
    while retries < max_retries:
        try:
            api_key = ""  # replace with your actual API key
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer "
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2048,
                "temperature": 0.7
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error: {str(e)}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                return f"Sorry, I encountered an error: {str(e)}"
def get_operator_fn(op):
    return {
        '+': operator.add,
        'plus': operator.add,
        '-': operator.sub,
        'minus': operator.sub,
        'x': operator.mul,
        'times': operator.mul,
        'divided': operator.truediv,
    }.get(op)

def eval_binary_expr(op1, oper, op2):
    op1, op2 = int(op1), int(op2)
    return get_operator_fn(oper)(op1, op2)

# Start the reminder checking thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()
camera_opened = False
if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand().lower()

        if 'set reminder' in query or 'set a reminder' in query:
            speak("What should I remind you about?")
            subject = takecommand().lower()

            speak("When should I remind you? You can say a time like '5 40 pm' or 'in 30 seconds'")
            time_str = takecommand().lower()

            reminder_time = parse_time(time_str)

            if reminder_time:
                reminders.append({
                    'subject': subject,
                    'time': reminder_time
                })
                # Format the confirmation message based on the type of reminder
                time_diff = reminder_time - datetime.datetime.now()
                if time_diff.total_seconds() < 60:  # If reminder is in seconds
                    speak(f"Okay, I'll remind you about {subject} in {int(time_diff.total_seconds())} seconds")
                else:  # If reminder is at a specific time
                    speak(f"Okay, I'll remind you about {subject} at {reminder_time.strftime('%-I:%M %p')}")
            else:
                speak("Sorry, I couldn't understand the time format. Please use either '5 40 pm' or 'in 30 seconds'")

        # Rest of the code remains the same...

        elif 'show reminders' in query or 'list reminders' in query:
            if reminders:
                speak("Here are your current reminders:")
                for reminder in reminders:
                    time_diff = reminder['time'] - datetime.datetime.now()
                    if time_diff.total_seconds() < 60:
                        speak(f"{reminder['subject']} in {int(time_diff.total_seconds())} seconds")
                    else:
                        speak(f"{reminder['subject']} at {reminder['time'].strftime('%-I:%M %p')}")
            else:
                speak("You don't have any active reminders.")

        elif 'clear reminders' in query or 'delete reminders' in query:
            reminders.clear()
            speak("All reminders have been cleared.")

        elif 'rimas' in query:
            print("Yes sir")
            speak("Yes sir")
        elif "who are you" in query:
            print('My name is RIMAS')
            speak('My name is RIMAS')
            print('What can I do for you')
            speak('What can I do for you')
        elif "who created you" in query:
            print("I don't know, but I was created using the Python language")
            speak("I don't know, but I was created using the Python language")
        elif 'what is' in query or 'who is' in query:
            speak('Searching Wikipedia...')
            query = query.replace("what is", "").replace("who is", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia...")
            print(results)
            speak(results)
        elif 'just open google' in query:
            webbrowser.open('google.com')
        elif 'open google' in query:
            speak("What should I search?")
            qry = takecommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={qry}")
            results = wikipedia.summary(qry, sentences=1)
            speak(results)
        elif 'just open youtube' in query:
            webbrowser.open('youtube.com')
        elif 'open youtube' in query:
            speak('What do you want to watch?')
            query = takecommand().lower()
            if 'entertaining' in query or 'funny' in query:
                speak("I'm sorry, but you can't watch entertaining or funny videos.")
            else:
                wk.playonyt(f"{query}")
                threading.Thread(target=close_browser_after_delay, args=(300,)).start()
        elif 'search on youtube' in query:
            query = query.replace("search on youtube", "")
            if 'entertaining' in query or 'funny' in query:
                speak("I'm sorry, but you can't watch entertaining or funny videos.")
            else:
                webbrowser.open(f"www.youtube.com/results?search_query={query}")
                threading.Thread(target=close_browser_after_delay, args=(300,)).start()
        elif 'close browser' in query:
            os.system("taskkill /f /im msedge.exe")
        elif 'increase volume by' in query:
            try:
                delta = int(query.split('increase volume by')[1].strip())
                change_volume(delta)
            except ValueError:
                speak("Sorry, I couldn't understand the volume amount.")
        elif 'decrease volume by' in query:
            try:
                delta = int(query.split('decrease volume by')[1].strip())
                change_volume(-delta)
            except ValueError:
                speak("Sorry, I couldn't understand the volume amount.")
        elif 'set volume to' in query:
            try:
                level = int(query.split('set volume to')[1].strip())
                set_volume(level)
                speak(f"Volume set to {level} percent")
            except ValueError:
                speak("Sorry, I couldn't understand the volume level.")
        elif 'open notepad' in query:
            npath = "C:/WINDOWS/system32/notepad.exe"
            os.startfile(npath)
        elif 'close notepad' in query:
            os.system("taskkill /f /im notepad.exe")
        elif 'open command prompt' in query:
            os.system("start cmd")
        elif 'close command prompt' in query:
            os.system('taskkill /f /im cmd.exe')
        elif 'play music' in query:
            speak("You can't listen to music while working")
        elif 'tell me the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif 'open netflix' in query:
            speak("You can't open Netflix while working")
        elif 'open camera' in query:
            if not camera_opened:
                # Open the default camera application
                os.startfile("microsoft.windows.camera:")
                camera_opened = True
                speak("Camera opened.")
            else:
                speak("Camera is already open.")

        elif 'close camera' in query:
            # Close the camera application
            os.system("taskkill /f /im WindowsCamera.exe")
            camera_opened = False
            speak("Camera closed.")
        elif "take screenshot" in query:
            speak('Tell me a name for the file.')
            name = takecommand().lower()
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f'{name}.png')
            speak("Screenshot saved.")
        elif "calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Ready")
                print("Listening...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

                try:
                    my_string = r.recognize_google(audio)
                    print("Heard:", my_string)
                    # Attempt to split the input and calculate
                    parts = my_string.split()
                    if len(parts) == 3:
                        op1, oper, op2 = parts
                        result = eval_binary_expr(op1, oper, op2)
                        speak(f"Your result is {result}")
                    else:
                        speak("Please say the calculation in the form of 'number operator number', like '1 plus 2'.")
                except Exception as e:
                    print("Error:", e)
                    speak("Sorry, I could not understand.")
        elif 'open gpt' in query:
            webbrowser.open('https://chat.openai.com')
            # speak("What would you like to ask ChatGPT?")
            # question = takecommand().lower()
            # if question != "none":
            #     response = ask_chatgpt(question)
            #     print("ChatGPT's response:", response)
            #     speak(response)
            # else:
            #     speak("I couldn't understand your question. Please try again.")
        elif 'exit' in query:
            print("Goodbye!")
            speak("Goodbye!")
            sys.exit()