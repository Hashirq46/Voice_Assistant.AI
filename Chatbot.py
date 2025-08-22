import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import webbrowser
import random
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize TTS engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize recognizer
r = sr.Recognizer()
def take_command(prompt="Say Something..."):
    with sr.Microphone() as source:
        print(prompt)
        speak(prompt)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
            text = r.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except sr.WaitTimeoutError:
            print("No speech detected.")
            speak("You did not speak in time.")
        except sr.UnknownValueError:
            speak("I didn't understand.")
        except sr.RequestError:
            speak("I can't process your request.")
    return ""

# YouTube search function
def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=1,
        type="video"
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return f"https://www.youtube.com/watch?v={video_id}"

# Initialize Gemini Chat
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Main loop
speak("Say 'Hey Gemini' to start.")
while True:
    wake_command = take_command()
    if "hey gemini" in wake_command:
        speak("How can I help you, Hashir?")
        command = take_command()

        if "ok thanks" in command:
            speak("Goodbye, Hashir!")
            break

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "search on youtube" in command:
            speak("What should I search on YouTube?")
            search_query = take_command()
            if search_query:
                video_link = search_youtube(search_query)
                speak(f"Here's what I found for {search_query}")
                webbrowser.open(video_link)

        elif "open netflix" in command:
            webbrowser.open("https://netfree2.cc/home")
            speak("Opening Netflix")

        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        else:
            response = chat.send_message(command)
            print("Gemini:", response.text)
            speak(response.text)

    elif "ok thanks" in wake_command:
        speak("Goodbye, Hashir!")
        break
