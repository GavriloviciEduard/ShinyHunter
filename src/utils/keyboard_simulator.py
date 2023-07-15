import ctypes
import time

import win32con
import win32api

from utils.keys_config import KeysConfig


class KeyboardSimulator:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.keys_config = KeysConfig()
        self.user32 = ctypes.WinDLL("user32")
        self.user32.SendMessageW.argtypes = (ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint)
        self.reset_key_combination = [
            self.keys_config.b,
            self.keys_config.select,
            self.keys_config.start,
            self.keys_config.a,
        ]
        self._press_key(win32con.WM_KEYDOWN, self.keys_config.b)

    def _press_key(self, direction: int, key: int) -> None:
        """Press a list of keys.

        Args:
            keys (list[str]):Given list of keys to press
        """

        self.user32.SendMessageW(self.hwnd, direction, key, 0)
        time.sleep(0.1)

    def press_continue(self, times: int = 1) -> None:
        """Press the continue button."""

        # Define the virtual key code for the x key
        x_key = 0x58

        # Press the x key down
        win32api.keybd_event(x_key, 0, 0, 0)

        # Release the x key
        win32api.keybd_event(x_key, 0, win32con.KEYEVENTF_KEYUP, 0)

    def press_alternate_continue(self, times: int = 1) -> None:
        """Press the continue button."""

        while times > 0:
            self._press_key(win32con.WM_KEYDOWN, self.keys_config.b)
            self._press_key(win32con.WM_KEYUP, self.keys_config.b)
            times -= 1

    def press_reset(self) -> None:
        """Press the key combination for reset."""
        # for key in self.reset_key_combination:
        #     self._press_key(win32con.WM_KEYDOWN, key)
        # for key in self.reset_key_combination:
        #     self._press_key(win32con.WM_KEYUP, key)
        # Get the current mouse position
        x, y = win32api.GetCursorPos()

        # Send a right-click event at the current mouse position
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(0.1)

    def press_run(self) -> None:
        """Press the run button."""

        self._press_key(win32con.WM_KEYDOWN, self.keys_config.right)
        self._press_key(win32con.WM_KEYUP, self.keys_config.right)
        self._press_key(win32con.WM_KEYDOWN, self.keys_config.down)
        self._press_key(win32con.WM_KEYUP, self.keys_config.down)
        self.press_continue(5)

    def press_move(self) -> None:
        """Press buttons to start encounter."""

        self._press_key(win32con.WM_KEYDOWN, self.keys_config.left)
        self._press_key(win32con.WM_KEYUP, self.keys_config.left)
        self._press_key(win32con.WM_KEYDOWN, self.keys_config.right)
        self._press_key(win32con.WM_KEYUP, self.keys_config.right)

    def press_start(self) -> None:
        self._press_key(win32con.WM_KEYDOWN, self.keys_config.start)
        self._press_key(win32con.WM_KEYUP, self.keys_config.start)

    def press_up(self) -> None:
        self._press_key(win32con.WM_KEYDOWN, self.keys_config.up)
        self._press_key(win32con.WM_KEYUP, self.keys_config.up)

    def press_down(self) -> None:
        self._press_key(win32con.WM_KEYDOWN, self.keys_config.down)
        self._press_key(win32con.WM_KEYUP, self.keys_config.down)

    def press_right(self) -> None:
        self._press_key(win32con.WM_KEYDOWN, self.keys_config.right)
        self._press_key(win32con.WM_KEYUP, self.keys_config.right)
