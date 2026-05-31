"""
Settings Tab (PyQt6) - FIXED VERSION with visible content
Author: Eng. Justo Torres
"""

import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QComboBox, QProgressBar,
    QMessageBox, QSlider, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from translations import translator, t
from updater import Updater
from core.printer import PrinterManager


class UpdateThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def run(self):
        try:
            for i in range(0, 101, 10):
                self.progress.emit(i)
                self.msleep(200)
            success, message = Updater.download_and_install_update()
            self.finished.emit(success, message)
        except Exception as e:
            self.finished.emit(False, str(e))


class SettingsPage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.update_thread = None
        self.printer_manager = PrinterManager()

        self.settings_file = Path.home() / '.pdf_print_manager' / 'settings.json'
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        self.settings = self.load_settings()

        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setup_ui()

    def load_settings(self):
        default_settings = {'default_printer': None, 'theme': 'dark', 'wait_time': 3, 'language': 'en'}
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    default_settings.update(saved_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
        return default_settings

    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def setup_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(32)

        # Header
        title = QLabel("⚙️ Settings")
        title.setStyleSheet("color: #FFFFFF; font-size: 24px; font-weight: 900;")
        layout.addWidget(title)

        subtitle = QLabel("Configure your application preferences")
        subtitle.setStyleSheet("color: #94A3B8; font-size: 12px;")
        layout.addWidget(subtitle)

        # Appearance Card
        appearance_card = QFrame()
        appearance_card.setObjectName("card")
        appearance_layout = QVBoxLayout(appearance_card)
        appearance_layout.setContentsMargins(32, 32, 32, 32)
        appearance_layout.setSpacing(20)

        card_title = QLabel("🎨 Appearance")
        card_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        appearance_layout.addWidget(card_title)

        # Language
        lang_row = QHBoxLayout()
        lang_label = QLabel("Language:")
        lang_label.setStyleSheet("color: #94A3B8; font-size: 14px; font-weight: 600;")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Español"])
        self.lang_combo.setCurrentText("English" if translator.language == 'en' else "Español")
        self.lang_combo.currentTextChanged.connect(self.on_language_changed)
        lang_row.addWidget(lang_label)
        lang_row.addWidget(self.lang_combo, 1)
        appearance_layout.addLayout(lang_row)

        # Theme
        theme_row = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("color: #94A3B8; font-size: 14px; font-weight: 600;")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCurrentText("Dark" if self.settings.get('theme', 'dark') == 'dark' else "Light")
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_combo, 1)
        appearance_layout.addLayout(theme_row)

        layout.addWidget(appearance_card)

        # Printer Card
        printer_card = QFrame()
        printer_card.setObjectName("card")
        printer_layout = QVBoxLayout(printer_card)
        printer_layout.setContentsMargins(32, 32, 32, 32)
        printer_layout.setSpacing(20)

        printer_title = QLabel("🖨️ Default Printer")
        printer_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        printer_layout.addWidget(printer_title)

        printer_desc = QLabel("Select the printer to be used by default:")
        printer_desc.setStyleSheet("color: #94A3B8; font-size: 13px;")
        printer_layout.addWidget(printer_desc)

        printers = self.printer_manager.get_printers()
        self.printer_combo = QComboBox()
        self.printer_combo.addItems(printers if printers else ["No printers found"])
        if self.settings.get('default_printer') and self.settings['default_printer'] in printers:
            self.printer_combo.setCurrentText(self.settings['default_printer'])
        printer_layout.addWidget(self.printer_combo)

        layout.addWidget(printer_card)

        # Print Settings Card
        print_card = QFrame()
        print_card.setObjectName("card")
        print_layout = QVBoxLayout(print_card)
        print_layout.setContentsMargins(32, 32, 32, 32)
        print_layout.setSpacing(20)

        print_title = QLabel("🔧 Print Settings")
        print_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        print_layout.addWidget(print_title)

        wait_desc = QLabel("Wait time between prints (seconds):")
        wait_desc.setStyleSheet("color: #94A3B8; font-size: 13px;")
        print_layout.addWidget(wait_desc)

        self.wait_slider = QSlider(Qt.Orientation.Horizontal)
        self.wait_slider.setMinimum(1)
        self.wait_slider.setMaximum(10)
        self.wait_slider.setValue(self.settings.get('wait_time', 3))
        self.wait_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.wait_slider.setTickInterval(1)
        self.wait_slider.valueChanged.connect(self.on_wait_time_changed)
        print_layout.addWidget(self.wait_slider)

        self.wait_label = QLabel(f"{self.wait_slider.value()} seconds")
        self.wait_label.setStyleSheet("color: #94A3B8; font-size: 12px;")
        print_layout.addWidget(self.wait_label)

        layout.addWidget(print_card)

        # License Card
        license_card = QFrame()
        license_card.setObjectName("card")
        license_layout = QVBoxLayout(license_card)
        license_layout.setContentsMargins(32, 32, 32, 32)
        license_layout.setSpacing(20)

        license_title = QLabel("🔑 License")
        license_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        license_layout.addWidget(license_title)

        if self.parent_window and hasattr(self.parent_window, 'license_manager'):
            license_info = self.parent_window.license_manager.get_license_info()
            if license_info and license_info['is_valid']:
                days = license_info['days_remaining']
                color = "#10B981" if days > 7 else "#F59E0B"
                license_text = f"✅ License active\n\nExpires: {license_info['expires_at'].strftime('%Y-%m-%d')}\nDays remaining: {days}"
            else:
                color = "#DC2626"
                license_text = "❌ No active license"
        else:
            color = "#DC2626"
            license_text = "❌ License status unknown"

        license_label = QLabel(license_text)
        license_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: 600; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 6px;")
        license_layout.addWidget(license_label)

        btn_license = QPushButton("🔑  Renew / Activate License")
        btn_license.setObjectName("primaryButton")
        btn_license.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_license.setMinimumHeight(45)
        btn_license.clicked.connect(self.show_license_window)
        license_layout.addWidget(btn_license)

        layout.addWidget(license_card)

        # Updates Card
        update_card = QFrame()
        update_card.setObjectName("card")
        update_layout = QVBoxLayout(update_card)
        update_layout.setContentsMargins(32, 32, 32, 32)
        update_layout.setSpacing(20)

        update_title = QLabel("🔄 Application Updates")
        update_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        update_layout.addWidget(update_title)

        version_label = QLabel(f"Current Version: {getattr(self.parent_window, 'VERSION', '1.0.0')}")
        version_label.setStyleSheet("color: #94A3B8; font-size: 14px;")
        update_layout.addWidget(version_label)

        btn_update = QPushButton("🔍  Check for Updates")
        btn_update.setObjectName("secondaryButton")
        btn_update.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_update.setMinimumHeight(45)
        btn_update.clicked.connect(self.check_for_updates)
        update_layout.addWidget(btn_update)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(30)
        update_layout.addWidget(self.progress_bar)

        layout.addWidget(update_card)

        # Action Buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(16)

        btn_save = QPushButton("💾  Save Settings")
        btn_save.setObjectName("successButton")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setMinimumHeight(50)
        btn_save.clicked.connect(self.save_settings_clicked)
        button_row.addWidget(btn_save)

        btn_reset = QPushButton("↺  Restore Defaults")
        btn_reset.setObjectName("dangerButton")
        btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reset.setMinimumHeight(50)
        btn_reset.clicked.connect(self.reset_settings_clicked)
        button_row.addWidget(btn_reset)

        layout.addLayout(button_row)
        layout.addStretch()

        self.setWidget(container)

    def on_language_changed(self, text):
        lang = 'en' if text == "English" else 'es'
        translator.set_language(lang)
        self.settings['language'] = lang
        if self.parent_window:
            self.parent_window.update_texts()

    def on_theme_changed(self, text):
        is_dark = text == "Dark"
        self.settings['theme'] = 'dark' if is_dark else 'light'
        if self.parent_window:
            self.parent_window.switch_theme(is_dark)

    def on_wait_time_changed(self, value):
        self.wait_label.setText(f"{value} seconds")

    def show_license_window(self):
        if self.parent_window:
            self.parent_window.switch_page(4)

    def check_for_updates(self):
        try:
            has_update, current, latest = Updater.check_for_updates()
            if has_update:
                reply = QMessageBox.question(
                    self, "Update Available",
                    f"A new version is available!\n\nCurrent: {current}\nLatest: {latest}\n\nWould you like to download it now?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.start_update()
            else:
                QMessageBox.information(self, "No Updates", f"You are already running the latest version ({current}).")
        except Exception as e:
            QMessageBox.warning(self, "Update Check Failed", f"Could not check for updates:\n{str(e)}")

    def start_update(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.update_thread = UpdateThread()
        self.update_thread.progress.connect(lambda v: self.progress_bar.setValue(v))
        self.update_thread.finished.connect(self.on_update_finished)
        self.update_thread.start()

    def on_update_finished(self, success, message):
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(self, "Update Complete", "The application has been updated successfully!\nPlease restart the application to use the new version.")
        else:
            QMessageBox.warning(self, "Update Failed", f"Update failed:\n{message}")

    def save_settings_clicked(self):
        self.settings['default_printer'] = self.printer_combo.currentText()
        self.settings['theme'] = 'dark' if self.theme_combo.currentText() == "Dark" else 'light'
        self.settings['wait_time'] = self.wait_slider.value()
        self.settings['language'] = 'en' if self.lang_combo.currentText() == "English" else 'es'

        if self.save_settings():
            QMessageBox.information(self, "Settings Saved", "Settings were saved successfully!")
            if self.settings['default_printer'] != "No printers found":
                self.printer_manager.set_default_printer(self.settings['default_printer'])
        else:
            QMessageBox.critical(self, "Error", "Could not save settings.")

    def reset_settings_clicked(self):
        reply = QMessageBox.question(
            self, "Confirm Reset",
            "Are you sure you want to restore default settings?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.settings = {'default_printer': None, 'theme': 'dark', 'wait_time': 3, 'language': 'en'}
            self.theme_combo.setCurrentText("Dark")
            self.wait_slider.setValue(3)
            self.lang_combo.setCurrentText("English")
            printers = self.printer_manager.get_printers()
            if printers:
                self.printer_combo.setCurrentText(printers[0])
            self.save_settings()
            QMessageBox.information(self, "Settings Reset", "Settings were restored to defaults.")

    def animate_in(self):
        pass
