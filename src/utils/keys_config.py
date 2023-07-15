import configparser
from os.path import abspath, dirname


class KeysConfig:
    """Class used to map application keys."""

    def __init__(self):
        parent_dir = dirname(dirname(dirname(abspath(__file__))))
        parser = configparser.ConfigParser()
        with open(f"{parent_dir}/config/key_config.ini", "r") as config_file:
            parser.read_file(config_file)
            self.a = parser.getint("KeyMapping", "a_alias")
            self.b = parser.getint("KeyMapping", "b_alias")
            self.up = parser.getint("KeyMapping", "up_alias")
            self.down = parser.getint("KeyMapping", "down_alias")
            self.left = parser.getint("KeyMapping", "left_alias")
            self.right = parser.getint("KeyMapping", "right_alias")
            self.start = parser.getint("KeyMapping", "start_alias")
            self.select = parser.getint("KeyMapping", "select_alias")
