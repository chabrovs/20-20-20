"""
This module contains concrete implementation for the Wayland tracker.

Linux on Wayland does not let mouse tracking outside of the app's windows
    bounds. To address this issue, Linux suggest to use the DBus to check
    for how long the user was idle.
It's done by a simple Linux command, on the other hand, Python suggest
    a core concise and clean approach by utilizing the ``pybus`` library.

Platform requirements:
    - python3.11.3 <=;
    `sudo apt install python3-gi python3-pydbus gir1.2-glib-2.0`;

Pip requirements:
    - pygobject;
"""


import sys

from pydbus import SessionBus

from settings import Settings
from src.trackers.base import ActivityTracker


class WaylandTracker(ActivityTracker):
    def __init__(self):
        self.bus = SessionBus()
        self.idle_monitor = self.bus.get(
            "org.gnome.Mutter.IdleMonitor",
            "/org/gnome/Mutter/IdleMonitor/Core"
        )

    def is_active(self) -> bool:
        """Return True if user is active, False if idle."""

        try:
            idle_time = self.idle_monitor.GetIdletime() / 1000.0

            if Settings.DEBUG.value:
                print(
                        f"[DEBUG]: idle_for={idle_time} sec. is_active="
                        f"{idle_time <= Settings.I_MINUTES.value * 60}"
                )

            return idle_time <= Settings.I_MINUTES.value * 60
        except Exception as e:
            print(f"[ERROR]: DBUS error: ({e})")
            sys.exit(1)

    def get_idle_time_ms(self) -> float:
        """Return idle time is ms according to DBus"""

        return self.idle_monitor.GetIdletime()

    def get_idle_time_s(self) -> float:
        """Return idle time is s according to DBus"""

        return self.idle_monitor.GetIdletime() / 1000.0
