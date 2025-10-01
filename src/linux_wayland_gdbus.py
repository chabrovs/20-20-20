import tkinter as tk
import threading
import time
import platform
from pydbus import SessionBus
from gi.repository import GLib
import subprocess
from enum import Enum


# Sound handling
if platform.system() == "Windows":
    import winsound
else:
    from playsound import playsound


class WindowSettings(Enum):
    TITLE: str = "20-20-20 Eye Care Timer"
    HIGHT: int = 300
    WIDTH: int = 150
    FONT: tuple = ("Arial", 40, "bold")
    RESIZABLE: bool = False


class Settings(Enum):
    """ Timer settings Enum.

    :Attrs:
    :T_MINUTES: Timer in minutes.
    :I_MINUTES: Idle for N minutes. After idle for N minutes timer resets 
        to its T_MINUTES value.
    """
    T_MINUTES: int = 2
    I_MINUTES: int = 2


class EyeCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WindowSettings.TITLE.value)
        self.root.geometry(f"{WindowSettings.HIGHT.value}x{WindowSettings.WIDTH.value}")
        self.root.resizable(WindowSettings.RESIZABLE.value, WindowSettings.RESIZABLE.value)

        # Timer variables
        self.timer_seconds = Settings.T_MINUTES.value * 60  # 20 minutes
        self.running = True

        # GUI
        self.label = tk.Label(root, text="20:00", font=(WindowSettings.FONT.value))
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
        self.timer_seconds = Settings.T_MINUTES.value * 60
        self.update_display()

    def update_display(self):
        minutes, seconds = divmod(self.timer_seconds, 60)
        self.label.config(text=f"{minutes:02}:{seconds:02}")

    def play_sound(self):
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

            elif platform.system() == "Darwin":  # macOS
                playsound("/System/Library/Sounds/Glass.aiff")

            else:  # Linux / Ubuntu
                # Try system sound first
                subprocess.Popen(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])

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

            if idle_time >= Settings.I_MINUTES.value * 60:  # idle for 1+ minutes
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

