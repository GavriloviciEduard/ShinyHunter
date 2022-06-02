class ColorPoint:
    """Class used for storing color points."""

    color: tuple[int, int, int]
    point: tuple[int, int]

    def __init__(self, color: tuple[int, int, int], point: tuple[int, int]):
        self.color = color
        self.point = point

    def __eq__(self, other):
        return self.color == other.color and self.point == other.point

    def __str__(self):
        return "Color: " + str(self.color) + ", Point: " + str(self.point)
