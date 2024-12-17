import os
import random
import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="your_openai_api_key")  #I am not giving my api key. Replace with your actual OpenAI API key to use open ai...

def take_query():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Please speak now.")
        audio = recognizer.listen(source)

    try:
        print("Recognizing... Please wait.")
        text = recognizer.recognize_google(audio, language="en-PK")
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return ""

def say_query(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Selecting a voice that matches the 'english-pakistan' accent
    for voice in voices:
        if "english" in voice.languages and "pakistan" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()

    # List of websites and their URLs
    websites = {
        "google": "https://www.google.com",
        "instagram": "https://www.instagram.com",
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.org",
        "facebook": "https://www.facebook.com",
        "openai": "https://www.openai.com"
    }

    # Check if the recognized text matches any of the websites
    for site in websites:
        if site in text.lower():
            webbrowser.open(websites[site])
            print(f"Opening {site}...")
            break

def play_random_music():
    music_folder = "D:\\Portfolio\\myaibot\\musics"
    music_files = [f"{i}.mp3" for i in range(1, 11)]
    random_music = os.path.join(music_folder, random.choice(music_files))

    # Use subprocess to open the music file with the default music player
    subprocess.run(["start", random_music], shell=True)
    print(f"Playing {random_music}")

def open_app(app_name):
    app_paths = {
        "photoshop": r"C:\Program Files\Adobe\Adobe Photoshop.exe",
        "v s code": r"C:\Users\YourUsername\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "word": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
        "power point": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",

    }

    if app_name.lower() in app_paths:
        app_path = app_paths[app_name.lower()]
        if app_name.lower() == "settings":
            subprocess.run(["start", app_path], shell=True)
        else:
            subprocess.Popen([app_path])
        print(f"Opening {app_name}")
    else:
        print(f"App {app_name} not found.")

def interact_with_ai(query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']['content']

def save_response_to_file(query, response):
    folder_path = "D:\\Portfolio\\myaibot\\openai"
    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists
    file_path = os.path.join(folder_path, f"{query[:50]}.txt")  # Truncate filename to 50 chars
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response)
    print(f"Response saved to {file_path}")

if __name__ == "__main__":
    print("Starting the voice recognition program.")
    while True:
        query = take_query()
        if query:
            if "exit" in query.lower():
                print("Exiting the program.")
                say_query("Exiting the program.")
                break
            elif "play music" in query.lower():
                play_random_music()
            elif query.lower() in ["photoshop", "v s code", "chrome", "word", "power point"]:
                open_app(query.lower())
            elif "using ai" in query.lower():
                while True:
                    print("How can I assist you?")
                    say_query("How can I assist you?")
                    user_query = take_query()
                    if user_query.lower() == "stop":
                        print("Stopping AI interaction.")
                        say_query("Stopping AI interaction.")
                        break
                    response = interact_with_ai(user_query)
                    print(f"AI Response: {response}")
                    say_query(response)
                    save_response_to_file(user_query, response)
            else:
                say_query(query)
    print("Program ended.")
