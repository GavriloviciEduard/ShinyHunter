import time
from typing import Optional

import mss
import win32com.client
import win32gui


class WindowCapture:
    def __init__(self, window_title: str):
        self.hwnd = self.get_hwnd_from_title(window_title)
        self.sct = mss.mss()
        if not self.hwnd:
            raise Exception(f"{window_title} not running")

    def focus_window(self):
        """Make sure the window if visible and focused."""

        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")
        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(0.1)

    def get_pixel(self, screen_x: int, screen_y: int) -> tuple[int, int, int]:
        """Get pixel at given screen coordinates.

        Args:
            screen_x (int): x coordinate of pixel.
            screen_y (int): y coordinate of pixel.

        Returns:
            tuple[int, int, int]: The pixel value as (R, G, B).
        """

        self.focus_window()
        pixel_box = {"top": screen_y, "left": screen_x, "width": 1, "height": 1}
        return self.sct.grab(pixel_box).pixel(0, 0)

    @staticmethod
    def get_hwnd_from_title(window_title: str) -> Optional[int]:
        """Get window handle from a given title.

        Args:
            window_title (str): Given window title.
        """

        def _window_callback(hwnd, all_windows):
            all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        windows = []
        win32gui.EnumWindows(_window_callback, windows)
        hwnds = [hwnd for hwnd, title in windows if window_title.lower() in title.lower()]
        return hwnds[0] if len(hwnds) else None
