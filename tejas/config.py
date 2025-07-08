import json
import os

# Default configuration values
DEFAULT_SETTINGS = {
    "assistant_name": "Tejas",
    "input_method": "voice",  # Options: 'voice', 'text'
    "voice_language": "en-US",  # Language for speech recognition
    "enable_notifications": True,
    "monitor_interval": 60  # Time in seconds for system monitoring (CPU, RAM)
}

SETTINGS_FILE_PATH = os.path.join(os.path.dirname(r"C:\Users\ITESH\Dropbox\Desktop\Jyputer projects\tejas_ai\tejas\config.py"), 'settings.json')


def load_settings():
    """Load settings from a JSON file or return default settings if the file doesn't exist."""
    if os.path.exists(SETTINGS_FILE_PATH):
        with open(SETTINGS_FILE_PATH, 'r') as file:
            settings = json.load(file)
            return settings
    else:
        return DEFAULT_SETTINGS


def save_settings(settings):
    """Save the current settings to a JSON file."""
    with open(SETTINGS_FILE_PATH, 'w') as file:
        json.dump(settings, file, indent=4)


def update_setting(key, value):
    """Update a specific setting and save it."""
    settings = load_settings()
    settings[key] = value
    save_settings(settings)


def get_setting(key):
    """Get a specific setting value."""
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))


# Load the initial settings when the module is imported
current_settings = load_settings()