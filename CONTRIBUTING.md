# Contribution guidelines

First of all, thanks for thinking of contributing to this project. 💖

From here on, we assume you have the application up and running. Before creating a pull request, please make sure that you've tested everything thoroughly and you've run all the linting tools:

```py
python -m poetry run black .\src\ --check
python -m poetry run isort .\src\ --diff
python -m poetry run flake8 .\src\ --statistics
```

## Adding new dependencies 

To add new dependencies to the project, please check the <a href="https://python-poetry.org/docs/basic-usage/" target="_blank">Poetry documentation</a>.

## Utilities 

All utils cand be found in the [`utils`](src/utils) directory. Here you can contribute by improving or implementing stuff regarding:
  - [`Keyboard interaction with the GB Operator software`](src/utils/keyboard_simulator.py)
  - [`Retrieving image data from the GB Operator software`](src/utils/window_capture.py)
  - Whatever you can think of 

## Shiny hunters

The core source code for the shiny hunters can be found in the [`shunter`](src/shunter) directory. If you want to create a new shiny hunter you must implement the [`shiny hunter interface`](src/shunter/abstract/abstract_shiny_hunter.py) when doing so. You can extend the [`shiny hunter interface`](src/shunter/abstract/abstract_shiny_hunter.py), if needed, or create new interfaces in the [`abstract`](src/shunter/abstract) directory. If you want to create a data object, do it under the [`models`](src/shunter/models) directory by using [`pydantic`](https://pydantic-docs.helpmanual.io/). The newly created shiny hunter should be located in the [`shunter`](src/shunter) directory. The last step, to make the newly created shiny hunter available, is to add a new type in the [`ShinyHunterType class`](src/shunter/models/shiny_hunter.py) and expose it in [`main`](src/main.py):

```py
class ShinyHunterType(Enum):
    stationary = "stationary"
    new_shiny_hunter = "new_shiny_hunter"
```

```py
def main():
    shiny_hunter = None
    hunter_type = parse_hunter_type()
    if hunter_type == ShinyHunterType.stationary:
        shiny_hunter = ShinyHunterStationary()
    elif hunter_type == ShinyHunterType.new_shiny_hunter:
        shiny_hunter = NewShinyHunter()
    shiny_hunter.start_loop()
```

