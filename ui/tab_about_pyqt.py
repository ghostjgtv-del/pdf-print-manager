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

from translations import translator, t


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
        title = QLabel("ℹ️ " + t("about_title"))
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel(t("about_subtitle"))
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        # App info card
        info_card = QFrame()
        info_card.setObjectName("card")
        info_card_layout = QVBoxLayout(info_card)
        info_card_layout.setContentsMargins(32, 32, 32, 32)
        info_card_layout.setSpacing(24)

        # Logo Container with gradient background for contrast
        logo_path = Path(__file__).parent.parent / "logo-app.png"
        if logo_path.exists():
            # Create dedicated frame for logo with gradient
            logo_container = QFrame()
            logo_container.setObjectName("logoContainerAbout")
            logo_container.setMinimumHeight(220)
            logo_container.setMaximumHeight(260)

            logo_container_layout = QVBoxLayout(logo_container)
            logo_container_layout.setContentsMargins(30, 30, 30, 30)
            logo_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Logo label with larger size
            logo_label = QLabel()
            pixmap = QPixmap(str(logo_path))

            # Much larger size for better visibility
            scaled_pixmap = pixmap.scaled(
                220, 220,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            logo_label.setPixmap(scaled_pixmap)
            logo_label.setScaledContents(False)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setMinimumSize(220, 180)
            logo_label.setMaximumSize(240, 200)

            logo_container_layout.addWidget(logo_label)
            info_card_layout.addWidget(logo_container)

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
        dev_title.setObjectName("cardTitle")
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

        dev_phone = QLabel("📱  +1 (725) 292-4402")
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

    def refresh_for_theme(self):
        """Rebuild UI when theme changes"""
        container = self.widget()
        if container:
            container.deleteLater()
        self.setup_ui()

    def update_texts(self):
        """Rebuild UI when language changes"""
        container = self.widget()
        if container:
            container.deleteLater()
        self.setup_ui()
