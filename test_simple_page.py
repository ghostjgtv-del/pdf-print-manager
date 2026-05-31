"""
Test simple para verificar que las páginas se muestran
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import Qt

class SimplePage(QWidget):
    def __init__(self, title, color):
        super().__init__()
        layout = QVBoxLayout(self)

        label = QLabel(title)
        label.setStyleSheet(f"font-size: 32px; color: {color}; font-weight: bold;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Pages")
        self.setMinimumSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        # Buttons
        btn_layout = QHBoxLayout()
        btn1 = QPushButton("Page 1")
        btn2 = QPushButton("Page 2")
        btn3 = QPushButton("Page 3")

        btn1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn2.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn3.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        btn_layout.addWidget(btn1)
        btn_layout.addWidget(btn2)
        btn_layout.addWidget(btn3)

        main_layout.addLayout(btn_layout)

        # Stack
        self.stack = QStackedWidget()
        self.stack.addWidget(SimplePage("PAGE 1 - RED", "red"))
        self.stack.addWidget(SimplePage("PAGE 2 - GREEN", "green"))
        self.stack.addWidget(SimplePage("PAGE 3 - BLUE", "blue"))

        main_layout.addWidget(self.stack)

        self.stack.setCurrentIndex(0)

app = QApplication(sys.argv)
window = TestWindow()
window.show()
sys.exit(app.exec())
