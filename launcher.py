"""
Launcher for Cigarette Battery Widget

This module provides a GUI launcher that allows users to choose between
two display modes for the battery widget: overlay or wallpaper mode.
The launched widget process is fully detached from the terminal, ensuring
it continues running even after the launcher or terminal is closed.
"""

import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class Launcher(QWidget):
    """
    Main launcher window for the Cigarette Battery Widget.
    
    Provides a simple GUI with two buttons to launch the widget in either
    overlay mode (always on top) or wallpaper mode (behind other windows).
    """
    
    def __init__(self):
        """
        Initialize the launcher window with styled buttons and layout.
        """
        
        super().__init__()
        self.setWindowTitle("Cigarette Battery Widget")
        self.setFixedSize(320, 160)
        
        # Apply dark theme styling
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
        
        # Create UI elements
        label = QLabel("How do you want to display the widget?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        overlay_btn = QPushButton("Overlay (Always on Top)")
        wallpaper_btn = QPushButton("Wallpaper Mode")
        
        # Connect buttons to launch method
        overlay_btn.clicked.connect(lambda: self.launch("overlay"))
        wallpaper_btn.clicked.connect(lambda: self.launch("wallpaper"))
        
        # Setup layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addWidget(overlay_btn)
        layout.addWidget(wallpaper_btn)
        self.setLayout(layout)
    
    def launch(self, mode):
        """
        Launch the battery widget in the specified mode as a detached process.
        
        The widget process is completely decoupled from the terminal and launcher,
        allowing it to persist independently even after this launcher closes.
        
        Args:
            mode (str): Display mode for the widget. Either "overlay" or "wallpaper".
        
        Platform-specific behavior:
            - Windows: Uses DETACHED_PROCESS flag to create a process without
              a console window and CREATE_NEW_PROCESS_GROUP to separate it from
              the parent process group.
            - Linux/Mac: Uses start_new_session=True to create a new session,
              effectively orphaning the process from the terminal.
        
        Note:
            All standard streams (stdin, stdout, stderr) are redirected to DEVNULL
            to ensure complete independence from the parent process.
        """
        if sys.platform == "win32":
            # Windows: Use CREATE_NEW_PROCESS_GROUP and DETACHED_PROCESS
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(
                [sys.executable, "main.py", f"--mode={mode}"],
                creationflags=DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
        else:
            # Linux/Mac: Use start_new_session to create a new process group
            subprocess.Popen(
                [sys.executable, "main.py", f"--mode={mode}"],
                start_new_session=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
        
        # Close the launcher after starting the widget
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec())