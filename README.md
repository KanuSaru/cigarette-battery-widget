# Cigarette Battery Widget

A small desktop widget that displays your laptop's battery level using pixelated cigarette sprites. The widget can be shown as an overlay on top of windows or fixed to the desktop background.

---

## Features

- Shows real battery percentage and charging status.  
- Smooth fade animations for text and glow effect while charging.  
- Click to simulate battery levels in test mode.  
- Two display modes:  
  - **Overlay:** always visible above all windows.  
  - **Wallpaper mode:** stays behind windows, as part of the desktop.  
- Runs independently: the widget continues running even after closing the terminal or launcher.
- Minimal, pixel-art inspired design.

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
├── main.py
├── launcher.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

1. Make sure you have Python 3.10 or newer installed.  
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

1. After running `launcher.py`.  
2. Choose how you want the widget to appear:
   - **Overlay:** stays on top of all windows.  
   - **Wallpaper mode:** sits behind windows on the desktop.  
3. The widget will start and display your current battery level.
4. Close the launcher and terminal safely — the widget will keep running in the background.
5. You can move it by clicking and dragging.  
6. Click it again to cycle through test battery levels.

### Closing the Widget
To stop the widget, use your system's task manager or process manager to end the `main.py` process.

---

## Requirements

- Python 3.10+  
- PyQt6  
- psutil  

These are listed in `requirements.txt`.

---

## Optional Setup: Auto-start

If you want the widget to start automatically on login:
1. Press `Win + R`, type `shell:startup`, and press Enter.  
2. Copy a shortcut to `launcher.py` into that folder.  

---

## License

This project is open source under the **MIT License**.
