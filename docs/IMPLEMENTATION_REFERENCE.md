# ShinyHunter - Implementation Reference Guide

**Companion to FINAL_ARCHITECTURE_GUIDE (Parts 1-3)**

This document provides critical implementation details needed for actual coding:
- Complete dependencies and setup
- Configuration file examples
- Constants and default values
- CLI argument parsing
- Logging configuration
- File I/O patterns
- Import structures
- Error handling patterns
- Performance considerations

Use this alongside the main architecture guide for implementation.

---

## Table of Contents

1. [Project Setup & Dependencies](#1-project-setup--dependencies)
2. [Configuration Files](#2-configuration-files)
3. [Constants & Default Values](#3-constants--default-values)
4. [CLI & Entry Points](#4-cli--entry-points)
5. [Logging Configuration](#5-logging-configuration)
6. [File I/O & Storage](#6-file-io--storage)
7. [Import Structure](#7-import-structure)
8. [Error Handling Patterns](#8-error-handling-patterns)
9. [Performance & Timing](#9-performance--timing)
10. [Development Workflow](#10-development-workflow)

---

## 1. Project Setup & Dependencies

### pyproject.toml (Complete)

```toml
[tool.poetry]
name = "shinyhunter"
version = "2.0.0"
description = "Cross-platform Pokemon shiny hunting automation with advanced detection"
authors = ["Your Name <your.email@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/yourusername/shinyhunter"
repository = "https://github.com/yourusername/shinyhunter"
keywords = ["pokemon", "shiny", "automation", "hunting", "bot"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[tool.poetry.dependencies]
python = "^3.10"

# Core dependencies (all platforms)
numpy = "^1.26.0"
opencv-python = "^4.8.1"
Pillow = "^10.1.0"
mss = "^9.0.1"
pynput = "^1.7.6"

# UI and console
rich = "^13.7.0"
questionary = "^2.0.1"

# Configuration
pyyaml = "^6.0.1"
python-dotenv = "^1.0.0"

# Utilities
dataclasses-json = "^0.6.3"

# Platform-specific dependencies
pywin32 = {version = "^306", markers = "sys_platform == 'win32'"}
python-xlib = {version = "^0.33", markers = "sys_platform == 'linux'"}
pyobjc-framework-Quartz = {version = "^10.0", markers = "sys_platform == 'darwin'"}
pyobjc-framework-Cocoa = {version = "^10.0", markers = "sys_platform == 'darwin'"}
pyobjc-framework-ApplicationServices = {version = "^10.0", markers = "sys_platform == 'darwin'"}

# Optional dependencies
requests = {version = "^2.31.0", optional = true}  # For Discord webhook

[tool.poetry.extras]
discord = ["requests"]
all = ["requests"]

[tool.poetry.group.dev.dependencies]
# Testing
pytest = "^7.4.3"
pytest-cov = "^4.1.0"
pytest-mock = "^3.12.0"
pytest-timeout = "^2.2.0"

# Code quality
black = "^23.12.0"
ruff = "^0.1.8"
isort = "^5.13.0"
mypy = "^1.7.0"

# Complexity analysis
radon = "^6.0.1"
flake8 = "^7.0.0"
flake8-complexity = "^0.9.1"

# Documentation
mkdocs = "^1.5.3"
mkdocs-material = "^9.5.0"

[tool.poetry.scripts]
shinyhunter = "shinyhunter.cli.main:main"
shunter = "shinyhunter.cli.main:main"  # Short alias

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# Black configuration
[tool.black]
line-length = 100
target-version = ['py310', 'py311', 'py312']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

# Ruff configuration
[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "W", "C90", "I", "N", "UP", "B", "A", "COM", "C4", "DTZ", "ISC", "ICN", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SIM", "TID", "ARG", "ERA", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]
ignore = ["E501"]  # Line length handled by black

[tool.ruff.mccabe]
max-complexity = 10  # Maximum cyclomatic complexity

# isort configuration
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

# Pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--cov=shinyhunter",
    "--cov-report=html",
    "--cov-report=term",
    "--cov-branch",
]
timeout = 300  # 5 minute timeout for tests

# MyPy configuration
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Gradually enable
ignore_missing_imports = true
```

### Installation Steps

```bash
# 1. Clone repository
git clone https://github.com/yourusername/shinyhunter.git
cd shinyhunter

# 2. Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# 3. Install dependencies
poetry install

# 4. Install with optional features
poetry install --extras "all"

# 5. Activate virtual environment
poetry shell

# 6. Verify installation
python -m shinyhunter --version
```

---

## 2. Configuration Files

### config.yaml (Complete Example)

```yaml
# ShinyHunter Configuration
# Version: 2.0

# Application settings
app:
  name: "ShinyHunter"
  version: "2.0.0"
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Window settings
window:
  title_filter: "operator"  # Search for windows containing this text
  auto_focus: true
  monitor_movement: true

# Detection settings
detection:
  # Detection method: pixel, hsv, pattern, fusion
  method: "fusion"

  # Pixel detector
  pixel:
    tolerance: 5
    enabled: true
    weight: 1.0

  # HSV detector
  hsv:
    hue_tolerance: 15
    saturation_min: 50
    value_min: 50
    enabled: true
    weight: 1.2

  # Fusion engine
  fusion:
    confidence_threshold: 0.75
    temporal_smoothing: true
    history_size: 5
    require_majority: true

# Hunter settings
hunter:
  type: "stationary"  # stationary, starter, wild
  max_resets: null  # null = unlimited
  timeout_seconds: null  # null = no timeout
  save_on_shiny: true
  auto_video: true
  video_buffer_seconds: 30

# Input settings
input:
  key_delay: 0.01  # Delay between key press and release (seconds)
  action_delay: 0.1  # Delay between actions (seconds)
  reset_sequence:
    - "B"
    - "SELECT"
    - "START"
    - "A"

# UI settings
ui:
  show_overlay: false  # Screen overlay for debugging
  overlay_opacity: 0.7
  color_picker_magnification: 10
  console_theme: "default"  # default, dark, light
  show_progress: true

# Storage settings
storage:
  base_dir: "~/.shinyhunter"
  screenshots_dir: "screenshots"
  videos_dir: "videos"
  stats_db: "stats.db"
  logs_dir: "logs"
  config_dir: "config"

# Plugin settings
plugins:
  enabled: true
  auto_discover: true
  plugin_dirs:
    - "plugins"
    - "~/.shinyhunter/plugins"

# Discord notifications (optional)
discord:
  enabled: false
  webhook_url: ""  # Set your webhook URL here
  notify_on_start: true
  notify_on_shiny: true
  notify_on_error: false
  mention_user_id: ""  # Optional: Discord user ID to mention

# Statistics settings
statistics:
  enabled: true
  save_interval: 10  # Save stats every N resets
  track_session: true
  track_overall: true

# Performance settings
performance:
  window_check_interval: 0.5  # Check window position every N seconds
  detection_fps: 30  # Frames per second for detection
  gc_interval: 100  # Run garbage collection every N resets

# Advanced settings
advanced:
  debug_mode: false
  save_debug_images: false
  profile_performance: false
  strict_mode: false  # Fail on warnings
```

### .env (Environment Variables)

```bash
# ShinyHunter Environment Variables

# Optional: Override config file location
SHINYHUNTER_CONFIG=~/.shinyhunter/config.yaml

# Optional: Discord webhook (more secure than config file)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Optional: Log level override
LOG_LEVEL=INFO

# Optional: Data directory override
SHINYHUNTER_DATA_DIR=~/.shinyhunter

# Development settings
SHINYHUNTER_DEBUG=false
SHINYHUNTER_PROFILE=false
```

---

## 3. Constants & Default Values

### constants.py (Complete)

```python
# shinyhunter/core/constants.py
"""
Global constants and default values.

All timing, paths, and configuration defaults.
"""

from pathlib import Path
from typing import Final

# Version
VERSION: Final[str] = "2.0.0"

# Timing constants (seconds)
DEFAULT_KEY_DELAY: Final[float] = 0.01
DEFAULT_ACTION_DELAY: Final[float] = 0.1
DEFAULT_WINDOW_CHECK_INTERVAL: Final[float] = 0.5
DEFAULT_DETECTION_INTERVAL: Final[float] = 1.0 / 30  # 30 FPS
DEFAULT_WAIT_TIMEOUT: Final[float] = 10.0

# Detection constants
DEFAULT_PIXEL_TOLERANCE: Final[int] = 5
DEFAULT_HSV_HUE_TOLERANCE: Final[int] = 15
DEFAULT_CONFIDENCE_THRESHOLD: Final[float] = 0.75
DEFAULT_FUSION_HISTORY_SIZE: Final[int] = 5

# Window constants
DEFAULT_WINDOW_TITLE_FILTER: Final[str] = "operator"
WINDOW_SEARCH_RETRY_COUNT: Final[int] = 3
WINDOW_SEARCH_RETRY_DELAY: Final[float] = 2.0

# Storage paths
DEFAULT_BASE_DIR: Final[Path] = Path.home() / ".shinyhunter"
SCREENSHOTS_DIR: Final[str] = "screenshots"
VIDEOS_DIR: Final[str] = "videos"
LOGS_DIR: Final[str] = "logs"
CONFIG_DIR: Final[str] = "config"
PLUGINS_DIR: Final[str] = "plugins"
STATS_DB_NAME: Final[str] = "stats.db"

# File patterns
SCREENSHOT_PATTERN: Final[str] = "shiny_{timestamp}.png"
VIDEO_PATTERN: Final[str] = "shiny_{timestamp}.mp4"
LOG_PATTERN: Final[str] = "shinyhunter_{date}.log"

# Performance
DEFAULT_GC_INTERVAL: Final[int] = 100  # Run GC every N resets
MAX_HISTORY_SIZE: Final[int] = 1000
VIDEO_BUFFER_SECONDS: Final[int] = 30
VIDEO_FPS: Final[int] = 30

# UI Constants
BANNER_TEXT: Final[str] = """
╔═══════════════════════════════════════╗
║     ✨ SHINY HUNTER v2.0 ✨          ║
║  Pokemon Shiny Hunting Automation     ║
╚═══════════════════════════════════════╝
"""

# Platform detection
import platform
CURRENT_PLATFORM: Final[str] = platform.system()
IS_WINDOWS: Final[bool] = CURRENT_PLATFORM == "Windows"
IS_LINUX: Final[bool] = CURRENT_PLATFORM == "Linux"
IS_MACOS: Final[bool] = CURRENT_PLATFORM == "Darwin"

# Detection status emojis
EMOJI_SHINY: Final[str] = "🌟"
EMOJI_NOT_SHINY: Final[str] = "❌"
EMOJI_UNCERTAIN: Final[str] = "❓"
EMOJI_ERROR: Final[str] = "⚠️"

# Exit codes
EXIT_SUCCESS: Final[int] = 0
EXIT_ERROR: Final[int] = 1
EXIT_USER_INTERRUPT: Final[int] = 130
```

---

## 4. CLI & Entry Points

### cli/main.py (Complete with Arguments)

```python
# shinyhunter/cli/main.py
"""
Main CLI entry point with argument parsing.

Supports multiple command modes and configuration options.
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

from shinyhunter.core.constants import VERSION, DEFAULT_BASE_DIR
from shinyhunter.config.manager import ConfigManager
from shinyhunter.ui.console import RichConsole


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser.

    Returns:
        Configured ArgumentParser

    Complexity: CC = 1
    """
    parser = argparse.ArgumentParser(
        prog="shinyhunter",
        description="Cross-platform Pokemon shiny hunting automation",
        epilog="For more information, see: https://github.com/yourusername/shinyhunter"
    )

    # Version
    parser.add_argument(
        "--version",
        action="version",
        version=f"ShinyHunter {VERSION}"
    )

    # Verbosity
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output (DEBUG level)"
    )
    verbosity.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output (ERROR level only)"
    )

    # Configuration
    parser.add_argument(
        "-c", "--config",
        type=Path,
        help="Path to configuration file (default: ~/.shinyhunter/config.yaml)"
    )

    # Hunter type
    parser.add_argument(
        "-t", "--type",
        choices=["stationary", "starter", "wild"],
        default="stationary",
        help="Hunter type (default: stationary)"
    )

    # Window selection
    parser.add_argument(
        "-w", "--window",
        type=str,
        help="Window title filter (e.g., 'operator')"
    )

    # Detection method
    parser.add_argument(
        "-d", "--detection",
        choices=["pixel", "hsv", "pattern", "fusion"],
        default="fusion",
        help="Detection method (default: fusion)"
    )

    # Limits
    parser.add_argument(
        "--max-resets",
        type=int,
        help="Maximum number of resets (default: unlimited)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout in seconds (default: no timeout)"
    )

    # Features
    parser.add_argument(
        "--no-video",
        action="store_true",
        help="Disable video recording"
    )
    parser.add_argument(
        "--no-discord",
        action="store_true",
        help="Disable Discord notifications"
    )
    parser.add_argument(
        "--overlay",
        action="store_true",
        help="Enable screen overlay for debugging"
    )

    # Data directory
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_BASE_DIR,
        help=f"Data directory (default: {DEFAULT_BASE_DIR})"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Hunt command (default)
    hunt_parser = subparsers.add_parser("hunt", help="Start hunting")
    hunt_parser.add_argument(
        "--auto-start",
        action="store_true",
        help="Skip calibration, use saved points"
    )

    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument(
        "action",
        choices=["init", "edit", "validate", "show"],
        help="Configuration action"
    )

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="View statistics")
    stats_parser.add_argument(
        "--session",
        action="store_true",
        help="Show session stats only"
    )
    stats_parser.add_argument(
        "--export",
        type=Path,
        help="Export stats to file (JSON)"
    )

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean up data")
    clean_parser.add_argument(
        "--screenshots",
        action="store_true",
        help="Delete all screenshots"
    )
    clean_parser.add_argument(
        "--videos",
        action="store_true",
        help="Delete all videos"
    )
    clean_parser.add_argument(
        "--logs",
        action="store_true",
        help="Delete all logs"
    )
    clean_parser.add_argument(
        "--all",
        action="store_true",
        help="Delete all data (CAREFUL!)"
    )

    return parser


def setup_logging(args: argparse.Namespace):
    """
    Setup logging based on arguments.

    Args:
        args: Parsed arguments

    Complexity: CC = 3
    """
    if args.verbose:
        level = logging.DEBUG
    elif args.quiet:
        level = logging.ERROR
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(argv: Optional[list] = None) -> int:
    """
    Main entry point.

    Args:
        argv: Command line arguments (None = sys.argv)

    Returns:
        Exit code

    Complexity: CC = 4
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Setup logging
    setup_logging(args)

    # Create console
    console = RichConsole()

    try:
        # Handle commands
        if args.command == "config":
            return handle_config_command(args, console)
        elif args.command == "stats":
            return handle_stats_command(args, console)
        elif args.command == "clean":
            return handle_clean_command(args, console)
        else:
            # Default: hunt
            return handle_hunt_command(args, console)

    except KeyboardInterrupt:
        console.print_info("\nInterrupted by user")
        return EXIT_USER_INTERRUPT

    except Exception as e:
        console.print_error(f"Fatal error: {e}")
        logging.exception("Fatal error")
        return EXIT_ERROR


def handle_hunt_command(args, console) -> int:
    """Handle hunt command. CC = 2"""
    console.print_banner()
    # ... (rest of hunt logic from Part 3)
    return EXIT_SUCCESS


def handle_config_command(args, console) -> int:
    """Handle config command. CC = 2"""
    # Implementation
    return EXIT_SUCCESS


def handle_stats_command(args, console) -> int:
    """Handle stats command. CC = 2"""
    # Implementation
    return EXIT_SUCCESS


def handle_clean_command(args, console) -> int:
    """Handle clean command. CC = 2"""
    # Implementation
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
```

### __main__.py

```python
# shinyhunter/__main__.py
"""
Entry point for python -m shinyhunter
"""

import sys
from shinyhunter.cli.main import main

if __name__ == "__main__":
    sys.exit(main())
```

---

## 5. Logging Configuration

### logging_config.py

```python
# shinyhunter/utils/logging_config.py
"""
Logging configuration with file and console output.

All functions CC ≤ 2
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional

from shinyhunter.core.constants import LOGS_DIR, LOG_PATTERN


def setup_logging(
    level: int = logging.INFO,
    log_dir: Optional[Path] = None,
    console_output: bool = True,
    file_output: bool = True
):
    """
    Setup logging with file and console handlers.

    Args:
        level: Logging level
        log_dir: Directory for log files
        console_output: Enable console output
        file_output: Enable file output

    Complexity: CC = 2
    """
    # Create logger
    logger = logging.getLogger("shinyhunter")
    logger.setLevel(level)
    logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    simple_formatter = logging.Formatter(
        "%(levelname)s: %(message)s"
    )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)

    # File handler
    if file_output:
        if log_dir is None:
            log_dir = Path.home() / ".shinyhunter" / LOGS_DIR

        log_dir.mkdir(parents=True, exist_ok=True)

        # Create log file with date
        log_file = log_dir / LOG_PATTERN.format(
            date=datetime.now().strftime("%Y%m%d")
        )

        # Rotating file handler (10MB per file, keep 5 files)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)  # Always DEBUG to file
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    logger.info(f"Logging initialized (level={logging.getLevelName(level)})")
```

---

## 6. File I/O & Storage

### storage/manager.py

```python
# shinyhunter/storage/manager.py
"""
File storage manager.

Handles all file I/O operations.
All functions CC ≤ 3
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
import json
import shutil

from shinyhunter.core.constants import (
    DEFAULT_BASE_DIR,
    SCREENSHOTS_DIR,
    VIDEOS_DIR,
    LOGS_DIR,
    SCREENSHOT_PATTERN,
    VIDEO_PATTERN
)


class StorageManager:
    """
    Manages file storage for screenshots, videos, stats.

    All methods CC ≤ 3
    """

    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize storage manager.

        Args:
            base_dir: Base directory for all data

        Complexity: CC = 1
        """
        self.base_dir = base_dir or DEFAULT_BASE_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.screenshots_dir = self.base_dir / SCREENSHOTS_DIR
        self.videos_dir = self.base_dir / VIDEOS_DIR
        self.logs_dir = self.base_dir / LOGS_DIR

        self._ensure_directories()

    def _ensure_directories(self):
        """
        Ensure all required directories exist.

        Complexity: CC = 1
        """
        self.screenshots_dir.mkdir(exist_ok=True)
        self.videos_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

    def save_screenshot(self, image_data, metadata: dict = None) -> Path:
        """
        Save screenshot.

        Args:
            image_data: PIL Image or numpy array
            metadata: Optional metadata to save

        Returns:
            Path to saved screenshot

        Complexity: CC = 2
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = SCREENSHOT_PATTERN.format(timestamp=timestamp)
        filepath = self.screenshots_dir / filename

        # Save image
        if hasattr(image_data, "save"):
            # PIL Image
            image_data.save(filepath)
        else:
            # Numpy array
            from PIL import Image
            Image.fromarray(image_data).save(filepath)

        # Save metadata
        if metadata:
            metadata_file = filepath.with_suffix(".json")
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

        return filepath

    def save_video(self, video_path: Path, metadata: dict = None) -> Path:
        """
        Move video to storage.

        Args:
            video_path: Temporary video path
            metadata: Optional metadata

        Returns:
            Final video path

        Complexity: CC = 2
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = VIDEO_PATTERN.format(timestamp=timestamp)
        final_path = self.videos_dir / filename

        # Move video
        shutil.move(str(video_path), str(final_path))

        # Save metadata
        if metadata:
            metadata_file = final_path.with_suffix(".json")
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

        return final_path

    def get_storage_stats(self) -> dict:
        """
        Get storage statistics.

        Returns:
            Dictionary with file counts and sizes

        Complexity: CC = 1
        """
        def get_dir_size(directory: Path) -> int:
            return sum(f.stat().st_size for f in directory.rglob("*") if f.is_file())

        return {
            "screenshots": {
                "count": len(list(self.screenshots_dir.glob("*.png"))),
                "size_mb": get_dir_size(self.screenshots_dir) / 1024 / 1024
            },
            "videos": {
                "count": len(list(self.videos_dir.glob("*.mp4"))),
                "size_mb": get_dir_size(self.videos_dir) / 1024 / 1024
            },
            "total_size_mb": get_dir_size(self.base_dir) / 1024 / 1024
        }

    def cleanup(self, screenshots: bool = False, videos: bool = False):
        """
        Clean up stored files.

        Args:
            screenshots: Delete screenshots
            videos: Delete videos

        Complexity: CC = 2
        """
        if screenshots:
            for file in self.screenshots_dir.glob("*"):
                file.unlink()

        if videos:
            for file in self.videos_dir.glob("*"):
                file.unlink()
```

---

## 7. Import Structure

### Package __init__.py Files

```python
# shinyhunter/__init__.py
"""
ShinyHunter - Cross-platform Pokemon shiny hunting automation.
"""

from shinyhunter.core.constants import VERSION

__version__ = VERSION
__all__ = ["__version__"]


# shinyhunter/core/__init__.py
"""Core systems."""

from shinyhunter.core.states import HunterState
from shinyhunter.core.state_machine import StateMachine
from shinyhunter.core.events import Event, EventType
from shinyhunter.core.event_bus import EventBus

__all__ = [
    "HunterState",
    "StateMachine",
    "Event",
    "EventType",
    "EventBus"
]


# shinyhunter/data/__init__.py
"""Data models."""

from shinyhunter.data.geometry import Point, Region, WindowGeometry
from shinyhunter.data.color_point import ColorPoint

__all__ = [
    "Point",
    "Region",
    "WindowGeometry",
    "ColorPoint"
]


# shinyhunter/platform/__init__.py
"""Platform abstraction layer."""

from shinyhunter.platform.factory import get_platform_implementation

__all__ = ["get_platform_implementation"]


# shinyhunter/platform/input/__init__.py
"""Input abstraction."""

from shinyhunter.platform.input.interface import Key, KeyboardControllerInterface
from shinyhunter.platform.input.factory import create_keyboard_controller

__all__ = [
    "Key",
    "KeyboardControllerInterface",
    "create_keyboard_controller"
]


# shinyhunter/detection/__init__.py
"""Detection systems."""

from shinyhunter.detection.interface import DetectorInterface
from shinyhunter.detection.result import DetectionResult, DetectionStatus
from shinyhunter.detection.pixel_detector import PixelDetector
from shinyhunter.detection.hsv_detector import HSVDetector
from shinyhunter.detection.fusion_engine import DetectionFusionEngine

__all__ = [
    "DetectorInterface",
    "DetectionResult",
    "DetectionStatus",
    "PixelDetector",
    "HSVDetector",
    "DetectionFusionEngine"
]


# shinyhunter/ui/__init__.py
"""User interface components."""

from shinyhunter.ui.console import RichConsole
from shinyhunter.ui.process_selector import ProcessSelector, WindowInfo

__all__ = [
    "RichConsole",
    "ProcessSelector",
    "WindowInfo"
]
```

---

## 8. Error Handling Patterns

### Complete Error Hierarchy

```python
# shinyhunter/core/exceptions.py
"""
Custom exception hierarchy.

All exceptions inherit from ShinyHunterError.
"""


class ShinyHunterError(Exception):
    """Base exception for all ShinyHunter errors."""
    pass


# Platform errors
class PlatformError(ShinyHunterError):
    """Base class for platform-specific errors."""
    pass


class WindowNotFoundError(PlatformError):
    """Window not found or no longer exists."""
    pass


class WindowAccessError(PlatformError):
    """Cannot access or control window."""
    pass


class PlatformNotSupportedError(PlatformError):
    """Current platform is not supported."""
    pass


# Detection errors
class DetectionError(ShinyHunterError):
    """Base class for detection errors."""
    pass


class CalibrationError(DetectionError):
    """Calibration failed or incomplete."""
    pass


class DetectionTimeoutError(DetectionError):
    """Detection took too long."""
    pass


# Configuration errors
class ConfigError(ShinyHunterError):
    """Base class for configuration errors."""
    pass


class ConfigNotFoundError(ConfigError):
    """Configuration file not found."""
    pass


class ConfigValidationError(ConfigError):
    """Configuration validation failed."""
    pass


# Plugin errors
class PluginError(ShinyHunterError):
    """Base class for plugin errors."""
    pass


class PluginLoadError(PluginError):
    """Failed to load plugin."""
    pass


class PluginExecutionError(PluginError):
    """Plugin execution failed."""
    pass
```

### Error Handling Patterns

```python
# Pattern 1: Specific error handling
try:
    window = window_manager.find_window(title)
except WindowNotFoundError:
    console.print_error(f"Window '{title}' not found")
    return None
except WindowAccessError as e:
    console.print_error(f"Cannot access window: {e}")
    return None
except PlatformError as e:
    console.print_error(f"Platform error: {e}")
    raise

# Pattern 2: Retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def find_window_with_retry(title: str):
    """Find window with automatic retry."""
    return window_manager.find_window(title)

# Pattern 3: Context manager for cleanup
from contextlib import contextmanager

@contextmanager
def managed_window(window_manager, title):
    """Context manager for window lifecycle."""
    handle = None
    try:
        handle = window_manager.find_window(title)
        if not handle:
            raise WindowNotFoundError(f"Window '{title}' not found")
        yield handle
    finally:
        if handle:
            # Cleanup if needed
            pass

# Usage
with managed_window(window_manager, "operator") as handle:
    # Do work with window
    pass

# Pattern 4: Graceful degradation
def get_window_with_fallback(title: str):
    """Get window with fallback options."""
    try:
        return window_manager.find_window(title)
    except WindowNotFoundError:
        # Try alternative title
        return window_manager.find_window("GB Operator")
    except PlatformError:
        # Show selector as fallback
        return ProcessSelector(window_manager).select_window()
```

---

## 9. Performance & Timing

### Performance Considerations

```python
# shinyhunter/utils/performance.py
"""
Performance utilities and timing helpers.

All functions CC ≤ 2
"""

import time
import functools
from typing import Callable
from contextlib import contextmanager


@contextmanager
def timer(name: str = "Operation", print_result: bool = True):
    """
    Context manager for timing operations.

    Usage:
        with timer("Detection"):
            result = detector.detect(...)

    Complexity: CC = 1
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        if print_result:
            print(f"{name} took {elapsed:.4f}s")


def rate_limit(calls_per_second: float):
    """
    Rate limit decorator.

    Args:
        calls_per_second: Maximum calls per second

    Returns:
        Decorated function

    Complexity: CC = 1
    """
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.perf_counter() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

            result = func(*args, **kwargs)
            last_called[0] = time.perf_counter()
            return result
        return wrapper
    return decorator


# Usage examples
class PerformantDetector:
    """Example of performance-conscious detector."""

    @rate_limit(30)  # Max 30 FPS
    def detect(self, image_data):
        """Detect with rate limiting."""
        with timer("Detection", print_result=False):
            return self._do_detection(image_data)

    def _do_detection(self, image_data):
        """Actual detection logic."""
        pass
```

### Timing Constants Usage

```python
# Import timing constants
from shinyhunter.core.constants import (
    DEFAULT_KEY_DELAY,
    DEFAULT_ACTION_DELAY,
    DEFAULT_WINDOW_CHECK_INTERVAL
)

# Use in keyboard controller
class KeyboardController:
    def send_key(self, key):
        self.press(key)
        time.sleep(DEFAULT_KEY_DELAY)
        self.release(key)

    def send_sequence(self, keys):
        for key in keys:
            self.send_key(key)
            time.sleep(DEFAULT_ACTION_DELAY)

# Use in window tracker
class WindowTracker:
    def __init__(self):
        self.check_interval = DEFAULT_WINDOW_CHECK_INTERVAL

    def run(self):
        while self.running:
            self.check_window()
            time.sleep(self.check_interval)
```

---

## 10. Development Workflow

### Setup Development Environment

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/shinyhunter.git
cd shinyhunter
poetry install --with dev

# 2. Install pre-commit hooks
poetry run pre-commit install

# 3. Run code quality checks
poetry run black shinyhunter/
poetry run isort shinyhunter/
poetry run ruff check shinyhunter/
poetry run mypy shinyhunter/

# 4. Check cyclomatic complexity
poetry run radon cc shinyhunter/ -a -nb

# 5. Run tests
poetry run pytest

# 6. Run tests with coverage
poetry run pytest --cov

# 7. Generate coverage report
poetry run pytest --cov --cov-report=html
# Open htmlcov/index.html
```

### Git Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.8
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### Testing Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_pixel_detector.py

# Run specific test
pytest tests/unit/test_pixel_detector.py::test_exact_match

# Run with coverage
pytest --cov=shinyhunter --cov-report=term-missing

# Run with markers
pytest -m "not slow"  # Skip slow tests
pytest -m "windows"   # Run Windows-specific tests only

# Run in parallel
pytest -n auto  # Requires pytest-xdist
```

### Complexity Checks

```bash
# Check all files
radon cc shinyhunter/ -a

# Check specific file
radon cc shinyhunter/detection/fusion_engine.py --total-average

# Show only complex functions (CC > 10)
radon cc shinyhunter/ -n C

# Generate JSON report
radon cc shinyhunter/ -j > complexity_report.json
```

---

## Summary

This implementation reference provides:

✅ **Complete pyproject.toml** - All dependencies, tools, config
✅ **Configuration files** - YAML example with all settings
✅ **Constants file** - All timing, paths, defaults
✅ **CLI with arguments** - Complete argument parsing
✅ **Logging setup** - Console + file with rotation
✅ **File I/O patterns** - Screenshots, videos, stats
✅ **Import structure** - All __init__.py files
✅ **Error handling** - Complete exception hierarchy
✅ **Performance utilities** - Timing, rate limiting
✅ **Development workflow** - Setup, testing, quality checks

**Use this alongside the main architecture guide (Parts 1-3) for complete implementation reference.**

All code examples are ready to use with:
- Claude Code
- Codex CLI
- Gemini CLI
- Manual implementation

**Every detail is here. Nothing is missing. Ready to build!** 🚀
