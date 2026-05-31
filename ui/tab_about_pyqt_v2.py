"""
About Tab (PyQt6) - FIXED VERSION
Author: Eng. Justo Torres
"""

from PyQt6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from pathlib import Path


class AboutPage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setup_ui()

    def setup_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(32)

        # Header
        title = QLabel("ℹ️ About")
        title.setStyleSheet("color: #FFFFFF; font-size: 24px; font-weight: 900;")
        layout.addWidget(title)

        subtitle = QLabel("Application information and credits")
        subtitle.setStyleSheet("color: #94A3B8; font-size: 12px;")
        layout.addWidget(subtitle)

        # App info card
        info_card = QFrame()
        info_card.setObjectName("card")
        info_card_layout = QVBoxLayout(info_card)
        info_card_layout.setContentsMargins(32, 32, 32, 32)
        info_card_layout.setSpacing(24)

        # Logo
        logo_path = Path(__file__).parent.parent / "logo-app.png"
        if logo_path.exists():
            logo_label = QLabel()
            pixmap = QPixmap(str(logo_path))
            scaled_pixmap = pixmap.scaled(
                120, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_card_layout.addWidget(logo_label)

        # App name
        app_name = QLabel("PDF Print Manager")
        app_name.setStyleSheet("font-size: 28px; font-weight: 900; color: #1e88e5;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_card_layout.addWidget(app_name)

        # Version
        version = QLabel("Version 1.0.0")
        version.setStyleSheet("font-size: 16px; font-weight: 600; color: #94A3B8;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_card_layout.addWidget(version)

        # Description
        description = QLabel("Professional batch printing solution for managing PDF print jobs efficiently")
        description.setStyleSheet("font-size: 14px; color: #94A3B8; margin-top: 16px;")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        info_card_layout.addWidget(description)

        layout.addWidget(info_card)

        # Developer info card
        dev_card = QFrame()
        dev_card.setObjectName("card")
        dev_card_layout = QVBoxLayout(dev_card)
        dev_card_layout.setContentsMargins(32, 32, 32, 32)
        dev_card_layout.setSpacing(20)

        dev_title = QLabel("👨‍💻 Developer")
        dev_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        dev_card_layout.addWidget(dev_title)

        # Developer info
        dev_info_layout = QVBoxLayout()
        dev_info_layout.setSpacing(14)

        dev_name = QLabel("👨‍💻  Eng. Justo Torres")
        dev_name.setStyleSheet("font-size: 17px; font-weight: 700; color: #94A3B8; margin-bottom: 4px;")
        dev_info_layout.addWidget(dev_name)

        dev_email = QLabel("📧  ghost.jgtv@gmail.com")
        dev_email.setStyleSheet("font-size: 14px; font-weight: 500; color: #94A3B8;")
        dev_info_layout.addWidget(dev_email)

        dev_phone = QLabel("📱  +1 (555) 123-4567")
        dev_phone.setStyleSheet("font-size: 14px; font-weight: 500; color: #94A3B8;")
        dev_info_layout.addWidget(dev_phone)

        dev_role = QLabel("💼  Full-Stack Developer & Software Engineer")
        dev_role.setStyleSheet("font-size: 13px; font-weight: 500; color: rgba(176, 184, 196, 0.75); font-style: italic;")
        dev_info_layout.addWidget(dev_role)

        dev_card_layout.addLayout(dev_info_layout)

        layout.addWidget(dev_card)

        # Copyright
        copyright_label = QLabel("© 2026 Eng. Justo Torres. All rights reserved.")
        copyright_label.setStyleSheet("color: rgba(107, 114, 128, 0.7); font-size: 11px; margin-top: 24px;")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)

        layout.addStretch()

        self.setWidget(container)

    def animate_in(self):
        pass
