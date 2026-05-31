"""
PDF Print Manager - Main Application (PyQt6)
Commercial-Grade Professional Interface
Author: Eng. Justo Torres
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QPixmap

# Import translation system
from translations import translator, t

# Import UI components
from ui.sidebar_pyqt import PremiumSidebar
from ui.tab_queue_pyqt import QueuePage
from ui.tab_scheduler_pyqt import SchedulerPage
from ui.tab_history_pyqt import HistoryPage
from ui.tab_settings_pyqt import SettingsPage
from ui.tab_license_pyqt import LicensePage
from ui.tab_about_pyqt import AboutPage

# Import updater
from updater import Updater

# Import license manager
from license.license_manager import LicenseManager


class PDFPrintManager(QMainWindow):
    """Main application window"""

    VERSION = "1.0.0"

    def __init__(self):
        super().__init__()
        self.is_dark_mode = True
        self.license_manager = LicenseManager()

        # Check license on startup
        if not self.check_license():
            return

        self.setWindowTitle(t('app_name'))
        self.setMinimumSize(1500, 950)

        # Set window icon
        icon_path = Path(__file__).parent / "app_icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.setup_ui()
        self.load_theme()

        # Check for updates on startup
        QTimer.singleShot(2000, self.check_updates)

    def check_license(self):
        """Check if application is licensed"""
        is_valid, message, _ = self.license_manager.load_license()

        if not is_valid:
            # Show license activation window
            from ui.tab_license_pyqt import show_license_dialog
            result = show_license_dialog(self)
            if not result:
                # User cancelled, exit application
                sys.exit(0)
                return False

        return True

    def setup_ui(self):
        """Setup main UI"""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = PremiumSidebar(self)
        main_layout.addWidget(self.sidebar)

        # Content area
        content_container = QFrame()
        content_container.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.setMinimumSize(800, 600)

        # Create all pages
        self.page_queue = QueuePage(self)
        self.page_scheduler = SchedulerPage(self)
        self.page_history = HistoryPage(self)
        self.page_settings = SettingsPage(self)
        self.page_license = LicensePage(self)
        self.page_about = AboutPage(self)

        self.pages = [
            self.page_queue,
            self.page_scheduler,
            self.page_history,
            self.page_settings,
            self.page_license,
            self.page_about
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_container, 1)

        # Show first page by default
        self.stack.setCurrentIndex(0)

    def load_theme(self):
        """Load current theme stylesheet"""
        if self.is_dark_mode:
            qss_path = Path(__file__).parent / "styles_saas_dark_v2.qss"
        else:
            qss_path = Path(__file__).parent / "styles_saas_light_v2.qss"

        if qss_path.exists():
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

    def switch_theme(self, is_dark):
        """Switch between dark and light themes"""
        self.is_dark_mode = is_dark
        self.load_theme()

        # Refresh pages with inline styles
        for page in self.pages:
            if hasattr(page, 'refresh_for_theme'):
                page.refresh_for_theme()

    def switch_page(self, index):
        """Switch to a specific page"""
        if index < len(self.pages):
            self.stack.setCurrentIndex(index)
            current_page = self.pages[index]
            if hasattr(current_page, 'animate_in'):
                current_page.animate_in()

    def update_texts(self):
        """Update all UI texts when language changes"""
        self.setWindowTitle(t('app_name'))
        self.sidebar.update_texts()

        for page in self.pages:
            if hasattr(page, 'update_texts'):
                page.update_texts()

    def check_updates(self):
        """Check for application updates"""
        try:
            has_update, current, latest = Updater.check_for_updates()
            if has_update:
                reply = QMessageBox.question(
                    self,
                    "Update Available",
                    f"A new version is available!\n\n"
                    f"Current: {current}\n"
                    f"Latest: {latest}\n\n"
                    f"Would you like to download it now?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    # Trigger update from settings page
                    self.switch_page(3)  # Switch to settings
                    if hasattr(self.page_settings, 'start_update'):
                        self.page_settings.start_update()
        except Exception as e:
            print(f"Update check failed: {e}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("PDF Print Manager")
    app.setOrganizationName("JG Software")
    app.setApplicationVersion(PDFPrintManager.VERSION)

    # Set default font
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    app.setFont(font)

    # Create and show main window
    window = PDFPrintManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
