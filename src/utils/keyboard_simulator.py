import ctypes
import time

from utils.keys_config import KeysConfig

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
PostMessage = ctypes.windll.user32.PostMessageW


class KeyboardSimulator:
    def __init__(self, hwnds):
        self.keys_config = KeysConfig()
        self.hwnds = hwnds
        self.reset_key_combination = [
            self.keys_config.b,
            self.keys_config.select,
            self.keys_config.start,
            self.keys_config.a,
        ]

    def _press_key(self, keys: list[int], keydown: bool) -> None:
        """Press a list of keys.

        Args:
            keys (list[int]):Given list of keys to press
        """
        msg = WM_KEYDOWN if keydown else WM_KEYUP
        for hwnd in self.hwnds:
            for key in keys:
                PostMessage(hwnd, msg, key, 0)
                time.sleep(0.01)

    def press_continue(self) -> None:
        """Press the continue button."""

        self._press_key([self.keys_config.a], True)
        self._press_key([self.keys_config.a], False)

    def press_reset(self) -> None:
        """Press the key combination for reset."""
        self._press_key(self.reset_key_combination, True)
        self._press_key(self.reset_key_combination, False)
