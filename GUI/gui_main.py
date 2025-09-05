import tkinter as tk
from tkinter import ttk
from GUI.gui_record import gui_recording
from GUI.gui_player import gui_player


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("RIKBoard")
        self.setup()

    def setup(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Record", command=self.on_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Play", command=self.on_play).pack(side=tk.LEFT, padx=5)
        ttk.Button(text="Exit", command=self.on_exit).pack(side=tk.TOP, padx=5)

    def on_record(self):
        self.root.destroy()
        restart = gui_recording(on_back_callback=gui)
        if restart:
            gui()

    def on_play(self):
        self.root.destroy()
        restart = gui_player(on_back_callback=gui)
        if restart:
            gui()

    def on_exit(self):
        self.root.destroy()
        return False


def gui():
    root = tk.Tk()
    app = Gui(root)
    root.mainloop()

