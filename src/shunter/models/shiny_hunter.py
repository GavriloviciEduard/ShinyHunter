from enum import Enum


class ShinyHunterType(Enum):
    stationary = "stationary"

    def __str__(self):
        return self.value
