import configparser
from os.path import abspath, dirname


class KeysConfig:
    """Class used to map application keys."""

    def __init__(self):
        parent_dir = dirname(dirname(dirname(abspath(__file__))))
        parser = configparser.ConfigParser()
        with open(f"{parent_dir}/config/key_config.ini", "r") as config_file:
            parser.read_file(config_file)
            self.a = parser.get("KeyMapping", "a_alias")
            self.b = parser.get("KeyMapping", "b_alias")
            self.up = parser.get("KeyMapping", "up_alias")
            self.down = parser.get("KeyMapping", "down_alias")
            self.left = parser.get("KeyMapping", "left_alias")
            self.right = parser.get("KeyMapping", "right_alias")
            self.start = parser.get("KeyMapping", "start_alias")
            self.select = parser.get("KeyMapping", "select_alias")
