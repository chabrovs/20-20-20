"""
Application description:
"""


# pylint: disable=W0621


import os
import platform
import threading
import time
import tkinter as tk

from settings import Settings, WindowSettings
from src.sound.base import BaseSound
from src.sound.factory import get_sound_master
from src.trackers.base import ActivityTracker
from src.trackers.factory import get_activity_tracker


class EyeCareApp:
    def __init__(
        self, root,
        tracker: ActivityTracker,
        sound_master: BaseSound
    ):
        self.root = root
        self.root.title(WindowSettings.TITLE.value)
        self.root.geometry(
            f"{WindowSettings.HIGHT.value}x{WindowSettings.WIDTH.value}"
        )
        self.root.resizable(
            WindowSettings.RESIZABLE.value,
            WindowSettings.RESIZABLE.value
        )

        # Dependencies (Depend on Platform)
        self.tracker = tracker
        self.sound_master = sound_master

        # Timer variables
        self.timer_seconds = Settings.T_MINUTES.value * 60  # 20 minutes
        self.running = True

        # GUI
        self.label = tk.Label(
            root, text="20:00", font=(WindowSettings.FONT.value)
        )
        self.label.pack(expand=True)

        # Start background timer
        threading.Thread(target=self.update_timer, daemon=True).start()

    def reset_timer(self):
        self.timer_seconds = Settings.T_MINUTES.value * 60
        self.update_display()

    def update_display(self):
        minutes, seconds = divmod(self.timer_seconds, 60)
        self.label.config(text=f"{minutes:02}:{seconds:02}")

    def update_timer(self):
        while self.running:
            if not self.tracker.is_active():  # idle for 1+ minutes
                self.reset_timer()
            else:
                if self.timer_seconds > 0:
                    self.timer_seconds -= 1
                else:
                    self.sound_master.make_sys_sound()
                    self.reset_timer()

            self.update_display()
            time.sleep(1)


if __name__ == "__main__":
    root = tk.Tk()

    system: str = platform.system()
    session: str = os.environ.get("XDG_SESSION_TYPE", "")

    EyeCareApp(
        root, tracker=get_activity_tracker(system, session),
        sound_master=get_sound_master(system)
    )
    root.mainloop()
