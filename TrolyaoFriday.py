import pyttsx3
import datetime
import speech_recognition as sr 
import webbrowser as wb
import os 

friday = pyttsx3.init() # create object
voice = friday.getProperty('voices')
friday.setProperty('voice',voice[1].id) # 1 là giọng nữ, 0 là giọng nam

def speak(audio):
    print('FRIDAY: ' + audio)
    friday.say(audio)
    friday.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("̀%I:%M:%p") # số giờ, số phút, am hay pm
    speak(Time)
def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning sir")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon sir")
    elif hour >= 18 and hour < 24:
        speak("Good Night sir")
    speak('How can I help you ?')
def command():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold = 2 # dừng trong 2s 
        audio = c.listen(source)
    try:
        query = c.recognize_google(audio, language = 'en')
        print("Quang Anh: " + query)
    except sr.UnknownValueError:
        print("Please repeat or typing the command")
        query = str(input('Your order is: '))
    return query

if __name__ == "__main__":
    welcome()
    while True:
        query = command().lower()
        if "google" in query:
            speak("What shoule I search boss ?")
            search = command().lower()
            url = f"https://www.google.com/search?q={search}"
            wb.get().open(url)
            speak(f'Here is your {search} on google')
        if "youtube" in query:
            speak("What shoule I search boss ?")
            search = command().lower()
            url = f"https://www.youtube.com/search?q={search}"
            wb.get().open(url)
            speak(f'Here is your {search} on youtube')
        elif "open video":
            SN = r"C:\Users\Pham Quang Anh\OneDrive\OneDrive - Hanoi University of Science and Technology\Attachments\Me\SN.mp4"
            os.startfile(SN)
        elif "time" in query:
            time()
        elif "quit" in query:
            speak("FRIDAY is quitting sir. Goodbye boss")
            quit()