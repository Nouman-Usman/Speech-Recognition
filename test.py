import speech_recognition as sr
import os
# import nltk
import subprocess
import spacy
from gtts import gTTS
import os


def respond_with_tts(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    # os.system("mpg321 response.mp3")
    os.system("say response.mp3")


recognizer = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")


def get_installed_applications():
    try:
        command = 'ls /Applications'
        applications = subprocess.check_output(command, shell=True, universal_newlines=True).strip().split('\n')
        cleaned_names = [name.replace("''", "").replace(".app", "") for name in applications]
        return cleaned_names
    except Exception as e:
        print(f"Error: {e}")
        return []


application_aliases = {
    "chrome": "Google Chrome",
    "whatsapp": "WhatsApp",
    "pycharm": "PyCharm CE",
    "onedrive": "OneDrive",
    "bandwidth+": "Bandwidth+",
    "powerpoint": "Microsoft PowerPoint",
    "python": "Python 3.12",
    "visual studio": "Visual Studio",
    "vs code": "Visual Studio Code",
    "outlook": "Microsoft Outlook",
    "mysql": "MySQLWorkbench",
    "excel": "Microsoft Excel",
    "unarchiver": "The Unarchiver",
    "vlc": "VLC",
    "anaconda": "Anaconda-Navigator",
    "onenote": "Microsoft OneNote",
    "android studio": "Android Studio",
    "teams": "Microsoft Teams",
    "safari": "Safari",
    "obs": "OBS",
    "utilities": "Utilities",
    "word": "Microsoft Word",
    # Add more aliases for other applications as needed
}


def recognize_speech():
    arr = get_installed_applications()
    application_set = set(arr)
    print(application_set)

    with sr.Microphone() as source:
        print("Listening....")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio).lower()
            print(text)
            respond_with_tts(text)
            doc = nlp(text)
            for alias, app_name in application_aliases.items():
                if alias in text:
                    app_name = application_aliases[alias]
                    print(f"Recognized alias: {alias} (Actual Application: {app_name})")

                    if any(token.text in ["open", "launch", "start"] for token in doc):
                        os.system(f"say Opening {app_name}")
                        openApp(app_name)
                    elif any(token.text in ["close", "quit", "exit"] for token in doc):
                        os.system(f"say Closing {app_name}")
                        closeApp(app_name)
                    else:
                        os.system("say I'm sorry, I didn't understand that.")
                    break  # Exit the loop after processing the first match
            else:
                os.system("say I'm sorry, I didn't understand that.")

        except sr.UnknownValueError:
            os.system("say Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            os.system(f"say Sorry, I couldn't request results; {str(e)}")


def openApp(app_name):
    os.system(f"open -a '{app_name}'")


def closeApp(app_name):
    os.system(f"pkill -f '{app_name}'")


if __name__ == '__main__':
    recognize_speech()
