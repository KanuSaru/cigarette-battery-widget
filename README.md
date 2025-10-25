# Cigarette Battery Widget

A small desktop widget that displays your laptop's battery level using pixelated cigarette sprites.
It can run as an overlay on top of windows or be fixed to the desktop wallpaper.
Built with PyQt6, it provides smooth animations, interactive controls, and persistent background behavior.

---

## Features

* Single instance launch: prevents multiple widgets from running at the same time.
* Real battery monitoring: shows your system’s battery percentage and charging status in real time.
* Charging glow animation: the cigarette sprite gently pulses when charging.
* Smooth fade transitions: the text fades in and out when updating the battery level.
* Test mode: click the widget to cycle through fake battery levels (0%, 25%, 50%, 75%, 100%) for testing.
* Two display modes:

  * Overlay mode: always stays above all windows.
  * Wallpaper mode: fixed behind windows, blending with your desktop.
* System tray integration:

  * Show or hide the widget.
  * Toggle test mode.
  * Exit the app.
* Right-click menu on the widget:

  * Show or hide.
  * Enable or disable test mode.
  * Exit directly.
* Movable widget: drag with left-click to reposition anywhere on screen.
* Runs independently: continues running even after you close the terminal or launcher.
* Minimal pixel-art design: uses cigarette-shaped sprites to represent charge levels.

---

## Folder Structure

```
battery_widget/
│
├── assets/
│   ├── cig_0.png
│   ├── cig_25.png
│   ├── cig_50.png
│   ├── cig_75.png
│   └── cig_full.png
│
├── main.py          # Main widget logic and UI
├── launcher.py      # Launches widget once, handles mode selection
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

1. Make sure you have Python 3.10 - 3.13.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the launcher:

   ```bash
   python launcher.py
   ```

---

## Usage

1. Run `launcher.py`.
2. Choose how you want the widget to appear:

   * Overlay: stays on top of all windows.
   * Wallpaper mode: stays behind windows as part of your desktop.
3. The launcher automatically prevents multiple instances from running.
4. The widget displays your battery status and updates every few seconds.
5. You can move it by clicking and dragging.
6. Click it again to test different battery levels.
7. Right-click the widget to open a dropdown menu (Show/Hide, Test Mode, Exit).
8. You can also access these options from the tray icon.

### Closing the Widget

* Right-click the widget or tray icon and select Exit.
* Alternatively, end the process named `main.py` in your system’s task manager.

---

## Requirements

* Python 3.10 - 3.13
* PyQt6
* psutil

These are listed in `requirements.txt`.

---

## Optional Setup: Auto-start

To start the widget automatically on login:

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Copy a shortcut to `launcher.py` into that folder.

---

## License

This project is open source under the MIT License.

---
