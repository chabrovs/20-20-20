"""
This module contains base class for a sound function.
"""

from abc import ABC, abstractmethod


class BaseSound(ABC):
    """Interface for Sound masters classes.

    A sound master is an object that makes sound, for example,
        when the timer counts down to 0.
    """

    @abstractmethod
    def make_sys_sound(self) -> None:
        """Makes a simple system sound."""

        raise NotImplementedError()

    def start_sound(self) -> int:
        """Start a long last sound."""

        raise NotImplementedError("Coming soon!")

    def stop_sound(self) -> int:
        """Start the long last sound."""

        raise NotImplementedError("Coming soon!")
