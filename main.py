import tkinter as tk
from tkinter import messagebox
import threading
import psutil
import speech_recognition as sr
from time import sleep

def fade_in(window, steps=100, interval=10):
    for i in range(steps + 1):
        window.attributes('-alpha', i / steps)
        window.update()
        sleep(interval / 1000)

def show_splash_screen():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x300")
    splash.attributes('-alpha', 0)
    label = tk.Label(splash, text="Welcome to Tejas AI", font=("Arial", 20))
    label.pack(expand=True)
    fade_in(splash)
    sleep(2)
    splash.destroy()

def listen_wake_word():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    while True:
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                if "tejas" in command.lower():
                    messagebox.showinfo("Wake Word Detected", "Tejas is ready!")
        except sr.UnknownValueError:
            continue

def execute_command(command):
    if "cpu usage" in command.lower():
        cpu_usage = psutil.cpu_percent()
        messagebox.showinfo("CPU Usage", f"CPU Usage: {cpu_usage}%")
    elif "ram usage" in command.lower():
        ram_usage = psutil.virtual_memory().percent
        messagebox.showinfo("RAM Usage", f"RAM Usage: {ram_usage}%")
    else:
        messagebox.showinfo("Command", f"Executed command: {command}")

def process_text_command():
    command = command_entry.get()
    if command:
        history.append(command)
        update_history()
        execute_command(command)

def process_voice_command():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            history.append(command)
            update_history()
            execute_command(command)
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand the voice command.")

def update_history():
    history_text.delete("1.0", tk.END)
    for command in history:
        history_text.insert(tk.END, command + "\n")

def clear_history():
    history.clear()
    update_history()

# Main GUI
root = tk.Tk()
root.title("Tejas AI")
root.geometry("600x400")

# Display splash screen
show_splash_screen()

# History
history = []
history_label = tk.Label(root, text="Command History", font=("Arial", 12))
history_label.pack()
history_text = tk.Text(root, height=10, width=50)
history_text.pack()
history_clear_button = tk.Button(root, text="Clear History", command=clear_history)
history_clear_button.pack()

# Command input
command_label = tk.Label(root, text="Enter Command", font=("Arial", 12))
command_label.pack()
command_entry = tk.Entry(root, width=50)
command_entry.pack()

# Buttons
text_command_button = tk.Button(root, text="Execute Text Command", command=process_text_command)
text_command_button.pack()
voice_command_button = tk.Button(root, text="Execute Voice Command", command=process_voice_command)
voice_command_button.pack()

# Start wake word detection in a separate thread
wake_word_thread = threading.Thread(target=listen_wake_word, daemon=True)
wake_word_thread.start()

root.mainloop()
