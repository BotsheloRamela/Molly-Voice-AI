from typing import Text
import speech_recognition as sr
import webbrowser
import time
import os
import random
import requests
import playsound
from gtts import gTTS
from time import ctime
import pyttsx3
import datetime

r = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            alexis_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            r.adjust_for_ambient_noise(source)
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            alexis_speak("Sorry, I did not get that")
        except sr.RequestError:
            alexis_speak("Sorry my speech service is down")
        return voice_data


def alexis_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en-gb')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    # os.remove(audio_string)


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        alexis_speak("Good Morning sir, great day isn't it...")
    elif hour >= 12 and hour < 18:
        alexis_speak("Good Afternoon sir, great day isn't it...")
    else:
        alexis_speak("Good Evening sir, beautiful night isn't it...")


def respond(voice_data):
    if 'what is your name' in voice_data or "what's your name" in voice_data or 'identify yourself' in voice_data:
        alexis_speak('My name is Alexis')

    if 'who made you' in voice_data or 'who created you' in voice_data or 'who is your creator' in voice_data or "who's your creator" in voice_data:
        alexis_speak("My creator is Botshelo Ramela")

    if 'what time is it' in voice_data or "what's the time" in voice_data:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        alexis_speak(f"the time is {strTime}")

    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        alexis_speak('Here is what I found for ' + search)

    if 'find location' in voice_data:
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        alexis_speak('Here is the location of ' + location)

    if 'open YouTube' in voice_data:
        webbrowser.get().open('https://youtube.com/')
        alexis_speak('Youtube is now open')

    if 'open my emails' in voice_data or 'check my emails' in voice_data:
        webbrowser.get().open("https://gmail.com/")
        alexis_speak("here are your emails")

    if "how's the weather" in voice_data or "how is the weather" in voice_data:
        api_key = "2fb1b5b52a5a1fde20815591121e0383"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        alexis_speak("what is the name of the city")
        city_name = record_audio()
        complete_url = base_url+"appid="+api_key+"&q="+city_name+"&units=metric"
        alexis_speak("Alright, give me a second sir while a search for that")
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            alexis_speak("The temperature in " + city_name + " is " + str(current_temperature) + " degrees celcius" + " with a humidity of " +
                         str(current_humidiy) + " percent" + " and we have a" + str(weather_description))
            print(" Temperature in celcius is " +
                  str(current_temperature) +
                  "\n humidity (in percentage) = " +
                  str(current_humidiy) +
                  "\n description = " +
                  str(weather_description))

    if 'exit' in voice_data:
        alexis_speak(
            "your personal assistant Alexis is shutting down, see you later sir")
        exit()


time.sleep(1)
wishMe()
alexis_speak("What can I assist you with?")

while 1:
    voice_data = record_audio()
    respond(voice_data)
