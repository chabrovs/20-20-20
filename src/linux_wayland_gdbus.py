import tkinter as tk
import threading
import time
import platform
from pydbus import SessionBus
from gi.repository import GLib

# Sound handling
if platform.system() == "Windows":
    import winsound
else:
    from playsound import playsound


class EyeCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("20-20-20 Eye Care Timer")
        self.root.geometry("300x150")
        self.root.resizable(False, False)

        # Timer variables
        self.timer_seconds = 20 * 60  # 20 minutes
        self.running = True

        # GUI
        self.label = tk.Label(root, text="20:00", font=("Arial", 40, "bold"))
        self.label.pack(expand=True)

        # Connect to DBus IdleMonitor
        self.bus = SessionBus()
        self.idle_monitor = self.bus.get(
            "org.gnome.Mutter.IdleMonitor",
            "/org/gnome/Mutter/IdleMonitor/Core"
        )

        # Start background timer
        threading.Thread(target=self.update_timer, daemon=True).start()

    def reset_timer(self):
        self.timer_seconds = 20 * 60
        self.update_display()

    def update_display(self):
        minutes, seconds = divmod(self.timer_seconds, 60)
        self.label.config(text=f"{minutes:02}:{seconds:02}")

    def play_sound(self):
        try:
            if platform.system() == "Windows":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            else:
                playsound("/System/Library/Sounds/Glass.aiff")
        except Exception as e:
            print("Sound error:", e)

    def get_idle_time(self):
        """Return idle time in seconds via GNOME Mutter IdleMonitor DBus"""
        try:
            idle_ms = self.idle_monitor.GetIdletime()
            print(f"idle for={idle_ms / 1000.0}")
            return idle_ms / 1000.0
        except Exception as e:
            print("DBus error:", e)
            return 0

    def update_timer(self):
        while self.running:
            idle_time = self.get_idle_time()

            if idle_time >= 60:  # idle for 1+ minutes
                self.reset_timer()
            else:
                if self.timer_seconds > 0:
                    self.timer_seconds -= 1
                else:
                    self.play_sound()
                    self.reset_timer()

            self.update_display()
            time.sleep(1)


if __name__ == "__main__":
    root = tk.Tk()
    app = EyeCareApp(root)
    root.mainloop()

