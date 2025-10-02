"""
This module contains concrete implementations for the Linux Sound Master.

Linux processes system sounds in a distinct subprocess utilizing
    the `playsound`' library.
"""


from settings import SoundSettings
from src.sound.base import BaseSound


class SoundMaster(BaseSound):
    """ Sound master for Windows.

    The concrete implementation of the ``BaseSound`` class.
    Knows how to play sounds in Windows.
    """

    def __init__(self, winsound: ...):
        self.winsound = winsound

    def make_sys_sound(self) -> None:
        try:
            winsound.MessageBeep(self.winsound.MB_ICONEXCLAMATION)
        except Exception as e:
            print(f"Sound error: ({str(e)})")


if __name__ == "__main__":
    sound_master = SoundMaster()
    sound_master.make_sys_sound()
