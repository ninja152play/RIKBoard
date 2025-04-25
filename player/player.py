import threading
import json
import time
import os
from pynput import keyboard, mouse


class KeyboardMousePlayer:
    def __init__(self, filename, key_switch):
        self.filename = os.path.join(os.getcwd(), "RecordFiles", f"{filename}.json")
        self.keyboard = keyboard.Controller()
        self.mouse = mouse.Controller()
        self.events = []
        self._load_events()
        self.is_playing = False
        self.stop_key = getattr(keyboard.Key, key_switch.lower())

    def _load_events(self):
        """Загружает все события из файла в память"""
        self.events = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    event = json.loads(line.strip())
                    if 'metadata' not in event:
                        self.events.append(event)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

        self.events.sort(key=lambda e: e['time'])

    def _parse_key(self, key_str):
        """Преобразует строковое представление клавиши в объект pynput"""
        try:
            if key_str.startswith('Key.'):
                return getattr(keyboard.Key, key_str[4:])
            elif key_str.startswith("'") and key_str.endswith("'"):
                return key_str[1:-1]  # Обычный символ в кавычках
            else:
                # Пробуем преобразовать как обычный символ
                return key_str if len(key_str) == 1 else None
        except Exception:
            return None

    def _parse_button(self, button_str):
        """Преобразует строковое представление кнопки мыши"""
        try:
            if button_str.startswith('Button.'):
                return getattr(mouse.Button, button_str[7:])
            return None
        except Exception:
            return None

    def _execute_event(self, event):
        """Выполняет одно событие"""
        try:
            event_type = event['type']
            action = event['action']

            if event_type == 'keyboard':
                key = self._parse_key(event['key'])
                if key is None:
                    print(f"Неизвестная клавиша: {event['key']}")
                    return

                if action == 'press':
                    self.keyboard.press(key)
                elif action == 'release':
                    self.keyboard.release(key)

            elif event_type == 'mouse':
                if action == 'move':
                    self.mouse.position = (event['x'], event['y'])
                elif action in ['press', 'release']:
                    button = self._parse_button(event['button'])
                    if button:
                        if action == 'press':
                            self.mouse.press(button)
                        else:
                            self.mouse.release(button)
                elif action == 'scroll':
                    self.mouse.scroll(event['dx'], event['dy'])
        except Exception as e:
            print(f"Ошибка при выполнении события: {e}")

    def _stop_listener(self):
        """Слушатель клавиши для остановки"""

        def on_press(key):
            if key == self.stop_key:
                self.is_playing = False
                print("Воспроизведение остановлено!")
                return False  # Останавливаем слушатель

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def play(self, speed=1.0):
        """Воспроизводит запись с заданной скоростью"""
        self.is_playing = True
        stop_thread = threading.Thread(target=self._stop_listener, daemon=True)
        stop_thread.start()

        time.sleep(3)
        if not self.events:
            print("Нет событий для воспроизведения.")
            return

        start_time = self.events[0]['time']
        prev_time = start_time

        for event in self.events:
            if not self.is_playing:
                break
            current_time = event['time']
            delay = (current_time - prev_time) / speed
            if delay > 0:
                time.sleep(delay)

            self._execute_event(event)
            prev_time = current_time


    def play_loop(self, speed=1.0):
        """Воспроизводит запись с заданной скоростью"""
        time.sleep(3)
        self.is_playing = True
        while self.is_playing:
            self.play(speed)