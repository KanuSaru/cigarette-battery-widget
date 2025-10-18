import sys, os
import psutil
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

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

        # Create a container to stack image + text
        self.container = QWidget(self)
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.container.setFixedSize(128, 128)
        
        # Image
        self.sprite_label = QLabel(self.container)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setGeometry(0, 0, 128, 128)

        # Text overlay
        self.text_overlay = QLabel(self.container)
        self.text_overlay.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.text_overlay.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.text_overlay.setStyleSheet("color: white; text-shadow: 1px 1px 2px black;")
        self.text_overlay.setGeometry(8, 28, 128, 20)
        
        # Opacity effect for fade animation
        self.opacity_effect = QGraphicsOpacityEffect()
        self.text_overlay.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(600)  
        
        # Sprite glow effect
        self.sprite_opacity = QGraphicsOpacityEffect()
        self.sprite_label.setGraphicsEffect(self.sprite_opacity)
        self.sprite_animation = QPropertyAnimation(self.sprite_opacity, b"opacity")
        self.sprite_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.sprite_animation.setDuration(1000)
        self.sprite_animation.setLoopCount(-1)  # Infinite while charging

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.container)
        self.setLayout(layout)

        # Paths 
        self.asset_path = os.path.join(os.path.dirname(__file__), "assets")

        # Mode 
        self.test_mode = False  # Set to True to enable test mode
        self.test_levels = [0, 25, 50, 75, 100]
        self.current_test_index = 0

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_battery)
        self.timer.start(5000)

        self.update_battery()
        self.offset = None

    def update_battery(self):
        # Updates the sprite and overlay text.
        if self.test_mode:
            percent = self.test_levels[self.current_test_index]
            # Simulate charging on high levels
            self.charging = (percent >= 80)
        else:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                self.charging = battery.power_plugged
            else:
                percent = 100
                self.charging = False

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

        text = f"{percent}% {'⚡' if self.charging else ''}"
        self.fade_text_change(text)

        # Handle glow effect for charging
        self.handle_glow_animation()
        
    def fade_text_change(self, new_text):
        # Smooth fade-out, update, fade-in animation for text.
        self.animation.stop()

        # Fade out
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(300)
        self.animation.finished.connect(lambda: self._update_text(new_text))
        self.animation.start()


    def _update_text(self, new_text):
        self.text_overlay.setText(new_text)

        # Disconnect old connections to avoid stacking animations
        try:
            self.animation.finished.disconnect()
        except Exception:
            pass
        
        # Fade back in
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(300)
        self.animation.start()
        
    def handle_glow_animation(self):
        # Start or stop the glowing animation depending on charging state.
        if self.charging:
            if not self.sprite_animation.state():
                self.sprite_animation.stop()
                self.sprite_animation.setStartValue(0.8)
                self.sprite_animation.setEndValue(1.0)
                self.sprite_animation.start()
        else:
            if self.sprite_animation.state():
                self.sprite_animation.stop()
                self.sprite_opacity.setOpacity(1.0)

    def choose_sprite(self, percent):
        if percent >= 90:
            return "cig_full.png"
        elif percent >= 75:
            return "cig_75.png"
        elif percent >= 50:
            return "cig_50.png"
        elif percent >= 25:
            return "cig_25.png"
        else:
            return "cig_0.png"

    def mousePressEvent(self, event):
        # Handle clicks and dragging.
        if event.button() == Qt.MouseButton.LeftButton:
            # Click → cycle test level
            self.cycle_test_level()
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def cycle_test_level(self):
        # Cycle through test battery levels when clicked.
        self.current_test_index = (self.current_test_index + 1) % len(self.test_levels)
        self.update_battery()

if __name__ == "__main__":
    # Detect mode from command-line arguments
    mode = "overlay"
    for arg in sys.argv:
        if arg.startswith("--mode="):
            mode = arg.split("=")[1]

    app = QApplication(sys.argv)
    widget = CigaretteBatteryWidget()

    # Apply the correct window mode
    from PyQt6.QtCore import Qt
    flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
    if mode == "overlay":
        flags |= Qt.WindowType.WindowStaysOnTopHint

    widget.setWindowFlags(flags)
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    widget.show()
    sys.exit(app.exec())