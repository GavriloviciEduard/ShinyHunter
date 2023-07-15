from enum import Enum


class ShinyHunterType(Enum):
    stationary = "stationary"
    wild = "wild"
    starter = "starter"

    def __str__(self):
        return self.value
