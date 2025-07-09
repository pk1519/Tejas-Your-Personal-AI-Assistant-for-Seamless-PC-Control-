from datetime import datetime
import os
import webbrowser
import pyautogui
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import wikipedia as googleScrap
from tejas.system_monitor import get_cpu_usage, get_ram_usage

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
engine.setProperty("voice", engine.getProperty("voices")[0].id)
engine.setProperty("rate", 170)

# Initialize speech recognizer
recognizer = sr.Recognizer()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def execute_command(command):
    if 'open browser' in command:
        open_browser()
    elif 'shutdown' in command:
        shutdown_pc()
    elif 'search wikipedia' in command:
        search_wikipedia(command)
    elif 'fathers' in command:
        search_inventors()
    elif 'date' in command:
        print_date()
    elif 'time' in command:
        print_time()
    elif 'cpu usage' in command:
        print(f"CPU Usage: {get_cpu_usage()}%")
    elif 'ram usage' in command:
        ram_usage = get_ram_usage()
        print(f"Memory Available: {ram_usage['memory_available']}MB")
        print(f"Memory Total: {ram_usage['memory_total']}MB")
        print(f"Memory Used: {ram_usage['memory_used']}MB")
    elif 'open' in command:
        app_name = command.replace('open ', '').strip()
        open_application(app_name)
    elif 'take screenshot' in command:
        take_screenshot()
    elif 'task manager' in command:
        open_task_manager()
    elif 'file manager' in command:
        open_file_manager()
    elif 'downloads' in command:
        open_downloads()
    elif 'weather' in command:
        city = command.replace('weather in ', '').strip()
        weather_report = get_weather(city)
        print(weather_report)
        speak(weather_report)
    elif 'open folder' in command:
        folder_name = command.replace('open folder ', '').strip()
        open_folder(folder_name)
    elif 'google' in command:
        search_google(command)
    elif 'youtube' in command:
        search_youtube(command)
    elif 'exit' in command:
        exit_program()
    else:
        print("Command not recognized. Please try again.")


def open_browser():
    print("Opening browser...")
    os.system("start brave")


def search_inventors():
    print("Fathers are:")
    print("Priyanshu Kumar")
    print("Piyush Raj")
    print("Nikhil Kumar Tiwari")
    print("Ritvik Jindal")


def shutdown_pc():
    print("Shutting down PC...")
    os.system("shutdown /s /t 1")


def search_wikipedia(command):
    search_term = command.replace('search wikipedia', '').strip()
    if search_term:
        url = f"https://en.wikipedia.org/wiki/{search_term.replace(' ', '_')}"
        print(f"Searching Wikipedia for: {search_term}")
        webbrowser.open(url)
    else:
        print("No search term provided for Wikipedia.")


def print_date():
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d')}")


def print_time():
    print(f"Current time: {datetime.now().strftime('%H:%M:%S')}")


def exit_program():
    print("Exiting the program...")
    exit(0)


def open_application(app_name):
    try:
        os.system(f"start {app_name}")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")


def open_task_manager():
    print("Opening Task Manager...")
    os.system("start taskmgr")


def open_file_manager():
    print("Opening File Manager...")
    os.system("start explorer")


def open_downloads():
    print("Opening Downloads folder...")
    downloads_path = os.path.expanduser("~\\Downloads")
    os.system(f"start {downloads_path}")


def open_folder(folder_path):
    print(f"Opening folder: {folder_path}")
    expanded_path = os.path.expanduser(folder_path)
    if os.path.isdir(expanded_path):
        os.system(f"start {expanded_path}")
    else:
        print(f"Folder not found: {folder_path}")


def get_weather(city):
    api_key = "your_token"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"  # Metric for Celsius

    try:
        response = requests.get(complete_url)
        weather_data = response.json()

        if weather_data["cod"] != "404":
            main = weather_data["main"]
            wind = weather_data["wind"]
            weather_desc = weather_data["weather"][0]["description"]

            temperature = main["temp"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]

            return (f"Weather in {city.capitalize()}:\n"
                    f"Temperature: {temperature}°C\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind Speed: {wind_speed} m/s\n"
                    f"Description: {weather_desc.capitalize()}")
        else:
            return "City not found, please try again."
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"


def take_screenshot():
    screenshots_folder = os.path.join(os.path.expanduser("~"), "Screenshots")
    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot_filename = os.path.join(screenshots_folder, f"screenshot_{current_time}.png")

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_filename)

    print(f"Screenshot saved as: {screenshot_filename}")
    speak(f"Screenshot taken and saved as {screenshot_filename}")


def search_google(query):
    query = query.replace("google search", "").replace("google", "").strip()
    if query:
        speak("This is what I found on Google")
        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 1)
            speak(result)
        except Exception as e:
            speak("No speakable output available")
            print(f"Error: {e}")


def search_youtube(query):
    query = query.replace("youtube search", "").replace("youtube", "").strip()
    if query:
        speak("This is what I found for your search!")
        web = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")


def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.energy_threshold = 300
        try:
            audio = recognizer.listen(source, timeout=4)
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}\n")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            print("Sorry, there was a problem with the request.")
            return "None"
    return query
