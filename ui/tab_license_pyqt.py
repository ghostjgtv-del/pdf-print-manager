"""
License Tab (PyQt6) - FIXED VERSION
Author: Eng. Justo Torres
"""

from PyQt6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QLineEdit, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt

from license.license_manager import LicenseManager
from translations import translator, t


class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.license_manager = LicenseManager()
        self.setWindowTitle("Activate License")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Enter License Code")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1e88e5;")
        layout.addWidget(title)

        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        self.license_input.setMinimumHeight(50)
        layout.addWidget(self.license_input)

        pc_id_label = QLabel(f"PC ID: {self.license_manager.pc_id}")
        pc_id_label.setObjectName("cardDescription")
        layout.addWidget(pc_id_label)

        button_layout = QHBoxLayout()
        btn_activate = QPushButton("Activate")
        btn_activate.setObjectName("primaryButton")
        btn_activate.setMinimumHeight(45)
        btn_activate.clicked.connect(self.activate_license)
        button_layout.addWidget(btn_activate)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("secondaryButton")
        btn_cancel.setMinimumHeight(45)
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)

        layout.addLayout(button_layout)

    def activate_license(self):
        license_code = self.license_input.text().strip()
        if not license_code:
            QMessageBox.warning(self, "Error", "Please enter a license code")
            return

        success = self.license_manager.activate_license(license_code)
        if success:
            QMessageBox.information(self, "Success", "License activated successfully!")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Invalid license code or activation failed")


class LicensePage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.license_manager = LicenseManager()
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setup_ui()

    def setup_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(32)

        # Header
        title = QLabel("🔑 " + t("license_title"))
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel(t("license_subtitle"))
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        # License status card
        status_card = QFrame()
        status_card.setObjectName("card")
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(32, 32, 32, 32)
        status_layout.setSpacing(20)

        card_title = QLabel("License Status")
        card_title.setObjectName("cardTitle")
        status_layout.addWidget(card_title)

        # Get license info
        license_info = self.license_manager.get_license_info()

        if license_info and license_info['is_valid']:
            days = license_info['days_remaining']
            color = "#10B981" if days > 7 else "#F59E0B"
            status_text = f"✅ License Active\n\nExpires: {license_info['expires_at'].strftime('%Y-%m-%d')}\nDays Remaining: {days}"
        else:
            color = "#DC2626"
            status_text = "❌ No Active License\n\nPlease activate a license to use this application"

        status_label = QLabel(status_text)
        status_label.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: 600; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 6px;")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(status_label)

        layout.addWidget(status_card)

        # PC Info card
        pc_card = QFrame()
        pc_card.setObjectName("card")
        pc_layout = QVBoxLayout(pc_card)
        pc_layout.setContentsMargins(32, 32, 32, 32)
        pc_layout.setSpacing(20)

        pc_title = QLabel("💻 PC Information")
        pc_title.setObjectName("cardTitle")
        pc_layout.addWidget(pc_title)

        pc_id_label = QLabel(f"PC ID: {self.license_manager.pc_id}")
        pc_id_label.setStyleSheet("color: #94A3B8; font-size: 14px; font-family: monospace;")
        pc_layout.addWidget(pc_id_label)

        pc_desc = QLabel("Use this PC ID when requesting a license")
        pc_desc.setObjectName("cardDescription")
        pc_layout.addWidget(pc_desc)

        layout.addWidget(pc_card)

        # Actions
        btn_activate = QPushButton("🔑  Activate New License")
        btn_activate.setObjectName("primaryButton")
        btn_activate.setMinimumHeight(50)
        btn_activate.clicked.connect(self.show_activation_dialog)
        layout.addWidget(btn_activate)

        btn_refresh = QPushButton("🔄  Refresh Status")
        btn_refresh.setObjectName("secondaryButton")
        btn_refresh.setMinimumHeight(50)
        btn_refresh.clicked.connect(self.refresh_status)
        layout.addWidget(btn_refresh)

        # Contact
        contact_card = QFrame()
        contact_card.setObjectName("card")
        contact_layout = QVBoxLayout(contact_card)
        contact_layout.setContentsMargins(32, 32, 32, 32)

        contact_title = QLabel("📧 Need a License?")
        contact_title.setObjectName("cardTitle")
        contact_layout.addWidget(contact_title)

        contact_text = QLabel("Contact:\nEng. Justo Torres\nghost.jgtv@gmail.com")
        contact_text.setObjectName("cardLabel")
        contact_layout.addWidget(contact_text)

        layout.addWidget(contact_card)

        layout.addStretch()

        self.setWidget(container)

    def show_activation_dialog(self):
        dialog = LicenseDialog(self)
        if dialog.exec():
            self.refresh_status()

    def refresh_status(self):
        # Reload the page
        container = self.widget()
        if container:
            container.deleteLater()
        self.setup_ui()

    def animate_in(self):
        pass

    def refresh_for_theme(self):
        """Rebuild UI when theme changes"""
        self.refresh_status()

    def update_texts(self):
        """Rebuild UI when language changes"""
        self.refresh_status()


def show_license_dialog(parent=None):
    """Show license dialog for initial activation"""
    dialog = LicenseDialog(parent)
    return dialog.exec() == QDialog.DialogCode.Accepted
