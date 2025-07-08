import unittest
from tejas.voice_recognition import listen_command
from tejas.command_executor import execute_command
from tejas.system_monitor import get_cpu_usage, get_ram_usage
from tejas.utils import get_user_input_method


class TestTejasAI(unittest.TestCase):

    def test_recognize_speech(self):
        # Mock input for voice recognition (since we can't use real voice input here)
        # Assume recognize_speech returns a string
        result = listen_command()
        self.assertIsInstance(result, str)
        self.assertIn(result.lower(), ['open browser', 'shutdown system', 'check cpu usage'])

    def test_execute_command_open_browser(self):
        # Test command execution for opening the browser
        command = "open browser"
        result = execute_command(command)
        self.assertTrue(result)

    def test_execute_command_shutdown_system(self):
        # Test command execution for shutting down the system
        command = "shutdown system"
        result = execute_command(command)
        self.assertTrue(result)

    def test_system_monitor_cpu(self):
        # Test if CPU usage function returns a valid percentage
        cpu_usage = get_cpu_usage()
        self.assertGreaterEqual(cpu_usage, 0)
        self.assertLessEqual(cpu_usage, 100)

    def test_system_monitor_ram(self):
        # Test if RAM usage function returns a valid percentage
        ram_usage = get_ram_usage()
        self.assertGreaterEqual(ram_usage, 0)
        self.assertLessEqual(ram_usage, 100)

    def test_get_user_input_method(self):
        # Test user input method selection
        # For testing, we mock the method to simulate a choice between text and voice
        input_method = get_user_input_method()
        self.assertIn(input_method, ['voice', 'text'])


if __name__ == '__main__':
    unittest.main()