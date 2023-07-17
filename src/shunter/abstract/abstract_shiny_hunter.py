import contextlib
from abc import ABC, abstractmethod
from datetime import datetime

from pynput import keyboard

from utils.color_point_picker import ColorPointPicker
from utils.keyboard_simulator import KeyboardSimulator


class AbstractShinyHunter(ABC):
    def __init__(self, window_title: str):
        self.soft_resets = 0
        self.stop = False
        self.shiny_found = False
        self.start_time = datetime.now()
        self.picker = ColorPointPicker(window_title)
        self.key_sim = KeyboardSimulator(self.picker.window_capture.get_hwnd_from_title(window_title, True))
        self.listener = keyboard.Listener(on_press=self._on_exit)
        self.listener.start()

    @abstractmethod
    def _check_shiny(self) -> bool:
        """Check if shiny was found. Abstract method."""
        raise NotImplementedError

    @abstractmethod
    def start_loop(self):
        """Start the loop of the hunter. Abstract method."""
        raise NotImplementedError

    def _display_current_status(self):
        """Display the current status of the hunter.
        Status: the time since the hunter started, the number of soft resets."""

        dif = datetime.now() - self.start_time
        time = divmod(dif.total_seconds(), 60)
        mins, secs = int(time[0]), round(time[1], 2)
        print(f"Reset... Soft resets: {self.soft_resets}, Time elapsed: {mins} minutes {secs} seconds")

    def _on_exit(self, key):
        """Keyboard pressed listener used for stopping app.
        App is stopped by pressing 'q' key.

        Args:
            key (pynput.backend.Key): Keyboard key pressed.
        """

        with contextlib.suppress(AttributeError):
            if key.char == "q":
                print("Exiting...")
                self.stop = True
