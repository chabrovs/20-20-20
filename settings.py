"""
This module contains settings for the project.

You can edit these setting to make the app for your needs!
"""


from enum import Enum


class WindowSettings(Enum):
    """ Window setting.

    This class contains constant for that are responsible 
        for appearance of the main window.
    
    :Attrs:
    :TITLE: Title of the window.
    :HIGHT: Hight of the window.
    :WIDTH: Width of the window.
    :FONT: (Fort, Size, Options).
    :RESIZABLE: makes the window resizable.
    """

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
    T_MINUTES: int = 1
    I_MINUTES: int = 2
    DEBUG: bool = True


class SoundSettings(Enum):
    """ Sound settings.
    
    :Attrs:
    :LINUX_SHORT_SOUND_PATH: path to short system sound in Linux.
        (usually stored in "/usr/share/sounds/*/stereo/*.oga"
        Example: "/usr/share/sounds/freedesktop/stereo/complete.oga"
    """

    LINUX_SHORT_SOUND_PATH: str = str(
            "/usr/share/sounds/sound-icons/xylofon.wav"
        )
