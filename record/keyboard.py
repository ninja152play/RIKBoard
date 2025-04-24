import time
import json
import os
from threading import Lock
from pynput import keyboard


class Keyboard:
    def __init__(self, key_switch: str = 'f9', file_prefix: str = 'key_record'):
        self.FILE_PREFIX = file_prefix
        self.RECORDING_FILE = os.path.join(os.getcwd(), "RecordFiles", f"{file_prefix}.json")

        try:
            self.START_STOP_KEY = getattr(keyboard.Key, key_switch.lower())
        except AttributeError:
            self.START_STOP_KEY = keyboard.Key.f9
            print(f"Warning: Key {key_switch} not found. Using F9 as default")

        self.is_recording = False
        self.events = []
        self.active_keys = set()
        self.file_lock = Lock()
        self.listener = None

        # Оптимизация: буферизация записей
        self.buffer_size = 100
        self.event_buffer = []

    def on_press(self, key):
        if key == self.START_STOP_KEY:
            self.toggle_recording()
            return

        if self.is_recording and key not in self.active_keys:
            self.active_keys.add(key)
            event = {
                'time': time.time(),
                'type': 'keyboard',
                'action': 'press',
                'key': str(key),
            }
            self._add_event(event)

    def on_release(self, key):
        if self.is_recording and key in self.active_keys:
            self.active_keys.remove(key)
            event = {
                'time': time.time(),
                'type': 'keyboard',
                'action': 'release',
                'key': str(key),
            }
            self._add_event(event)

    def _add_event(self, event):
        """Буферизация событий для оптимизации записи"""
        with self.file_lock:
            self.event_buffer.append(event)
            if len(self.event_buffer) >= self.buffer_size:
                self._flush_buffer()

    def _flush_buffer(self):
        """Запись буфера в файл"""
        if not self.event_buffer:
            return

        try:
            with open(self.RECORDING_FILE, 'a') as f:
                for event in self.event_buffer:
                    f.write(json.dumps(event) + '\n')
            self.event_buffer.clear()
        except Exception as e:
            print(f"Error saving events: {e}")

    def toggle_recording(self):
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        self.is_recording = True
        self.events = []
        self.active_keys.clear()
        self.RECORDING_FILE = os.path.join(os.getcwd(), "RecordFiles" , f"{self.FILE_PREFIX}.json")
        print(f"Recording started. Press {self.START_STOP_KEY} to stop")

    def _stop_recording(self):
        self.is_recording = False
        self._flush_buffer()
        print(f"Recording stopped. Data saved to {self.RECORDING_FILE}")
        self.listener.stop()

    # Start keyboard listener
    def keyboard_listener(self):
        print(f"Program ready. Press {self.START_STOP_KEY} to start recording.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()
        return True
