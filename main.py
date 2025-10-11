import sys
import os
import psutil
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer


class CigaretteBatteryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cigarette Battery Widget")

        # Frameless, always-on-top, transparent background
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Layout setup
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        self.sprite_label = QLabel(self)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sprite_label)

        self.text_label = QLabel("", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(self.text_label)

        self.setLayout(layout)
        self.asset_path = os.path.join(os.path.dirname(__file__), "assets")

        # Manual test mode
        self.test_mode = True
        self.test_levels = [0, 25, 50, 75, 100]
        self.current_test_index = 0

        # Timer to update battery info
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_battery)
        self.timer.start(5000)

        self.update_battery()

        # For dragging
        self.offset = None

    def update_battery(self):
        """Updates the sprite and label based on battery level or test mode"""
        if self.test_mode:
            percent = self.test_levels[self.current_test_index]
            charging = False
        else:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                charging = battery.power_plugged
            else:
                percent = 100
                charging = False

        sprite_name = self.choose_sprite(percent)
        sprite_path = os.path.join(self.asset_path, sprite_name)

        if os.path.exists(sprite_path):
            pixmap = QPixmap(sprite_path)
            pixmap = pixmap.scaled(
                128, 128,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation
            )
            self.sprite_label.setPixmap(pixmap)

        text = f"{percent}% {'⚡' if charging else ''}"
        self.text_label.setText(text)

    def choose_sprite(self, percent):
        if percent >= 90:
            return "cig_full.png"
        elif percent >= 75:
            return "cig_60.png"
        elif percent >= 50:
            return "cig_40.png"
        elif percent >= 25:
            return "cig_20.png"
        else:
            return "cig_0.png"

    def mousePressEvent(self, event):
        """Handle clicks and dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            if event.pos().y() < self.sprite_label.height():
                # Click on sprite → cycle level
                self.cycle_test_level()
            else:
                # Click on text → drag widget
                self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def cycle_test_level(self):
        """Cycle through test battery levels when clicked"""
        self.current_test_index = (self.current_test_index + 1) % len(self.test_levels)
        self.update_battery()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CigaretteBatteryWidget()
    widget.show()
    sys.exit(app.exec())
