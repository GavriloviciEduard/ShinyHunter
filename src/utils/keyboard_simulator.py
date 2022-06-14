import time

from pywinauto import application

from utils.keys_config import KeysConfig


class KeyboardSimulator:
    def __init__(self, hwnd):
        self.keys_config = KeysConfig()
        self.keyboard = application.Application().connect(handle=hwnd)
        self.reset_key_combination = [
            self.keys_config.b,
            self.keys_config.select,
            self.keys_config.start,
            self.keys_config.a,
        ]

    def _press_key(self, keys: list[str]) -> None:
        """Press a list of keys.

        Args:
            keys (list[str]):Given list of keys to press
        """

        self.keyboard.window().type_keys("".join(keys))
        time.sleep(0.1)

    def press_continue(self) -> None:
        """Press the continue button."""

        self._press_key([f"{{{self.keys_config.a} down}}"])
        self._press_key([f"{{{self.keys_config.a} up}}"])

    def press_reset(self) -> None:
        """Press the key combination for reset."""

        for key in self.reset_key_combination:
            self._press_key([f"{{{key} down}}"])
        for key in self.reset_key_combination:
            self._press_key([f"{{{key} up}}"])
