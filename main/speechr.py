import speech_recognition as sr 
import time

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Speak anything: ')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
    except:
        print("Couldn't understand what you want to say!")