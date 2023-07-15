import os

from shunter.abstract.abstract_shiny_hunter import AbstractShinyHunter


class ShinyHunterStationary(AbstractShinyHunter):
    def __init__(self):
        AbstractShinyHunter.__init__(self)
        self.reference_cp = None  # value must not change

    def start_loop(self):
        """Start the loop of the hunter."""

        self._pick_color_points_loop()
        self._find_shiny_loop()

    def _color_points_picked(self) -> bool:
        """Check if target point and reference point are picked.

        Returns:
            bool: True if both points are picked, false otherwise.
        """

        return self.reference_cp and self.target_cp

    def _reference_color_found(self) -> bool:
        """Check if reference color is found.
        If the reference color is found and the target color has not changed,
        we must reset the game to search further.

        Returns:
            bool: True if the reference color is found, false otherwise.
        """

        return self.reference_cp.color == self.window_capture.get_pixel(*self.reference_cp.point)

    def _pick_color_points(self) -> None:
        """Pick target color point first and then the reference color point."""

        if not self.reference_cp:
            print("Picking reference color and position...")
            self.reference_cp = self.picker.pick_color()
            if self.reference_cp:
                return
        if not self.target_cp and not self.picker.clicked or self.reference_cp:
            print("Picking target color and position...")
            self.target_cp = self.picker.pick_color()

    def _pick_color_points_loop(self) -> None:
        """Loop for picking needed color points (target and reference)."""

        print_flag = True
        self.picker.mouse_listener.start()
        while not self._color_points_picked():
            if print_flag:
                current = "target" if self.reference_cp else "reference"
                print(f"Click to select color point ({current})...")
                print_flag = False
            if self.picker.clicked:
                self._pick_color_points()
                self.picker.clicked = False
                print_flag = True
        self.picker.mouse_listener.stop()

    def _find_shiny_loop(self) -> None:
        """Loop for finding a shiny."""

        os.system("cls")
        import time

        time.sleep(5)
        while not self.shiny_found and not self.stop:
            self.key_sim.press_reset()
            while not self._reference_color_found() and not self.stop:
                self.key_sim.press_continue()
            time.sleep(0.2)
            self.shiny_found = self._check_shiny()
            if not self.shiny_found:
                self.soft_resets += 1
                self._display_current_status()
        if not self.stop:
            print(f"Shiny found after {self.soft_resets} soft resets!")
