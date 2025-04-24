import time
import json
import os
from threading import Lock
from pynput import keyboard, mouse


class KeyboardMouse:
    def __init__(self, key_switch: str = 'f9', file_prefix: str = 'km_record'):
        self.FILE_PREFIX = file_prefix
        self.RECORDING_FILE = os.path.join(os.getcwd(), "RecordFiles", f"{file_prefix}.json")

        try:
            self.START_STOP_KEY = getattr(keyboard.Key, key_switch.lower())
        except AttributeError:
            self.START_STOP_KEY = keyboard.Key.f9
            print(f"Key {key_switch} not found. Using F9 as default")

        self.is_recording = False
        self.file_lock = Lock()
        self.buffer_size = 50
        self.event_buffer = []

        # Состояния
        self.active_keys = set()
        self.active_mouse_buttons = set()

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

    def on_key_press(self, key):
        if key == self.START_STOP_KEY:
            self.toggle_recording()
            return

        if self.is_recording and key not in self.active_keys:
            self.active_keys.add(key)
            event = {
                'time': time.time(),
                'type': 'keyboard',
                'action': 'press',
                'key': str(key)
            }
            self._add_event(event)

    def on_key_release(self, key):
        if self.is_recording and key in self.active_keys:
            self.active_keys.remove(key)
            event = {
                'time': time.time(),
                'type': 'keyboard',
                'action': 'release',
                'key': str(key)
            }
            self._add_event(event)

    def on_mouse_click(self, x, y, button, pressed):
        if self.is_recording:
            if pressed:
                self.active_mouse_buttons.add(button)
                event = {
                    'time': time.time(),
                    'type': 'mouse',
                    'action': 'press',
                    'button': str(button),
                    'x': x,
                    'y': y
                }
            else:
                if button in self.active_mouse_buttons:
                    self.active_mouse_buttons.remove(button)
                    event = {
                        'time': time.time(),
                        'type': 'mouse',
                        'action': 'release',
                        'button': str(button),
                        'x': x,
                        'y': y
                    }
                else:
                    return

            self._add_event(event)

    def on_mouse_move(self, x, y):
        if self.is_recording:
            event = {
                'time': time.time(),
                'type': 'mouse',
                'action': 'move',
                'x': x,
                'y': y
            }
            self._add_event(event)

    def on_mouse_scroll(self, x, y, dx, dy):
        if self.is_recording:
            event = {
                'time': time.time(),
                'type': 'mouse',
                'action': 'scroll',
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy
            }
            self._add_event(event)

    def toggle_recording(self):
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        self.is_recording = True
        self.active_keys.clear()
        self.active_mouse_buttons.clear()
        self.RECORDING_FILE = os.path.join(os.getcwd(), "RecordFiles" , f"{self.FILE_PREFIX}.json")
        print(f"Recording started. Press {self.START_STOP_KEY} to stop")

    def _stop_recording(self):
        self.is_recording = False
        self._flush_buffer()
        print(f"Recording stopped. Data saved to {self.RECORDING_FILE}")
        self.stop()

    def start(self):
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release)

        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click,
            on_move=self.on_mouse_move,
            on_scroll=self.on_mouse_scroll)

        self.keyboard_listener.start()
        self.mouse_listener.start()

        self.keyboard_listener.join()
        self.mouse_listener.join()

    def stop(self):
        if hasattr(self, 'keyboard_listener'):
            self.keyboard_listener.stop()
        if hasattr(self, 'mouse_listener'):
            self.mouse_listener.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    # Запускаем оба слушателя
    def keyboard_mouse_listener(self):
        print(f"Program ready. Press {self.START_STOP_KEY} to start recording.")
        with self as listener:
            pass
        return True




