import tkinter as tk
from tkinter import messagebox
import json
import os
import threading
import time
from pynput.mouse import Button, Controller
from pynput import keyboard


class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('AutoClicker Pro')
        self.root.geometry('300x200')
        self.root.config(bg='#2c3e50')
        self.root.iconbitmap('lib/icons/pointer_cursor_mouse_touch_click_hand_icon_250747.ico')

        self.config_file = "lib/autoclicker_config.json"
        self.running = False
        self.mouse = Controller()
        self.load_settings()

        self.setup_menu()
        self.create_widgets()

        self.listener = keyboard.Listener(on_press=self.handle_keypress)
        self.listener.start()
        
        self.scanning()

    def load_settings(self):
        """Loads keys from file or sets defaults."""
        defaults = {'start_key': 'f1', 'stop_key': 'f2'}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.settings = json.load(f)
            except:
                self.settings = defaults
        else:
            self.settings = defaults

    def save_settings(self, start_k, stop_k):
        """Writes settings to JSON and updates main display."""
        self.settings['start_key'] = start_k.lower()
        self.settings['stop_key'] = stop_k.lower()
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f)
        self.update_info_label()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Settings", command=self.open_settings_window)
        options_menu.add_separator()
        options_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Menu", menu=options_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        self.status_label = tk.Label(self.root, text="STATUS: IDLE",  font=("Arial", 14, "bold"), bg='#2c3e50', fg='white')
        self.status_label.pack(pady=10)

        self.info_label = tk.Label(self.root, text="", font=("Arial", 10), bg='#2c3e50', fg='#bdc3c7')
        self.info_label.pack(pady=5)
        self.update_info_label()

        btn_frame = tk.Frame(self.root, bg='#2c3e50')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Start Clicking", bg="#27ae60", fg="white",width=20, command=self.start_clicking).grid(row=0, column=0, pady=5)

        tk.Button(btn_frame, text="Stop Clicking", bg="#c0392b", fg="white",width=20, command=self.stop_clicking).grid(row=1, column=0, pady=5)

    def update_info_label(self):
        msg = f"Start: [{self.settings['start_key'].upper()}] | Stop: [{self.settings['stop_key'].upper()}]"
        self.info_label.config(text=msg)

    def scanning(self):
        """Your integrated logic: recursive loop using .after()"""
        if self.running:
            self.mouse.press(Button.left)
            time.sleep(0.001)
            self.mouse.release(Button.left)
        
        self.root.after(1, self.scanning)

    def start_clicking(self):
        self.running = True
        self.status_label.config(text="STATUS: CLICKING", fg="#2ecc71")

    def stop_clicking(self):
        self.running = False
        self.status_label.config(text="STATUS: IDLE", fg="white")

    def handle_keypress(self, key):
        """Global key listener logic."""
        try:
            k_name = ""
            if isinstance(key, keyboard.Key):
                k_name = key.name
            elif isinstance(key, keyboard.KeyCode):
                k_name = key.char

            if k_name == self.settings['start_key']:
                self.start_clicking()
            elif k_name == self.settings['stop_key']:
                self.stop_clicking()
        except AttributeError:
            pass

    def open_settings_window(self):
        """ Creates the settings popup. """
        settings_win = tk.Toplevel(self.root)
        settings_win.title("AutoClicker Settings")
        settings_win.geometry("350x180")
        settings_win.iconbitmap('lib/icons/pointer_cursor_mouse_touch_click_hand_icon_250747.ico')
        tk.Label(settings_win, text="Start Key (e.g. f1 or s):", font=("Open Sans", 11, "bold")).pack(pady=15, padx=5)
        start_ent = tk.Entry(settings_win)
        start_ent.insert(0, self.settings['start_key'])
        start_ent.pack()

        tk.Label(settings_win, text="Stop Key (e.g. f2 or q):", font=("Open Sans", 11, "bold")).pack(pady=5)
        stop_ent = tk.Entry(settings_win)
        stop_ent.insert(0, self.settings['stop_key'])
        stop_ent.pack()

        def apply():
            self.save_settings(start_ent.get(), stop_ent.get())
            settings_win.destroy()
            messagebox.showinfo("Settings", "Keys updated successfully!")

        tk.Button(settings_win, text="Save Settings File", command=apply, font=("Open Sans", 11, "bold"), background="Green", foreground="White", width=20, height=15).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()