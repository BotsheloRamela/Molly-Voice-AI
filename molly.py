import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import pyaudio
import requests
from time import sleep
from time import ctime
from datetime import date

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)
#rate = engine.getProperty('rate')
# print(rate)
# print(voices)

r = sr.Recognizer()


def recognize_voice(ask=False):
  # create an instance of the Microphone class
    with sr.Microphone() as source:
        if ask:
            molly_speak(ask)
        text = ''
        # adjust for ambient noise
        r.adjust_for_ambient_noise(source)
    # capture the voice
        voice = r.listen(source)
    # let's recognize it
    try:
        text = r.recognize_google(voice)
    except sr.UnknownValueError:
        molly_speak("Sorry, I did not get that")
    except sr.RequestError:
        molly_speak("Sorry my speech service is down")
    return text.lower()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        molly_speak("Good Morning sir, great day isn't it...")
    elif hour >= 12 and hour < 18:
        molly_speak("Good Afternoon sir, great day isn't it...")
    else:
        molly_speak("Good Evening sir, beautiful night isn't it...")
    today = date.today()
    time = datetime.datetime.now().strftime("%H:%M")
    molly_speak(f"Today is {today} and it is {time}")


def reply(voice_data):
    # name
    if 'what is your name' in voice_data or "what's your name" in voice_data or 'identify yourself' in voice_data:
        molly_speak("My name is Molly")

    # date
    if "date" in voice_data or 'what date is it' in voice_data or 'what is the date' in voice_data or "what is today's date" in voice_data:
        # get today's date and format it
        today = date.today()
        molly_speak(f"the date is {today}")
    # time
    if "time" in voice_data or 'what is the time' in voice_data or 'what time is it' in voice_data:
        # get current time and format it like - 02 28
        time = datetime.datetime.now().strftime("%H:%M")
        molly_speak(f"the time is {time}")

    if 'who made you' in voice_data or 'who created you' in voice_data or 'who is your creator' in voice_data or "who's your creator" in voice_data:
        molly_speak("My creator is Botshelo Ramela")

    # search google
    if "search" in voice_data or "google" in voice_data or "search google" in voice_data:
        molly_speak("What do you want me to search for?")
        keyword = recognize_voice()
        # if "keyword" is not empty
        if keyword != '':
            url = "https://google.com/search?q=" + keyword
            # webbrowser module to work with the webbrowser
            molly_speak("Here are the search results for " + keyword)
            webbrowser.open(url)

    if 'find location' in voice_data:
        location = recognize_voice("What is the location you're looking for?")
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        molly_speak('Here is the location of ' + location)

    if 'open my emails' in voice_data or 'check my emails' in voice_data:
        webbrowser.get().open("https://gmail.com/")
        molly_speak("here are your emails")

    if 'Facebook' in voice_data or "open facebook" in voice_data:
        url = 'https://facebook.com'
        webbrowser.get().open(url)
        molly_speak("opening facebook")

    if 'Twitter' in voice_data or "open twitter" in voice_data:
        url = 'https://twitter.com'
        webbrowser.get().open(url)
        molly_speak("opening Twitter")

    if 'Youtube' in voice_data or "open youtube" in voice_data or "continue last session" in voice_data or "open you tube" in voice_data:
        search = recognize_voice("What do you want to search for")
        url = 'https://www.youtube.com/results?search_query=' + search
        webbrowser.get().open(url)
        molly_speak("Here are the youtube search results for " + search)

    if "how's the weather" in voice_data or "how is the weather" in voice_data:
        api_key = "2fb1b5b52a5a1fde20815591121e0383"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        molly_speak("what is the name of the city")
        city_name = recognize_voice()
        complete_url = base_url+"appid="+api_key+"&q="+city_name+"&units=metric"
        molly_speak("Alright, give me a second sir while a search for that")
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            molly_speak("The temperature in " + city_name + " is " + str(current_temperature) + " degrees celcius" + " with a humidity of " +
                        str(current_humidiy) + " percent" + " and there is " + str(weather_description))
            print(" Temperature in celcius is " +
                  str(current_temperature) +
                  "\n humidity (in percentage) = " +
                  str(current_humidiy) +
                  "\n description = " +
                  str(weather_description))

    # quit/exit
    if "quit" in voice_data or "exit" in voice_data:
        molly_speak(
            "your personal assistant Molly is shutting down, see you later sir")
        exit()


def molly_speak(text):
    engine.say(text)
    engine.runAndWait()


time.sleep(1)
wishMe()
molly_speak("What can I assist you with?")

while 1:
    voice_data = recognize_voice()
    reply(voice_data)
