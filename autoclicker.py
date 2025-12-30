import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
import webbrowser
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key

class AutoclickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Autoclicker Pro")
        self.root.geometry("350x480")
        self.root.resizable(False, False)

        # --- Variables ---
        self.clicking = False
        self.running = True
        self.mouse = Controller()
        
        self.cps_var = tk.DoubleVar(value=10.0)
        self.button_var = tk.StringVar(value="Left")
        self.hotkey_var = tk.StringVar(value="s")
        self.status_var = tk.StringVar(value="Status: Idle")
        
        self.recording_hotkey = False
        self.hotkey_code = KeyCode.from_char('s')

        # Links
        self.feedback_url = "https://docs.google.com/forms/d/e/1FAIpQLSc4DCHERaBeH79YgTZr20faBUSvtMiQWTJDIU0JlOYbUh1YyQ/viewform?usp=dialog"
        self.help_url = "https://docs.google.com/forms/d/e/1FAIpQLSf0_nx8zAgSlapfneT0lQKcMER2yVmVvppCmH8rZYQFLp6BCw/viewform?usp=publish-editor"

        self.setup_ui()
        
        # Start the background clicker thread
        self.click_thread = threading.Thread(target=self.click_worker, daemon=True)
        self.click_thread.start()

        # Start the keyboard listener
        self.keyboard_listener = Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # Top bar for Help button
        top_bar = ttk.Frame(self.root)
        top_bar.pack(fill=tk.X, padx=10, pady=5)

        # Help Menu Button
        help_btn = ttk.Menubutton(top_bar, text="Help ▾")
        help_menu = tk.Menu(help_btn, tearoff=0)
        help_menu.add_command(label="Help", command=lambda: webbrowser.open(self.help_url))
        help_menu.add_command(label="Feedback", command=lambda: webbrowser.open(self.feedback_url))
        help_btn["menu"] = help_menu
        help_btn.pack(side=tk.RIGHT)

        # Main Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        ttk.Label(main_frame, text="Autoclicker Settings", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # CPS Setting
        ttk.Label(main_frame, text="Clicks Per Second (CPS):").pack(anchor="w")
        cps_spin = ttk.Spinbox(main_frame, from_=1, to=100, textvariable=self.cps_var)
        cps_spin.pack(fill=tk.X, pady=5)

        # Mouse Button Selection
        ttk.Label(main_frame, text="Mouse Button:").pack(anchor="w", pady=(10, 0))
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        ttk.Radiobutton(btn_frame, text="Left Click", variable=self.button_var, value="Left").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(btn_frame, text="Right Click", variable=self.button_var, value="Right").pack(side=tk.LEFT, padx=5)

        # Hotkey Setting
        ttk.Label(main_frame, text="Toggle Hotkey:").pack(anchor="w", pady=(10, 0))
        self.hotkey_btn = ttk.Button(main_frame, textvariable=self.hotkey_var, command=self.start_recording)
        self.hotkey_btn.pack(fill=tk.X, pady=5)
        ttk.Label(main_frame, text="(Click button then press a key)", font=("Segoe UI", 8, "italic")).pack()

        # Status & Instructions
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Segoe UI", 10, "bold"), foreground="#0078d7")
        status_label.pack(pady=20)

        ttk.Label(main_frame, text="Press the hotkey anytime to Start/Stop", wraplength=250).pack()

    def start_recording(self):
        self.recording_hotkey = True
        self.hotkey_var.set("Press any key...")
        self.status_var.set("Status: Recording Key...")

    def on_key_press(self, key):
        if self.recording_hotkey:
            self.hotkey_code = key
            # Format the key name for display
            key_name = str(key).replace("'", "").replace("Key.", "")
            self.hotkey_var.set(key_name)
            self.recording_hotkey = False
            self.status_var.set("Status: Idle")
            return

        # Toggle Logic
        if key == self.hotkey_code:
            self.clicking = not self.clicking
            if self.clicking:
                self.status_var.set("Status: CLICKING...")
            else:
                self.status_var.set("Status: Idle")

    def click_worker(self):
        while self.running:
            if self.clicking:
                try:
                    btn = Button.left if self.button_var.get() == "Left" else Button.right
                    self.mouse.click(btn, 1)
                    # Avoid division by zero
                    delay = 1.0 / max(self.cps_var.get(), 0.1)
                    time.sleep(delay)
                except Exception:
                    pass
            else:
                time.sleep(0.1)

    def on_close(self):
        self.running = False
        self.clicking = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam') 
    app = AutoclickerApp(root)
    root.mainloop()