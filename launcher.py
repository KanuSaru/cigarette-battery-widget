import sys, os, subprocess
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cigarette Battery Widget")
        self.setFixedSize(320, 160)
        self.setStyleSheet("""
            QWidget {
                background-color: #222;
                color: white;
                font-family: Arial;
            }
            QPushButton {
                background-color: #444;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)

        label = QLabel("How do you want to display the widget?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        overlay_btn = QPushButton("💬 Overlay (Always on Top)")
        wallpaper_btn = QPushButton("🖼️ Wallpaper Mode")

        overlay_btn.clicked.connect(lambda: self.launch("overlay"))
        wallpaper_btn.clicked.connect(lambda: self.launch("wallpaper"))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addWidget(overlay_btn)
        layout.addWidget(wallpaper_btn)
        self.setLayout(layout)

    def launch(self, mode):
        if getattr(sys, "frozen", False):
          exe_path = os.path.join(os.path.dirname(sys.executable), "main.exe")
          subprocess.Popen([exe_path, f"--mode={mode}"])
        else:
            subprocess.Popen([sys.executable, "main.py", f"--mode={mode}"])
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec())
