import argparse

from shunter.models.shiny_hunter import ShinyHunterType
from shunter.starter import ShinyHunterStarter
from shunter.stationary import ShinyHunterStationary
from shunter.wild import ShinyHunterWild


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
    elif hunter_type == ShinyHunterType.wild:
        shiny_hunter = ShinyHunterWild()
    elif hunter_type == ShinyHunterType.starter:
        shiny_hunter = ShinyHunterStarter()
    shiny_hunter.start_loop()


if __name__ == "__main__":
    main()
