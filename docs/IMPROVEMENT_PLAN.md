# ShinyHunter - Comprehensive Improvement Plan

## Executive Summary

This document outlines a complete roadmap to transform ShinyHunter from a Windows-only prototype into a robust, cross-platform, production-ready shiny hunting framework. The plan addresses architecture, platform compatibility, user experience, detection reliability, and code reusability.

---

## Table of Contents

1. [Future-Proof Architecture](#1-future-proof-architecture)
2. [Cross-Platform Support](#2-cross-platform-support)
3. [Enhanced Color Picker with Visual Feedback](#3-enhanced-color-picker-with-visual-feedback)
4. [Screen Overlay System](#4-screen-overlay-system)
5. [Reusable Shiny Hunting Core Package](#5-reusable-shiny-hunting-core-package)
6. [Advanced Debugging & Logging](#6-advanced-debugging--logging)
7. [Improved Detection Algorithms](#7-improved-detection-algorithms)
8. [Additional Improvements](#8-additional-improvements)
9. [Implementation Roadmap](#9-implementation-roadmap)
10. [Technology Stack](#10-technology-stack)

---

## 1. Future-Proof Architecture

### Current Issues
- Tightly coupled platform-specific code (pywin32)
- No clear abstraction for platform-dependent components
- Limited extensibility for new hunter types
- Hard-coded configuration values

### Proposed Architecture

```
shinyhunter/
├── core/                           # Platform-agnostic core logic
│   ├── __init__.py
│   ├── hunter_base.py              # Abstract base class (improved)
│   ├── color_detector.py           # Advanced color detection algorithms
│   ├── state_machine.py            # State management for hunting loops
│   └── events.py                   # Event system for hooks/plugins
│
├── detection/                      # Detection strategies
│   ├── __init__.py
│   ├── pixel_detector.py           # Pixel-based detection
│   ├── pattern_detector.py         # Pattern matching detection
│   ├── sparkle_detector.py         # Shiny sparkle animation detection
│   └── audio_detector.py           # Audio-based detection (future)
│
├── platform/                       # Platform-specific implementations
│   ├── __init__.py
│   ├── base.py                     # Platform abstraction interfaces
│   ├── windows.py                  # Windows implementation
│   ├── linux.py                    # Linux implementation
│   ├── macos.py                    # macOS implementation
│   └── factory.py                  # Platform factory pattern
│
├── ui/                             # User interface components
│   ├── __init__.py
│   ├── color_picker.py             # Enhanced color picker
│   ├── overlay.py                  # Screen overlay system
│   ├── console.py                  # Rich console output
│   └── widgets.py                  # Reusable UI widgets
│
├── hunters/                        # Hunter implementations
│   ├── __init__.py
│   ├── stationary.py               # Stationary Pokemon
│   ├── starter.py                  # Starter Pokemon (new)
│   ├── wild_encounter.py           # Wild encounters (new)
│   └── registry.py                 # Hunter registry system
│
├── config/                         # Configuration system
│   ├── __init__.py
│   ├── settings.py                 # Settings manager
│   ├── profiles.py                 # User profiles
│   └── presets/                    # Pre-configured color presets
│       ├── gen1.json
│       ├── gen2.json
│       └── gen3.json
│
├── utils/                          # Utilities
│   ├── __init__.py
│   ├── logging.py                  # Logging configuration
│   ├── statistics.py               # Statistics tracking
│   └── validators.py               # Input validation
│
└── plugins/                        # Plugin system
    ├── __init__.py
    ├── plugin_manager.py
    └── hooks.py
```

### Key Architectural Patterns

#### 1. **Strategy Pattern** for Detection Methods
```python
# core/color_detector.py
from abc import ABC, abstractmethod
from enum import Enum

class DetectionStrategy(ABC):
    @abstractmethod
    def detect(self, image_data) -> bool:
        """Detect if shiny based on image data"""
        pass

class PixelDetectionStrategy(DetectionStrategy):
    def __init__(self, tolerance: int = 0):
        self.tolerance = tolerance

    def detect(self, image_data) -> bool:
        # Pixel-based detection with tolerance
        pass

class HSVDetectionStrategy(DetectionStrategy):
    def __init__(self, hue_range: tuple, sat_range: tuple):
        self.hue_range = hue_range
        self.sat_range = sat_range

    def detect(self, image_data) -> bool:
        # HSV color space detection
        pass

class SparkleDetectionStrategy(DetectionStrategy):
    def detect(self, image_data) -> bool:
        # Detect shiny sparkle animation
        pass
```

#### 2. **Abstract Factory Pattern** for Platform Components
```python
# platform/factory.py
import platform
from typing import Protocol

class PlatformInterface(Protocol):
    """Interface for platform-specific operations"""

    def get_window_capture(self, window_title: str):
        """Get window capture implementation"""
        ...

    def get_keyboard_simulator(self, window_handle):
        """Get keyboard simulator implementation"""
        ...

    def get_overlay_manager(self):
        """Get screen overlay manager"""
        ...

def get_platform_implementation() -> PlatformInterface:
    """Factory method to get platform-specific implementation"""
    system = platform.system()

    if system == "Windows":
        from .windows import WindowsPlatform
        return WindowsPlatform()
    elif system == "Linux":
        from .linux import LinuxPlatform
        return LinuxPlatform()
    elif system == "Darwin":  # macOS
        from .macos import MacOSPlatform
        return MacOSPlatform()
    else:
        raise NotImplementedError(f"Platform {system} not supported")
```

#### 3. **Observer Pattern** for Event System
```python
# core/events.py
from typing import Callable, Dict, List
from enum import Enum

class HunterEvent(Enum):
    HUNT_STARTED = "hunt_started"
    RESET_PERFORMED = "reset_performed"
    SHINY_DETECTED = "shiny_detected"
    HUNT_STOPPED = "hunt_stopped"
    ERROR_OCCURRED = "error_occurred"

class EventManager:
    def __init__(self):
        self._listeners: Dict[HunterEvent, List[Callable]] = {}

    def subscribe(self, event: HunterEvent, callback: Callable):
        """Subscribe to an event"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def emit(self, event: HunterEvent, data: dict = None):
        """Emit an event to all subscribers"""
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(data or {})
```

#### 4. **Plugin System** for Extensibility
```python
# plugins/plugin_manager.py
from typing import List, Type
import importlib
import inspect

class Plugin:
    """Base plugin class"""

    def on_hunt_start(self, hunter):
        """Called when hunt starts"""
        pass

    def on_shiny_found(self, hunter, pokemon_data):
        """Called when shiny found"""
        pass

    def on_reset(self, hunter, reset_count):
        """Called on each reset"""
        pass

class PluginManager:
    def __init__(self):
        self.plugins: List[Plugin] = []

    def register_plugin(self, plugin: Plugin):
        """Register a plugin"""
        self.plugins.append(plugin)

    def discover_plugins(self, plugin_dir: str):
        """Auto-discover plugins from directory"""
        # Implementation for plugin discovery
        pass

    def trigger_event(self, event_name: str, *args, **kwargs):
        """Trigger event on all plugins"""
        for plugin in self.plugins:
            if hasattr(plugin, event_name):
                method = getattr(plugin, event_name)
                method(*args, **kwargs)
```

### Benefits
- **Modularity**: Each component has a single responsibility
- **Testability**: Easy to unit test individual components
- **Extensibility**: New features can be added without modifying core
- **Maintainability**: Clear separation of concerns
- **Scalability**: Can handle complex hunting scenarios

---

## 2. Cross-Platform Support

### Current Platform Dependencies

| Component | Current | Issue |
|-----------|---------|-------|
| Window Capture | `win32gui` | Windows-only |
| Keyboard Simulation | `ctypes.windll.user32.PostMessageW` | Windows-only |
| Screen Overlay | Not implemented | - |
| File Paths | Hardcoded paths | Not portable |

### Cross-Platform Solutions

#### A. Window Management & Capture

**Current (Windows-only):**
```python
import win32gui
import win32com.client
```

**Proposed (Cross-platform):**
```python
# platform/base.py
from abc import ABC, abstractmethod
from typing import Tuple, Optional

class WindowCaptureBase(ABC):
    @abstractmethod
    def find_window(self, title: str) -> Optional[int]:
        """Find window by title"""
        pass

    @abstractmethod
    def activate_window(self, handle: int):
        """Bring window to foreground"""
        pass

    @abstractmethod
    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        """Get pixel color at coordinates"""
        pass

    @abstractmethod
    def capture_region(self, x: int, y: int, width: int, height: int):
        """Capture screen region"""
        pass

# platform/windows.py
import win32gui
import win32com.client
from mss import mss

class WindowsWindowCapture(WindowCaptureBase):
    def __init__(self):
        self.sct = mss()

    def find_window(self, title: str) -> Optional[int]:
        windows = []
        win32gui.EnumWindows(lambda hwnd, ctx: ctx.append(hwnd), windows)
        for hwnd in windows:
            if title.lower() in win32gui.GetWindowText(hwnd).lower():
                return hwnd
        return None

    def activate_window(self, handle: int):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")
        win32gui.SetForegroundWindow(handle)

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        pixel_box = {"top": y, "left": x, "width": 1, "height": 1}
        return self.sct.grab(pixel_box).pixel(0, 0)

# platform/linux.py
import subprocess
from Xlib import X, display
from mss import mss

class LinuxWindowCapture(WindowCaptureBase):
    def __init__(self):
        self.display = display.Display()
        self.sct = mss()

    def find_window(self, title: str) -> Optional[int]:
        # Use wmctrl or xdotool
        result = subprocess.run(
            ['xdotool', 'search', '--name', title],
            capture_output=True, text=True
        )
        if result.stdout:
            return int(result.stdout.strip().split()[0], 16)
        return None

    def activate_window(self, handle: int):
        subprocess.run(['xdotool', 'windowactivate', str(handle)])

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        pixel_box = {"top": y, "left": x, "width": 1, "height": 1}
        return self.sct.grab(pixel_box).pixel(0, 0)

# platform/macos.py
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionAll, kCGNullWindowID
from AppKit import NSWorkspace
from mss import mss

class MacOSWindowCapture(WindowCaptureBase):
    def __init__(self):
        self.sct = mss()

    def find_window(self, title: str) -> Optional[int]:
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionAll, kCGNullWindowID
        )
        for window in window_list:
            if title.lower() in window.get('kCGWindowName', '').lower():
                return window['kCGWindowNumber']
        return None

    def activate_window(self, handle: int):
        # macOS window activation
        workspace = NSWorkspace.sharedWorkspace()
        # Implementation details
        pass

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        pixel_box = {"top": y, "left": x, "width": 1, "height": 1}
        return self.sct.grab(pixel_box).pixel(0, 0)
```

#### B. Keyboard Simulation

**Current (Windows-only):**
```python
PostMessage = ctypes.windll.user32.PostMessageW
PostMessage(hwnd, WM_KEYDOWN, key, 0)
```

**Proposed (Cross-platform):**
```python
# platform/base.py
class KeyboardSimulatorBase(ABC):
    @abstractmethod
    def send_key(self, key: str, window_handle: int = None):
        """Send key press to window"""
        pass

    @abstractmethod
    def send_key_combo(self, keys: List[str], window_handle: int = None):
        """Send key combination"""
        pass

# platform/windows.py
import ctypes

class WindowsKeyboardSimulator(KeyboardSimulatorBase):
    WM_KEYDOWN = 0x0100
    WM_KEYUP = 0x0101

    def __init__(self):
        self.post_message = ctypes.windll.user32.PostMessageW

    def send_key(self, key: str, window_handle: int = None):
        key_code = self._get_key_code(key)
        if window_handle:
            self.post_message(window_handle, self.WM_KEYDOWN, key_code, 0)
            self.post_message(window_handle, self.WM_KEYUP, key_code, 0)

# platform/linux.py
import subprocess

class LinuxKeyboardSimulator(KeyboardSimulatorBase):
    def send_key(self, key: str, window_handle: int = None):
        if window_handle:
            # Send to specific window using xdotool
            subprocess.run(['xdotool', 'key', '--window', str(window_handle), key])
        else:
            subprocess.run(['xdotool', 'key', key])

# platform/macos.py
from Quartz import CGEventCreateKeyboardEvent, CGEventPost, kCGHIDEventTap

class MacOSKeyboardSimulator(KeyboardSimulatorBase):
    def send_key(self, key: str, window_handle: int = None):
        key_code = self._get_key_code(key)
        event = CGEventCreateKeyboardEvent(None, key_code, True)
        CGEventPost(kCGHIDEventTap, event)
        event = CGEventCreateKeyboardEvent(None, key_code, False)
        CGEventPost(kCGHIDEventTap, event)
```

### New Dependencies for Cross-Platform Support

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.10"
mss = "^9.0.1"              # Cross-platform screen capture
pynput = "^1.7.6"           # Cross-platform input (already present)
opencv-python = "^4.8.1"    # Image processing for advanced detection

# Platform-specific dependencies
pywin32 = {version = "^306", platform = "win32"}
python-xlib = {version = "^0.33", platform = "linux"}
pyobjc-framework-Quartz = {version = "^10.0", platform = "darwin"}
pyobjc-framework-Cocoa = {version = "^10.0", platform = "darwin"}

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-cov = "^4.1.0"
```

---

## 3. Enhanced Color Picker with Visual Feedback

### Current Issues
- No visual feedback when selecting pixels
- No preview of selected area
- Hard to know exactly what pixel you're clicking
- No magnification for precise selection
- No way to save/load color presets

### Proposed Solution: Interactive Color Picker with Overlay

#### Features
1. **Real-time color preview** under cursor
2. **Magnified view** of pixel area
3. **Crosshair overlay** for precise selection
4. **Color history** of recent selections
5. **Preset management** (save/load color points)
6. **HSV/RGB display** with color swatch

#### Implementation

```python
# ui/color_picker.py
from dataclasses import dataclass
from typing import Optional, Tuple, List
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import json

@dataclass
class ColorPoint:
    """Enhanced color point with metadata"""
    color_rgb: Tuple[int, int, int]
    color_hsv: Tuple[int, int, int]
    position: Tuple[int, int]
    name: str = ""
    timestamp: str = ""

class EnhancedColorPicker:
    def __init__(self, window_capture, preset_file: str = "color_presets.json"):
        self.window_capture = window_capture
        self.preset_file = preset_file
        self.overlay_window = None
        self.preview_window = None
        self.current_position = (0, 0)
        self.selected_points: List[ColorPoint] = []
        self.magnification = 10

    def start_picking(self) -> Optional[ColorPoint]:
        """Start interactive color picking mode"""
        self._create_overlay()
        self._create_preview_window()
        self._bind_mouse_events()

        # Run event loop
        self.overlay_window.mainloop()

        return self.selected_points[-1] if self.selected_points else None

    def _create_overlay(self):
        """Create transparent overlay with crosshair"""
        self.overlay_window = tk.Tk()
        self.overlay_window.attributes('-alpha', 0.3)
        self.overlay_window.attributes('-topmost', True)
        self.overlay_window.attributes('-fullscreen', True)

        # Create canvas for crosshair
        self.canvas = tk.Canvas(
            self.overlay_window,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Draw crosshair
        self.crosshair_h = self.canvas.create_line(0, 0, 0, 0, fill='red', width=2)
        self.crosshair_v = self.canvas.create_line(0, 0, 0, 0, fill='red', width=2)

        # Instruction text
        self.instruction_text = self.canvas.create_text(
            10, 10,
            text="Click to select pixel | ESC to cancel | SPACE to confirm",
            fill='white',
            anchor='nw',
            font=('Arial', 12, 'bold')
        )

    def _create_preview_window(self):
        """Create preview window showing magnified pixel area and color info"""
        preview = tk.Toplevel(self.overlay_window)
        preview.title("Color Picker Preview")
        preview.attributes('-topmost', True)
        preview.geometry("350x450+50+50")

        # Magnified view
        self.mag_label = tk.Label(preview)
        self.mag_label.pack(pady=10)

        # Color swatch
        self.color_frame = tk.Frame(preview, width=100, height=100, bg='black')
        self.color_frame.pack(pady=5)

        # Color info
        info_frame = tk.Frame(preview)
        info_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.rgb_label = tk.Label(info_frame, text="RGB: (0, 0, 0)", font=('Courier', 10))
        self.rgb_label.pack()

        self.hsv_label = tk.Label(info_frame, text="HSV: (0, 0, 0)", font=('Courier', 10))
        self.hsv_label.pack()

        self.pos_label = tk.Label(info_frame, text="Position: (0, 0)", font=('Courier', 10))
        self.pos_label.pack()

        self.hex_label = tk.Label(info_frame, text="HEX: #000000", font=('Courier', 10))
        self.hex_label.pack()

        # History
        tk.Label(info_frame, text="Recent Selections:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        self.history_listbox = tk.Listbox(info_frame, height=5)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)

        self.preview_window = preview

    def _bind_mouse_events(self):
        """Bind mouse and keyboard events"""
        self.overlay_window.bind('<Motion>', self._on_mouse_move)
        self.overlay_window.bind('<Button-1>', self._on_click)
        self.overlay_window.bind('<Escape>', lambda e: self.overlay_window.quit())
        self.overlay_window.bind('<space>', self._on_confirm)

    def _on_mouse_move(self, event):
        """Update preview when mouse moves"""
        x, y = event.x_root, event.y_root
        self.current_position = (x, y)

        # Update crosshair
        self.canvas.coords(self.crosshair_h, 0, y, self.canvas.winfo_width(), y)
        self.canvas.coords(self.crosshair_v, x, 0, x, self.canvas.winfo_height())

        # Update preview
        self._update_preview(x, y)

    def _update_preview(self, x: int, y: int):
        """Update magnified preview and color info"""
        # Capture area around cursor
        size = 20
        region = self.window_capture.capture_region(
            x - size // 2, y - size // 2, size, size
        )

        # Magnify
        magnified = region.resize(
            (size * self.magnification, size * self.magnification),
            Image.NEAREST
        )

        # Draw center pixel indicator
        draw = ImageDraw.Draw(magnified)
        center = size * self.magnification // 2
        box_size = self.magnification
        draw.rectangle(
            [center - box_size//2, center - box_size//2,
             center + box_size//2, center + box_size//2],
            outline='red', width=2
        )

        # Update magnified view
        photo = ImageTk.PhotoImage(magnified)
        self.mag_label.config(image=photo)
        self.mag_label.image = photo  # Keep reference

        # Get color at exact pixel
        rgb = self.window_capture.get_pixel(x, y)
        hsv = self._rgb_to_hsv(rgb)

        # Update color info
        self.color_frame.config(bg=f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}')
        self.rgb_label.config(text=f"RGB: {rgb}")
        self.hsv_label.config(text=f"HSV: {hsv}")
        self.pos_label.config(text=f"Position: ({x}, {y})")
        self.hex_label.config(text=f"HEX: #{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")

    def _on_click(self, event):
        """Handle click to select color"""
        x, y = event.x_root, event.y_root
        rgb = self.window_capture.get_pixel(x, y)
        hsv = self._rgb_to_hsv(rgb)

        color_point = ColorPoint(
            color_rgb=rgb,
            color_hsv=hsv,
            position=(x, y),
            timestamp=datetime.now().isoformat()
        )

        self.selected_points.append(color_point)

        # Update history
        self.history_listbox.insert(
            0,
            f"{rgb} @ ({x}, {y})"
        )

    def _on_confirm(self, event):
        """Confirm selection and close"""
        self.overlay_window.quit()

    def save_preset(self, name: str, points: List[ColorPoint]):
        """Save color preset to file"""
        try:
            with open(self.preset_file, 'r') as f:
                presets = json.load(f)
        except FileNotFoundError:
            presets = {}

        presets[name] = [
            {
                'color_rgb': p.color_rgb,
                'color_hsv': p.color_hsv,
                'position': p.position,
                'name': p.name
            }
            for p in points
        ]

        with open(self.preset_file, 'w') as f:
            json.dump(presets, f, indent=2)

    def load_preset(self, name: str) -> List[ColorPoint]:
        """Load color preset from file"""
        with open(self.preset_file, 'r') as f:
            presets = json.load(f)

        return [
            ColorPoint(**point_data)
            for point_data in presets.get(name, [])
        ]

    @staticmethod
    def _rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert RGB to HSV"""
        import colorsys
        r, g, b = [x / 255.0 for x in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (int(h * 180), int(s * 255), int(v * 255))  # OpenCV format
```

---

## 4. Screen Overlay System

### Purpose
Display reference points and detection areas visually on screen so users can:
- See exactly where the bot is monitoring
- Verify reference points are correct
- Debug detection issues
- Monitor hunting progress visually

### Implementation

```python
# ui/overlay.py
import tkinter as tk
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

class OverlayMarkerType(Enum):
    REFERENCE_POINT = "reference"
    TARGET_POINT = "target"
    DETECTION_AREA = "detection_area"
    STATUS_TEXT = "status"

@dataclass
class OverlayMarker:
    type: OverlayMarkerType
    position: Tuple[int, int]
    label: str = ""
    color: str = "red"
    size: int = 10

class ScreenOverlay:
    """Transparent overlay to display reference points and detection areas"""

    def __init__(self):
        self.root = None
        self.canvas = None
        self.markers: List[OverlayMarker] = []
        self.visible = False

    def initialize(self):
        """Create transparent overlay window"""
        self.root = tk.Tk()

        # Configure transparent overlay
        self.root.attributes('-alpha', 0.7)
        self.root.attributes('-topmost', True)
        self.root.attributes('-fullscreen', True)

        # Platform-specific transparency
        try:
            # Windows
            self.root.wm_attributes('-transparentcolor', 'black')
        except tk.TclError:
            try:
                # macOS
                self.root.wm_attributes('-transparent', True)
            except tk.TclError:
                # Linux - use alpha
                pass

        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Make click-through on Linux
        self.root.overrideredirect(True)

        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

    def add_marker(self, marker: OverlayMarker):
        """Add a marker to the overlay"""
        self.markers.append(marker)
        self._draw_marker(marker)

    def _draw_marker(self, marker: OverlayMarker):
        """Draw a marker on the overlay"""
        x, y = marker.position

        if marker.type == OverlayMarkerType.REFERENCE_POINT:
            # Draw crosshair for reference point
            size = marker.size
            self.canvas.create_line(
                x - size, y, x + size, y,
                fill=marker.color, width=2, tags='marker'
            )
            self.canvas.create_line(
                x, y - size, x, y + size,
                fill=marker.color, width=2, tags='marker'
            )
            # Circle around
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                outline=marker.color, width=2, tags='marker'
            )
            # Label
            if marker.label:
                self.canvas.create_text(
                    x, y - size - 10,
                    text=marker.label,
                    fill=marker.color,
                    font=('Arial', 10, 'bold'),
                    tags='marker'
                )

        elif marker.type == OverlayMarkerType.TARGET_POINT:
            # Draw square for target point
            size = marker.size
            self.canvas.create_rectangle(
                x - size, y - size, x + size, y + size,
                outline=marker.color, width=3, tags='marker'
            )
            # Label
            if marker.label:
                self.canvas.create_text(
                    x, y - size - 10,
                    text=marker.label,
                    fill=marker.color,
                    font=('Arial', 10, 'bold'),
                    tags='marker'
                )

        elif marker.type == OverlayMarkerType.STATUS_TEXT:
            # Draw status text
            self.canvas.create_text(
                x, y,
                text=marker.label,
                fill=marker.color,
                font=('Arial', 14, 'bold'),
                tags='status'
            )

    def update_status(self, text: str, position: Tuple[int, int] = (20, 20)):
        """Update status text on overlay"""
        self.canvas.delete('status')
        marker = OverlayMarker(
            type=OverlayMarkerType.STATUS_TEXT,
            position=position,
            label=text,
            color='lime'
        )
        self._draw_marker(marker)

    def clear_markers(self):
        """Clear all markers"""
        self.canvas.delete('marker')
        self.markers.clear()

    def show(self):
        """Show overlay"""
        if self.root:
            self.root.deiconify()
            self.visible = True

    def hide(self):
        """Hide overlay"""
        if self.root:
            self.root.withdraw()
            self.visible = False

    def update(self):
        """Update overlay (call in main loop)"""
        if self.root and self.visible:
            self.root.update()
```

### Usage Example

```python
# In hunter implementation
overlay = ScreenOverlay()
overlay.initialize()

# Add reference point marker
overlay.add_marker(OverlayMarker(
    type=OverlayMarkerType.REFERENCE_POINT,
    position=reference_point,
    label="REF",
    color="cyan"
))

# Add target point marker
overlay.add_marker(OverlayMarker(
    type=OverlayMarkerType.TARGET_POINT,
    position=target_point,
    label="TARGET",
    color="yellow"
))

overlay.show()

# During hunting loop
overlay.update_status(f"Resets: {reset_count} | Time: {elapsed}")
overlay.update()
```

---

## 5. Reusable Shiny Hunting Core Package

### Package Structure

Create a standalone, reusable package that can be installed via pip:

```
shinyhunter-core/
├── setup.py
├── pyproject.toml
├── README.md
├── LICENSE
├── shinyhunter_core/
│   ├── __init__.py
│   ├── hunter.py              # Main hunter interface
│   ├── detector.py            # Detection algorithms
│   ├── state.py               # State management
│   └── utils.py               # Utility functions
├── examples/
│   ├── basic_usage.py
│   ├── custom_detector.py
│   └── plugin_example.py
├── tests/
│   ├── test_hunter.py
│   ├── test_detector.py
│   └── test_state.py
└── docs/
    ├── getting_started.md
    ├── api_reference.md
    └── advanced_usage.md
```

### Core Package API

```python
# shinyhunter_core/__init__.py
"""
ShinyHunter Core - Reusable shiny hunting framework

Example usage:
    from shinyhunter_core import ShinyHunter, PixelDetector

    hunter = ShinyHunter(
        detector=PixelDetector(tolerance=5),
        on_shiny_found=lambda: print("Shiny!")
    )
    hunter.start()
"""

__version__ = "1.0.0"

from .hunter import ShinyHunter, HunterConfig
from .detector import (
    DetectorBase,
    PixelDetector,
    HSVDetector,
    PatternDetector
)
from .state import HunterState, StateMachine

__all__ = [
    'ShinyHunter',
    'HunterConfig',
    'DetectorBase',
    'PixelDetector',
    'HSVDetector',
    'PatternDetector',
    'HunterState',
    'StateMachine'
]

# shinyhunter_core/hunter.py
from dataclasses import dataclass
from typing import Callable, Optional
from .detector import DetectorBase
from .state import StateMachine, HunterState

@dataclass
class HunterConfig:
    """Configuration for shiny hunter"""
    window_title: str = "operator"
    max_resets: Optional[int] = None
    timeout: Optional[float] = None
    enable_logging: bool = True
    enable_statistics: bool = True

class ShinyHunter:
    """Main shiny hunter class - reusable core"""

    def __init__(
        self,
        detector: DetectorBase,
        config: HunterConfig = None,
        on_shiny_found: Callable = None,
        on_reset: Callable = None
    ):
        self.detector = detector
        self.config = config or HunterConfig()
        self.on_shiny_found = on_shiny_found
        self.on_reset = on_reset
        self.state_machine = StateMachine()
        self.reset_count = 0
        self.running = False

    def start(self):
        """Start hunting"""
        self.running = True
        self.state_machine.transition(HunterState.HUNTING)
        self._hunt_loop()

    def stop(self):
        """Stop hunting"""
        self.running = False
        self.state_machine.transition(HunterState.STOPPED)

    def _hunt_loop(self):
        """Main hunting loop - platform-agnostic"""
        while self.running:
            # Perform reset
            self._perform_reset()

            # Wait for encounter
            self._wait_for_encounter()

            # Check if shiny
            if self.detector.is_shiny():
                self.state_machine.transition(HunterState.SHINY_FOUND)
                if self.on_shiny_found:
                    self.on_shiny_found()
                break

            self.reset_count += 1
            if self.on_reset:
                self.on_reset(self.reset_count)

            # Check max resets
            if self.config.max_resets and self.reset_count >= self.config.max_resets:
                break

    def _perform_reset(self):
        """Override in subclass for platform-specific reset"""
        raise NotImplementedError

    def _wait_for_encounter(self):
        """Override in subclass for platform-specific encounter detection"""
        raise NotImplementedError
```

### Example Usage

```python
# examples/basic_usage.py
from shinyhunter_core import ShinyHunter, PixelDetector, HunterConfig

# Configure detector
detector = PixelDetector(
    reference_point=(100, 200),
    target_point=(150, 250),
    tolerance=5
)

# Configure hunter
config = HunterConfig(
    window_title="GB Operator",
    max_resets=1000,
    enable_logging=True
)

# Create custom hunter by extending core
class GBOperatorHunter(ShinyHunter):
    def _perform_reset(self):
        # Platform-specific reset logic
        self.keyboard.press_keys(['B', 'Select', 'Start', 'A'])

    def _wait_for_encounter(self):
        # Wait for reference color
        while not self.detector.reference_found():
            self.keyboard.press('A')

# Run hunter
hunter = GBOperatorHunter(
    detector=detector,
    config=config,
    on_shiny_found=lambda: print("🌟 SHINY FOUND! 🌟"),
    on_reset=lambda count: print(f"Reset #{count}")
)

hunter.start()
```

### Publishing to PyPI

```bash
# Build package
poetry build

# Publish to PyPI
poetry publish

# Users can install with:
pip install shinyhunter-core

# Or with poetry:
poetry add shinyhunter-core
```

---

## 6. Advanced Debugging & Logging

### Current Issues
- Basic `print()` statements
- No log levels
- No file logging
- No timestamps
- No color coding
- No debug mode

### Proposed Solution: Rich Console with Structured Logging

```python
# utils/logging.py
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from datetime import datetime
from pathlib import Path

class ShinyHunterLogger:
    """Enhanced logger with Rich console output"""

    def __init__(self, log_file: str = "shinyhunter.log", level=logging.DEBUG):
        self.console = Console()
        self.log_file = log_file

        # Setup logging
        logging.basicConfig(
            level=level,
            format="%(message)s",
            handlers=[
                RichHandler(
                    console=self.console,
                    rich_tracebacks=True,
                    tracebacks_show_locals=True
                ),
                logging.FileHandler(log_file)
            ]
        )
        self.logger = logging.getLogger("shinyhunter")

    def print_banner(self):
        """Print application banner"""
        banner = """
        ╔═══════════════════════════════════════╗
        ║     ✨ SHINY HUNTER v2.0 ✨          ║
        ║  Pokemon Shiny Hunting Automation     ║
        ╚═══════════════════════════════════════╝
        """
        self.console.print(banner, style="bold cyan")

    def log_hunt_start(self, config: dict):
        """Log hunt start with configuration"""
        table = Table(title="🎯 Hunt Configuration", style="cyan")
        table.add_column("Setting", style="yellow")
        table.add_column("Value", style="green")

        for key, value in config.items():
            table.add_row(key, str(value))

        self.console.print(table)
        self.logger.info("Hunt started")

    def log_reset(self, count: int, elapsed_time: str):
        """Log reset with color-coded count"""
        # Color based on reset count
        if count < 100:
            style = "green"
        elif count < 500:
            style = "yellow"
        elif count < 1000:
            style = "orange1"
        else:
            style = "red"

        self.console.print(
            f"[{style}]🔄 Reset #{count}[/{style}] | "
            f"[cyan]⏱️  {elapsed_time}[/cyan]"
        )
        self.logger.debug(f"Reset performed: {count}")

    def log_shiny_found(self, reset_count: int, total_time: str):
        """Log shiny found with celebration"""
        panel = Panel.fit(
            f"""
            [bold green]🌟 SHINY POKEMON FOUND! 🌟[/bold green]

            [yellow]Resets:[/yellow] [bold]{reset_count}[/bold]
            [yellow]Total Time:[/yellow] [bold]{total_time}[/bold]
            [yellow]Timestamp:[/yellow] [bold]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold]
            """,
            border_style="bright_green",
            title="SUCCESS!"
        )
        self.console.print(panel)
        self.logger.info(f"Shiny found after {reset_count} resets")

    def log_color_point(self, name: str, color: tuple, position: tuple):
        """Log selected color point"""
        r, g, b = color
        hex_color = f"#{r:02x}{g:02x}{b:02x}"

        self.console.print(
            f"[bold]{name}:[/bold] "
            f"RGB{color} | "
            f"Position{position} | "
            f"[{hex_color}]████[/{hex_color}] {hex_color}"
        )
        self.logger.debug(f"Color point '{name}': {color} @ {position}")

    def log_detection_debug(self, expected: tuple, actual: tuple, match: bool):
        """Log detection comparison for debugging"""
        status = "✅ MATCH" if match else "❌ NO MATCH"
        style = "green" if match else "red"

        table = Table(title=f"🔍 Detection Debug - {status}", style=style)
        table.add_column("Type")
        table.add_column("RGB Value")
        table.add_column("Hex")

        exp_hex = f"#{expected[0]:02x}{expected[1]:02x}{expected[2]:02x}"
        act_hex = f"#{actual[0]:02x}{actual[1]:02x}{actual[2]:02x}"

        table.add_row("Expected", str(expected), exp_hex)
        table.add_row("Actual", str(actual), act_hex)

        self.console.print(table)
        self.logger.debug(f"Detection: expected={expected}, actual={actual}, match={match}")

    def log_error(self, error: Exception):
        """Log error with rich traceback"""
        self.console.print_exception(show_locals=True)
        self.logger.error(f"Error occurred: {error}", exc_info=True)

    def create_progress(self, description: str = "Hunting..."):
        """Create progress bar for long operations"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        )

# Usage example
logger = ShinyHunterLogger()
logger.print_banner()
logger.log_hunt_start({
    "Hunter Type": "Stationary",
    "Window": "GB Operator",
    "Detection": "Pixel-based"
})

for i in range(1, 100):
    logger.log_reset(i, f"{i * 5}s")

logger.log_shiny_found(99, "8m 15s")
```

### Debug Mode Features

```python
# Add --debug flag support
# main.py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--hunter', type=str, required=True)
parser.add_argument('--debug', action='store_true', help='Enable debug mode')
parser.add_argument('--verbose', '-v', action='count', default=0)

args = parser.parse_args()

# Configure logging level
if args.debug:
    log_level = logging.DEBUG
elif args.verbose >= 2:
    log_level = logging.DEBUG
elif args.verbose == 1:
    log_level = logging.INFO
else:
    log_level = logging.WARNING

logger = ShinyHunterLogger(level=log_level)

# In debug mode, show:
# - Each pixel read
# - Timing information
# - Memory usage
# - Detection algorithm details
if args.debug:
    logger.log_detection_debug(expected_color, actual_color, is_match)
```

---

## 7. Improved Detection Algorithms

### Current Issues
- **Exact pixel matching** - no tolerance for compression artifacts
- **Single pixel detection** - vulnerable to noise
- **No averaging** - can miss subtle color changes
- **Timing-sensitive** - reads during animation frames

### Proposed Improvements

#### A. Color Tolerance Detection

```python
# detection/pixel_detector.py
import numpy as np
from typing import Tuple

class TolerantPixelDetector:
    """Pixel detector with color tolerance"""

    def __init__(self, tolerance: int = 5):
        """
        Args:
            tolerance: Maximum RGB difference to still consider a match (0-255)
        """
        self.tolerance = tolerance

    def colors_match(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int]
    ) -> bool:
        """Check if two colors match within tolerance"""
        return all(
            abs(c1 - c2) <= self.tolerance
            for c1, c2 in zip(color1, color2)
        )

    def euclidean_distance(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int]
    ) -> float:
        """Calculate Euclidean distance between two RGB colors"""
        return np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

    def is_similar(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        threshold: float = 10.0
    ) -> bool:
        """Check if colors are similar using Euclidean distance"""
        return self.euclidean_distance(color1, color2) < threshold
```

#### B. HSV Color Space Detection

```python
# detection/hsv_detector.py
import cv2
import numpy as np
from typing import Tuple

class HSVDetector:
    """HSV-based color detection for better lighting invariance"""

    def __init__(
        self,
        hue_range: Tuple[int, int] = None,
        sat_range: Tuple[int, int] = (50, 255),
        val_range: Tuple[int, int] = (50, 255),
        hue_tolerance: int = 10
    ):
        """
        Args:
            hue_range: Target hue range (0-180 in OpenCV)
            sat_range: Saturation range (0-255)
            val_range: Value range (0-255)
            hue_tolerance: Tolerance for hue matching
        """
        self.hue_range = hue_range
        self.sat_range = sat_range
        self.val_range = val_range
        self.hue_tolerance = hue_tolerance

    def rgb_to_hsv(self, rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert RGB to HSV (OpenCV format)"""
        rgb_array = np.uint8([[rgb]])
        hsv_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2HSV)
        return tuple(hsv_array[0][0])

    def detect_in_range(self, hsv: Tuple[int, int, int]) -> bool:
        """Check if HSV color is within defined ranges"""
        h, s, v = hsv

        # Check hue (with wrapping for red colors)
        if self.hue_range:
            h_min, h_max = self.hue_range
            if h_min > h_max:  # Wrapping case (e.g., red: 170-10)
                hue_match = h >= h_min or h <= h_max
            else:
                hue_match = h_min <= h <= h_max
        else:
            hue_match = True

        # Check saturation and value
        sat_match = self.sat_range[0] <= s <= self.sat_range[1]
        val_match = self.val_range[0] <= v <= self.val_range[1]

        return hue_match and sat_match and val_match

    def is_shiny_color(
        self,
        normal_rgb: Tuple[int, int, int],
        current_rgb: Tuple[int, int, int]
    ) -> bool:
        """Detect if color has changed significantly in HSV space"""
        normal_hsv = self.rgb_to_hsv(normal_rgb)
        current_hsv = self.rgb_to_hsv(current_rgb)

        # Calculate hue difference (with wrapping)
        h_diff = abs(normal_hsv[0] - current_hsv[0])
        if h_diff > 90:  # Handle wrapping
            h_diff = 180 - h_diff

        # Significant hue shift indicates shiny
        return h_diff > self.hue_tolerance
```

#### C. Multi-Point Sampling

```python
# detection/pattern_detector.py
from typing import List, Tuple
import numpy as np

class MultiPointDetector:
    """Sample multiple points for more reliable detection"""

    def __init__(self, sample_points: List[Tuple[int, int]], tolerance: int = 5):
        """
        Args:
            sample_points: List of (x, y) coordinates to sample
            tolerance: Color tolerance for each point
        """
        self.sample_points = sample_points
        self.tolerance = tolerance
        self.reference_colors = []

    def calibrate(self, window_capture):
        """Capture reference colors for all sample points"""
        self.reference_colors = [
            window_capture.get_pixel(x, y)
            for x, y in self.sample_points
        ]

    def detect_change(self, window_capture, threshold_ratio: float = 0.5) -> bool:
        """
        Detect if enough points have changed color

        Args:
            window_capture: Window capture instance
            threshold_ratio: Minimum ratio of changed points (0.0-1.0)

        Returns:
            True if more than threshold_ratio of points changed
        """
        if not self.reference_colors:
            raise ValueError("Must call calibrate() first")

        changed_count = 0

        for (x, y), ref_color in zip(self.sample_points, self.reference_colors):
            current_color = window_capture.get_pixel(x, y)

            # Check if color changed beyond tolerance
            if not self._colors_match(ref_color, current_color):
                changed_count += 1

        change_ratio = changed_count / len(self.sample_points)
        return change_ratio >= threshold_ratio

    def _colors_match(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> bool:
        """Check if colors match within tolerance"""
        return all(abs(c1 - c2) <= self.tolerance for c1, c2 in zip(color1, color2))

    def get_average_color(self, window_capture) -> Tuple[int, int, int]:
        """Get average color across all sample points"""
        colors = [
            window_capture.get_pixel(x, y)
            for x, y in self.sample_points
        ]

        avg_color = tuple(
            int(np.mean([c[i] for c in colors]))
            for i in range(3)
        )

        return avg_color
```

#### D. Temporal Smoothing

```python
# detection/smoothing.py
from collections import deque
from typing import Tuple, Deque
import numpy as np

class TemporalSmoother:
    """Smooth detection over time to reduce false positives"""

    def __init__(self, window_size: int = 5, confidence_threshold: float = 0.7):
        """
        Args:
            window_size: Number of recent samples to consider
            confidence_threshold: Minimum confidence to report shiny (0.0-1.0)
        """
        self.window_size = window_size
        self.confidence_threshold = confidence_threshold
        self.detection_history: Deque[bool] = deque(maxlen=window_size)

    def add_detection(self, is_shiny: bool):
        """Add a detection result"""
        self.detection_history.append(is_shiny)

    def get_confidence(self) -> float:
        """Get confidence that pokemon is shiny (0.0-1.0)"""
        if not self.detection_history:
            return 0.0

        return sum(self.detection_history) / len(self.detection_history)

    def is_confident_shiny(self) -> bool:
        """Check if confident that pokemon is shiny"""
        return self.get_confidence() >= self.confidence_threshold

    def reset(self):
        """Reset detection history"""
        self.detection_history.clear()
```

#### E. Pattern Recognition (Advanced)

```python
# detection/sparkle_detector.py
import cv2
import numpy as np
from typing import Tuple, Optional

class SparkleDetector:
    """Detect shiny sparkle animation using computer vision"""

    def __init__(self, sparkle_region: Tuple[int, int, int, int]):
        """
        Args:
            sparkle_region: (x, y, width, height) region to monitor for sparkles
        """
        self.sparkle_region = sparkle_region
        self.previous_frame = None

    def detect_sparkle(self, current_frame: np.ndarray) -> bool:
        """
        Detect sparkle animation by looking for bright spots

        Args:
            current_frame: Current video frame as numpy array

        Returns:
            True if sparkle detected
        """
        x, y, w, h = self.sparkle_region
        region = current_frame[y:y+h, x:x+w]

        # Convert to grayscale
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

        # Detect bright spots (sparkles are typically white/bright)
        _, bright_spots = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Count bright pixels
        bright_pixel_count = np.sum(bright_spots == 255)

        # Sparkles typically appear as small bright areas
        # Adjust threshold based on your specific game
        sparkle_threshold = w * h * 0.05  # 5% of region

        has_sparkle = bright_pixel_count > sparkle_threshold

        # Store frame for next comparison
        self.previous_frame = current_frame.copy()

        return has_sparkle

    def detect_motion_sparkle(self, current_frame: np.ndarray) -> bool:
        """Detect sparkle by looking for motion/change"""
        if self.previous_frame is None:
            self.previous_frame = current_frame.copy()
            return False

        # Calculate difference between frames
        diff = cv2.absdiff(self.previous_frame, current_frame)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Threshold the difference
        _, motion = cv2.threshold(gray_diff, 50, 255, cv2.THRESH_BINARY)

        # Count changed pixels
        motion_pixels = np.sum(motion == 255)

        self.previous_frame = current_frame.copy()

        # Sparkle animation causes significant change
        return motion_pixels > 100  # Adjust threshold
```

### Recommended Detection Pipeline

```python
# Combine multiple detection methods for best results
class HybridDetector:
    """Combines multiple detection strategies for robust shiny detection"""

    def __init__(self):
        self.pixel_detector = TolerantPixelDetector(tolerance=5)
        self.hsv_detector = HSVDetector(hue_tolerance=15)
        self.multi_point = MultiPointDetector(sample_points=[...])
        self.smoother = TemporalSmoother(window_size=5, confidence_threshold=0.8)

    def detect(self, window_capture) -> bool:
        """Run all detection methods and combine results"""
        # Method 1: Pixel comparison with tolerance
        pixel_result = self.pixel_detector.is_shiny()

        # Method 2: HSV color space detection
        hsv_result = self.hsv_detector.is_shiny_color(...)

        # Method 3: Multi-point sampling
        pattern_result = self.multi_point.detect_change(window_capture)

        # Combine results (at least 2 out of 3 methods agree)
        detection = sum([pixel_result, hsv_result, pattern_result]) >= 2

        # Method 4: Temporal smoothing
        self.smoother.add_detection(detection)

        return self.smoother.is_confident_shiny()
```

---

## 8. Additional Improvements

### A. Configuration Management

```python
# config/settings.py
from dataclasses import dataclass, asdict
from typing import Optional
import yaml
from pathlib import Path

@dataclass
class DetectionConfig:
    """Detection algorithm configuration"""
    method: str = "hybrid"  # pixel, hsv, pattern, hybrid
    tolerance: int = 5
    hue_tolerance: int = 15
    multi_point_count: int = 5
    temporal_smoothing: bool = True
    confidence_threshold: float = 0.8

@dataclass
class UIConfig:
    """UI configuration"""
    show_overlay: bool = True
    overlay_opacity: float = 0.7
    color_picker_magnification: int = 10
    console_theme: str = "monokai"

@dataclass
class HunterConfig:
    """Hunter behavior configuration"""
    hunter_type: str = "stationary"
    max_resets: Optional[int] = None
    timeout_seconds: Optional[int] = None
    auto_save_video: bool = True
    notification_enabled: bool = True

@dataclass
class PlatformConfig:
    """Platform-specific configuration"""
    window_title: str = "operator"
    key_mapping_file: str = "config/key_config.ini"

@dataclass
class AppConfig:
    """Main application configuration"""
    detection: DetectionConfig = None
    ui: UIConfig = None
    hunter: HunterConfig = None
    platform: PlatformConfig = None

    def __post_init__(self):
        if self.detection is None:
            self.detection = DetectionConfig()
        if self.ui is None:
            self.ui = UIConfig()
        if self.hunter is None:
            self.hunter = HunterConfig()
        if self.platform is None:
            self.platform = PlatformConfig()

    @classmethod
    def load(cls, path: str = "config.yaml") -> "AppConfig":
        """Load configuration from YAML file"""
        config_path = Path(path)
        if not config_path.exists():
            # Create default config
            config = cls()
            config.save(path)
            return config

        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)

        return cls(
            detection=DetectionConfig(**data.get('detection', {})),
            ui=UIConfig(**data.get('ui', {})),
            hunter=HunterConfig(**data.get('hunter', {})),
            platform=PlatformConfig(**data.get('platform', {}))
        )

    def save(self, path: str = "config.yaml"):
        """Save configuration to YAML file"""
        data = {
            'detection': asdict(self.detection),
            'ui': asdict(self.ui),
            'hunter': asdict(self.hunter),
            'platform': asdict(self.platform)
        }

        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, indent=2)
```

### B. Statistics Tracking

```python
# utils/statistics.py
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json
from pathlib import Path

@dataclass
class HuntStatistics:
    """Track hunting statistics"""
    start_time: datetime
    end_time: Optional[datetime] = None
    total_resets: int = 0
    shinies_found: int = 0
    average_reset_time: float = 0.0
    fastest_hunt: Optional[int] = None
    slowest_hunt: Optional[int] = None

    def update(self, reset_count: int):
        """Update statistics after finding shiny"""
        self.end_time = datetime.now()
        self.total_resets += reset_count
        self.shinies_found += 1

        if self.fastest_hunt is None or reset_count < self.fastest_hunt:
            self.fastest_hunt = reset_count

        if self.slowest_hunt is None or reset_count > self.slowest_hunt:
            self.slowest_hunt = reset_count

    def get_duration(self) -> timedelta:
        """Get total hunt duration"""
        end = self.end_time or datetime.now()
        return end - self.start_time

    def save(self, path: str = "statistics.json"):
        """Save statistics to file"""
        data = asdict(self)
        data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()

        # Load existing stats
        stats_path = Path(path)
        if stats_path.exists():
            with open(stats_path, 'r') as f:
                all_stats = json.load(f)
        else:
            all_stats = []

        all_stats.append(data)

        with open(stats_path, 'w') as f:
            json.dump(all_stats, f, indent=2)

    @classmethod
    def load_history(cls, path: str = "statistics.json") -> list:
        """Load hunting history"""
        stats_path = Path(path)
        if not stats_path.exists():
            return []

        with open(stats_path, 'r') as f:
            return json.load(f)
```

### C. Notifications

```python
# utils/notifications.py
from typing import Optional
import platform

class NotificationManager:
    """Cross-platform notification system"""

    def __init__(self):
        self.system = platform.system()

    def notify(self, title: str, message: str, sound: bool = True):
        """Send system notification"""
        if self.system == "Windows":
            self._notify_windows(title, message, sound)
        elif self.system == "Linux":
            self._notify_linux(title, message, sound)
        elif self.system == "Darwin":
            self._notify_macos(title, message, sound)

    def _notify_windows(self, title: str, message: str, sound: bool):
        """Windows notification using plyer or win10toast"""
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(
                title,
                message,
                duration=10,
                threaded=True
            )
        except ImportError:
            print(f"Notification: {title} - {message}")

    def _notify_linux(self, title: str, message: str, sound: bool):
        """Linux notification using notify-send"""
        import subprocess
        subprocess.run(['notify-send', title, message])

    def _notify_macos(self, title: str, message: str, sound: bool):
        """macOS notification using osascript"""
        import subprocess
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(['osascript', '-e', script])
```

### D. Video Recording

```python
# utils/video_recorder.py
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

class VideoRecorder:
    """Record video of shiny encounters"""

    def __init__(self, output_dir: str = "recordings", buffer_seconds: int = 30):
        """
        Args:
            output_dir: Directory to save recordings
            buffer_seconds: Seconds of video to keep before shiny found
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.buffer_seconds = buffer_seconds
        self.frame_buffer = []
        self.fps = 30
        self.recording = False
        self.writer = None

    def add_frame(self, frame: np.ndarray):
        """Add frame to buffer"""
        self.frame_buffer.append(frame)

        # Keep only last N seconds
        max_frames = self.fps * self.buffer_seconds
        if len(self.frame_buffer) > max_frames:
            self.frame_buffer.pop(0)

    def start_recording(self):
        """Start recording after shiny found"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"shiny_{timestamp}.mp4"

        # Get frame dimensions
        height, width = self.frame_buffer[0].shape[:2]

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(
            str(filename),
            fourcc,
            self.fps,
            (width, height)
        )

        # Write buffered frames
        for frame in self.frame_buffer:
            self.writer.write(frame)

        self.recording = True
        return filename

    def write_frame(self, frame: np.ndarray):
        """Write frame to video"""
        if self.recording and self.writer:
            self.writer.write(frame)

    def stop_recording(self):
        """Stop recording and save file"""
        if self.writer:
            self.writer.release()
        self.recording = False
        self.frame_buffer.clear()
```

### E. Web Dashboard (Bonus)

```python
# Optional: Web-based dashboard to monitor hunting progress
# dashboard/server.py
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading

class HunterDashboard:
    """Web dashboard for monitoring hunts"""

    def __init__(self, port: int = 5000):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.port = port
        self.stats = {}

        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('dashboard.html')

        @self.app.route('/api/stats')
        def get_stats():
            return jsonify(self.stats)

    def update_stats(self, reset_count: int, elapsed_time: str):
        """Update dashboard stats"""
        self.stats = {
            'resets': reset_count,
            'elapsed_time': elapsed_time,
            'status': 'hunting'
        }
        self.socketio.emit('stats_update', self.stats)

    def notify_shiny(self):
        """Notify dashboard of shiny find"""
        self.stats['status'] = 'shiny_found'
        self.socketio.emit('shiny_found', self.stats)

    def run(self):
        """Run dashboard server in background thread"""
        thread = threading.Thread(
            target=lambda: self.socketio.run(self.app, port=self.port)
        )
        thread.daemon = True
        thread.start()
```

---

## 9. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Restructure project with new architecture
- [ ] Implement platform abstraction layer
- [ ] Set up cross-platform CI/CD
- [ ] Create configuration system
- [ ] Add Rich logging

### Phase 2: Core Features (Weeks 3-4)
- [ ] Implement enhanced color picker
- [ ] Build screen overlay system
- [ ] Add HSV detection algorithm
- [ ] Implement multi-point sampling
- [ ] Add temporal smoothing

### Phase 3: Platform Support (Weeks 5-6)
- [ ] Implement Linux support
- [ ] Implement macOS support
- [ ] Test on all platforms
- [ ] Fix platform-specific bugs

### Phase 4: Polish & Package (Weeks 7-8)
- [ ] Extract core package
- [ ] Write documentation
- [ ] Create examples
- [ ] Add unit tests
- [ ] Publish to PyPI

### Phase 5: Advanced Features (Weeks 9-10)
- [ ] Add sparkle detection
- [ ] Implement video recording
- [ ] Add notification system
- [ ] Create web dashboard
- [ ] Add plugin system

### Phase 6: Hunter Types (Weeks 11-12)
- [ ] Implement starter hunter
- [ ] Implement wild encounter hunter
- [ ] Add breeding/egg hunter
- [ ] Create hunter presets

---

## 10. Technology Stack

### Core Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.10"

# Cross-platform libraries
mss = "^9.0.1"              # Screen capture (all platforms)
pynput = "^1.7.6"           # Input monitoring (all platforms)
opencv-python = "^4.8.1"    # Computer vision
numpy = "^1.24.0"           # Numerical operations
Pillow = "^10.1.0"          # Image processing

# UI and display
rich = "^13.7.0"            # Beautiful console output
tkinter-color picker = "^2.1.3"  # Color picker widget

# Configuration
pyyaml = "^6.0.1"           # YAML config files
python-dotenv = "^1.0.0"    # Environment variables

# Platform-specific (conditional)
pywin32 = {version = "^306", platform = "win32"}
python-xlib = {version = "^0.33", platform = "linux"}
pyobjc-framework-Quartz = {version = "^10.0", platform = "darwin"}
pyobjc-framework-Cocoa = {version = "^10.0", platform = "darwin"}

# Optional features
win10toast = {version = "^0.9", platform = "win32", optional = true}
Flask = {version = "^3.0.0", optional = true}
Flask-SocketIO = {version = "^5.3.0", optional = true}

[tool.poetry.extras]
notifications = ["win10toast"]
dashboard = ["Flask", "Flask-SocketIO"]
full = ["win10toast", "Flask", "Flask-SocketIO"]

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-cov = "^4.1.0"
pytest-mock = "^3.12.0"
black = "^23.12.0"
ruff = "^0.1.8"             # Modern linter (replaces flake8)
isort = "^5.13.0"
mypy = "^1.7.0"             # Type checking
pre-commit = "^3.6.0"       # Git hooks

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Development Tools

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12"]

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Poetry
        run: pip install poetry

      - name: Install dependencies
        run: poetry install --with dev

      - name: Run linting
        run: |
          poetry run ruff check src/
          poetry run black --check src/
          poetry run isort --check src/

      - name: Run type checking
        run: poetry run mypy src/

      - name: Run tests
        run: poetry run pytest --cov=src tests/

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Summary of Key Improvements

### 🏗️ Architecture
- Modular, platform-agnostic core
- Plugin system for extensibility
- Event-driven architecture
- Clear separation of concerns

### 🖥️ Cross-Platform
- Windows, Linux, macOS support
- Platform abstraction layer
- Conditional dependencies
- CI/CD for all platforms

### 🎨 User Experience
- Enhanced color picker with magnification
- Visual overlay showing reference points
- Rich, colorful console output
- Save/load color presets

### 🔍 Detection
- HSV color space for lighting invariance
- Multi-point sampling
- Temporal smoothing
- Tolerance-based matching
- Sparkle animation detection

### 📦 Reusability
- Standalone core package
- Published on PyPI
- Well-documented API
- Examples and tutorials

### 🐛 Debugging
- Structured logging with Rich
- Debug mode with verbose output
- Visual detection feedback
- Performance metrics

### 📊 Extras
- Statistics tracking
- Video recording
- System notifications
- Web dashboard (optional)

---

## Next Steps

1. **Review this plan** and prioritize features
2. **Set up development environment** with new structure
3. **Implement Phase 1** (Foundation)
4. **Test on multiple platforms** early and often
5. **Iterate based on feedback**

This improvement plan transforms ShinyHunter into a professional, production-ready application while maintaining its core simplicity and ease of use.
