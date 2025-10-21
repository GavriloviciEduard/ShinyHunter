# ShinyHunter - Detailed Architecture & Implementation Guide

## Table of Contents

1. [Research Analysis: Learning from Popular Shiny Hunting Bots](#1-research-analysis)
2. [Comprehensive Architecture Design](#2-comprehensive-architecture-design)
3. [Window Movement Support (Critical Feature)](#3-window-movement-support)
4. [State Machine Implementation](#4-state-machine-implementation)
5. [Advanced Detection Systems](#5-advanced-detection-systems)
6. [Plugin & Event System](#6-plugin--event-system)
7. [Complete Module Structure](#7-complete-module-structure)
8. [Implementation Details](#8-implementation-details)

---

## 1. Research Analysis: Learning from Popular Shiny Hunting Bots

### 1.1 PokéBot Gen3 - The Gold Standard

**Repository:** https://github.com/40Cakes/pokebot-gen3

#### Architecture Insights

**Core Technology:**
- Built on libmgba + mGBA Python bindings (emulator control)
- Frame-perfect timing through emulator integration
- Direct memory reading for 100% accurate detection
- Supports Ruby, Sapphire, Emerald, FireRed, LeafGreen

**Directory Structure:**
```
pokebot-gen3/
├── pokebot.py                    # Main entry point
├── modules/
│   ├── plugin_interface.py       # Plugin base class
│   ├── built_in_plugins/         # Core plugins
│   ├── memory.py                 # Memory reading (assumed)
│   ├── game_state.py             # Game state management
│   ├── battle.py                 # Battle handling
│   └── modes/                    # Different bot modes
├── plugins/                      # User plugins (git-ignored)
├── profiles/                     # User profiles
│   └── <profile_name>/
│       ├── stats.db              # SQLite database
│       ├── stats/pokemon/        # Caught Pokemon data
│       ├── screenshots/gif/      # Shiny GIFs
│       └── screenshots/cards/    # TCG cards
└── config/
    └── logging.yml               # YAML configuration
```

**Key Features We Should Adopt:**

1. **Plugin System:**
```python
# modules/plugin_interface.py (their approach)
class BotPlugin:
    """Base class for all plugins"""

    def on_battle_started(self, opponent):
        """Called when battle begins"""
        pass

    def on_pokemon_encountered(self, pokemon):
        """Called when pokemon encountered"""
        pass

    def on_shiny_found(self, pokemon):
        """Called when shiny detected"""
        pass

    def on_egg_hatched(self, pokemon):
        """Called when egg hatches"""
        pass

    def on_battle_ended(self, result):
        """Called when battle ends"""
        pass
```

2. **Memory Reading for Perfect Detection:**
   - Reads Personality ID (PID) directly from memory
   - Shiny Value (SV) = f(PID), if SV < 8 → Shiny
   - Zero false positives/negatives
   - Can peek at eggs before hatching
   - **For GB Operator:** We use visual detection, but can apply similar certainty through multi-method validation

3. **Profile System:**
   - Multiple user profiles
   - Per-profile statistics database (SQLite)
   - Per-profile screenshots and recordings
   - Configuration isolation

4. **Debug Mode:**
   - Extra debug pane showing:
     - Currently running game tasks
     - Callback queue
     - Emulator inputs
     - Battle information
     - Player status
     - Current map data
     - Daycare status
     - Event flags

**What We Can Learn:**
- ✅ Modular plugin architecture with lifecycle hooks
- ✅ Profile-based organization
- ✅ SQLite for statistics (better than JSON)
- ✅ Comprehensive debug UI
- ✅ YAML configuration files
- ✅ Git-ignored user content directories

---

### 1.2 DBJoran/Shinyhunter - Visual Detection Pioneer

**Repository:** https://github.com/DBJoran/Shinyhunter

#### Architecture Insights

**Technology Stack:**
- OpenCV-Python for visual detection
- scikit-learn Bagging classifier for OCR
- Normalizer preprocessing
- VisualBoyAdvance emulator integration
- DirectKeys for keyboard simulation

**Detection Method:**
```python
# Their approach (conceptual):
def detect_shiny(screen_region):
    """
    Use OpenCV to get color of certain pixels
    Compare with reference colors
    """
    current_color = cv2.mean(screen_region)

    # Check if color changed from normal variant
    if color_distance(current_color, normal_color) > threshold:
        return True
    return False
```

**OCR for State Detection:**
```python
# They use OCR to read screen text
# This helps determine battle state, menu state, etc.
from sklearn.ensemble import BaggingClassifier
from sklearn.preprocessing import Normalizer

# Train on screenshot data
# Recognize: "FIGHT", "BAG", "RUN", etc.
```

**What We Can Learn:**
- ✅ OCR for robust state detection (know where we are in the game)
- ✅ Color distance metrics instead of exact matching
- ✅ OpenCV integration for advanced image processing
- ✅ Machine learning for text recognition

**Limitations They Faced:**
- ❌ `.joblib` models became outdated
- ❌ Only vertical movement supported
- ❌ Tightly coupled to specific emulator

**How We'll Improve:**
- Use modern OCR (Tesseract, EasyOCR)
- Support all movement directions
- Abstract emulator/GB Operator interface

---

### 1.3 prawigya/shiny-bot-pokemon - Simplicity Approach

**Repository:** https://github.com/prawigya/shiny-bot-pokemon

#### Key Insights

**Detection Strategy:**
- Screenshot-based comparison
- Timed sleeps for navigation
- Simple soft-reset automation

**Problems Identified:**
- ❌ Timed sleeps are unreliable (developer admitted failures)
- ❌ No visual feedback
- ❌ Hard to debug timing issues

**What We Can Learn:**
- ✅ Sometimes simplicity is good for initial MVP
- ❌ **Don't rely on timed sleeps** - use state detection instead

---

### 1.4 ErebosGoD/shiny-hunting-bot - Screenshot Comparison

**Repository:** https://github.com/ErebosGoD/shiny-hunting-bot

#### Key Method

**Template Matching:**
```python
# Their approach:
import cv2

def compare_screenshots(reference, current):
    """Compare reference screenshot with current"""
    result = cv2.matchTemplate(current, reference, cv2.TM_CCOEFF_NORMED)

    # If similarity below threshold, shiny detected
    if max(result) < threshold:
        return True
    return False
```

**What We Can Learn:**
- ✅ Template matching is powerful for detecting changes
- ✅ Can detect entire sprite changes, not just pixels
- ✅ More robust against minor variations

---

### 1.5 vincenzocascone/shiny-hunting-bot - Hardware Approach

**Repository:** https://github.com/vincenzocascone/shiny-hunting-bot

#### Arduino-Based Detection

**Unique Approach:**
- Arduino microcontroller
- Photoresistor to detect light changes
- Physical button pressing
- Works on real hardware (4th gen games)

**Detection Logic:**
```
Shiny sparkle animation → Brighter screen → Photoresistor detects change
```

**What We Can Learn:**
- ✅ Hardware-based timing is more reliable than software
- ✅ Sparkle animation is consistent across Pokemon
- ✅ Can detect shinies without OCR or complex vision
- ✅ Physical separation of detection from control

**Our GB Operator Advantage:**
- GB Operator provides both display and control
- We can combine visual detection (like Arduino's photoresistor) with direct input
- Best of both worlds: software flexibility + hardware reliability

---

### 1.6 vyabor/shiny-pokemon-ML - Machine Learning Approach

**Repository:** https://github.com/vyabor/shiny-pokemon-ML

#### Modern AI Detection

**Technology:**
- Ultralytics YOLOv8 (object detection)
- Real-time detection while playing
- Currently supports Swablu (expandable)

**Architecture:**
```python
from ultralytics import YOLO

# Load trained model
model = YOLO('shiny_detector.pt')

# Real-time detection
results = model(frame)

for result in results:
    if result.confidence > threshold:
        # Shiny detected!
        trigger_alert()
```

**What We Can Learn:**
- ✅ ML can detect shinies based on visual appearance
- ✅ Works while actively playing (not just automation)
- ✅ Can be trained for any Pokemon
- ✅ Future-proof: improves with more data

**Implementation for Us:**
- Train YOLO on normal vs shiny sprites
- Use as secondary validation method
- Combine with pixel/color detection for highest confidence

---

### 1.7 PokemonAutomation - Enterprise-Grade Solution

**Website:** https://pokemonautomation.github.io/

#### Professional Architecture

**Technology Stack:**
- Computer-control with capture card
- Video and audio analysis
- Machine learning detection
- Supports Switch, DS, and other consoles

**Detection Methods:**
1. **Visual:** Shiny sparkle animation recognition
2. **Audio:** Shiny sound effect detection
3. **Hybrid:** Combined confidence scoring

**Key Features:**
- Automatic video recording on shiny
- Distinguishes star vs square shinies
- Notification system
- Multi-game support
- Unattended operation

**What We Can Learn:**
- ✅ **Multi-modal detection** (visual + audio) for certainty
- ✅ Confidence scoring instead of binary yes/no
- ✅ Automatic video capture of encounters
- ✅ Star vs square distinction (attention to detail)
- ✅ Production-ready notification system

---

## 2. Comprehensive Architecture Design

### 2.1 High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          ShinyHunter Application                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐            │
│  │     CLI      │      │  GUI (opt)   │      │ Web Dashboard│            │
│  │   Interface  │      │   Tkinter    │      │   (Flask)    │            │
│  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘            │
│         │                     │                      │                     │
│         └─────────────────────┴──────────────────────┘                     │
│                                │                                            │
│  ┌─────────────────────────────▼──────────────────────────────┐           │
│  │                     Application Core                        │           │
│  │  ┌────────────────────────────────────────────────────┐   │           │
│  │  │         Hunter Orchestrator                         │   │           │
│  │  │  - Manages hunter lifecycle                         │   │           │
│  │  │  - Coordinates between subsystems                   │   │           │
│  │  │  - Event dispatching                                │   │           │
│  │  └────────────┬───────────────────────────────────────┘   │           │
│  │               │                                             │           │
│  │  ┌────────────▼────────────┐  ┌───────────────────────┐  │           │
│  │  │   State Machine         │  │   Event System        │  │           │
│  │  │  - IDLE                 │  │  - Observers          │  │           │
│  │  │  - CALIBRATING          │  │  - Event bus          │  │           │
│  │  │  - HUNTING              │  │  - Plugin hooks       │  │           │
│  │  │  - RESETTING            │  │                       │  │           │
│  │  │  - CHECKING             │  │                       │  │           │
│  │  │  - SHINY_FOUND          │  │                       │  │           │
│  │  └─────────────────────────┘  └───────────────────────┘  │           │
│  └─────────────────────────────────────────────────────────────┘           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      Detection Layer                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │   Pixel      │  │     HSV      │  │   Pattern    │              │  │
│  │  │  Detector    │  │  Detector    │  │  Detector    │              │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │  │
│  │         │                  │                  │                       │  │
│  │  ┌──────▼──────────────────▼──────────────────▼───────┐             │  │
│  │  │        Detection Fusion Engine                      │             │  │
│  │  │  - Combines multiple detection methods              │             │  │
│  │  │  - Confidence scoring                                │             │  │
│  │  │  - Temporal smoothing                                │             │  │
│  │  │  - Voting system                                     │             │  │
│  │  └─────────────────────────────────────────────────────┘             │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                    Platform Abstraction Layer                        │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │  │
│  │  │ Window Manager   │  │  Input Simulator │  │  Screen Capture  │  │  │
│  │  │  - Find window   │  │  - Send keys     │  │  - Grab pixels   │  │  │
│  │  │  - Track position│  │  - Press combos  │  │  - Get regions   │  │  │
│  │  │  - Activate      │  │  - Focus-aware   │  │  - Rel. coords   │  │  │
│  │  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  │  │
│  │           │                     │                      │             │  │
│  │  ┌────────▼─────────────────────▼──────────────────────▼─────────┐  │  │
│  │  │              Platform Factory                                  │  │  │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────┐                │  │  │
│  │  │  │  Windows   │ │   Linux    │ │   macOS    │                │  │  │
│  │  │  │Implementation│ │Implementation│ │Implementation│                │  │  │
│  │  │  └────────────┘ └────────────┘ └────────────┘                │  │  │
│  │  └───────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      Subsystems                                      │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │  │
│  │  │  UI Layer  │ │ Statistics │ │   Logger   │ │  Recorder  │       │  │
│  │  │  - Overlay │ │  - Tracker │ │  - Rich    │ │  - Video   │       │  │
│  │  │  - Picker  │ │  - Database│ │  - Files   │ │  - Buffer  │       │  │
│  │  │  - Console │ │  - Export  │ │  - Levels  │ │  - FFmpeg  │       │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │  │
│  │                                                                       │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐                       │  │
│  │  │  Notifier  │ │   Config   │ │  Profiles  │                       │  │
│  │  │  - System  │ │  - YAML    │ │  - Manager │                       │  │
│  │  │  - Discord │ │  - Schema  │ │  - Switch  │                       │  │
│  │  │  - Email   │ │  - Validate│ │  - Isolate │                       │  │
│  │  └────────────┘ └────────────┘ └────────────┘                       │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      Plugin System                                   │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │              Plugin Manager                                   │   │  │
│  │  │  - Discover plugins from plugins/ directory                   │   │  │
│  │  │  - Load and initialize                                        │   │  │
│  │  │  - Lifecycle management                                       │   │  │
│  │  │  - Hook into events                                           │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                       │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │  │
│  │  │  Discord   │ │  Telegram  │ │   Stats    │ │   Custom   │       │  │
│  │  │   Plugin   │ │   Plugin   │ │  Exporter  │ │  Plugins   │       │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Detailed Module Structure

```
shinyhunter/
├── pyproject.toml
├── setup.py
├── README.md
├── LICENSE
├── .env.example
│
├── shinyhunter/                      # Main package
│   ├── __init__.py
│   ├── __main__.py                   # Entry point for `python -m shinyhunter`
│   │
│   ├── core/                         # Core business logic
│   │   ├── __init__.py
│   │   ├── orchestrator.py           # Main hunter orchestrator
│   │   ├── hunter_base.py            # Abstract hunter base class
│   │   ├── state_machine.py          # State machine implementation
│   │   ├── event_bus.py              # Event system
│   │   ├── exceptions.py             # Custom exceptions
│   │   └── types.py                  # Type definitions, enums
│   │
│   ├── hunters/                      # Hunter implementations
│   │   ├── __init__.py
│   │   ├── registry.py               # Hunter registry
│   │   ├── stationary.py             # Stationary Pokemon hunter
│   │   ├── starter.py                # Starter Pokemon hunter
│   │   ├── wild_encounter.py         # Wild encounter hunter
│   │   ├── breeding.py               # Egg breeding hunter
│   │   └── legendary.py              # Legendary Pokemon hunter
│   │
│   ├── detection/                    # Detection algorithms
│   │   ├── __init__.py
│   │   ├── base.py                   # Detection interface
│   │   ├── pixel.py                  # Pixel-based detection
│   │   ├── hsv.py                    # HSV color space detection
│   │   ├── pattern.py                # Template matching
│   │   ├── sparkle.py                # Sparkle animation detection
│   │   ├── ml.py                     # Machine learning detection
│   │   ├── fusion.py                 # Detection fusion engine
│   │   ├── smoothing.py              # Temporal smoothing
│   │   └── calibration.py            # Auto-calibration system
│   │
│   ├── platform/                     # Platform-specific code
│   │   ├── __init__.py
│   │   ├── base.py                   # Platform interface (Protocol)
│   │   ├── factory.py                # Platform factory
│   │   ├── window_manager.py         # Window management base
│   │   ├── input_simulator.py        # Input simulation base
│   │   ├── screen_capture.py         # Screen capture base
│   │   │
│   │   ├── windows/
│   │   │   ├── __init__.py
│   │   │   ├── window_manager.py
│   │   │   ├── input_simulator.py
│   │   │   └── screen_capture.py
│   │   │
│   │   ├── linux/
│   │   │   ├── __init__.py
│   │   │   ├── window_manager.py
│   │   │   ├── input_simulator.py
│   │   │   └── screen_capture.py
│   │   │
│   │   └── macos/
│   │       ├── __init__.py
│   │       ├── window_manager.py
│   │       ├── input_simulator.py
│   │       └── screen_capture.py
│   │
│   ├── ui/                           # User interface components
│   │   ├── __init__.py
│   │   ├── console.py                # Rich console interface
│   │   ├── overlay.py                # Screen overlay system
│   │   ├── color_picker.py           # Enhanced color picker
│   │   ├── calibration_ui.py         # Calibration wizard UI
│   │   ├── dashboard.py              # Web dashboard (Flask)
│   │   └── widgets/
│   │       ├── __init__.py
│   │       ├── magnifier.py          # Magnifying glass widget
│   │       ├── color_swatch.py       # Color display widget
│   │       └── crosshair.py          # Crosshair overlay
│   │
│   ├── config/                       # Configuration management
│   │   ├── __init__.py
│   │   ├── manager.py                # Config manager
│   │   ├── schema.py                 # Configuration schema
│   │   ├── validator.py              # Configuration validation
│   │   ├── profiles.py               # Profile management
│   │   └── defaults.py               # Default configurations
│   │
│   ├── data/                         # Data models
│   │   ├── __init__.py
│   │   ├── color_point.py            # Color point model
│   │   ├── detection_result.py       # Detection result model
│   │   ├── hunt_session.py           # Hunt session model
│   │   ├── statistics.py             # Statistics model
│   │   └── window_info.py            # Window information model
│   │
│   ├── storage/                      # Data persistence
│   │   ├── __init__.py
│   │   ├── database.py               # SQLite database manager
│   │   ├── migrations/               # Database migrations
│   │   │   ├── __init__.py
│   │   │   ├── v1_initial.py
│   │   │   └── v2_add_profiles.py
│   │   ├── repositories/             # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── hunt_repository.py
│   │   │   ├── stats_repository.py
│   │   │   └── profile_repository.py
│   │   └── exporters/                # Export functionality
│   │       ├── __init__.py
│   │       ├── csv_exporter.py
│   │       ├── json_exporter.py
│   │       └── html_exporter.py
│   │
│   ├── plugins/                      # Plugin system
│   │   ├── __init__.py
│   │   ├── manager.py                # Plugin manager
│   │   ├── interface.py              # Plugin interface
│   │   ├── loader.py                 # Plugin loader
│   │   ├── hooks.py                  # Hook definitions
│   │   └── builtin/                  # Built-in plugins
│   │       ├── __init__.py
│   │       ├── discord_notifier.py
│   │       ├── telegram_notifier.py
│   │       ├── auto_save_video.py
│   │       └── statistics_logger.py
│   │
│   ├── recording/                    # Video/screenshot recording
│   │   ├── __init__.py
│   │   ├── recorder.py               # Video recorder
│   │   ├── buffer.py                 # Circular buffer
│   │   ├── screenshot.py             # Screenshot manager
│   │   └── gif_maker.py              # GIF creation
│   │
│   ├── notifications/                # Notification system
│   │   ├── __init__.py
│   │   ├── manager.py                # Notification manager
│   │   ├── system.py                 # System notifications
│   │   ├── discord.py                # Discord integration
│   │   ├── telegram.py               # Telegram integration
│   │   ├── email.py                  # Email notifications
│   │   └── webhook.py                # Generic webhook
│   │
│   ├── utils/                        # Utility modules
│   │   ├── __init__.py
│   │   ├── logging.py                # Logging configuration
│   │   ├── timing.py                 # Timing utilities
│   │   ├── color.py                  # Color conversion utilities
│   │   ├── image.py                  # Image processing utilities
│   │   ├── validators.py             # Input validators
│   │   ├── coordinates.py            # Coordinate system utilities
│   │   └── decorators.py             # Useful decorators
│   │
│   └── cli/                          # Command-line interface
│       ├── __init__.py
│       ├── main.py                   # Main CLI entry point
│       ├── commands/                 # CLI commands
│       │   ├── __init__.py
│       │   ├── hunt.py               # Hunt command
│       │   ├── calibrate.py          # Calibration command
│       │   ├── stats.py              # Statistics command
│       │   ├── config.py             # Configuration command
│       │   └── profile.py            # Profile management
│       └── formatters.py             # Output formatters
│
├── config/                           # Configuration files
│   ├── default.yaml                  # Default configuration
│   ├── presets/                      # Preset configurations
│   │   ├── gen1_red_blue.yaml
│   │   ├── gen2_gold_silver.yaml
│   │   ├── gen3_ruby_sapphire.yaml
│   │   └── custom_example.yaml
│   └── schemas/                      # JSON schemas
│       ├── config_schema.json
│       └── preset_schema.json
│
├── profiles/                         # User profiles (git-ignored)
│   ├── default/
│   │   ├── config.yaml
│   │   ├── color_presets.json
│   │   ├── statistics.db
│   │   ├── screenshots/
│   │   ├── videos/
│   │   └── logs/
│   └── .gitkeep
│
├── plugins/                          # User plugins (git-ignored)
│   ├── README.md                     # Plugin development guide
│   ├── example_plugin.py.example     # Example plugin template
│   └── .gitkeep
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest configuration
│   ├── unit/                         # Unit tests
│   │   ├── test_detection.py
│   │   ├── test_state_machine.py
│   │   ├── test_color_picker.py
│   │   └── ...
│   ├── integration/                  # Integration tests
│   │   ├── test_hunter_flow.py
│   │   ├── test_plugin_system.py
│   │   └── ...
│   ├── platform/                     # Platform-specific tests
│   │   ├── test_windows.py
│   │   ├── test_linux.py
│   │   └── test_macos.py
│   └── fixtures/                     # Test fixtures
│       ├── images/
│       ├── configs/
│       └── recordings/
│
├── docs/                             # Documentation
│   ├── README.md
│   ├── getting_started.md
│   ├── architecture.md
│   ├── api/                          # API documentation
│   │   ├── core.md
│   │   ├── detection.md
│   │   ├── platform.md
│   │   └── plugins.md
│   ├── guides/                       # User guides
│   │   ├── calibration.md
│   │   ├── creating_plugins.md
│   │   ├── custom_hunters.md
│   │   └── troubleshooting.md
│   └── examples/                     # Code examples
│       ├── basic_usage.py
│       ├── custom_detector.py
│       └── plugin_example.py
│
└── scripts/                          # Utility scripts
    ├── setup_dev.sh
    ├── run_tests.sh
    ├── build.sh
    └── generate_docs.sh
```

---

## 3. Window Movement Support (Critical Feature)

### 3.1 The Problem

**Current Issue:**
- Color picker and detection use **absolute screen coordinates**
- When user moves GB Operator window → coordinates become invalid
- Bot breaks immediately after window movement

**Example:**
```python
# Current (BROKEN) approach:
reference_point = (500, 300)  # Absolute screen coordinates
color = get_pixel(500, 300)   # ❌ Wrong if window moved!
```

### 3.2 The Solution: Window-Relative Coordinates

**Coordinate System Types:**

1. **Screen/Absolute Coordinates:**
   - Origin (0,0) = top-left corner of screen
   - Never changes
   - Used by: mouse, display systems

2. **Window-Relative Coordinates:**
   - Origin (0,0) = top-left corner of window **client area**
   - Changes when window moves
   - Independent of window position

3. **Client vs Non-Client Area:**
   ```
   ┌──────────────────────────────────────┐  ┐
   │  Title Bar                      │☐│✕│  │ Non-client area
   ├──────────────────────────────────────┤  ┘
   │                                      │  ┐
   │         Client Area                  │  │ Client area
   │    (actual game display)             │  │ (what we care about)
   │                                      │  │
   │                                      │  │
   └──────────────────────────────────────┘  ┘
   ```

### 3.3 Implementation

#### A. Window Position Tracker

```python
# platform/window_manager.py
from dataclasses import dataclass
from typing import Tuple, Optional
from abc import ABC, abstractmethod

@dataclass
class WindowGeometry:
    """Complete window geometry information"""
    # Screen-absolute coordinates
    x: int                    # Window position X (including frame)
    y: int                    # Window position Y (including frame)
    width: int                # Total window width (including frame)
    height: int               # Total window height (including frame)

    # Client area (actual content)
    client_x: int             # Client area position X (absolute)
    client_y: int             # Client area position Y (absolute)
    client_width: int         # Client area width
    client_height: int        # Client area height

    # Frame dimensions
    frame_left: int           # Left border width
    frame_top: int            # Title bar + top border height
    frame_right: int          # Right border width
    frame_bottom: int         # Bottom border height

    def client_to_screen(self, client_x: int, client_y: int) -> Tuple[int, int]:
        """Convert client-relative to screen-absolute coordinates"""
        screen_x = self.client_x + client_x
        screen_y = self.client_y + client_y
        return (screen_x, screen_y)

    def screen_to_client(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Convert screen-absolute to client-relative coordinates"""
        client_x = screen_x - self.client_x
        client_y = screen_y - self.client_y
        return (client_x, client_y)

    def is_point_in_client(self, screen_x: int, screen_y: int) -> bool:
        """Check if screen coordinates are within client area"""
        return (
            self.client_x <= screen_x < self.client_x + self.client_width and
            self.client_y <= screen_y < self.client_y + self.client_height
        )

class WindowManagerBase(ABC):
    """Base class for window management"""

    @abstractmethod
    def find_window(self, title: str) -> Optional[int]:
        """Find window by title, return handle"""
        pass

    @abstractmethod
    def get_geometry(self, handle: int) -> WindowGeometry:
        """Get complete window geometry"""
        pass

    @abstractmethod
    def set_foreground(self, handle: int):
        """Bring window to foreground"""
        pass

    @abstractmethod
    def is_window_valid(self, handle: int) -> bool:
        """Check if window handle is still valid"""
        pass
```

#### B. Platform-Specific Implementations

**Windows Implementation:**
```python
# platform/windows/window_manager.py
import ctypes
from ctypes import wintypes
import win32gui
import win32con
from typing import Optional

class WindowsWindowManager(WindowManagerBase):
    """Windows-specific window management"""

    def __init__(self):
        self.user32 = ctypes.windll.user32

    def find_window(self, title: str) -> Optional[int]:
        """Find window by partial title match"""
        windows = []

        def enum_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if title.lower() in window_title.lower():
                    windows.append(hwnd)
            return True

        win32gui.EnumWindows(enum_callback, None)
        return windows[0] if windows else None

    def get_geometry(self, handle: int) -> WindowGeometry:
        """Get window geometry using Windows API"""
        # Get window rectangle (includes frame)
        window_rect = win32gui.GetWindowRect(handle)
        x, y, right, bottom = window_rect
        width = right - x
        height = bottom - y

        # Get client rectangle (content area only)
        client_rect = win32gui.GetClientRect(handle)
        client_width = client_rect[2]
        client_height = client_rect[3]

        # Convert client (0,0) to screen coordinates
        client_topleft = win32gui.ClientToScreen(handle, (0, 0))
        client_x, client_y = client_topleft

        # Calculate frame sizes
        frame_left = client_x - x
        frame_top = client_y - y
        frame_right = (x + width) - (client_x + client_width)
        frame_bottom = (y + height) - (client_y + client_height)

        return WindowGeometry(
            x=x,
            y=y,
            width=width,
            height=height,
            client_x=client_x,
            client_y=client_y,
            client_width=client_width,
            client_height=client_height,
            frame_left=frame_left,
            frame_top=frame_top,
            frame_right=frame_right,
            frame_bottom=frame_bottom
        )

    def set_foreground(self, handle: int):
        """Activate window"""
        # Windows requires special handling for SetForegroundWindow
        if win32gui.IsIconic(handle):
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)

        # Use alt-tab trick to allow SetForegroundWindow
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")
        win32gui.SetForegroundWindow(handle)

    def is_window_valid(self, handle: int) -> bool:
        """Check if window still exists"""
        return win32gui.IsWindow(handle)
```

**Linux Implementation:**
```python
# platform/linux/window_manager.py
import subprocess
from Xlib import X, display, Xutil
from typing import Optional

class LinuxWindowManager(WindowManagerBase):
    """Linux-specific window management using X11"""

    def __init__(self):
        self.display = display.Display()
        self.root = self.display.screen().root

    def find_window(self, title: str) -> Optional[int]:
        """Find window by title using xdotool"""
        try:
            result = subprocess.run(
                ['xdotool', 'search', '--name', title],
                capture_output=True,
                text=True,
                check=False
            )

            if result.stdout:
                # Return first matching window ID
                window_id = result.stdout.strip().split('\n')[0]
                return int(window_id)
            return None
        except FileNotFoundError:
            raise RuntimeError("xdotool not installed. Install with: sudo apt-get install xdotool")

    def get_geometry(self, handle: int) -> WindowGeometry:
        """Get window geometry using Xlib"""
        window = self.display.create_resource_object('window', handle)

        # Get window geometry
        geom = window.get_geometry()

        # Translate to root window coordinates
        coords = window.translate_coords(self.root, 0, 0)

        # Get window attributes for border width
        attrs = window.get_attributes()
        border_width = attrs.border_width

        # Get frame extents (decorations)
        frame_extents = self._get_frame_extents(window)

        return WindowGeometry(
            x=coords.x - frame_extents['left'],
            y=coords.y - frame_extents['top'],
            width=geom.width + frame_extents['left'] + frame_extents['right'],
            height=geom.height + frame_extents['top'] + frame_extents['bottom'],
            client_x=coords.x,
            client_y=coords.y,
            client_width=geom.width,
            client_height=geom.height,
            frame_left=frame_extents['left'],
            frame_top=frame_extents['top'],
            frame_right=frame_extents['right'],
            frame_bottom=frame_extents['bottom']
        )

    def _get_frame_extents(self, window) -> dict:
        """Get window decoration sizes"""
        try:
            atom = self.display.intern_atom('_NET_FRAME_EXTENTS')
            prop = window.get_full_property(atom, X.AnyPropertyType)

            if prop and prop.value:
                left, right, top, bottom = prop.value
                return {
                    'left': left,
                    'right': right,
                    'top': top,
                    'bottom': bottom
                }
        except:
            pass

        # Fallback to defaults if not available
        return {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    def set_foreground(self, handle: int):
        """Activate window using xdotool"""
        subprocess.run(['xdotool', 'windowactivate', str(handle)])

    def is_window_valid(self, handle: int) -> bool:
        """Check if window exists"""
        try:
            window = self.display.create_resource_object('window', handle)
            window.get_attributes()
            return True
        except:
            return False
```

**macOS Implementation:**
```python
# platform/macos/window_manager.py
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionAll,
    kCGNullWindowID,
    CGWindowListCreateDescriptionFromArray
)
from AppKit import NSWorkspace, NSRunningApplication
from typing import Optional
import Quartz

class MacOSWindowManager(WindowManagerBase):
    """macOS-specific window management"""

    def find_window(self, title: str) -> Optional[int]:
        """Find window by title"""
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionAll,
            kCGNullWindowID
        )

        for window in window_list:
            window_title = window.get('kCGWindowName', '')
            if title.lower() in window_title.lower():
                return window['kCGWindowNumber']

        return None

    def get_geometry(self, handle: int) -> WindowGeometry:
        """Get window geometry"""
        # Get specific window info
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionAll,
            kCGNullWindowID
        )

        window_info = None
        for window in window_list:
            if window['kCGWindowNumber'] == handle:
                window_info = window
                break

        if not window_info:
            raise ValueError(f"Window {handle} not found")

        bounds = window_info['kCGWindowBounds']

        # macOS doesn't distinguish between client and window area easily
        # For most apps, they're the same
        return WindowGeometry(
            x=int(bounds['X']),
            y=int(bounds['Y']),
            width=int(bounds['Width']),
            height=int(bounds['Height']),
            client_x=int(bounds['X']),
            client_y=int(bounds['Y']),
            client_width=int(bounds['Width']),
            client_height=int(bounds['Height']),
            frame_left=0,
            frame_top=0,
            frame_right=0,
            frame_bottom=0
        )

    def set_foreground(self, handle: int):
        """Activate window"""
        # Get app that owns this window
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionAll,
            kCGNullWindowID
        )

        for window in window_list:
            if window['kCGWindowNumber'] == handle:
                pid = window['kCGWindowOwnerPID']
                app = NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
                if app:
                    app.activateWithOptions_(1)  # NSApplicationActivateIgnoringOtherApps
                break

    def is_window_valid(self, handle: int) -> bool:
        """Check if window exists"""
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionAll,
            kCGNullWindowID
        )

        for window in window_list:
            if window['kCGWindowNumber'] == handle:
                return True
        return False
```

#### C. Window-Aware Screen Capture

```python
# platform/screen_capture.py
from typing import Tuple
import numpy as np
from mss import mss

class WindowAwareScreenCapture:
    """Screen capture that tracks window position"""

    def __init__(self, window_manager: WindowManagerBase, window_handle: int):
        self.window_manager = window_manager
        self.window_handle = window_handle
        self.sct = mss()
        self._update_geometry()

    def _update_geometry(self):
        """Update window geometry (call before each capture)"""
        self.geometry = self.window_manager.get_geometry(self.window_handle)

    def get_pixel(self, rel_x: int, rel_y: int) -> Tuple[int, int, int]:
        """
        Get pixel color using window-relative coordinates

        Args:
            rel_x: X coordinate relative to window client area (0 = left edge)
            rel_y: Y coordinate relative to window client area (0 = top edge)

        Returns:
            RGB tuple
        """
        # Update geometry in case window moved
        self._update_geometry()

        # Convert to screen coordinates
        screen_x, screen_y = self.geometry.client_to_screen(rel_x, rel_y)

        # Capture 1x1 pixel
        pixel_box = {
            "top": screen_y,
            "left": screen_x,
            "width": 1,
            "height": 1
        }

        return self.sct.grab(pixel_box).pixel(0, 0)

    def get_region(
        self,
        rel_x: int,
        rel_y: int,
        width: int,
        height: int
    ) -> np.ndarray:
        """
        Capture screen region using window-relative coordinates

        Args:
            rel_x: X coordinate relative to window client area
            rel_y: Y coordinate relative to window client area
            width: Region width
            height: Region height

        Returns:
            numpy array (BGR format)
        """
        # Update geometry
        self._update_geometry()

        # Convert to screen coordinates
        screen_x, screen_y = self.geometry.client_to_screen(rel_x, rel_y)

        # Capture region
        region_box = {
            "top": screen_y,
            "left": screen_x,
            "width": width,
            "height": height
        }

        screenshot = self.sct.grab(region_box)
        return np.array(screenshot)

    def get_entire_client_area(self) -> np.ndarray:
        """Capture entire window client area"""
        self._update_geometry()

        region_box = {
            "top": self.geometry.client_y,
            "left": self.geometry.client_x,
            "width": self.geometry.client_width,
            "height": self.geometry.client_height
        }

        screenshot = self.sct.grab(region_box)
        return np.array(screenshot)
```

#### D. Color Point with Relative Coordinates

```python
# data/color_point.py
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class ColorPoint:
    """
    Immutable color point using window-relative coordinates
    """
    # Color information
    color_rgb: Tuple[int, int, int]     # RGB color
    color_hsv: Tuple[int, int, int]     # HSV color (for reference)

    # Position (window-relative)
    rel_x: int                          # X relative to window client area
    rel_y: int                          # Y relative to window client area

    # Metadata
    name: str = ""                      # Optional label
    confidence: float = 1.0             # Detection confidence (0-1)

    # Screen coordinates at time of capture (for reference only)
    screen_x: int = 0                   # Absolute screen X when picked
    screen_y: int = 0                   # Absolute screen Y when picked

    def __str__(self) -> str:
        return (
            f"ColorPoint({self.name!r}, "
            f"RGB{self.color_rgb}, "
            f"rel_pos=({self.rel_x}, {self.rel_y}))"
        )
```

#### E. Updated Color Picker

```python
# ui/color_picker.py
from typing import Optional
import tkinter as tk
from pynput import mouse

class WindowRelativeColorPicker:
    """Color picker that stores window-relative coordinates"""

    def __init__(
        self,
        window_manager: WindowManagerBase,
        window_handle: int,
        screen_capture: WindowAwareScreenCapture
    ):
        self.window_manager = window_manager
        self.window_handle = window_handle
        self.screen_capture = screen_capture
        self.geometry = window_manager.get_geometry(window_handle)

    def pick_color(self) -> Optional[ColorPoint]:
        """
        Interactive color picking with window-relative storage

        Returns:
            ColorPoint with window-relative coordinates
        """
        print("Click on the pixel you want to select...")
        print("(Make sure the window doesn't move during selection)")

        selected = {'point': None}

        def on_click(x, y, button, pressed):
            if button == mouse.Button.left and pressed:
                # Update geometry in case window moved
                self.geometry = self.window_manager.get_geometry(self.window_handle)

                # Check if click is within window client area
                if not self.geometry.is_point_in_client(x, y):
                    print(f"❌ Click at ({x}, {y}) is outside window client area")
                    return False

                # Convert screen to window-relative coordinates
                rel_x, rel_y = self.geometry.screen_to_client(x, y)

                # Get color at this pixel
                rgb = self.screen_capture.get_pixel(rel_x, rel_y)
                hsv = self._rgb_to_hsv(rgb)

                # Display info
                print(f"\nSelected pixel:")
                print(f"  Screen position: ({x}, {y})")
                print(f"  Window-relative: ({rel_x}, {rel_y})")
                print(f"  RGB: {rgb}")
                print(f"  HSV: {hsv}")

                # Ask for confirmation
                confirm = input("Save this color point? (y/n): ").lower()

                if confirm == 'y':
                    name = input("Enter name for this point (optional): ").strip()

                    selected['point'] = ColorPoint(
                        color_rgb=rgb,
                        color_hsv=hsv,
                        rel_x=rel_x,
                        rel_y=rel_y,
                        name=name,
                        screen_x=x,
                        screen_y=y
                    )
                    return False  # Stop listener
                else:
                    print("Selection cancelled. Click again...")

            return True  # Continue listening

        # Start mouse listener
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

        return selected['point']

    @staticmethod
    def _rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert RGB to HSV (OpenCV format)"""
        import colorsys
        r, g, b = [x / 255.0 for x in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (int(h * 180), int(s * 255), int(v * 255))
```

#### F. Movement Detection & Auto-Recovery

```python
# core/window_tracker.py
from typing import Optional, Callable
import time
import threading

class WindowMovementTracker:
    """
    Monitors window for movement and triggers callbacks
    """

    def __init__(
        self,
        window_manager: WindowManagerBase,
        window_handle: int,
        check_interval: float = 0.5  # Check every 500ms
    ):
        self.window_manager = window_manager
        self.window_handle = window_handle
        self.check_interval = check_interval

        self.last_geometry: Optional[WindowGeometry] = None
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None

        # Callbacks
        self.on_moved: Optional[Callable] = None
        self.on_resized: Optional[Callable] = None
        self.on_closed: Optional[Callable] = None

    def start_monitoring(self):
        """Start monitoring window for changes"""
        if self.monitoring:
            return

        self.monitoring = True
        self.last_geometry = self.window_manager.get_geometry(self.window_handle)

        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)

    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                # Check if window still exists
                if not self.window_manager.is_window_valid(self.window_handle):
                    if self.on_closed:
                        self.on_closed()
                    break

                # Get current geometry
                current = self.window_manager.get_geometry(self.window_handle)

                # Check for movement
                if (current.client_x != self.last_geometry.client_x or
                    current.client_y != self.last_geometry.client_y):

                    if self.on_moved:
                        self.on_moved(self.last_geometry, current)

                    self.last_geometry = current

                # Check for resize
                elif (current.client_width != self.last_geometry.client_width or
                      current.client_height != self.last_geometry.client_height):

                    if self.on_resized:
                        self.on_resized(self.last_geometry, current)

                    self.last_geometry = current

            except Exception as e:
                # Log error but continue monitoring
                print(f"Error monitoring window: {e}")

            time.sleep(self.check_interval)
```

### 3.4 Usage Example

```python
# Example: Using window-relative coordinates in hunter

from platform.factory import get_platform_implementation

# Initialize platform-specific components
platform = get_platform_implementation()
window_manager = platform.get_window_manager()

# Find GB Operator window
window_handle = window_manager.find_window("operator")
if not window_handle:
    raise RuntimeError("GB Operator window not found")

# Create window-aware screen capture
screen_capture = WindowAwareScreenCapture(window_manager, window_handle)

# Pick color points (stores window-relative coordinates)
picker = WindowRelativeColorPicker(window_manager, window_handle, screen_capture)

print("Select reference point...")
reference_point = picker.pick_color()

print("Select target point...")
target_point = picker.pick_color()

# Setup movement tracking
tracker = WindowMovementTracker(window_manager, window_handle)

def on_window_moved(old_geom, new_geom):
    print(f"⚠️  Window moved from ({old_geom.client_x}, {old_geom.client_y}) "
          f"to ({new_geom.client_x}, {new_geom.client_y})")
    print("✅ No problem! Using window-relative coordinates.")

def on_window_closed():
    print("❌ GB Operator window closed!")
    # Stop hunting
    hunter.stop()

tracker.on_moved = on_window_moved
tracker.on_closed = on_window_closed
tracker.start_monitoring()

# Hunt loop - works regardless of window position!
while hunting:
    # These use window-relative coordinates, so they work even if window moves
    ref_color = screen_capture.get_pixel(reference_point.rel_x, reference_point.rel_y)
    target_color = screen_capture.get_pixel(target_point.rel_x, target_point.rel_y)

    if ref_color == reference_point.color_rgb:
        # Reference found, check target
        if target_color != target_point.color_rgb:
            print("🌟 SHINY FOUND! 🌟")
            break
```

---

## 4. State Machine Implementation

### 4.1 Hunter States

Based on research from PokemonAutomation and PokéBot Gen3, we'll implement a comprehensive state machine:

```python
# core/state_machine.py
from enum import Enum, auto
from typing import Dict, Set, Optional, Callable
from dataclasses import dataclass
import logging

class HunterState(Enum):
    """All possible hunter states"""

    # Initial states
    UNINITIALIZED = auto()      # Bot not yet set up
    INITIALIZING = auto()       # Setting up platform, window, etc.

    # Calibration states
    CALIBRATING = auto()        # User selecting color points
    CALIBRATION_FAILED = auto() # Calibration failed

    # Ready state
    READY = auto()              # Calibrated and ready to hunt

    # Hunting states
    STARTING_HUNT = auto()      # Initializing hunt session
    HUNTING = auto()            # Main hunting loop active
    RESETTING = auto()          # Performing soft reset
    WAITING_FOR_LOAD = auto()   # Waiting for game to load
    CHECKING_POKEMON = auto()   # Checking if shiny

    # Result states
    SHINY_FOUND = auto()        # Shiny detected!
    HUNT_PAUSED = auto()        # User paused
    HUNT_STOPPED = auto()       # User stopped

    # Error states
    ERROR = auto()              # Error occurred
    WINDOW_LOST = auto()        # Target window closed/lost

    # Cleanup
    CLEANING_UP = auto()        # Shutting down gracefully
    TERMINATED = auto()         # Fully shut down

@dataclass
class StateTransition:
    """Represents a state transition"""
    from_state: HunterState
    to_state: HunterState
    event: str
    condition: Optional[Callable[[], bool]] = None
    action: Optional[Callable] = None

class HunterStateMachine:
    """
    State machine for hunter lifecycle

    Based on patterns from:
    - pytransitions library
    - Game Programming Patterns book
    - PokéBot Gen3 architecture
    """

    def __init__(self):
        self.current_state = HunterState.UNINITIALIZED
        self.previous_state: Optional[HunterState] = None
        self.logger = logging.getLogger(__name__)

        # Transition definitions
        self.transitions: Dict[HunterState, Dict[str, StateTransition]] = {}
        self._define_transitions()

        # State entry/exit callbacks
        self.on_enter_callbacks: Dict[HunterState, list] = {state: [] for state in HunterState}
        self.on_exit_callbacks: Dict[HunterState, list] = {state: [] for state in HunterState}

        # Transition callbacks
        self.on_transition_callbacks: list = []

    def _define_transitions(self):
        """Define all valid state transitions"""

        # Initial transitions
        self._add_transition(
            HunterState.UNINITIALIZED,
            HunterState.INITIALIZING,
            'initialize'
        )

        self._add_transition(
            HunterState.INITIALIZING,
            HunterState.CALIBRATING,
            'init_success'
        )

        self._add_transition(
            HunterState.INITIALIZING,
            HunterState.ERROR,
            'init_failed'
        )

        # Calibration transitions
        self._add_transition(
            HunterState.CALIBRATING,
            HunterState.READY,
            'calibration_complete'
        )

        self._add_transition(
            HunterState.CALIBRATING,
            HunterState.CALIBRATION_FAILED,
            'calibration_failed'
        )

        self._add_transition(
            HunterState.CALIBRATION_FAILED,
            HunterState.CALIBRATING,
            'retry_calibration'
        )

        # Hunt start
        self._add_transition(
            HunterState.READY,
            HunterState.STARTING_HUNT,
            'start_hunt'
        )

        self._add_transition(
            HunterState.STARTING_HUNT,
            HunterState.HUNTING,
            'hunt_started'
        )

        # Main hunting loop
        self._add_transition(
            HunterState.HUNTING,
            HunterState.RESETTING,
            'perform_reset'
        )

        self._add_transition(
            HunterState.RESETTING,
            HunterState.WAITING_FOR_LOAD,
            'reset_complete'
        )

        self._add_transition(
            HunterState.WAITING_FOR_LOAD,
            HunterState.CHECKING_POKEMON,
            'game_loaded'
        )

        self._add_transition(
            HunterState.CHECKING_POKEMON,
            HunterState.SHINY_FOUND,
            'shiny_detected'
        )

        self._add_transition(
            HunterState.CHECKING_POKEMON,
            HunterState.HUNTING,
            'not_shiny'
        )

        # Pause/Resume
        for state in [HunterState.HUNTING, HunterState.RESETTING,
                     HunterState.WAITING_FOR_LOAD, HunterState.CHECKING_POKEMON]:
            self._add_transition(state, HunterState.HUNT_PAUSED, 'pause')

        self._add_transition(
            HunterState.HUNT_PAUSED,
            HunterState.HUNTING,
            'resume'
        )

        # Stop from any hunting state
        for state in [HunterState.HUNTING, HunterState.RESETTING,
                     HunterState.WAITING_FOR_LOAD, HunterState.CHECKING_POKEMON,
                     HunterState.HUNT_PAUSED, HunterState.SHINY_FOUND]:
            self._add_transition(state, HunterState.HUNT_STOPPED, 'stop')

        # Error handling - can error from any state
        for state in HunterState:
            if state not in [HunterState.ERROR, HunterState.CLEANING_UP, HunterState.TERMINATED]:
                self._add_transition(state, HunterState.ERROR, 'error')

        # Window lost
        for state in [HunterState.HUNTING, HunterState.RESETTING,
                     HunterState.WAITING_FOR_LOAD, HunterState.CHECKING_POKEMON]:
            self._add_transition(state, HunterState.WINDOW_LOST, 'window_closed')

        # Cleanup from terminal states
        for state in [HunterState.SHINY_FOUND, HunterState.HUNT_STOPPED,
                     HunterState.ERROR, HunterState.WINDOW_LOST]:
            self._add_transition(state, HunterState.CLEANING_UP, 'cleanup')

        self._add_transition(
            HunterState.CLEANING_UP,
            HunterState.TERMINATED,
            'cleanup_complete'
        )

    def _add_transition(
        self,
        from_state: HunterState,
        to_state: HunterState,
        event: str,
        condition: Optional[Callable[[], bool]] = None,
        action: Optional[Callable] = None
    ):
        """Add a transition to the state machine"""
        if from_state not in self.transitions:
            self.transitions[from_state] = {}

        self.transitions[from_state][event] = StateTransition(
            from_state=from_state,
            to_state=to_state,
            event=event,
            condition=condition,
            action=action
        )

    def trigger(self, event: str) -> bool:
        """
        Trigger a state transition

        Args:
            event: Event name

        Returns:
            True if transition occurred, False otherwise
        """
        # Check if transition exists for current state and event
        if self.current_state not in self.transitions:
            self.logger.warning(
                f"No transitions defined for state {self.current_state.name}"
            )
            return False

        if event not in self.transitions[self.current_state]:
            self.logger.warning(
                f"No transition for event '{event}' in state {self.current_state.name}"
            )
            return False

        transition = self.transitions[self.current_state][event]

        # Check condition if present
        if transition.condition and not transition.condition():
            self.logger.debug(
                f"Transition condition failed for {self.current_state.name} "
                f"-[{event}]-> {transition.to_state.name}"
            )
            return False

        # Execute transition
        return self._execute_transition(transition)

    def _execute_transition(self, transition: StateTransition) -> bool:
        """Execute a state transition"""
        old_state = self.current_state
        new_state = transition.to_state

        self.logger.info(
            f"State transition: {old_state.name} -[{transition.event}]-> {new_state.name}"
        )

        # Call exit callbacks for old state
        for callback in self.on_exit_callbacks[old_state]:
            try:
                callback(old_state, new_state)
            except Exception as e:
                self.logger.error(f"Error in exit callback: {e}")

        # Execute transition action
        if transition.action:
            try:
                transition.action()
            except Exception as e:
                self.logger.error(f"Error in transition action: {e}")
                return False

        # Update state
        self.previous_state = old_state
        self.current_state = new_state

        # Call enter callbacks for new state
        for callback in self.on_enter_callbacks[new_state]:
            try:
                callback(old_state, new_state)
            except Exception as e:
                self.logger.error(f"Error in enter callback: {e}")

        # Call global transition callbacks
        for callback in self.on_transition_callbacks:
            try:
                callback(old_state, new_state, transition.event)
            except Exception as e:
                self.logger.error(f"Error in transition callback: {e}")

        return True

    def on_enter(self, state: HunterState, callback: Callable):
        """Register callback for entering a state"""
        self.on_enter_callbacks[state].append(callback)

    def on_exit(self, state: HunterState, callback: Callable):
        """Register callback for exiting a state"""
        self.on_exit_callbacks[state].append(callback)

    def on_transition(self, callback: Callable):
        """Register callback for any transition"""
        self.on_transition_callbacks.append(callback)

    def is_state(self, state: HunterState) -> bool:
        """Check if current state matches"""
        return self.current_state == state

    def is_any_of(self, *states: HunterState) -> bool:
        """Check if current state is any of the given states"""
        return self.current_state in states

    def can_trigger(self, event: str) -> bool:
        """Check if event can be triggered in current state"""
        if self.current_state not in self.transitions:
            return False

        if event not in self.transitions[self.current_state]:
            return False

        transition = self.transitions[self.current_state][event]

        if transition.condition:
            return transition.condition()

        return True
```

### 4.2 State Machine Usage Example

```python
# Example: Using state machine in hunter

class StationaryHunter:
    def __init__(self):
        self.state_machine = HunterStateMachine()
        self.setup_state_callbacks()

    def setup_state_callbacks(self):
        """Setup state machine callbacks"""

        # Enter hunting state
        self.state_machine.on_enter(
            HunterState.HUNTING,
            lambda old, new: print("🎯 Started hunting!")
        )

        # Enter resetting state
        self.state_machine.on_enter(
            HunterState.RESETTING,
            lambda old, new: self.perform_reset()
        )

        # Enter checking state
        self.state_machine.on_enter(
            HunterState.CHECKING_POKEMON,
            lambda old, new: self.check_if_shiny()
        )

        # Enter shiny found state
        self.state_machine.on_enter(
            HunterState.SHINY_FOUND,
            lambda old, new: self.on_shiny_found()
        )

        # Global transition logger
        self.state_machine.on_transition(
            lambda old, new, event: logger.debug(
                f"Transition: {old.name} -[{event}]-> {new.name}"
            )
        )

    def run(self):
        """Main hunter loop"""
        # Initialize
        self.state_machine.trigger('initialize')
        self.state_machine.trigger('init_success')

        # Calibrate
        self.state_machine.trigger('calibration_complete')

        # Start hunt
        self.state_machine.trigger('start_hunt')
        self.state_machine.trigger('hunt_started')

        # Main loop
        while not self.state_machine.is_any_of(
            HunterState.SHINY_FOUND,
            HunterState.HUNT_STOPPED,
            HunterState.ERROR
        ):
            if self.state_machine.is_state(HunterState.HUNTING):
                self.state_machine.trigger('perform_reset')

            elif self.state_machine.is_state(HunterState.WAITING_FOR_LOAD):
                if self.is_game_loaded():
                    self.state_machine.trigger('game_loaded')

            elif self.state_machine.is_state(HunterState.CHECKING_POKEMON):
                if self.is_shiny:
                    self.state_machine.trigger('shiny_detected')
                else:
                    self.state_machine.trigger('not_shiny')

        # Cleanup
        self.state_machine.trigger('cleanup')
        self.state_machine.trigger('cleanup_complete')
```

This is part 1 of the detailed guide. Should I continue with the remaining sections (Detection Systems, Plugin System, Complete Code Examples)?

