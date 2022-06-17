import time
from difflib import SequenceMatcher
from typing import Optional

import mss
import win32com.client
import win32gui

from utils.ocr import OCR


class WindowCapture:
    def __init__(self, window_title: str):
        self.hwnd = self.get_hwnd_from_title(window_title)
        self.sct = mss.mss()
        self.ocr = OCR()
        if not self.hwnd:
            raise Exception(f"{window_title} not running")

    def focus_window(self) -> None:
        """Make sure the window if visible and focused."""

        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")
        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(0.1)

    def get_window_rect(self, exclude_border: bool = True) -> list[int]:
        """_summary_

        Args:
            exclude_border (bool, optional): _description_. Defaults to True.

        Returns:
            list[int]: _description_
        """

        if not exclude_border:
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        else:
            left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
            left, top = win32gui.ClientToScreen(self.hwnd, (left, top))
            right, bottom = win32gui.ClientToScreen(self.hwnd, (right, bottom))
        return [left, top, right, bottom]

    def get_pixel(self, screen_x: int, screen_y: int) -> tuple[int, int, int]:
        """Get pixel at given screen coordinates.

        Args:
            screen_x (int): x coordinate of pixel.
            screen_y (int): y coordinate of pixel.

        Returns:
            tuple[int, int, int]: The pixel value as (R, G, B).
        """

        self.focus_window()
        pixel_box = {
            "top": screen_y,
            "left": screen_x,
            "width": 1,
            "height": 1,
        }
        return self.sct.grab(pixel_box).pixel(0, 0)

    def contains_string(self, target: str) -> bool:
        """Check if the window contains the given string.

        Args:
            target (str): Text to check for.
        """

        self.focus_window()
        rect = self.get_window_rect()
        win_box = {
            "top": rect[1],
            "left": rect[0],
            "width": rect[2] - rect[0],
            "height": rect[3] - rect[1],
        }
        win_sct = self.sct.grab(win_box)
        text = self.ocr.get_image_text(win_sct)
        for string in text:
            if string := string.lower().strip():
                ratio = SequenceMatcher(a=target, b=string).ratio()
                if ratio >= self.ocr.confidence_threshold:
                    return True
        return False

    @staticmethod
    def get_hwnd_from_title(window_title: str) -> Optional[int]:
        """Get window handle from a given title.

        Args:
            window_title (str): Given window title.
        """

        def _window_callback(hwnd, all_windows) -> None:
            all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        windows = []
        win32gui.EnumWindows(_window_callback, windows)
        hwnds = [hwnd for hwnd, title in windows if window_title.lower() in title.lower()]
        return hwnds[0] if len(hwnds) else None
