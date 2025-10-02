"""
This module contains concrete implementations for the Linux Sound Master.

Linux processes system sounds in a distinct subprocess utilizing
    the `playsound`' library.
"""


import subprocess

from settings import Settings, SoundSettings
from src.sound.base import BaseSound


class SoundMaster(BaseSound):
    """ Sound master for Linux.

    The concrete implementation of the ``BaseSound`` class.
    Knows how to play sounds in Linux.
    """

    def make_sys_sound(self) -> None:
        if Settings.DEBUG.value:
            print(f"[DEBUG](SoundMaster): make_sys_sound was called.")

        try:
            with subprocess.Popen([
                "paplay",
                SoundSettings.LINUX_SHORT_SOUND_PATH.value
            ]):
                pass
        except Exception as e:
            print(f"Sound error: ({str(e)})")


if __name__ == "__main__":
    sound_master = SoundMaster()
    sound_master.make_sys_sound()
