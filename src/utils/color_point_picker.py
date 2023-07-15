from typing import Callable, Optional

from pynput import mouse

from utils.color_point import ColorPoint


class ColorPointPicker:
    def __init__(self, get_pixel: Callable):
        self.mouse_listener = mouse.Listener(on_click=self._on_click)
        self.get_pixel = get_pixel
        self.clicked = False
        self.current_x = -1
        self.current_y = -1

    def _on_click(self, x: int, y: int, button, pressed: bool) -> None:
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

        pixel = self.get_pixel(self.current_x, self.current_y)
        answer = input(f"Save this color{str(pixel)} and position{self.current_x, self.current_y}? ([Y]es/[N]o): ")
        if answer.lower() in ["y", "yes"]:
            return ColorPoint(pixel, (self.current_x, self.current_y))
        return None
