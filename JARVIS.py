import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import cohere
from gtts import gTTS
import pygame
import time
import os

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 180)

# News API key
newsapi = "4186bdbfef154b628cc0978496e1cbc8"

# Initialize Cohere
co = cohere.Client("1zBCvuhGnrdz0OvL7kCQK0DPN156z621652ODk2O")

# Initialize pygame mixer
pygame.mixer.init()

# Play an MP3 file
def play_mp3(filename):
    if os.path.exists(filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print(f"File not found: {filename}")

# Speak using pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Recognize voice from microphone
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

# Get AI response using Cohere
def aiProcess(command):
    response = co.generate(
        model='command-r-plus',
        prompt=command,
        max_tokens=100
    )
    return response.generations[0].text.strip()

# Process common commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]  # Fix split to capture full song name
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            for article in articles[:5]:  # Limit to top 5 headlines
                title = article.get("title")
                if title:
                    speak(title)
        else:
            speak("Sorry, I couldn't fetch the news right now.")
    else:
        output = aiProcess(c)
        speak(output)

# MAIN wake word loop
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Yes Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("HELLOOOOOO")
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print(f"Error: {e}")
