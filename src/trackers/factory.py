"""
This module contains factory methods to instantiate a required
    'ActivityTracker' instance.

Methods:
    - get_activity_tracker
"""

from .base import ActivityTracker
from src.trackers import wayland


def get_activity_tracker(
    system: str,
    session: str | None = None
) -> ActivityTracker:
    """
    A factory method to get an activity tracker based on the
        user's platform.

    :Parameters:
    :system: ``<class str>``: A name of the platform
        (e.g., "Linux", "Windows").
    :session: ``<class str>``: Linux session. Required only
        if the system=="Linux".
    """

    match system.capitalize():
        case "Linux":
            if not session:
                from src.trackers import x11
                return x11.X11Tracker()

            if session.lower() == "wayland":
                return wayland.WaylandTracker()

        case "Windows":
            raise NotImplementedError("Coming soon!")
        case "Darwin":
            raise NotImplementedError("Coming soon!")
        case _:
            raise ValueError(
                "Supported options are Windows, Linux, Darwin"
            )


if __name__ == "__main__":
    tracker = get_activity_tracker("Linux", "wayland")
    print(tracker)
