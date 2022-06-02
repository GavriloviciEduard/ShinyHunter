from typing import Optional

from pynput import mouse

from utils.color_point import ColorPoint
from utils.window_capture import WindowCapture


class ColorPicker:
    def __init__(self, window_title: str):
        self.window_capture = WindowCapture(window_title)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        self.clicked = False
        self.current_x = -1
        self.current_y = -1

    def on_click(self, x: int, y: int, button, pressed: bool):
        """Mouse click listener.

        Args:
            x (int): x screen coordinate.
            y (int): y screen coordinate.
            button (pynput.backend.Button): Mouse button pressed.
            pressed (bool): Whether the button was pressed.
        """

        if button == button.left and pressed and not self.clicked:
            self.current_x, self.current_y = x, y
            self.clicked = True

    def pick_color(self) -> Optional[ColorPoint]:
        """Try to pick a color.

        Returns:
            Optional[ColorPoint]: Picked ColorPoint if selected, None otherwise.
        """

        pixel = self.window_capture.get_pixel(self.current_x, self.current_y)
        answer = input(f"Save this color{str(pixel)} and position{self.current_x, self.current_y}? ([Y]es/[N]o): ")
        if answer.lower() == "y" or answer.lower() == "yes":
            return ColorPoint(pixel, (self.current_x, self.current_y))
        return None
