import tkinter as tk
from tkinter import scrolledtext
import psutil  # To get system information like CPU and RAM usage
import time
from tejas.voice_recognition import listen_command
from tejas.command_executor import execute_command


# Splash screen function
def splash_screen():
    splash = tk.Tk()
    splash.title("Tejas AI Assistant")
    splash.geometry("400x400")
    splash.config(bg='white')

    # Display splash text or logo
    splash_label = tk.Label(splash, text="Tejas AI Assistant", font=('Helvetica', 40, 'bold'), fg="blue", bg='white')
    splash_label.pack(pady=150)

    # Delay for 3 seconds before closing splash screen
    splash.after(3000, splash.destroy)
    splash.mainloop()


# System statistics functions (from Code B)
def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    return {
        'cpu_usage': cpu_usage,
        'memory_available': memory_info.available / (1024 * 1024),
        'memory_total': memory_info.total / (1024 * 1024)
    }


def get_cpu_usage():
    """Return the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)


def get_ram_usage():
    """Return the current RAM usage in megabytes."""
    memory_info = psutil.virtual_memory()
    return {
        'memory_available': memory_info.available / (1024 * 1024),
        'memory_total': memory_info.total / (1024 * 1024),
        'memory_used': memory_info.used / (1024 * 1024)
    }


def report_system_stats():
    stats = get_system_stats()
    print(f"CPU Usage: {stats['cpu_usage']}%")
    print(f"Memory Available: {stats['memory_available']}MB of {stats['memory_total']}MB")


# Function to handle voice command input
def handle_voice_command():
    result_text.set("Listening for a voice command...")  # Feedback when listening starts
    root.update_idletasks()  # Update UI immediately
    command = listen_command()  # Call your voice recognition function
    if command:
        process_command(command)
    else:
        result_text.set("No command recognized. Please try again.")


# Function to handle text input command
def handle_text_command():
    command = text_entry.get()  # Get text from the input field
    if command.strip():  # Only proceed if the command is not empty
        process_command(command)
        text_entry.delete(0, tk.END)  # Clear input after execution
    else:
        result_text.set("Please enter a valid command.")


# Function to process the command and show output in a new window for specific commands
def process_command(command):
    if command.lower() in ['cpu usage', 'ram usage']:
        show_output_window(command)
    else:
        execute_command(command)
        update_command_history(f"Text: {command}")
        result_text.set(f"Executed Command: {command}")


# Function to show the CPU or RAM usage in a new GUI window
def show_output_window(command):
    output_window = tk.Toplevel(root)
    output_window.title(f"{command.capitalize()} Output")

    # Text box to show the output
    output_textbox = scrolledtext.ScrolledText(output_window, width=50, height=10, wrap=tk.WORD)
    output_textbox.pack(padx=10, pady=10)

    if command.lower() == 'cpu usage':
        cpu_percent = get_cpu_usage()
        output_textbox.insert(tk.END, f"CPU Usage: {cpu_percent}%\n")
    elif command.lower() == 'ram usage':
        ram_stats = get_ram_usage()
        output_textbox.insert(tk.END, f"RAM Usage: {ram_stats['memory_used']}MB of {ram_stats['memory_total']}MB\n")

    output_textbox.config(state=tk.DISABLED)  # Disable editing of the output box

    # Button to close the output window
    close_button = tk.Button(output_window, text="Close", command=output_window.destroy)
    close_button.pack(pady=5)


# Function to update the command history
def update_command_history(command):
    command_history.append(command)  # Store the command in history list


# Function to open the history panel in a new window
def open_history_window():
    history_window = tk.Toplevel(root)  # Create a new window
    history_window.title("Command History")

    # Create a scrollable text area in the new window to show the command history
    history_textbox = scrolledtext.ScrolledText(history_window, width=50, height=10, wrap=tk.WORD)
    history_textbox.pack(padx=10, pady=10)

    # Populate the textbox with the command history
    for command in command_history:
        history_textbox.insert(tk.END, f"{command}\n")
    history_textbox.config(state=tk.DISABLED)  # Make the text box read-only

    # Function to clear the command history
    def clear_history():
        global command_history
        command_history.clear()  # Clear the list
        history_textbox.config(state=tk.NORMAL)  # Enable editing to clear the textbox
        history_textbox.delete(1.0, tk.END)  # Clear all text from the textbox
        history_textbox.config(state=tk.DISABLED)  # Disable editing again

    # Button to clear the history
    clear_history_button = tk.Button(history_window, text="Clear History", command=clear_history)
    clear_history_button.pack(pady=5)

    # Button to close the history window
    close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
    close_button.pack(pady=5)


# GUI setup
def create_gui():
    global text_entry, result_text, root, command_history

    command_history = []  # Initialize the command history list

    root = tk.Tk()
    root.title("Tejas AI Assistant")

    # Make the window full screen
    root.attributes('-fullscreen', True)

    # Large "Tejas AI" label
    tejas_ai_label = tk.Label(root, text="Tejas AI", font=('Helvetica', 60, 'bold'), fg="blue")
    tejas_ai_label.pack(pady=50)

    # Create label and entry field for text input
    label = tk.Label(root, text="Enter your command:", font=('Helvetica', 20))
    label.pack(pady=10)

    text_entry = tk.Entry(root, width=40, font=('Helvetica', 16))
    text_entry.pack(pady=10)

    # Create button to handle text input commands
    text_button = tk.Button(root, text="Execute Command", command=handle_text_command, font=('Helvetica', 16))
    text_button.pack(pady=10)

    # Create button to handle voice commands
    voice_button = tk.Button(root, text="Use Voice Command", command=handle_voice_command, font=('Helvetica', 16))
    voice_button.pack(pady=10)

    # Result label to display the executed command or result
    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, font=('Helvetica', 20), fg="green")
    result_label.pack(pady=10)

    # Create a button to open the command history window
    history_button = tk.Button(root, text="Show History", command=open_history_window, font=('Helvetica', 16))
    history_button.pack(pady=10)

    # Create a quit button to exit the application
    quit_button = tk.Button(root, text="Quit", command=root.quit, font=('Helvetica', 16))
    quit_button.pack(pady=10)

    root.mainloop()  # Start the Tkinter event loop


def main():
    print("Initializing Tejas AI Assistant...")

    # Show splash screen first
    splash_screen()

    # Initialize the GUI after the splash screen
    create_gui()


if __name__ == "__main__":
    main()
