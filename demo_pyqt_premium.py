"""
Premium PyQt6 Demo - PDF Print Manager
Professional UI with glassmorphism, animations, and multilanguage support
Author: Eng. Justo Torres
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QStackedWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QScrollArea,
    QGraphicsOpacityEffect, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    QSequentialAnimationGroup, QTimer, QPoint, QSize
)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from pathlib import Path

# Import translation system
from translations import translator, t


class LanguageSwitcher(QWidget):
    """Language switcher with flag buttons"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # EN button
        self.btn_en = QPushButton("EN")
        self.btn_en.setObjectName("langButton")
        self.btn_en.setFixedSize(50, 32)
        self.btn_en.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_en.clicked.connect(lambda: self.change_language('en'))

        # ES button
        self.btn_es = QPushButton("ES")
        self.btn_es.setObjectName("langButton")
        self.btn_es.setFixedSize(50, 32)
        self.btn_es.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_es.clicked.connect(lambda: self.change_language('es'))

        layout.addWidget(self.btn_en)
        layout.addWidget(self.btn_es)

        # Set initial active state
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
    """Custom navigation button with icon and text"""

    def __init__(self, text, icon_text, parent=None):
        super().__init__(parent)
        self.icon_text = icon_text
        self.setText(f"  {icon_text}  {text}")
        self.setObjectName("navButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("active", False)

    def set_active(self, active):
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)


class Sidebar(QFrame):
    """Premium sidebar with glassmorphism effect"""

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

        # Header section
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 30, 20, 20)

        # App title
        self.title = QLabel()
        self.title.setObjectName("sidebarTitle")
        self.title.setWordWrap(True)

        # App subtitle
        self.subtitle = QLabel()
        self.subtitle.setObjectName("sidebarSubtitle")
        self.subtitle.setWordWrap(True)

        # Separator line
        separator = QFrame()
        separator.setObjectName("separator")

        header_layout.addWidget(self.title)
        header_layout.addWidget(self.subtitle)
        header_layout.addWidget(separator)

        layout.addWidget(header)

        # Navigation buttons
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 10, 0, 0)
        nav_layout.setSpacing(4)

        # Create navigation buttons
        self.btn_queue = NavigationButton("", "📋")
        self.btn_scheduler = NavigationButton("", "⏰")
        self.btn_history = NavigationButton("", "📊")
        self.btn_settings = NavigationButton("", "⚙️")
        self.btn_license = NavigationButton("", "🔑")
        self.btn_about = NavigationButton("", "ℹ️")

        self.buttons = [
            self.btn_queue,
            self.btn_scheduler,
            self.btn_history,
            self.btn_settings,
            self.btn_license,
            self.btn_about
        ]

        for btn in self.buttons:
            nav_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, b=btn: self.on_nav_clicked(b))

        nav_layout.addStretch()

        layout.addWidget(nav_container)

        # Footer - Language switcher and version
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(20, 10, 20, 20)
        footer_layout.setSpacing(10)

        # Language switcher
        lang_container = QWidget()
        lang_layout = QHBoxLayout(lang_container)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        lang_label = QLabel("🌐")
        lang_label.setStyleSheet("color: #b0b8c4; font-size: 16px;")
        self.lang_switcher = LanguageSwitcher(self.parent_window)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_switcher)
        lang_layout.addStretch()

        # Version info
        self.version_label = QLabel()
        self.version_label.setStyleSheet("""
            color: #6b7280;
            font-size: 11px;
            padding: 8px;
        """)

        footer_layout.addWidget(lang_container)
        footer_layout.addWidget(self.version_label)

        layout.addWidget(footer)

        # Set initial texts
        self.update_texts()

        # Set first button active
        self.btn_queue.set_active(True)

    def update_texts(self):
        """Update all texts with current language"""
        self.title.setText(t('app_name'))
        self.subtitle.setText(t('app_subtitle'))
        self.version_label.setText(f"{t('version')} 1.0.0")

        # Update button texts
        self.btn_queue.setText(f"  📋  {t('nav_queue')}")
        self.btn_scheduler.setText(f"  ⏰  {t('nav_scheduler')}")
        self.btn_history.setText(f"  📊  {t('nav_history')}")
        self.btn_settings.setText(f"  ⚙️  {t('nav_settings')}")
        self.btn_license.setText(f"  🔑  {t('nav_license')}")
        self.btn_about.setText(f"  ℹ️  {t('nav_about')}")

    def on_nav_clicked(self, clicked_button):
        # Update active state
        for btn in self.buttons:
            btn.set_active(btn == clicked_button)

        # Get index and switch page
        index = self.buttons.index(clicked_button)
        if self.parent_window:
            self.parent_window.switch_page(index)


class StatCard(QFrame):
    """Statistic card with animation"""

    def __init__(self, icon, title, value, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.icon = icon
        self.title_text = title
        self.value_text = value
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Icon and title row
        header_layout = QHBoxLayout()

        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("font-size: 32px;")

        title_label = QLabel(self.title_text)
        title_label.setObjectName("cardTitle")

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Value
        value_label = QLabel(self.value_text)
        value_label.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #1e88e5;
            margin-top: 10px;
        """)

        layout.addLayout(header_layout)
        layout.addWidget(value_label)

        # Setup opacity for animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

    def animate_in(self, delay=0):
        """Fade in animation"""
        # Fade animation
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(600)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Start with delay
        if delay > 0:
            QTimer.singleShot(delay, self.fade_anim.start)
        else:
            self.fade_anim.start()


class QueuePage(QScrollArea):
    """Print Queue page with premium design"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setup_ui()

    def setup_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)

        # Page header
        self.page_title = QLabel()
        self.page_title.setObjectName("pageTitle")

        self.page_subtitle = QLabel()
        self.page_subtitle.setObjectName("pageSubtitle")

        layout.addWidget(self.page_title)
        layout.addWidget(self.page_subtitle)

        # Statistics cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.card_files = StatCard("📁", t('queue_total_files'), "0")
        self.card_pages = StatCard("📄", t('queue_total_pages'), "0")
        self.card_time = StatCard("⏱️", t('queue_estimated_time'), "0 min")

        stats_layout.addWidget(self.card_files)
        stats_layout.addWidget(self.card_pages)
        stats_layout.addWidget(self.card_time)

        layout.addLayout(stats_layout)

        # Main content card
        content_card = QFrame()
        content_card.setObjectName("card")
        content_layout = QVBoxLayout(content_card)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(20)

        # Card title
        card_title = QLabel()
        card_title.setObjectName("cardTitle")
        content_layout.addWidget(card_title)
        self.card_title_label = card_title

        # Drag and drop area
        drop_area = QFrame()
        drop_area.setObjectName("card")
        drop_area.setMinimumHeight(150)
        drop_area.setStyleSheet("""
            QFrame#card {
                background-color: #252b3b;
                border: 2px dashed #3d4558;
                border-radius: 16px;
            }
            QFrame#card:hover {
                border: 2px dashed #1e88e5;
                background-color: #2d3548;
            }
        """)

        drop_layout = QVBoxLayout(drop_area)
        drop_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        drop_icon = QLabel("📎")
        drop_icon.setStyleSheet("font-size: 48px;")
        drop_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.drop_text = QLabel()
        self.drop_text.setStyleSheet("""
            color: #b0b8c4;
            font-size: 14px;
            font-weight: 500;
        """)
        self.drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        drop_layout.addWidget(drop_icon)
        drop_layout.addWidget(self.drop_text)

        content_layout.addWidget(drop_area)

        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.btn_add = QPushButton()
        self.btn_add.setObjectName("primaryButton")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_clear = QPushButton()
        self.btn_clear.setObjectName("secondaryButton")
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_remove = QPushButton()
        self.btn_remove.setObjectName("dangerButton")
        self.btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)

        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_clear)
        buttons_layout.addWidget(self.btn_remove)
        buttons_layout.addStretch()

        content_layout.addLayout(buttons_layout)

        # Files table
        self.table = QTableWidget(0, 4)
        self.table.setMinimumHeight(300)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        content_layout.addWidget(self.table)

        # Printer configuration
        printer_layout = QHBoxLayout()

        self.printer_label = QLabel()
        self.printer_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 600;")

        self.printer_combo = QComboBox()
        self.printer_combo.addItems(["Default Printer", "HP LaserJet Pro", "Canon PIXMA"])

        printer_layout.addWidget(self.printer_label)
        printer_layout.addWidget(self.printer_combo)
        printer_layout.addStretch()

        content_layout.addLayout(printer_layout)

        # Print all button
        self.btn_print_all = QPushButton()
        self.btn_print_all.setObjectName("successButton")
        self.btn_print_all.setFixedHeight(56)
        self.btn_print_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_print_all.setStyleSheet("""
            QPushButton#successButton {
                font-size: 16px;
                font-weight: 700;
                letter-spacing: 1px;
            }
        """)

        content_layout.addWidget(self.btn_print_all)

        # Tip card
        tip_card = QFrame()
        tip_card.setObjectName("card")
        tip_card.setStyleSheet("""
            QFrame#card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(30, 136, 229, 0.1),
                    stop:1 rgba(100, 181, 246, 0.05));
                border-left: 4px solid #1e88e5;
            }
        """)

        tip_layout = QHBoxLayout(tip_card)
        tip_layout.setContentsMargins(20, 16, 20, 16)

        tip_icon = QLabel("💡")
        tip_icon.setStyleSheet("font-size: 24px;")

        tip_text_container = QWidget()
        tip_text_layout = QVBoxLayout(tip_text_container)
        tip_text_layout.setContentsMargins(0, 0, 0, 0)
        tip_text_layout.setSpacing(4)

        self.tip_title = QLabel()
        self.tip_title.setStyleSheet("color: #1e88e5; font-weight: 700; font-size: 13px;")

        self.tip_text = QLabel()
        self.tip_text.setStyleSheet("color: #b0b8c4; font-size: 13px;")
        self.tip_text.setWordWrap(True)

        tip_text_layout.addWidget(self.tip_title)
        tip_text_layout.addWidget(self.tip_text)

        tip_layout.addWidget(tip_icon)
        tip_layout.addWidget(tip_text_container, 1)

        content_layout.addWidget(tip_card)

        layout.addWidget(content_card)
        layout.addStretch()

        self.setWidget(container)

        # Setup opacity for animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        container.setGraphicsEffect(self.opacity_effect)

        # Update texts
        self.update_texts()

    def update_texts(self):
        """Update all texts with current language"""
        self.page_title.setText(t('queue_title'))
        self.page_subtitle.setText(t('queue_subtitle'))
        self.card_title_label.setText(t('queue_files_in_queue'))
        self.drop_text.setText(t('queue_drag_drop'))
        self.btn_add.setText(f"➕  {t('queue_add_files')}")
        self.btn_clear.setText(f"🗑️  {t('queue_clear_all')}")
        self.btn_remove.setText(f"✖️  {t('queue_remove')}")
        self.printer_label.setText(t('queue_select_printer'))
        self.btn_print_all.setText(f"🖨️  {t('queue_print_all')}")
        self.tip_title.setText(t('queue_tip'))
        self.tip_text.setText(t('queue_tip_text'))

        # Update table headers
        self.table.setHorizontalHeaderLabels([
            t('table_filename'),
            t('table_path'),
            t('table_pages'),
            t('table_status')
        ])

        # Update stat cards
        self.card_files.title_text = t('queue_total_files')
        self.card_pages.title_text = t('queue_total_pages')
        self.card_time.title_text = t('queue_estimated_time')

    def animate_in(self):
        """Animate page entrance"""
        # Fade in main content
        anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim.setDuration(400)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

        # Animate stat cards with stagger
        self.card_files.animate_in(100)
        self.card_pages.animate_in(200)
        self.card_time.animate_in(300)


class PlaceholderPage(QWidget):
    """Placeholder for other pages"""

    def __init__(self, title, subtitle, icon, parent=None):
        super().__init__(parent)
        self.title_text = title
        self.subtitle_text = subtitle
        self.icon = icon
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("font-size: 80px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title_label = QLabel()
        self.title_label.setObjectName("pageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("pageSubtitle")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Coming soon message
        self.message = QLabel()
        self.message.setStyleSheet("""
            color: #b0b8c4;
            font-size: 16px;
            margin-top: 20px;
        """)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.message)

        # Setup opacity
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.update_texts()

    def update_texts(self):
        """Update texts"""
        self.title_label.setText(self.title_text)
        self.subtitle_label.setText(self.subtitle_text)
        self.message.setText(t('placeholder_coming_soon'))

    def animate_in(self):
        """Animate page entrance"""
        anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim.setDuration(400)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()


class MainWindow(QMainWindow):
    """Premium main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Print Manager")
        self.setMinimumSize(1400, 900)

        # Set window icon if exists
        icon_path = Path(__file__).parent / "app-icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.setup_ui()
        self.load_styles()

        # Initial animation
        QTimer.singleShot(100, self.animate_initial_page)

    def setup_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        # Content area with stacked pages
        content_container = QFrame()
        content_container.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()

        # Create pages
        self.page_queue = QueuePage()
        self.page_scheduler = PlaceholderPage(
            t('scheduler_title'),
            t('scheduler_subtitle'),
            "⏰"
        )
        self.page_history = PlaceholderPage(
            t('history_title'),
            t('history_subtitle'),
            "📊"
        )
        self.page_settings = PlaceholderPage(
            t('settings_title'),
            t('settings_subtitle'),
            "⚙️"
        )
        self.page_license = PlaceholderPage(
            t('license_title'),
            t('license_subtitle'),
            "🔑"
        )
        self.page_about = PlaceholderPage(
            t('about_title'),
            t('about_subtitle'),
            "ℹ️"
        )

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

    def load_styles(self):
        """Load premium QSS styles"""
        qss_path = Path(__file__).parent / "styles_premium.qss"
        if qss_path.exists():
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        else:
            # Fallback to regular styles
            qss_path = Path(__file__).parent / "styles.qss"
            if qss_path.exists():
                with open(qss_path, 'r', encoding='utf-8') as f:
                    self.setStyleSheet(f.read())

    def switch_page(self, index):
        """Switch to page with animation"""
        if index < len(self.pages):
            self.stack.setCurrentIndex(index)
            # Trigger page animation
            current_page = self.pages[index]
            if hasattr(current_page, 'animate_in'):
                current_page.animate_in()

    def animate_initial_page(self):
        """Animate the initial page"""
        self.page_queue.animate_in()

    def update_texts(self):
        """Update all UI texts when language changes"""
        self.sidebar.update_texts()
        self.page_queue.update_texts()

        # Update placeholder pages
        self.page_scheduler.title_text = t('scheduler_title')
        self.page_scheduler.subtitle_text = t('scheduler_subtitle')
        self.page_scheduler.update_texts()

        self.page_history.title_text = t('history_title')
        self.page_history.subtitle_text = t('history_subtitle')
        self.page_history.update_texts()

        self.page_settings.title_text = t('settings_title')
        self.page_settings.subtitle_text = t('settings_subtitle')
        self.page_settings.update_texts()

        self.page_license.title_text = t('license_title')
        self.page_license.subtitle_text = t('license_subtitle')
        self.page_license.update_texts()

        self.page_about.title_text = t('about_title')
        self.page_about.subtitle_text = t('about_subtitle')
        self.page_about.update_texts()


def main():
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("PDF Print Manager")
    app.setOrganizationName("JG Software")
    app.setApplicationVersion("1.0.0")

    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
