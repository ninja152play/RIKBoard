import time
import os
import datetime
from threading import Lock
from pynput import keyboard, mouse


class AHKRecord:
    def __init__(self, key_switch: str = 'f9', file_prefix: str = 'km_record', x=1920, y=1080):
        self.FILE_PREFIX = file_prefix
        self.RECORDING_FILE = os.path.join(os.getcwd(), "AHK", f"{file_prefix}.txt")

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

        # Центр экрана

        self.center_x = x / 2
        self.center_y = y / 2

        # Запись поворота мыши
        self.mouse_rotations_x = ''
        self.mouse_rotations_y = ''

        self.mouse_move_x = 0
        self.mouse_move_y = 0

        # Вычисление времени нажатия клавиши
        self.start_time = 0

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
                    f.write(event + '\n')
            self.event_buffer.clear()
        except Exception as e:
            print(f"Error saving events: {e}")

    def on_key_press(self, key):
        if key == self.START_STOP_KEY:
            self.toggle_recording()
            return

        if self.is_recording and key not in self.active_keys:
            self.active_keys.add(key)
            self.start_time = time.time()
            event = 'Send, {' + str(key).replace("'", '') + ' down}'
            self._add_event(event)

    def on_key_release(self, key):
        if self.is_recording and key in self.active_keys:
            self.active_keys.remove(key)
            end_time = time.time()
            time_delta = end_time - self.start_time
            dt = datetime.datetime.fromtimestamp(time_delta)
            seconds = dt.second
            milliseconds = int(dt.microsecond / 1000)
            time_sleep = int((seconds * 1000) + milliseconds)
            event = ('Sleep ' + str(time_sleep) + '\n'
                     'Send, {' + str(key).replace("'", '') + ' up}')
            self._add_event(event)

    def on_mouse_click(self, x, y, button, pressed):
        if self.is_recording:
            if pressed:
                self.active_mouse_buttons.add(button)
                print(button)
                if button == mouse.Button.left:
                    event = 'Send, {LButton down}'
                elif button == mouse.Button.middle:
                    event = 'Send, {MButton down}'
                elif button == mouse.Button.right:
                    event = 'Send, {RButton down}'
                else:
                    event = 'MouseClickUndefined'
            else:
                if button in self.active_mouse_buttons:
                    self.active_mouse_buttons.remove(button)
                    if button == mouse.Button.left:
                        event = 'Send, {LButton up}'
                    elif button == mouse.Button.middle:
                        event = 'Send, {MButton up}'
                    elif button == mouse.Button.right:
                        event = 'Send, {RButton up}'
                    else:
                        event = 'MouseClickUndefined'

            self._add_event(event)

    def on_mouse_move(self, x, y):
        if self.is_recording:
            if x > self.center_x:
                if self.mouse_rotations_x == 'L':
                    self._add_event(f'MouseMove, {int(self.mouse_move_x) // 3}, 0, 50, R')
                    self.mouse_move_x = 0
                self.mouse_move_x += x - self.center_x
                self.mouse_rotations_x = 'R'
            elif x < self.center_x:
                if self.mouse_rotations_x == 'R':
                    self._add_event(f'MouseMove, {int(self.mouse_move_x) // 3}, 0, 50, R')
                    self.mouse_move_x = 0
                self.mouse_move_x += x - self.center_x
                self.mouse_rotations_x = 'L'
            print(x, y)
            if y > self.center_y:
                if self.mouse_rotations_y == 'U':
                    self._add_event(f'MouseMove, 0, {int(self.mouse_move_y) // 3}, 50, R')
                    self.mouse_move_y = 0
                self.mouse_move_y += y - self.center_y
                self.mouse_rotations_y = 'D'
            elif y < self.center_y:
                if self.mouse_rotations_y == 'D':
                    self._add_event(f'MouseMove, 0, {int(self.mouse_move_y) // 3}, 50, R')
                    self.mouse_move_y = 0
                self.mouse_move_y += y - self.center_y
                self.mouse_rotations_y = 'U'

    def toggle_recording(self):
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        self.is_recording = True
        self.active_keys.clear()
        self.active_mouse_buttons.clear()
        self.RECORDING_FILE = os.path.join(os.getcwd(), "AHK" , f"{self.FILE_PREFIX}.txt")
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
            on_move=self.on_mouse_move)

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
    def ahk_listener(self):
        print(f"Program ready. Press {self.START_STOP_KEY} to start recording.")
        with self as listener:
            pass
        return True