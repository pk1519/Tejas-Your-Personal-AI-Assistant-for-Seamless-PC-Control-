# Import core modules so they can be easily accessed when tejas is imported
from .voice_recognition import listen_command
from .command_executor import execute_command
from .system_monitor import get_cpu_usage, get_ram_usage
from .config import load_settings

# Optionally, you can initialize default settings or configurations here
settings = load_settings()

_all_ = ['recognize_speech', 'execute_command', 'get_cpu_usage', 'get_ram_usage', 'send_notification', 'settings']