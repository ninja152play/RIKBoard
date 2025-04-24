import tkinter as tk
from tkinter import ttk

from record.AHK import AHKRecord
from record.keyboard import Keyboard
from record.keyboard_mouse import KeyboardMouse


class GuiRecord:
    def __init__(self, root, on_back_callback=None):
        self.root = root
        self.root.title("Record")
        self.on_back_callback = on_back_callback
        self.setup()

    def setup(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Keyboard", command=self.on_keyboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Keyboard and Mouse", command=self.on_keyboard_and_mouse).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="AHK", command=self.on_ahk).pack(side=tk.TOP, padx=5)
        ttk.Button(text="Back", command=self.on_back).pack(side=tk.TOP, padx=5)

    def on_keyboard(self):
        self.root.destroy()
        gui_keyboard()


    def on_keyboard_and_mouse(self):
        self.root.destroy()
        gui_keyboard_mouse()

    def on_ahk(self):
        self.root.destroy()
        gui_ahk()

    def on_back(self):
        self.root.destroy()
        if self.on_back_callback:
            self.on_back_callback()


def gui_recording(on_back_callback=None):
    root = tk.Tk()
    app = GuiRecord(root, on_back_callback)
    root.mainloop()


class GuiKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard")
        self.setup()

    def setup(self):
        ttk.Label(self.root, text="Select key to record start/stop (f1-f12)\n Key standard: 'f9'").pack(pady=15)
        self.key = ttk.Entry(self.root, width=20)
        self.key.pack(pady=10)

        self.name = ttk.Label(self.root, text="Write the name of the entry")
        self.name.pack(pady=15)
        self.entry_name = ttk.Entry(self.root, width=20)
        self.entry_name.pack(pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Start", command=self.on_start).pack(side=tk.TOP, padx=10)
        ttk.Button(button_frame, text="Back", command=self.on_back).pack(side=tk.BOTTOM, padx=10)

    def on_start(self):
        self.key_str = self.key.get().lower()
        self.entry_name_str = self.entry_name.get()
        if self.key_str == "":
            self.key_str = "f9"
        if self.entry_name_str != "":
            self.root.destroy()
            restart = Keyboard(self.key_str, self.entry_name_str).keyboard_listener()
            if restart:
                gui_keyboard()
        else:
            self.name.config(text="Error: write the name!")

    def on_back(self):
        self.root.destroy()
        gui_recording()


def gui_keyboard():
    root = tk.Tk()
    app = GuiKeyboard(root)
    root.mainloop()


class GuiKeyboardMouse:
    def __init__(self, root):
        self.root = root
        self.root.title("KeyboardMouse")
        self.setup()

    def setup(self):
        ttk.Label(self.root, text="Select key to record start/stop (f1-f12)\n Key standard: 'f9'").pack(pady=15)
        self.key = ttk.Entry(self.root, width=20)
        self.key.pack(pady=10)

        self.name = ttk.Label(self.root, text="Write the name of the entry")
        self.name.pack(pady=15)
        self.entry_name = ttk.Entry(self.root, width=20)
        self.entry_name.pack(pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Start", command=self.on_start).pack(side=tk.TOP, padx=10)
        ttk.Button(button_frame, text="Back", command=self.on_back).pack(side=tk.BOTTOM, padx=10)

    def on_start(self):
        self.key_str = self.key.get().lower()
        self.entry_name_str = self.entry_name.get()
        if self.key_str == "":
            self.key_str = "f9"
        if self.entry_name_str != "":
            self.root.destroy()
            restart = KeyboardMouse(self.key_str, self.entry_name_str).keyboard_mouse_listener()
            if restart:
                gui_keyboard_mouse()
        else:
            self.name.config(text="Error: write the name!")

    def on_back(self):
        self.root.destroy()
        gui_recording()


def gui_keyboard_mouse():
    root = tk.Tk()
    app = GuiKeyboardMouse(root)
    root.mainloop()


class GuiAHK:
    def __init__(self, root):
        self.root = root
        self.root.title("AHK")
        self.setup()

    def setup(self):
        ttk.Label(self.root, text="Write your horizontal in pixels").pack(pady=15)
        self.x = ttk.Entry(self.root, width=20)
        self.x.pack(pady=10)

        ttk.Label(self.root, text="Write your vertical in pixels").pack(pady=15)
        self.y = ttk.Entry(self.root, width=20)
        self.y.pack(pady=10)

        ttk.Label(self.root, text="Select key to record start/stop (f1-f12)\n Key standard: 'f9'").pack(pady=15)
        self.key = ttk.Entry(self.root, width=20)
        self.key.pack(pady=10)

        self.name = ttk.Label(self.root, text="Write the name of the entry")
        self.name.pack(pady=15)
        self.entry_name = ttk.Entry(self.root, width=20)
        self.entry_name.pack(pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Start", command=self.on_start).pack(side=tk.TOP, padx=10)
        ttk.Button(button_frame, text="Back", command=self.on_back).pack(side=tk.BOTTOM, padx=10)

    def on_start(self):
        self.key_str = self.key.get().lower()
        self.entry_name_str = self.entry_name.get()
        x = self.x.get()
        y = self.y.get()
        if x == "":
            x = 1920
        else:
            x = int(x)
        if y == "":
            y = 1080
        else:
            y = int(y)
        if self.key_str == "":
            self.key_str = "f9"
        if self.entry_name_str != "":
            self.root.destroy()
            restart = AHKRecord(self.key_str, self.entry_name_str, x, y).ahk_listener()
            if restart:
                gui_ahk()
        else:
            self.name.config(text="Error: write the name!")

    def on_back(self):
        self.root.destroy()
        gui_recording()


def gui_ahk():
    root = tk.Tk()
    app = GuiAHK(root)
    root.mainloop()
