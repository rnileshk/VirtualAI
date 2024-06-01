import imdb
import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import imdb
import wolframalpha
import subprocess as sp
from datetime import datetime
from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}. How may i help you?")


listening = False


def start_listening():
    global listening
    listening = True
    print("Started Listening...")


def pause_listening():
    global listening
    listening = False
    print("Stopped Listening.")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, Take care!")
            else:
                speak(f"{HOSTNAME} Stopped, Have a good day sir!")
            exit()

    except Exception:
        speak("Sorry I couldn't Understand. Can you please repeat it again.")
        queri = 'None'
    return queri


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I'm Absolutely fine. what about you sir?")

            elif "fine" in query:
                speak("Okay Sir that's good, I'm here to help you tell me how can i assist you.")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening Camera")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "open notepad" in query:
                speak("Opening Notepad for you sir")
                notepad_path = "C:\Windows\\notepad.exe"
                os.startfile(notepad_path)

            elif "open discord" in query:
                speak("Opening Discord for you master")
                discord_path = "https://discord.com/login"
                os.startfile(discord_path)

            elif "open youtube" in query:
                speak("Opening Youtube for you master")
                youtube_path = "https://www.youtube.com/"
                os.startfile(youtube_path)

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"your ip address is {ip_address}")
                print(f"your ip address is {ip_address}")

            elif "open youtube" in query:
                speak("what do you want to play on youtube sir?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"what do you want to search on google Boss")
                query = take_command().lower()
                search_on_google(query)

            elif "open wikipedia" in query:
                speak("what do you want to search on wikipedia")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia, {results}")
                speak("I am printing in on terminal")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send sir? please enter in the terminal")
                receiver_add = input("Email address: ")
                speak("what should be the subject sir?")
                subject = take_command().capitalize()
                speak("what is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add,subject,message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("Something went wrong Please check the error log")

            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today sir.")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(), sep='\n')

            elif "weather" in query:
                ip_address = find_my_ip()
                speak("Tell me the name of your city")
                city = input("Enter name of your city: ")
                speak(f"Getting weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also the weather report talks about {weather}")
                speak("For your Convenience, I am printing on the screen sir.")
                print(f"Description: {weather}\ntemperature: {temp}\nFeels like: {feels_like}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name :")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("Searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title} - {year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline', 'plot summary not available')
                    speak(f"{title} was released in {year} has imdb rating of {rating}. It has a cast of {actor}. The"
                          f"plot summary of movie is {plot}")
                    print(f"{title} was released in {year} has imdb rating of {rating}. It has a cast of {actor}. The"
                          f"plot summary of movie is {plot}")

            elif "calculate" in query:
                app_id = "98EGJQ-X4AG42K94W"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except:
                    StopIteration:
                    speak("I couldn't find that. Please try again")

            elif "what is" in query or "who is" in query or " which is" in query:
                app_id = "98EGJQ-X4AG42K94W"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                        query.lower().index("which is") if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind+2:]
                        result = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer " + ans)
                        print("The answer " + ans)
                    else:
                        speak("I couldn't find that")

                except StopIteration:
                    speak("I couldn't find that. Please try again")

