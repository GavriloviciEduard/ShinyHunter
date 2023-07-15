import contextlib
import os
from abc import ABC, abstractmethod
from datetime import datetime

from pynput import keyboard

from utils.color_point_picker import ColorPointPicker
from utils.keyboard_simulator import KeyboardSimulator
from utils.window_capture import WindowCapture


class AbstractShinyHunter(ABC):
    def __init__(self, window_title: str = "operator", ocr_on: bool = False):
        self.soft_resets = 0
        self.stop = False
        self.shiny_found = False
        self.target_cp = None
        self.start_time = datetime.now()
        self.window_capture = WindowCapture(window_title, ocr_on)
        self.picker = ColorPointPicker(self.window_capture.get_pixel)
        self.key_sim = KeyboardSimulator(self.window_capture.hwnd)
        self.listener = keyboard.Listener(on_press=self._on_exit)
        self.listener.start()

    @abstractmethod
    def start_loop(self) -> None:
        """Start the loop of the hunter. Abstract method."""
        raise NotImplementedError

    @abstractmethod
    def _find_shiny_loop(self) -> None:
        # todo: doc
        raise NotImplementedError

    def _check_shiny(self) -> bool:
        """Compare the target color with the current color of the target point.
        If the color at the same position has changed, we have found a shiny.

        Returns:
            bool: True if shiny found, false otherwise.
        """
        print("Target color point", self.target_cp)
        pixel = self.window_capture.get_pixel(*self.target_cp.point)
        print("Current pixel", pixel)
        return self.target_cp.color != pixel

    def _display_current_status(self):
        """Display the current status of the hunter.
        Status: the time since the hunter started, the number of soft resets."""

        os.system("cls")
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

        # todo: fix not working while entering data
        with contextlib.suppress(AttributeError):
            if key.char == "q":
                print("Exiting...")
                self.stop = True
