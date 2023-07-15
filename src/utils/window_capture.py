import ctypes
import time
from difflib import SequenceMatcher
from typing import Optional

import mss
import numpy as np
import win32com.client
import win32gui
from mss.screenshot import ScreenShot

from utils.ocr import OCR

SW_RESTORE = 9
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 32
WS_EX_TOOLWINDOW = 128
LWA_ALPHA = 0x00000002


class WindowCapture:
    def __init__(self, window_title: str, ocr_on: bool):
        self.ocr = None
        self.hwnd = self.get_hwnd_from_title(window_title)
        self.window_style = None
        self.user32 = ctypes.WinDLL("user32")
        if not self.hwnd:
            raise Exception(f"{window_title} not running")
        if ocr_on:
            self.ocr = OCR()

    def take_screenshot(self, box: dict, pixel: bool = False) -> ScreenShot:  # todo add pixel
        with mss.mss() as sct:
            sct.compression_level = 1
            screenshot = sct.grab(box)
            return screenshot.pixel(0, 0) if pixel else screenshot

    def get_window_rect(self, exclude_border: bool = True) -> list[int]:
        """# todo

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

    def split_screenshot(self, screenshot, pos: int):
        # todo
        m = screenshot.shape[0] // 2
        n = screenshot.shape[1] // 2
        return [
            screenshot[x : x + m, y : y + n]
            for x in range(0, screenshot.shape[0], m)
            for y in range(0, screenshot.shape[1], n)
        ][pos]

    def get_pixel(self, screen_x: int, screen_y: int) -> tuple[int, int, int]:
        """Get pixel at given screen coordinates.

        Args:
            screen_x (int): x coordinate of pixel.
            screen_y (int): y coordinate of pixel.

        Returns:
            tuple[int, int, int]: The pixel value as (R, G, B).
        """
        pixel_box = {
            "top": screen_y,
            "left": screen_x,
            "width": 1,
            "height": 1,
        }
        return self.take_screenshot(pixel_box, True)

    def contains_string(self, target: str, pos: int) -> bool:
        """Check if the window contains the given string.

        Args:
            target (str): Text to check for.
        """

        if not self.ocr:
            raise Exception("OCR is not enabled")

        rect = self.get_window_rect()
        win_box = {
            "top": rect[1],
            "left": rect[0],
            "width": rect[2] - rect[0],
            "height": rect[3] - rect[1],
        }
        win_sct = self.take_screenshot(win_box)
        text = self.ocr.get_image_text(self.split_screenshot(np.array(win_sct, dtype=np.uint8), pos))
        for string in text:
            if string := string.lower().strip():
                ratio = SequenceMatcher(a=target, b=string).ratio()
                if ratio >= self.ocr.confidence_threshold or target in string:
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

    def _show_window(self) -> None:
        """Show window by restoring its initial style."""

        self.user32.SetWindowLongA(
            self.hwnd,
            GWL_EXSTYLE,
            self.window_style,
        )

    def _hide_window(self) -> None:
        """Hide everything related to window while taking a screenshot."""

        self.window_style = self.user32.GetWindowLongA(
            self.hwnd,
            GWL_EXSTYLE,
        )
        self.user32.SetWindowLongA(
            self.hwnd,
            GWL_EXSTYLE,
            int(self.window_style) | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW,
        )
        # self.user32.SetLayeredWindowAttributes(
        #     self.hwnd,
        #     wintypes.COLORREF(0),
        #     0,
        #     LWA_ALPHA,
        # )
