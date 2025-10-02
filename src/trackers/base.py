"""
This module contains base class for an activity tracker.
"""


from abc import ABC, abstractmethod


class ActivityTracker(ABC):
    """Interface for Activity Tracker classes.

    An activity tracker is an object that tracks user's activity,
        for example, mouse movement, keyboard presses, etc.
    """

    @abstractmethod
    def is_active(self) -> bool:
        """Return True if user is active, False if idle"""

        raise NotImplementedError()

    @abstractmethod
    def get_idle_time_ms(self) -> float:
        """Return idle time in ms."""

        raise NotImplementedError()
