"""
This module contains factory methods to instantiate a required
    'BaseSound' instance.

Methods:
    - get_sound_master
"""

from .base import BaseSound
from src.sound import linux, windows


def get_sound_master(
    system: str,
    session: str | None = None
) -> BaseSound:
    """
    A factory method to get a master sound instance based on the
        user's platform.

    :Parameters:
    :system: ``<class str>``: A name of a platform
        (e.g., "Linux", "Windows").
    :session: ``<class str>``: Linux session. Required only
        if the system=="Linux".
    """

    match system.capitalize():
        case "Linux":
            return linux.SoundMaster()
        case "Windows":
            import winsound as ws
            return windows.SoundMaster(winsound=ws)
        case "Darwin":
            raise NotImplementedError("Coming soon!")
        case _:
            raise ValueError(
                "Supported options are Windows, Linux, Darwin"
            )


if __name__ == "__main__":
    sound_master = get_activity_tracker("Linux")
    print(sound_master)
