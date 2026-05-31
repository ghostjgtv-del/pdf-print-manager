"""
Test de QueuePage simplificado
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow
)
from PyQt6.QtCore import Qt

class SimpleQueuePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Title
        title = QLabel("PRINT QUEUE PAGE")
        title.setStyleSheet("font-size: 32px; color: white; font-weight: bold;")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("This is the queue page content")
        subtitle.setStyleSheet("font-size: 16px; color: #94A3B8;")
        layout.addWidget(subtitle)

        # More content
        content = QLabel("If you see this, the page is rendering correctly!")
        content.setStyleSheet("font-size: 14px; color: #10B981;")
        layout.addWidget(content)

        layout.addStretch()

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Queue Page")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background: #0A0B10;")

        page = SimpleQueuePage()
        self.setCentralWidget(page)

app = QApplication(sys.argv)
window = TestWindow()
window.show()
sys.exit(app.exec())
