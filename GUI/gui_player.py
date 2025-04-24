import tkinter as tk
import os
from tkinter import ttk

from player.player import KeyboardMousePlayer


class GuiPlayer:
    def __init__(self, root, on_back_callback=None):
        self.root = root
        self.root.title("Player")
        self.on_back_callback = on_back_callback
        self.setup()

    def setup(self):
        ttk.Button(self.root, text="Load file", command=self.on_load).pack(pady=5)
        self.file_label = tk.Label(self.root, text="")
        self.file_label.pack(pady=5)
        tk.Label(self.root, text="Write file name").pack(pady=5)
        self.file_name = ttk.Entry(self.root, width=40)
        self.file_name.pack(pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Start", command=self.on_start).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Start Loop", command=self.on_start_loop).pack(side=tk.LEFT, padx=5)
        ttk.Button(text="Back", command=self.on_back).pack(side=tk.TOP, padx=5)

    def on_load(self):
        path = os.path.join(os.getcwd(), "RecordFiles")
        files = os.listdir(path)
        file_names = ''
        for file in files:
            file_names += file.split('.')[0] + ", "
        self.file_label.config(text=file_names)

    def on_start(self):
        self.file_name_str = self.file_name.get()
        self.root.destroy()
        play = KeyboardMousePlayer(self.file_name_str).play()

    def on_start_loop(self):
        self.file_name_str = self.file_name.get()
        self.root.destroy()
        play = KeyboardMousePlayer(self.file_name_str).play_loop()

    def on_back(self):
        self.root.destroy()
        if self.on_back_callback:
            self.on_back_callback()


def gui_player(on_back_callback=None):
    root = tk.Tk()
    app = GuiPlayer(root, on_back_callback)
    root.mainloop()


