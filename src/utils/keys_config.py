import configparser
from os.path import abspath, dirname


class KeysConfig:
    """Class used to map application keys."""

    def __init__(self):
        parent_dir = dirname(dirname(dirname(abspath(__file__))))
        parser = configparser.ConfigParser()
        with open(f"{parent_dir}/config/key_config.ini", "r") as config_file:
            parser.read_file(config_file)
            self.a = int(parser.get("WinKeyMapping", "a_alias"), 16)
            self.b = int(parser.get("WinKeyMapping", "b_alias"), 16)
            self.up = int(parser.get("WinKeyMapping", "up_alias"), 16)
            self.down = int(parser.get("WinKeyMapping", "down_alias"), 16)
            self.left = int(parser.get("WinKeyMapping", "left_alias"), 16)
            self.right = int(parser.get("WinKeyMapping", "right_alias"), 16)
            self.start = int(parser.get("WinKeyMapping", "start_alias"), 16)
            self.select = int(parser.get("WinKeyMapping", "select_alias"), 16)
