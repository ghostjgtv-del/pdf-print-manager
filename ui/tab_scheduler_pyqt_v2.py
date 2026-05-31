"""
Scheduler Tab (PyQt6) - Simple visible version
Author: Eng. Justo Torres
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class SchedulerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("⏰")
        icon.setStyleSheet("font-size: 96px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        layout.addSpacing(24)

        title = QLabel("Scheduler")
        title.setStyleSheet("color: #FFFFFF; font-size: 32px; font-weight: 900;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Schedule print jobs")
        subtitle.setStyleSheet("color: #94A3B8; font-size: 16px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        message = QLabel("🚧 Coming Soon\n\nThis feature will allow you to schedule\nPDF print jobs for specific times")
        message.setStyleSheet("color: #94A3B8; font-size: 18px; font-weight: 600; margin-top: 24px;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)

    def animate_in(self):
        pass
