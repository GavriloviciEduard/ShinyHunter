import os
import time

from shunter.abstract.abstract_shiny_hunter import AbstractShinyHunter


class ShinyHunterStarter(AbstractShinyHunter):
    def __init__(self, window_title: str = "epilogue"):
        AbstractShinyHunter.__init__(self, window_title, True)
        self.print_flag = True
        self.timeout = 6

    def start_loop(self):
        """Start the loop of the hunter."""

        self._pick_target_color_point()
        self._find_shiny_loop()

    def _pick_target_color_point(self) -> None:
        self.picker.mouse_listener.start()
        while not self.target_cp:
            if self.print_flag:
                print("Click to select target color point...")
                self.print_flag = False
            if self.picker.clicked:
                print("Picking target color and position...")
                self.target_cp = self.picker.pick_color()
                self.picker.clicked = False
                self.print_flag = True
        self.picker.mouse_listener.stop()

    def _find_shiny_loop(self) -> None:
        """Loop for finding a shiny."""
        os.system("cls")
        while not self.shiny_found and not self.stop:
            self.key_sim.press_reset()
            while not self.window_capture.contains_string("torchic", 3):
                self.key_sim.press_continue()
                time.sleep(1.5)
            start = time.time()
            while time.time() - start < 1:
                self.key_sim.press_right()
            self.key_sim.press_right()
            time.sleep(1)
            self.key_sim.press_continue()
            self.key_sim.press_continue()
            start = time.time()
            while time.time() - start < 4:
                self.key_sim.press_continue()
            time.sleep(1.5)
            self.shiny_found = self._check_shiny()
            if not self.shiny_found:
                self.soft_resets += 1
                self._display_current_status()
        if not self.stop:
            print(f"Shiny found after {self.soft_resets} soft resets!")
