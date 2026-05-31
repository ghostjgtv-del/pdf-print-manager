"""
Premium Sidebar Component (PyQt6)
Author: Eng. Justo Torres
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from pathlib import Path

from translations import translator, t


class ThemeSwitcher(QWidget):
    """Theme toggle button"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.is_dark = True
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn_theme = QPushButton("☀️")
        self.btn_theme.setObjectName("themeButton")
        self.btn_theme.setFixedSize(40, 36)
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.setToolTip("Switch to Light Mode")
        self.btn_theme.clicked.connect(self.toggle_theme)

        layout.addWidget(self.btn_theme)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        if self.is_dark:
            self.btn_theme.setText("☀️")
            self.btn_theme.setToolTip("Switch to Light Mode")
        else:
            self.btn_theme.setText("🌙")
            self.btn_theme.setToolTip("Switch to Dark Mode")

        if self.parent_window:
            self.parent_window.switch_theme(self.is_dark)


class LanguageSwitcher(QWidget):
    """Language switcher component"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.btn_en = QPushButton("🇺🇸 EN")
        self.btn_en.setObjectName("langButton")
        self.btn_en.setFixedSize(70, 36)
        self.btn_en.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_en.clicked.connect(lambda: self.change_language('en'))

        self.btn_es = QPushButton("🇪🇸 ES")
        self.btn_es.setObjectName("langButton")
        self.btn_es.setFixedSize(70, 36)
        self.btn_es.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_es.clicked.connect(lambda: self.change_language('es'))

        layout.addWidget(self.btn_en)
        layout.addWidget(self.btn_es)

        self.update_active_language()

    def change_language(self, lang):
        translator.set_language(lang)
        self.update_active_language()
        if self.parent_window:
            self.parent_window.update_texts()

    def update_active_language(self):
        current = translator.language
        self.btn_en.setProperty("active", current == 'en')
        self.btn_es.setProperty("active", current == 'es')
        self.btn_en.style().unpolish(self.btn_en)
        self.btn_en.style().polish(self.btn_en)
        self.btn_es.style().unpolish(self.btn_es)
        self.btn_es.style().polish(self.btn_es)


class NavigationButton(QPushButton):
    """Custom navigation button"""

    def __init__(self, text, icon, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.button_text = text
        self.setText(f"{icon}  {text}")
        self.setObjectName("navButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("active", False)
        self.setMinimumHeight(52)

    def set_active(self, active):
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)

    def update_text(self, text):
        self.button_text = text
        self.setText(f"{self.icon}  {text}")


class PremiumSidebar(QFrame):
    """Premium sidebar with logo and navigation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setObjectName("sidebar")
        self.buttons = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header with logo
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(28, 30, 28, 30)
        header_layout.setSpacing(12)

        # Logo Container with gradient background for contrast
        logo_path = Path(__file__).parent.parent / "logo-app.png"
        if logo_path.exists():
            # Create dedicated frame for logo with gradient
            logo_container = QFrame()
            logo_container.setObjectName("logoContainer")
            logo_container.setMinimumHeight(200)
            logo_container.setMaximumHeight(240)

            logo_container_layout = QVBoxLayout(logo_container)
            logo_container_layout.setContentsMargins(20, 25, 20, 25)
            logo_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Logo label with larger size
            logo_label = QLabel()
            pixmap = QPixmap(str(logo_path))

            # Much larger size for better visibility
            scaled_pixmap = pixmap.scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            logo_label.setPixmap(scaled_pixmap)
            logo_label.setScaledContents(False)  # Keep aspect ratio, smooth scaling
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setMinimumSize(200, 160)
            logo_label.setMaximumSize(220, 180)

            logo_container_layout.addWidget(logo_label)
            header_layout.addWidget(logo_container)

        # App title
        self.title = QLabel()
        self.title.setObjectName("sidebarTitle")
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        self.subtitle = QLabel()
        self.subtitle.setObjectName("sidebarSubtitle")
        self.subtitle.setWordWrap(True)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Separator
        separator = QFrame()
        separator.setObjectName("separator")

        header_layout.addWidget(self.title)
        header_layout.addWidget(self.subtitle)
        header_layout.addWidget(separator)

        layout.addWidget(header)

        # Navigation
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)

        # Navigation buttons
        self.btn_queue = NavigationButton("", "📋")
        self.btn_scheduler = NavigationButton("", "⏰")
        self.btn_history = NavigationButton("", "📊")
        self.btn_settings = NavigationButton("", "⚙️")
        self.btn_license = NavigationButton("", "🔑")
        self.btn_about = NavigationButton("", "ℹ️")

        self.buttons = [
            self.btn_queue, self.btn_scheduler, self.btn_history,
            self.btn_settings, self.btn_license, self.btn_about
        ]

        for btn in self.buttons:
            nav_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, b=btn: self.on_nav_clicked(b))

        nav_layout.addStretch()
        layout.addWidget(nav_container)

        # Footer
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(28, 16, 28, 28)
        footer_layout.setSpacing(16)

        # Theme + Language controls
        controls_container = QWidget()
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(12)

        # Theme switcher
        self.theme_switcher = ThemeSwitcher(self.parent_window)

        # Language switcher
        self.lang_switcher = LanguageSwitcher(self.parent_window)

        controls_layout.addWidget(self.theme_switcher)
        controls_layout.addStretch()
        controls_layout.addWidget(self.lang_switcher)

        # Version
        self.version_label = QLabel()
        self.version_label.setStyleSheet("""
            color: rgba(107, 114, 128, 0.6);
            font-size: 10px;
            font-weight: 600;
            padding: 8px;
            letter-spacing: 0.5px;
        """)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        footer_layout.addWidget(controls_container)
        footer_layout.addWidget(self.version_label)

        layout.addWidget(footer)

        self.update_texts()
        self.btn_queue.set_active(True)

    def update_texts(self):
        """Update all text labels"""
        self.title.setText(t('app_name'))
        self.subtitle.setText(t('app_subtitle'))
        self.version_label.setText(f"{t('version')} 1.0.0")

        self.btn_queue.update_text(t('nav_queue'))
        self.btn_scheduler.update_text(t('nav_scheduler'))
        self.btn_history.update_text(t('nav_history'))
        self.btn_settings.update_text(t('nav_settings'))
        self.btn_license.update_text(t('nav_license'))
        self.btn_about.update_text(t('nav_about'))

    def on_nav_clicked(self, clicked_button):
        """Handle navigation button click"""
        for btn in self.buttons:
            btn.set_active(btn == clicked_button)

        index = self.buttons.index(clicked_button)
        if self.parent_window:
            self.parent_window.switch_page(index)
