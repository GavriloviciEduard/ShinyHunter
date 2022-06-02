import argparse

from shunter.stationary import ShinyHunterStationary
from shunter.type import ShinyHunterType


def parse_hunter_type() -> ShinyHunterType:
    """Parse the command line arguments and returns the type of hunter to use.

    Returns:
        ShinyHunterType: Shiny hunter type to use.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--hunter",
        type=ShinyHunterType,
        choices=list(ShinyHunterType),
        help="Type of shiny hunter to use",
    )
    arguments = parser.parse_args()
    if not arguments.hunter:
        raise TypeError("Please specify the type of shiny hunter.")
    return arguments.hunter


def main():
    shiny_hunter = None
    hunter_type = parse_hunter_type()
    if hunter_type == ShinyHunterType.stationary:
        shiny_hunter = ShinyHunterStationary()
    shiny_hunter.start_loop()


if __name__ == "__main__":
    main()
