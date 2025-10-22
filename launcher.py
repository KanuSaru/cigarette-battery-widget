import sys, os, subprocess, psutil
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cigarette Battery Widget")
        self.setFixedSize(320, 160)

        self.setStyleSheet("""
            QWidget { background-color: #222; color: white; font-family: Arial; }
            QPushButton {
                background-color: #444;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #666; }
        """)

        label = QLabel("How do you want to display the widget?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        overlay_btn = QPushButton("Overlay (Always on Top)")
        wallpaper_btn = QPushButton("Wallpaper Mode")

        overlay_btn.clicked.connect(lambda: self.launch("overlay"))
        wallpaper_btn.clicked.connect(lambda: self.launch("wallpaper"))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addWidget(overlay_btn)
        layout.addWidget(wallpaper_btn)
        self.setLayout(layout)

    def is_already_running(self):
        """Check if main.py is already running."""
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'cmdline']):
            try:
                if proc.info['pid'] != current_pid and proc.info['cmdline']:
                    if 'python' in proc.info['cmdline'][0].lower() and 'main.py' in proc.info['cmdline'][-1]:
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def launch(self, mode):
        if self.is_already_running():
            print("Widget is already running.")
            self.close()
            return

        main_path = os.path.join(os.path.dirname(__file__), "main.py")

        if sys.platform == "win32":
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(
                [sys.executable, main_path, f"--mode={mode}"],
                creationflags=DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, close_fds=True
            )
        else:
            subprocess.Popen(
                [sys.executable, main_path, f"--mode={mode}"],
                start_new_session=True,
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, close_fds=True
            )

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec())
