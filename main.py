# main.py
import sys
import os
import psutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QGraphicsOpacityEffect, QGraphicsDropShadowEffect,
    QSystemTrayIcon, QMenu, QAction
)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    QSequentialAnimationGroup, QAbstractAnimation
)

SPRITE_SIZE = 128
TRAY_ICON_SIZE = 64

class CigaretteBatteryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cigarette Battery Widget")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.container = QWidget(self)
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.container.setFixedSize(SPRITE_SIZE, SPRITE_SIZE)

        self.sprite_label = QLabel(self.container)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setGeometry(0, 0, SPRITE_SIZE, SPRITE_SIZE)

        self.text_overlay = QLabel(self.container)
        self.text_overlay.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.text_overlay.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.text_overlay.setGeometry(8, 28, SPRITE_SIZE, 20)
        self.text_overlay.setStyleSheet("color: white;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(1, 1)
        shadow.setColor(Qt.GlobalColor.black)
        self.text_overlay.setGraphicsEffect(shadow)

        # Keep an opacity effect for fade animations
        self.opacity_effect = QGraphicsOpacityEffect()
        self.text_overlay.setGraphicsEffect(self.opacity_effect)

        # Sprite opacity for glow animation
        self.sprite_opacity = QGraphicsOpacityEffect()
        self.sprite_label.setGraphicsEffect(self.sprite_opacity)

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.container)
        self.setLayout(layout)

        self.asset_path = os.path.join(os.path.dirname(__file__), "assets")
        self.sprites = self.load_sprites()

        # Tray (created after sprites loaded so we can use an icon)
        self.tray = None
        self.create_tray()

        # Modes and state
        self.test_mode = False
        self.test_levels = [0, 25, 50, 75, 100]
        self.current_test_index = 0
        self.charging = False

        # Timer to poll battery
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_battery)
        self.timer.start(5000)

        self.update_battery()
        self.offset = None
        self.sprite_animation = None

    def load_sprites(self):
        names = ["cig_0.png", "cig_25.png", "cig_50.png", "cig_75.png", "cig_full.png"]
        sprites = {}
        for name in names:
            path = os.path.join(self.asset_path, name)
            if os.path.exists(path):
                sprites[name] = QPixmap(path).scaled(
                    SPRITE_SIZE, SPRITE_SIZE,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
        return sprites

    def create_tray(self):
        # Choose a tray icon from sprites if available
        icon = None
        fallback_pixmap = None
        for key in ("cig_full.png", "cig_75.png", "cig_50.png", "cig_25.png", "cig_0.png"):
            pm = self.sprites.get(key)
            if pm is not None:
                fallback_pixmap = pm.scaled(TRAY_ICON_SIZE, TRAY_ICON_SIZE,
                                            Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
                break

        if fallback_pixmap is not None:
            icon = QIcon(fallback_pixmap)
        else:
            # QIcon.fromTheme may or may not return something cross-platform; it's fine as fallback
            icon = QIcon.fromTheme("battery") or QIcon()

        tray = QSystemTrayIcon(icon, self)
        menu = QMenu()

        self.action_show_hide = QAction("Hide" if self.isVisible() else "Show", self)
        self.action_show_hide.triggered.connect(self.toggle_visibility)
        menu.addAction(self.action_show_hide)

        self.action_toggle_test = QAction("Enable Test Mode" if not self.test_mode else "Disable Test Mode", self)
        self.action_toggle_test.triggered.connect(self.toggle_test_mode)
        menu.addAction(self.action_toggle_test)

        menu.addSeparator()
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        tray.setContextMenu(menu)
        tray.activated.connect(self._tray_activated)
        tray.setVisible(True)
        self.tray = tray

    def _tray_activated(self, reason):
        # Left click toggles visibility
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_visibility()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
            if self.tray:
                self.action_show_hide.setText("Show")
        else:
            self.show()
            if self.tray:
                self.action_show_hide.setText("Hide")

    def toggle_test_mode(self):
        self.test_mode = not self.test_mode
        if self.tray:
            self.action_toggle_test.setText("Disable Test Mode" if self.test_mode else "Enable Test Mode")
        self.update_battery()

    def quit_app(self):
        # Clean up and exit
        self.timer.stop()
        if self.sprite_animation:
            self.sprite_animation.stop()
        if self.tray:
            self.tray.setVisible(False)
        QApplication.quit()

    def update_battery(self):
        if self.test_mode:
            percent = self.test_levels[self.current_test_index]
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
        pixmap = self.sprites.get(sprite_name)
        if pixmap:
            self.sprite_label.setPixmap(pixmap)

        text = f"{percent}% {'⚡' if self.charging else ''}"
        self.fade_text_change(text)
        self.handle_glow_animation()

    def fade_text_change(self, new_text):
        fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_out.setDuration(300)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)

        fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_in.setDuration(300)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)

        group = QSequentialAnimationGroup()
        group.addAnimation(fade_out)
        # small pause; addPause is available and doesn't require extra import
        group.addPause(100)
        group.addAnimation(fade_in)

        fade_out.finished.connect(lambda: self.text_overlay.setText(new_text))
        group.start()

    def handle_glow_animation(self):
        if self.sprite_animation and self.sprite_animation.state() == QAbstractAnimation.State.Running:
            self.sprite_animation.stop()

        if self.charging:
            self.sprite_animation = QPropertyAnimation(self.sprite_opacity, b"opacity")
            self.sprite_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
            self.sprite_animation.setDuration(1000)
            self.sprite_animation.setStartValue(0.8)
            self.sprite_animation.setEndValue(1.0)
            self.sprite_animation.setLoopCount(-1)
            self.sprite_animation.start()
        else:
            self.sprite_opacity.setOpacity(1.0)

    def choose_sprite(self, percent):
        ranges = [
            (90, "cig_full.png"),
            (75, "cig_75.png"),
            (50, "cig_50.png"),
            (25, "cig_25.png"),
            (0, "cig_0.png"),
        ]
        for threshold, name in ranges:
            if percent >= threshold:
                return name

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # hide to tray rather than quit
            self.hide()
            if self.tray:
                self.action_show_hide.setText("Show")
        elif event.button() == Qt.MouseButton.LeftButton:
            self.cycle_test_level()
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def cycle_test_level(self):
        self.current_test_index = (self.current_test_index + 1) % len(self.test_levels)
        self.update_battery()

    def closeEvent(self, event):
        # hide to tray instead of fully exiting; quit via tray menu
        event.ignore()
        self.hide()
        if self.tray:
            self.action_show_hide.setText("Show")


if __name__ == "__main__":
    mode = "overlay"
    for arg in sys.argv:
        if arg.startswith("--mode="):
            mode = arg.split("=")[1]

    app = QApplication(sys.argv)
    widget = CigaretteBatteryWidget()

    flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
    if mode == "overlay":
        flags |= Qt.WindowType.WindowStaysOnTopHint

    widget.setWindowFlags(flags)
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    widget.show()
    sys.exit(app.exec())
