import time

from shunter.abstract.abstract_shiny_hunter import AbstractShinyHunter


class ShinyHunterWild(AbstractShinyHunter):
    def __init__(self, window_title: str = "operator"):
        AbstractShinyHunter.__init__(self, window_title, True)
        self.target_pokemon_name = None
        self.target_pokemon_encounters = 0
        self.print_flag = True

    def start_loop(self):
        """Start the loop of the hunter."""

        self._pick_target_pokemon_name()
        self._pick_target_color_point()
        self._find_shiny_loop()

    def _pick_target_pokemon_name(self) -> None:
        # todo: add check that name exists
        while not self.target_pokemon_name:
            name = input("Enter target pokemon name: ")
            answer = input(f"Save this pokemon name {name}? ([Y]es/[N]o): ")
            if answer.lower() in ["y", "yes"]:
                self.target_pokemon_name = name

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

    def _target_pokemon_found(self) -> bool:
        return self.window_capture.contains_string(self.target_pokemon_name, 0)

    def _run_command_found(self) -> bool:
        return self.window_capture.contains_string("run", 3)

    def _find_shiny_loop(self) -> None:
        """Loop for finding a shiny."""
        
        # while not self._target_pokemon_found():
        #     self.key_sim.press_move()
        #     self.key_sim.press_alternate_continue()
        #     if not self._target_pokemon_found() and self._run_command_found():
        #         self.key_sim.press_run()
        
        # exit(0)
        
        time.sleep(10)
        self.window_capture._hide_window()

        while not self.shiny_found and not self.stop:
            self.key_sim.press_move()
            self.key_sim.press_alternate_continue()
            if self._target_pokemon_found():
                print(f"{self.target_pokemon_name} found! Checking if it's shiny...")
                self.target_pokemon_encounters += 1
                self.shiny_found = self._check_shiny()
            if not self.shiny_found and self._run_command_found():
                self.key_sim.press_run()
                self.soft_resets += 1
                self._display_current_status()
                print(f"{self.target_pokemon_name} encountered {self.target_pokemon_encounters} times")
        if not self.stop:
            print(f"Shiny found after {self.soft_resets} soft resets!")
        self.window_capture._show_window()
