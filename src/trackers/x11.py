"""
This module contains concrete implementation for the X11 tracker.

Platform requirements:
    - python3.11.3 <=;

Pip requirements:
    - pygobject;
"""


import time

from pynput import keyboard, mouse

from settings import Settings
from src.trackers.base import ActivityTracker


class X11Tracker(ActivityTracker):
    def __init__(self):
        self.last_activity = time.time()
        ml = mouse.Listener(
            on_move=self.on_activity,
            on_click=self.on_activity,
            on_scroll=self.on_activity
        )
        kl = keyboard.Listener(
            on_press=self.on_activity
        )

    def on_activity(self, *args):
        """Update the last activity on any activity."""

        self.last_activity = time.time()

    def is_active(self) -> bool:
        """Return True if user is active, False if idle."""

        if Settings.DEBUG.value:
            idle_time = self.get_idle_time_s()
            print(
                f"[DEBUG]: idle_for={idle_time} sec. is_active="
                f"{idle_time <= Settings.I_MINUTES.value * 60}"
            )


        return (time.time() - self.last_activity) <= Settings.I_MINUTES

    def get_idle_time_ms(self) -> float:
        """Return idle time is ms according to DBus"""

        return time.time() - self.last_activity

    def get_idle_time_s(self) -> float:
        """Return idle time is s according to DBus"""

        return time.time() - self.last_activity / 1000.0
