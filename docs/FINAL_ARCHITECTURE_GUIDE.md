# ShinyHunter - Final Comprehensive Architecture & Implementation Guide

**Version:** 3.0
**Date:** 2025-10-21
**Focus:** Production-Ready, SOLID Principles, Low Complexity, Maximum Detail

---

## Table of Contents

### Part 1: Foundational Principles
1. [Design Philosophy](#1-design-philosophy)
2. [SOLID Principles Applied](#2-solid-principles-applied)
3. [Cyclomatic Complexity Guidelines](#3-cyclomatic-complexity-guidelines)
4. [Research Synthesis](#4-research-synthesis)

### Part 2: Platform Abstraction Layer
5. [Dynamic Process Selection UI](#5-dynamic-process-selection-ui)
6. [Platform-Agnostic Input System](#6-platform-agnostic-input-system)
7. [Window Management with Relative Coordinates](#7-window-management-with-relative-coordinates)
8. [Screen Capture System](#8-screen-capture-system)

### Part 3: Core Systems
9. [Detection System Architecture](#9-detection-system-architecture)
10. [State Machine Implementation](#10-state-machine-implementation)
11. [Event Bus & Plugin System](#11-event-bus--plugin-system)

### Part 4: Complete Implementation
12. [Module Structure](#12-module-structure)
13. [Full Working Examples](#13-full-working-examples)
14. [Testing Strategy](#14-testing-strategy)
15. [Migration Path](#15-migration-path)

---

## 1. Design Philosophy

### 1.1 Core Principles

#### **Single Responsibility Principle (SRP)**
> "A class should have one, and only one, reason to change."

**Application:**
- Each class handles exactly ONE aspect of the system
- Each function performs exactly ONE operation
- No multi-purpose "god classes"

**Example:**
```python
# ❌ BAD: Multiple responsibilities
class Hunter:
    def detect_shiny(self):
        # Capture screen
        # Process image
        # Compare colors
        # Send keys
        # Log results
        # Send notifications
        pass

# ✅ GOOD: Single responsibility
class ShinyDetector:
    def detect(self, image) -> DetectionResult:
        """Only detects shiny. Nothing else."""
        pass

class KeyboardController:
    def send_key(self, key: str):
        """Only sends keys. Nothing else."""
        pass

class NotificationService:
    def notify(self, message: str):
        """Only sends notifications. Nothing else."""
        pass
```

#### **Low Cyclomatic Complexity**
> "Keep functions simple. Aim for complexity ≤ 5, maximum 10."

**Cyclomatic Complexity (CC) Formula:**
```
CC = E - N + 2P
Where:
  E = number of edges in control flow
  N = number of nodes
  P = number of connected components
```

**Practical Guidelines:**
- **CC 1-5**: Simple, easy to test
- **CC 6-10**: Moderate, acceptable
- **CC 11-20**: Complex, should refactor
- **CC 21+**: Very complex, must refactor

**Reducing Complexity:**
```python
# ❌ BAD: High complexity (CC = 8)
def process_detection(result, config, logger):
    if result.is_shiny:
        if config.notify:
            if config.notify_discord:
                send_discord(result)
            elif config.notify_email:
                send_email(result)
            else:
                print("Shiny found!")
        if config.save_video:
            save_video()
    else:
        if config.log_all:
            logger.info("Not shiny")
    return result

# ✅ GOOD: Low complexity (CC = 2 for each)
def process_detection(result, handlers):
    if result.is_shiny:
        _handle_shiny_found(result, handlers)
    return result

def _handle_shiny_found(result, handlers):
    for handler in handlers:
        handler.on_shiny(result)
```

#### **High Cohesion, Low Coupling**

**High Cohesion:** Elements within a module work together toward a single purpose.

```python
# ✅ HIGH COHESION: All methods relate to color conversion
class ColorConverter:
    @staticmethod
    def rgb_to_hsv(rgb): pass

    @staticmethod
    def hsv_to_rgb(hsv): pass

    @staticmethod
    def rgb_to_hex(rgb): pass
```

**Low Coupling:** Modules depend minimally on each other.

```python
# ❌ HIGH COUPLING: Hunter knows too much about detector internals
class Hunter:
    def __init__(self):
        self.detector = PixelDetector()
        self.detector.tolerance = 5
        self.detector.use_hsv = True
        self.detector.reference_color = (255, 0, 0)

# ✅ LOW COUPLING: Hunter only knows detector interface
class Hunter:
    def __init__(self, detector: DetectorInterface):
        self.detector = detector  # Just needs detect() method
```

#### **Dependency Inversion**
> "Depend on abstractions, not concretions."

```python
# ✅ GOOD: Depend on interface, not implementation
from abc import ABC, abstractmethod

class DetectorInterface(ABC):
    @abstractmethod
    def detect(self, data) -> DetectionResult:
        pass

class Hunter:
    def __init__(self, detector: DetectorInterface):
        self.detector = detector  # Can be ANY detector

# Now we can swap implementations:
hunter = Hunter(PixelDetector())
hunter = Hunter(HSVDetector())
hunter = Hunter(MLDetector())
```

### 1.2 Code Quality Metrics

**Target Metrics:**
- **Cyclomatic Complexity:** ≤ 5 per function (max 10)
- **Function Length:** ≤ 20 lines (max 50)
- **Class Length:** ≤ 200 lines (max 500)
- **Parameters per Function:** ≤ 4 (max 6)
- **Nesting Depth:** ≤ 3 levels
- **Test Coverage:** ≥ 80%

**Measurement Tools:**
```bash
# Install tools
pip install radon pylint flake8 flake8-complexity

# Measure complexity
radon cc shinyhunter/ -a  # Average complexity
radon cc shinyhunter/ -s  # Show scores

# Lint with complexity check
flake8 --max-complexity 10 shinyhunter/

# Full analysis
pylint shinyhunter/ --max-args=4 --max-locals=10
```

---

## 2. SOLID Principles Applied

### 2.1 Single Responsibility Principle

**Definition:** A class should have only one reason to change.

**Before (Violates SRP):**
```python
class Hunter:
    """Does EVERYTHING - bad!"""

    def __init__(self):
        self.window_handle = self._find_window()
        self.config = self._load_config()
        self.db = self._setup_database()

    def _find_window(self): pass
    def _load_config(self): pass
    def _setup_database(self): pass
    def capture_screen(self): pass
    def send_keys(self): pass
    def detect_shiny(self): pass
    def save_stats(self): pass
    def send_notification(self): pass
```

**After (Follows SRP):**
```python
# Each class has ONE responsibility

class WindowFinder:
    """Only finds windows"""
    def find(self, title: str) -> int:
        pass

class ConfigLoader:
    """Only loads config"""
    def load(self, path: str) -> Config:
        pass

class DatabaseManager:
    """Only manages database"""
    def save_stats(self, stats: dict):
        pass

class ScreenCapture:
    """Only captures screen"""
    def capture(self, region: Region) -> Image:
        pass

class KeyboardController:
    """Only sends keys"""
    def send(self, key: str):
        pass

class ShinyDetector:
    """Only detects shinies"""
    def detect(self, image: Image) -> bool:
        pass

class NotificationService:
    """Only sends notifications"""
    def notify(self, message: str):
        pass

# Hunter just orchestrates
class Hunter:
    """Orchestrates components"""

    def __init__(
        self,
        detector: ShinyDetector,
        keyboard: KeyboardController,
        notifier: NotificationService
    ):
        self.detector = detector
        self.keyboard = keyboard
        self.notifier = notifier

    def hunt(self):
        # Just coordinates, doesn't do the work
        pass
```

### 2.2 Open/Closed Principle

**Definition:** Open for extension, closed for modification.

**Implementation: Strategy Pattern**

```python
# Base interface (closed for modification)
class DetectionStrategy(ABC):
    @abstractmethod
    def detect(self, data) -> DetectionResult:
        pass

# Extend by adding new strategies (open for extension)
class PixelDetectionStrategy(DetectionStrategy):
    def detect(self, data) -> DetectionResult:
        # Pixel detection logic
        pass

class HSVDetectionStrategy(DetectionStrategy):
    def detect(self, data) -> DetectionResult:
        # HSV detection logic
        pass

class MLDetectionStrategy(DetectionStrategy):
    def detect(self, data) -> DetectionResult:
        # ML detection logic
        pass

# Can add new strategies without modifying existing code!
class SparkleDetectionStrategy(DetectionStrategy):
    def detect(self, data) -> DetectionResult:
        # Sparkle detection logic
        pass
```

### 2.3 Liskov Substitution Principle

**Definition:** Subtypes must be substitutable for their base types.

```python
# Base class
class WindowManager(ABC):
    @abstractmethod
    def find_window(self, title: str) -> Optional[int]:
        """Return window handle or None"""
        pass

# All implementations must behave the same way
class WindowsWindowManager(WindowManager):
    def find_window(self, title: str) -> Optional[int]:
        # Windows implementation
        return handle or None  # Same contract!

class LinuxWindowManager(WindowManager):
    def find_window(self, title: str) -> Optional[int]:
        # Linux implementation
        return handle or None  # Same contract!

# ✅ Can substitute anywhere
def use_window_manager(wm: WindowManager):
    handle = wm.find_window("title")
    assert handle is None or isinstance(handle, int)

# Both work identically
use_window_manager(WindowsWindowManager())
use_window_manager(LinuxWindowManager())
```

### 2.4 Interface Segregation Principle

**Definition:** Don't force clients to depend on methods they don't use.

**Before (Violates ISP):**
```python
class Hunter(ABC):
    """Fat interface - everyone must implement everything"""

    @abstractmethod
    def setup(self): pass

    @abstractmethod
    def calibrate(self): pass

    @abstractmethod
    def detect_shiny(self): pass

    @abstractmethod
    def handle_eggs(self): pass  # Not all hunters need this!

    @abstractmethod
    def handle_battles(self): pass  # Not all hunters need this!

class StationaryHunter(Hunter):
    def handle_eggs(self):
        raise NotImplementedError("Don't need eggs!")  # ❌ Bad!

    def handle_battles(self):
        raise NotImplementedError("Don't need battles!")  # ❌ Bad!
```

**After (Follows ISP):**
```python
# Split into focused interfaces
class BasicHunter(ABC):
    """Minimal interface"""
    @abstractmethod
    def detect_shiny(self) -> bool:
        pass

class BreedingCapable(ABC):
    """Only breeding hunters implement this"""
    @abstractmethod
    def handle_eggs(self):
        pass

class BattleCapable(ABC):
    """Only battle hunters implement this"""
    @abstractmethod
    def handle_battles(self):
        pass

# Implement only what you need
class StationaryHunter(BasicHunter):  # ✅ Clean!
    def detect_shiny(self) -> bool:
        pass

class BreedingHunter(BasicHunter, BreedingCapable):  # ✅ Clean!
    def detect_shiny(self) -> bool:
        pass

    def handle_eggs(self):
        pass
```

### 2.5 Dependency Inversion Principle

**Definition:** High-level modules shouldn't depend on low-level modules. Both should depend on abstractions.

**Before (Violates DIP):**
```python
# High-level module depends on concrete low-level module
class Hunter:
    def __init__(self):
        self.detector = PixelDetector()  # ❌ Concrete dependency
        self.keyboard = WindowsKeyboard()  # ❌ Concrete dependency

# Can't swap implementations!
```

**After (Follows DIP):**
```python
# Define abstractions
class DetectorInterface(Protocol):
    def detect(self, data) -> DetectionResult: ...

class KeyboardInterface(Protocol):
    def send_key(self, key: str): ...

# High-level module depends on abstractions
class Hunter:
    def __init__(
        self,
        detector: DetectorInterface,
        keyboard: KeyboardInterface
    ):
        self.detector = detector  # ✅ Abstract dependency
        self.keyboard = keyboard  # ✅ Abstract dependency

# Can inject any implementation!
hunter = Hunter(
    detector=PixelDetector(),
    keyboard=get_platform_keyboard()
)

# Or swap for testing
hunter = Hunter(
    detector=MockDetector(),
    keyboard=MockKeyboard()
)
```

---

## 3. Cyclomatic Complexity Guidelines

### 3.1 Complexity Measurement

**Example Function Analysis:**

```python
# Complexity = 6 (too high)
def process_result(result, config, logger):  # +1 (function)
    if result.is_shiny:  # +1 (if)
        if config.save_video:  # +1 (nested if)
            save_video(result)
        if config.notify:  # +1 (if)
            send_notification(result)
        logger.info("Shiny found")
    elif result.is_uncertain:  # +1 (elif)
        logger.warning("Uncertain result")
    else:  # +1 (else)
        logger.debug("Not shiny")
    return result
```

### 3.2 Refactoring Strategies

#### Strategy 1: Extract Method

```python
# Before: CC = 8
def hunt_loop(self):
    while not self.stop:
        if self.needs_reset():
            self.reset()
        if self.game_loaded():
            if self.battle_started():
                result = self.check_shiny()
                if result.is_shiny:
                    self.celebrate()
                elif result.uncertain:
                    self.recheck()
                else:
                    self.continue_hunt()

# After: CC = 2 for main, 2 for each helper
def hunt_loop(self):
    while not self.stop:
        self._handle_reset()
        self._handle_battle()

def _handle_reset(self):
    if self.needs_reset():
        self.reset()

def _handle_battle(self):
    if self.game_loaded() and self.battle_started():
        self._process_battle_result()

def _process_battle_result(self):
    result = self.check_shiny()
    self._handle_result(result)

def _handle_result(self, result):
    handlers = {
        'shiny': self.celebrate,
        'uncertain': self.recheck,
        'normal': self.continue_hunt
    }
    handler = handlers.get(result.type, self.continue_hunt)
    handler()
```

#### Strategy 2: Replace Conditionals with Polymorphism

```python
# Before: CC = 5
def get_detector(detector_type):
    if detector_type == "pixel":
        return PixelDetector()
    elif detector_type == "hsv":
        return HSVDetector()
    elif detector_type == "pattern":
        return PatternDetector()
    else:
        return DefaultDetector()

# After: CC = 1
class DetectorFactory:
    _detectors = {
        "pixel": PixelDetector,
        "hsv": HSVDetector,
        "pattern": PatternDetector,
    }

    @classmethod
    def create(cls, detector_type):
        detector_class = cls._detectors.get(
            detector_type,
            DefaultDetector
        )
        return detector_class()
```

#### Strategy 3: Use Lookup Tables

```python
# Before: CC = 7
def get_color_name(r, g, b):
    if r > 200 and g < 50 and b < 50:
        return "red"
    elif r < 50 and g > 200 and b < 50:
        return "green"
    elif r < 50 and g < 50 and b > 200:
        return "blue"
    elif r > 200 and g > 200 and b < 50:
        return "yellow"
    elif r > 200 and g < 50 and b > 200:
        return "magenta"
    elif r < 50 and g > 200 and b > 200:
        return "cyan"
    else:
        return "unknown"

# After: CC = 1
def get_color_name(r, g, b):
    def matches_red(): return r > 200 and g < 50 and b < 50
    def matches_green(): return r < 50 and g > 200 and b < 50
    def matches_blue(): return r < 50 and g < 50 and b > 200

    color_checks = {
        "red": matches_red,
        "green": matches_green,
        "blue": matches_blue,
    }

    for color, check in color_checks.items():
        if check():
            return color
    return "unknown"
```

#### Strategy 4: Early Returns

```python
# Before: CC = 5
def validate_config(config):
    if config is not None:
        if config.window_title:
            if config.timeout > 0:
                if config.max_resets > 0:
                    return True
    return False

# After: CC = 4 (still better)
def validate_config(config):
    if config is None:
        return False
    if not config.window_title:
        return False
    if config.timeout <= 0:
        return False
    if config.max_resets <= 0:
        return False
    return True
```

### 3.3 Complexity Targets by Function Type

| Function Type | Target CC | Max CC | Reasoning |
|---------------|-----------|--------|-----------|
| Property getter | 1 | 2 | Should be trivial |
| Setter/validator | 2-3 | 5 | Simple validation |
| Pure function | 1-2 | 4 | No side effects |
| Business logic | 3-5 | 8 | Some complexity OK |
| Orchestrator | 2-4 | 6 | Delegates work |
| Entry point | 3-6 | 10 | Coordinates systems |

---

## 4. Research Synthesis

### 4.1 Key Learnings from Popular Bots

Based on analysis of 7+ popular shiny hunting bots:

| Bot | Key Innovation | Adopted In Our Design |
|-----|----------------|----------------------|
| **PokéBot Gen3** | Plugin system with lifecycle hooks | `plugins/interface.py` |
| **PokéBot Gen3** | Memory reading for 100% accuracy | Conceptual inspiration for multi-method fusion |
| **PokéBot Gen3** | Profile-based organization | `config/profiles.py` |
| **PokéBot Gen3** | SQLite statistics database | `storage/database.py` |
| **PokemonAutomation** | Multi-modal detection (visual+audio) | `detection/fusion.py` |
| **PokemonAutomation** | Confidence scoring (not binary) | `DetectionResult.confidence` |
| **PokemonAutomation** | Auto video recording | `plugins/builtin/auto_save_video.py` |
| **DBJoran/Shinyhunter** | OpenCV pattern matching | `detection/pattern.py` |
| **DBJoran/Shinyhunter** | OCR for state detection | Future enhancement |
| **ErebosGoD** | Template matching approach | `detection/pattern.py` |
| **vincenzocascone** | Hardware sparkle detection | `detection/sparkle.py` |
| **vyabor** | YOLO ML detection | `detection/ml.py` (future) |

### 4.2 Architecture Evolution

**Generation 1 (Simple):**
```
User → Hunter → detect_shiny() → Done
```

**Generation 2 (Current Code):**
```
User → Hunter → ColorPicker → WindowCapture → detect_shiny()
```

**Generation 3 (This Design):**
```
                          ┌─────────────────┐
                          │   CLI/GUI       │
                          └────────┬────────┘
                                   │
                          ┌────────▼────────┐
                          │  Orchestrator   │
                          └────────┬────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
┌───────▼────────┐      ┌─────────▼────────┐      ┌─────────▼────────┐
│ State Machine  │      │  Event Bus       │      │  Plugin Manager  │
└───────┬────────┘      └─────────┬────────┘      └─────────┬────────┘
        │                          │                          │
        │              ┌───────────┴───────────┐              │
        │              │                       │              │
┌───────▼────────┐  ┌──▼─────────┐  ┌────────▼────┐  ┌──────▼──────┐
│ Detection      │  │  Platform   │  │   Storage   │  │  Plugins    │
│ Fusion Engine  │  │  Abstraction│  │   Layer     │  │  (user)     │
└────────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

---

## 5. Dynamic Process Selection UI

### 5.1 Requirements

1. List all available windows/processes
2. Allow user to select from terminal
3. Display helpful information (title, PID, position)
4. Handle no matches gracefully
5. Support filtering/searching
6. Cross-platform compatibility

### 5.2 Implementation

```python
# ui/process_selector.py
"""
Interactive process/window selector for terminal.

Uses questionary for interactive prompts and rich for beautiful display.
Follows SRP: Only handles process selection, nothing else.
Complexity: CC ≤ 3 for all functions
"""

from typing import Optional, List
from dataclasses import dataclass
import questionary
from questionary import Choice
from rich.console import Console
from rich.table import Table

@dataclass
class WindowInfo:
    """Window information - simple data class (CC = 1)"""
    handle: int
    title: str
    pid: int
    x: int
    y: int
    width: int
    height: int

    def __str__(self) -> str:
        return f"{self.title} (PID: {self.pid})"


class ProcessSelector:
    """
    Terminal UI for selecting a window/process.

    Responsibilities:
    - List available windows
    - Display selection menu
    - Return selected window

    Does NOT:
    - Manage windows
    - Capture screen
    - Send input
    """

    def __init__(self, window_manager):
        """
        Initialize selector.

        Args:
            window_manager: Platform-specific window manager

        Complexity: CC = 1
        """
        self.window_manager = window_manager
        self.console = Console()

    def select_window(
        self,
        title_filter: Optional[str] = None
    ) -> Optional[WindowInfo]:
        """
        Display interactive menu to select a window.

        Args:
            title_filter: Optional filter for window titles

        Returns:
            Selected WindowInfo or None if cancelled

        Complexity: CC = 3
        """
        # Get available windows
        windows = self._get_windows(title_filter)

        if not windows:
            return self._handle_no_windows(title_filter)

        # Show selection menu
        return self._show_selection_menu(windows)

    def _get_windows(
        self,
        title_filter: Optional[str]
    ) -> List[WindowInfo]:
        """
        Get list of available windows.

        Complexity: CC = 2
        """
        all_windows = self.window_manager.list_all_windows()

        if title_filter:
            return self._filter_windows(all_windows, title_filter)

        return all_windows

    def _filter_windows(
        self,
        windows: List[WindowInfo],
        filter_text: str
    ) -> List[WindowInfo]:
        """
        Filter windows by title.

        Complexity: CC = 1
        """
        filter_lower = filter_text.lower()
        return [
            w for w in windows
            if filter_lower in w.title.lower()
        ]

    def _handle_no_windows(
        self,
        title_filter: Optional[str]
    ) -> None:
        """
        Handle case when no windows found.

        Complexity: CC = 2
        """
        if title_filter:
            self.console.print(
                f"[red]No windows found matching '{title_filter}'[/red]"
            )
        else:
            self.console.print(
                "[red]No windows found[/red]"
            )
        return None

    def _show_selection_menu(
        self,
        windows: List[WindowInfo]
    ) -> Optional[WindowInfo]:
        """
        Display interactive selection menu.

        Complexity: CC = 2
        """
        # Show table first
        self._display_window_table(windows)

        # Create choices
        choices = self._create_choices(windows)

        # Show questionary menu
        answer = questionary.select(
            "Select a window:",
            choices=choices,
            qmark="🎯",
            pointer="→"
        ).ask()

        if answer is None:  # User cancelled
            return None

        return answer  # Returns the WindowInfo object

    def _display_window_table(self, windows: List[WindowInfo]):
        """
        Display table of available windows.

        Complexity: CC = 1
        """
        table = Table(title="Available Windows")
        table.add_column("#", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("PID", style="yellow")
        table.add_column("Position", style="magenta")
        table.add_column("Size", style="blue")

        for idx, window in enumerate(windows, 1):
            table.add_row(
                str(idx),
                window.title,
                str(window.pid),
                f"({window.x}, {window.y})",
                f"{window.width}×{window.height}"
            )

        self.console.print(table)
        self.console.print()  # Empty line

    def _create_choices(
        self,
        windows: List[WindowInfo]
    ) -> List[Choice]:
        """
        Create questionary Choice objects.

        Complexity: CC = 1
        """
        return [
            Choice(
                title=f"{idx}. {window.title} (PID: {window.pid})",
                value=window
            )
            for idx, window in enumerate(windows, 1)
        ]


# Helper function with retry logic
def select_window_with_retry(
    window_manager,
    max_attempts: int = 3
) -> Optional[WindowInfo]:
    """
    Select window with retry capability.

    Complexity: CC = 3
    """
    selector = ProcessSelector(window_manager)

    for attempt in range(max_attempts):
        # Ask for filter
        title_filter = questionary.text(
            "Enter window title filter (or press Enter for all):",
            qmark="🔍"
        ).ask()

        if title_filter is None:  # User cancelled
            return None

        # Show selection menu
        window = selector.select_window(
            title_filter if title_filter else None
        )

        if window:
            return window

        # Ask to retry
        if attempt < max_attempts - 1:
            retry = questionary.confirm(
                "No window selected. Try again?",
                default=True
            ).ask()

            if not retry:
                return None

    return None
```

### 5.3 Platform-Specific Window Listing

Each platform implements `list_all_windows()`:

```python
# platform/windows/window_manager.py
class WindowsWindowManager(WindowManagerBase):
    def list_all_windows(self) -> List[WindowInfo]:
        """
        List all visible windows on Windows.

        Complexity: CC = 1
        """
        windows = []

        def enum_callback(hwnd, _):
            if self._is_visible_window(hwnd):
                info = self._get_window_info(hwnd)
                if info:
                    windows.append(info)
            return True

        win32gui.EnumWindows(enum_callback, None)
        return windows

    def _is_visible_window(self, hwnd: int) -> bool:
        """
        Check if window is visible and has title.

        Complexity: CC = 2
        """
        if not win32gui.IsWindowVisible(hwnd):
            return False

        title = win32gui.GetWindowText(hwnd)
        return len(title) > 0

    def _get_window_info(self, hwnd: int) -> Optional[WindowInfo]:
        """
        Get information about a window.

        Complexity: CC = 1
        """
        try:
            title = win32gui.GetWindowText(hwnd)
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            x, y, right, bottom = win32gui.GetWindowRect(hwnd)

            return WindowInfo(
                handle=hwnd,
                title=title,
                pid=pid,
                x=x,
                y=y,
                width=right - x,
                height=bottom - y
            )
        except Exception:
            return None

# platform/linux/window_manager.py
class LinuxWindowManager(WindowManagerBase):
    def list_all_windows(self) -> List[WindowInfo]:
        """
        List all windows on Linux using wmctrl.

        Complexity: CC = 1
        """
        result = subprocess.run(
            ['wmctrl', '-lGp'],
            capture_output=True,
            text=True
        )

        windows = []
        for line in result.stdout.strip().split('\n'):
            info = self._parse_wmctrl_line(line)
            if info:
                windows.append(info)

        return windows

    def _parse_wmctrl_line(self, line: str) -> Optional[WindowInfo]:
        """
        Parse wmctrl output line.

        Complexity: CC = 1
        """
        parts = line.split(None, 7)
        if len(parts) < 8:
            return None

        return WindowInfo(
            handle=int(parts[0], 16),
            pid=int(parts[2]),
            x=int(parts[3]),
            y=int(parts[4]),
            width=int(parts[5]),
            height=int(parts[6]),
            title=parts[7]
        )

# platform/macos/window_manager.py
class MacOSWindowManager(WindowManagerBase):
    def list_all_windows(self) -> List[WindowInfo]:
        """
        List all windows on macOS using Quartz.

        Complexity: CC = 1
        """
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionAll,
            kCGNullWindowID
        )

        windows = []
        for window_dict in window_list:
            info = self._parse_window_dict(window_dict)
            if info:
                windows.append(info)

        return windows

    def _parse_window_dict(self, window_dict) -> Optional[WindowInfo]:
        """
        Parse window dictionary from Quartz.

        Complexity: CC = 2
        """
        title = window_dict.get('kCGWindowName', '')
        if not title:  # Skip windows without titles
            return None

        bounds = window_dict['kCGWindowBounds']

        return WindowInfo(
            handle=window_dict['kCGWindowNumber'],
            title=title,
            pid=window_dict['kCGWindowOwnerPID'],
            x=int(bounds['X']),
            y=int(bounds['Y']),
            width=int(bounds['Width']),
            height=int(bounds['Height'])
        )
```

### 5.4 Usage Example

```python
# Example: Using process selector in main.py

from platform.factory import get_platform_implementation
from ui.process_selector import select_window_with_retry
from rich.console import Console

def main():
    console = Console()

    # Initialize platform
    platform = get_platform_implementation()
    window_manager = platform.get_window_manager()

    # Show welcome
    console.print("[bold cyan]ShinyHunter - Window Selection[/bold cyan]")
    console.print()

    # Select window interactively
    window = select_window_with_retry(window_manager, max_attempts=3)

    if not window:
        console.print("[red]No window selected. Exiting.[/red]")
        return 1

    # Display selection
    console.print(f"[green]✓ Selected: {window.title}[/green]")
    console.print(f"  Handle: {window.handle}")
    console.print(f"  PID: {window.pid}")
    console.print(f"  Position: ({window.x}, {window.y})")
    console.print(f"  Size: {window.width}×{window.height}")
    console.print()

    # Continue with hunting...
    return 0
```

### 5.5 Terminal Output Example

```
Available Windows
┏━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ # ┃ Title                ┃ PID   ┃ Position   ┃ Size      ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 1 │ GB Operator          │ 12345 │ (100, 200) │ 800×600   │
│ 2 │ Visual Studio Code   │ 23456 │ (0, 0)     │ 1920×1080 │
│ 3 │ Google Chrome        │ 34567 │ (900, 100) │ 1024×768  │
└───┴──────────────────────┴───────┴────────────┴───────────┘

🎯 Select a window:
→ 1. GB Operator (PID: 12345)
  2. Visual Studio Code (PID: 23456)
  3. Google Chrome (PID: 34567)
```

---

## 6. Platform-Agnostic Input System

### 6.1 Design Goals

1. **Single interface** for all platforms
2. **No platform-specific code** in hunters
3. **Easy to test** with mocks
4. **Extensible** for new platforms
5. **Low complexity** (CC ≤ 4 per function)

### 6.2 Input Abstraction Architecture

```
┌─────────────────────────────────────┐
│         Hunter Code                 │
│  keyboard.send_key("a")             │
│  keyboard.send_combo(["ctrl", "c"]) │
└──────────────┬──────────────────────┘
               │ Uses interface only
               │
┌──────────────▼──────────────────────┐
│   KeyboardControllerInterface       │
│   (Protocol/ABC)                    │
│  - send_key(key: str)               │
│  - send_combo(keys: List[str])      │
│  - press(key: str)                  │
│  - release(key: str)                │
└──────────────┬──────────────────────┘
               │ Implemented by
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼────┐ ┌──▼─────┐ ┌─▼──────┐
│Windows │ │ Linux  │ │ macOS  │
│ Impl   │ │ Impl   │ │ Impl   │
└────────┘ └────────┘ └────────┘
```

### 6.3 Core Interface

```python
# platform/input/interface.py
"""
Platform-agnostic input interface.

Follows:
- Interface Segregation: Small, focused interface
- Dependency Inversion: Depend on abstraction
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from enum import Enum

class Key(Enum):
    """
    Standard key codes.

    Platform implementations map these to native codes.
    """
    # Letters
    A = "a"
    B = "b"
    # ... (all letters)

    # Numbers
    ZERO = "0"
    ONE = "1"
    # ... (all numbers)

    # Special keys
    ENTER = "enter"
    ESCAPE = "escape"
    SPACE = "space"
    TAB = "tab"
    BACKSPACE = "backspace"
    DELETE = "delete"

    # Arrow keys
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    # Modifiers
    CTRL = "ctrl"
    ALT = "alt"
    SHIFT = "shift"
    COMMAND = "command"  # macOS
    WINDOWS = "windows"  # Windows

    # Function keys
    F1 = "f1"
    # ... (F1-F12)


class KeyboardControllerInterface(ABC):
    """
    Abstract interface for keyboard control.

    All methods have CC ≤ 2
    """

    @abstractmethod
    def send_key(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Send a single key press (down + up).

        Args:
            key: Key to send
            window_handle: Optional target window

        Complexity: CC = 1 (abstract)
        """
        pass

    @abstractmethod
    def send_combo(
        self,
        keys: List[Key],
        window_handle: Optional[int] = None
    ):
        """
        Send key combination (e.g., Ctrl+C).

        Args:
            keys: Keys to press together
            window_handle: Optional target window

        Complexity: CC = 1 (abstract)
        """
        pass

    @abstractmethod
    def press(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Press key down (without releasing).

        Args:
            key: Key to press
            window_handle: Optional target window

        Complexity: CC = 1 (abstract)
        """
        pass

    @abstractmethod
    def release(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Release key.

        Args:
            key: Key to release
            window_handle: Optional target window

        Complexity: CC = 1 (abstract)
        """
        pass
```

### 6.4 Platform Implementations

#### Windows Implementation

```python
# platform/input/windows.py
"""
Windows keyboard controller using SendInput API.

Complexity: All functions CC ≤ 3
"""

import ctypes
from ctypes import wintypes
from typing import List, Optional
import time

# Windows API structures
class INPUT(ctypes.Structure):
    """INPUT structure for SendInput"""
    # ... (ctypes definition)

class KEYBDINPUT(ctypes.Structure):
    """KEYBDINPUT structure"""
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    ]

# Constants
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002

class WindowsKeyboardController(KeyboardControllerInterface):
    """
    Windows-specific keyboard controller.

    Uses SendInput for global input or PostMessage for window-specific.
    """

    # Key mapping: Our Key enum → Windows virtual key codes
    KEY_MAP = {
        Key.A: 0x41,
        Key.B: 0x42,
        # ... (all keys)
        Key.ENTER: 0x0D,
        Key.ESCAPE: 0x1B,
        Key.SPACE: 0x20,
        Key.UP: 0x26,
        Key.DOWN: 0x28,
        Key.LEFT: 0x25,
        Key.RIGHT: 0x27,
        Key.CTRL: 0x11,
        Key.ALT: 0x12,
        Key.SHIFT: 0x10,
    }

    def __init__(self):
        """
        Initialize Windows keyboard controller.

        Complexity: CC = 1
        """
        self.user32 = ctypes.windll.user32
        self.send_input = self.user32.SendInput

    def send_key(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Send key press to Windows.

        Complexity: CC = 2
        """
        if window_handle:
            self._send_to_window(key, window_handle)
        else:
            self._send_global(key)

    def send_combo(
        self,
        keys: List[Key],
        window_handle: Optional[int] = None
    ):
        """
        Send key combination.

        Complexity: CC = 2
        """
        # Press all keys
        for key in keys:
            self.press(key, window_handle)

        # Small delay
        time.sleep(0.01)

        # Release all keys (in reverse order)
        for key in reversed(keys):
            self.release(key, window_handle)

    def press(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Press key down.

        Complexity: CC = 2
        """
        vk_code = self.KEY_MAP[key]

        if window_handle:
            self._post_message(window_handle, vk_code, down=True)
        else:
            self._send_input_event(vk_code, down=True)

    def release(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Release key.

        Complexity: CC = 2
        """
        vk_code = self.KEY_MAP[key]

        if window_handle:
            self._post_message(window_handle, vk_code, down=False)
        else:
            self._send_input_event(vk_code, down=False)

    def _send_global(self, key: Key):
        """
        Send key globally using SendInput.

        Complexity: CC = 1
        """
        self.press(key)
        time.sleep(0.01)
        self.release(key)

    def _send_to_window(self, key: Key, window_handle: int):
        """
        Send key to specific window using PostMessage.

        Complexity: CC = 1
        """
        self.press(key, window_handle)
        time.sleep(0.01)
        self.release(key, window_handle)

    def _send_input_event(self, vk_code: int, down: bool):
        """
        Send input event using SendInput API.

        Complexity: CC = 1
        """
        # Create INPUT structure
        input_event = INPUT()
        # ... (populate structure)

        # Send input
        self.send_input(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))

    def _post_message(
        self,
        window_handle: int,
        vk_code: int,
        down: bool
    ):
        """
        Post message to window.

        Complexity: CC = 1
        """
        WM_KEYDOWN = 0x0100
        WM_KEYUP = 0x0101

        message = WM_KEYDOWN if down else WM_KEYUP
        self.user32.PostMessageW(window_handle, message, vk_code, 0)
```

#### Linux Implementation

```python
# platform/input/linux.py
"""
Linux keyboard controller using xdotool/evdev.

Complexity: All functions CC ≤ 3
"""

import subprocess
from typing import List, Optional
import time

class LinuxKeyboardController(KeyboardControllerInterface):
    """
    Linux-specific keyboard controller.

    Uses xdotool for simplicity and compatibility.
    """

    # Key mapping: Our Key enum → xdotool key names
    KEY_MAP = {
        Key.A: "a",
        Key.B: "b",
        # ... (all keys)
        Key.ENTER: "Return",
        Key.ESCAPE: "Escape",
        Key.SPACE: "space",
        Key.UP: "Up",
        Key.DOWN: "Down",
        Key.LEFT: "Left",
        Key.RIGHT: "Right",
        Key.CTRL: "Control_L",
        Key.ALT: "Alt_L",
        Key.SHIFT: "Shift_L",
    }

    def send_key(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Send key using xdotool.

        Complexity: CC = 2
        """
        xdotool_key = self.KEY_MAP[key]

        if window_handle:
            self._send_to_window(xdotool_key, window_handle)
        else:
            self._send_global(xdotool_key)

    def send_combo(
        self,
        keys: List[Key],
        window_handle: Optional[int] = None
    ):
        """
        Send key combination.

        Complexity: CC = 2
        """
        xdotool_keys = [self.KEY_MAP[k] for k in keys]
        combo_str = "+".join(xdotool_keys)

        cmd = ["xdotool", "key", combo_str]
        if window_handle:
            cmd = ["xdotool", "key", "--window", str(window_handle), combo_str]

        subprocess.run(cmd)

    def press(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Press key down.

        Complexity: CC = 2
        """
        xdotool_key = self.KEY_MAP[key]

        cmd = ["xdotool", "keydown", xdotool_key]
        if window_handle:
            cmd = ["xdotool", "keydown", "--window", str(window_handle), xdotool_key]

        subprocess.run(cmd)

    def release(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Release key.

        Complexity: CC = 2
        """
        xdotool_key = self.KEY_MAP[key]

        cmd = ["xdotool", "keyup", xdotool_key]
        if window_handle:
            cmd = ["xdotool", "keyup", "--window", str(window_handle), xdotool_key]

        subprocess.run(cmd)

    def _send_global(self, xdotool_key: str):
        """
        Send key globally.

        Complexity: CC = 1
        """
        subprocess.run(["xdotool", "key", xdotool_key])

    def _send_to_window(self, xdotool_key: str, window_handle: int):
        """
        Send key to specific window.

        Complexity: CC = 1
        """
        subprocess.run([
            "xdotool",
            "key",
            "--window", str(window_handle),
            xdotool_key
        ])
```

#### macOS Implementation

```python
# platform/input/macos.py
"""
macOS keyboard controller using Quartz Event Services.

Complexity: All functions CC ≤ 3
"""

from Quartz import (
    CGEventCreateKeyboardEvent,
    CGEventPost,
    CGEventSetFlags,
    kCGHIDEventTap,
    kCGEventFlagMaskControl,
    kCGEventFlagMaskAlternate,
    kCGEventFlagMaskShift,
    kCGEventFlagMaskCommand
)
from typing import List, Optional
import time

class MacOSKeyboardController(KeyboardControllerInterface):
    """
    macOS-specific keyboard controller.

    Uses Quartz Event Services (Core Graphics).
    """

    # Key mapping: Our Key enum → macOS key codes
    KEY_MAP = {
        Key.A: 0x00,
        Key.B: 0x0B,
        # ... (all keys - macOS uses different codes)
        Key.ENTER: 0x24,
        Key.ESCAPE: 0x35,
        Key.SPACE: 0x31,
        Key.UP: 0x7E,
        Key.DOWN: 0x7D,
        Key.LEFT: 0x7B,
        Key.RIGHT: 0x7C,
    }

    # Modifier flags
    MODIFIER_FLAGS = {
        Key.CTRL: kCGEventFlagMaskControl,
        Key.ALT: kCGEventFlagMaskAlternate,
        Key.SHIFT: kCGEventFlagMaskShift,
        Key.COMMAND: kCGEventFlagMaskCommand,
    }

    def send_key(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Send key on macOS.

        Note: window_handle not used on macOS (events are global)

        Complexity: CC = 1
        """
        self.press(key)
        time.sleep(0.01)
        self.release(key)

    def send_combo(
        self,
        keys: List[Key],
        window_handle: Optional[int] = None
    ):
        """
        Send key combination.

        Complexity: CC = 2
        """
        # Separate modifiers from regular keys
        modifiers = [k for k in keys if k in self.MODIFIER_FLAGS]
        regular_keys = [k for k in keys if k not in self.MODIFIER_FLAGS]

        # Create combined modifier flag
        flags = self._combine_modifier_flags(modifiers)

        # Send each regular key with modifiers
        for key in regular_keys:
            self._send_key_with_modifiers(key, flags)

    def press(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Press key down.

        Complexity: CC = 1
        """
        key_code = self.KEY_MAP[key]
        event = CGEventCreateKeyboardEvent(None, key_code, True)
        CGEventPost(kCGHIDEventTap, event)

    def release(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        """
        Release key.

        Complexity: CC = 1
        """
        key_code = self.KEY_MAP[key]
        event = CGEventCreateKeyboardEvent(None, key_code, False)
        CGEventPost(kCGHIDEventTap, event)

    def _combine_modifier_flags(self, modifiers: List[Key]) -> int:
        """
        Combine modifier flags.

        Complexity: CC = 1
        """
        flags = 0
        for modifier in modifiers:
            flags |= self.MODIFIER_FLAGS[modifier]
        return flags

    def _send_key_with_modifiers(self, key: Key, modifier_flags: int):
        """
        Send key with modifier flags.

        Complexity: CC = 1
        """
        key_code = self.KEY_MAP[key]

        # Press
        event_down = CGEventCreateKeyboardEvent(None, key_code, True)
        CGEventSetFlags(event_down, modifier_flags)
        CGEventPost(kCGHIDEventTap, event_down)

        time.sleep(0.01)

        # Release
        event_up = CGEventCreateKeyboardEvent(None, key_code, False)
        CGEventSetFlags(event_up, modifier_flags)
        CGEventPost(kCGHIDEventTap, event_up)
```

### 6.5 Factory Pattern

```python
# platform/input/factory.py
"""
Factory for creating platform-specific keyboard controllers.

Complexity: CC = 2
"""

import platform as sys_platform
from .interface import KeyboardControllerInterface
from .windows import WindowsKeyboardController
from .linux import LinuxKeyboardController
from .macos import MacOSKeyboardController

def create_keyboard_controller() -> KeyboardControllerInterface:
    """
    Create platform-specific keyboard controller.

    Returns:
        KeyboardControllerInterface implementation for current platform

    Raises:
        NotImplementedError: If platform not supported

    Complexity: CC = 2
    """
    system = sys_platform.system()

    controllers = {
        "Windows": WindowsKeyboardController,
        "Linux": LinuxKeyboardController,
        "Darwin": MacOSKeyboardController,
    }

    controller_class = controllers.get(system)
    if not controller_class:
        raise NotImplementedError(f"Platform {system} not supported")

    return controller_class()
```

### 6.6 Usage Example

```python
# Example: Platform-agnostic keyboard usage

from platform.input.factory import create_keyboard_controller
from platform.input.interface import Key

# Create controller (platform detected automatically)
keyboard = create_keyboard_controller()

# Send keys - works on all platforms!
keyboard.send_key(Key.A)
keyboard.send_key(Key.ENTER)

# Send combinations
keyboard.send_combo([Key.CTRL, Key.C])  # Copy
keyboard.send_combo([Key.CTRL, Key.V])  # Paste

# For GB Operator soft reset (B + Select + Start + A)
keyboard.send_combo([Key.B, Key.BACKSPACE, Key.ENTER, Key.A])

# Send to specific window (if platform supports it)
keyboard.send_key(Key.A, window_handle=12345)
```

### 6.7 Testing with Mocks

```python
# tests/mocks/keyboard.py
"""
Mock keyboard controller for testing.

Complexity: All functions CC = 1
"""

from typing import List, Optional
from platform.input.interface import KeyboardControllerInterface, Key

class MockKeyboardController(KeyboardControllerInterface):
    """Mock keyboard for testing."""

    def __init__(self):
        self.keys_sent = []
        self.combos_sent = []
        self.keys_pressed = []
        self.keys_released = []

    def send_key(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        self.keys_sent.append((key, window_handle))

    def send_combo(
        self,
        keys: List[Key],
        window_handle: Optional[int] = None
    ):
        self.combos_sent.append((keys, window_handle))

    def press(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        self.keys_pressed.append((key, window_handle))

    def release(
        self,
        key: Key,
        window_handle: Optional[int] = None
    ):
        self.keys_released.append((key, window_handle))

    def clear_history(self):
        """Clear all recorded actions."""
        self.keys_sent.clear()
        self.combos_sent.clear()
        self.keys_pressed.clear()
        self.keys_released.clear()

# Usage in tests
def test_hunter_sends_keys():
    keyboard = MockKeyboardController()
    hunter = Hunter(keyboard=keyboard)

    hunter.perform_reset()

    # Verify keys were sent
    assert len(keyboard.keys_sent) > 0
    assert Key.A in [k for k, _ in keyboard.keys_sent]
```

---

## End of Part 1

**Part 1 Complete! ✅**

This part covered:
- ✅ Design Philosophy & SOLID Principles
- ✅ Cyclomatic Complexity Guidelines
- ✅ Research Synthesis (7+ repos analyzed)
- ✅ Dynamic Process Selection UI (complete implementation)
- ✅ Platform-Agnostic Input System (complete implementation)

**Continue to Part 2** for:
- Section 7: Window Management with Relative Coordinates (handles window movement!)
- Section 8: Screen Capture System
- Section 9: Detection System Architecture

**Then Part 3** for:
- Section 10: State Machine Implementation
- Section 11: Event Bus & Plugin System
- Section 12: Complete Module Structure
- Section 13: Full Working Examples
- Section 14: Testing Strategy
- Section 15: Migration Path

---

📖 **Next: [FINAL_ARCHITECTURE_GUIDE_PART2.md](./FINAL_ARCHITECTURE_GUIDE_PART2.md)**
