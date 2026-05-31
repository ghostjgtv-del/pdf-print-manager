"""
FINAL PREMIUM PyQt6 Demo - PDF Print Manager
Commercial-Grade with Dark/Light Mode & Logo
Author: Eng. Justo Torres
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QStackedWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QScrollArea,
    QGraphicsOpacityEffect, QGraphicsDropShadowEffect, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    QSequentialAnimationGroup, QTimer, QPoint, QSize, QRect, pyqtProperty
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from pathlib import Path

# Import translation system
from translations import translator, t


class AnimatedStatCard(QFrame):
    """Premium animated statistic card with glow effect"""

    def __init__(self, icon, title, value, gradient_colors, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.icon = icon
        self.title_text = title
        self.value_text = value
        self.gradient_colors = gradient_colors
        self.setup_ui()
        self.setup_effects()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header with icon and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(14)

        # Icon
        self.icon_label = QLabel(self.icon)
        self.icon_label.setStyleSheet(f"""
            font-size: 40px;
            color: {self.gradient_colors[0]};
        """)

        # Title container
        title_container = QVBoxLayout()
        title_container.setSpacing(4)

        self.title_label = QLabel(self.title_text)
        self.title_label.setStyleSheet("""
            color: rgba(176, 184, 196, 0.85);
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        """)

        self.value_label = QLabel(self.value_text)
        self.value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 900;
            color: {self.gradient_colors[0]};
            letter-spacing: -1px;
        """)

        title_container.addWidget(self.title_label)
        title_container.addWidget(self.value_label)

        header_layout.addWidget(self.icon_label)
        header_layout.addLayout(title_container)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Trend indicator
        self.trend_label = QLabel("📈 +12%")
        self.trend_label.setStyleSheet("""
            color: #10b981;
            font-size: 11px;
            font-weight: 700;
        """)
        layout.addWidget(self.trend_label)

    def setup_effects(self):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

    def animate_in(self, delay=0):
        """Smooth entrance animation"""
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_anim.setDuration(800)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        anim_group = QParallelAnimationGroup(self)
        anim_group.addAnimation(fade_anim)

        if delay > 0:
            QTimer.singleShot(delay, anim_group.start)
        else:
            anim_group.start()


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
    """Premium language switcher"""

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
    """Premium navigation button"""

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
    """Ultra-premium sidebar with logo"""

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

        # Logo
        logo_path = Path(__file__).parent / "logo-app.png"
        if logo_path.exists():
            logo_label = QLabel()
            pixmap = QPixmap(str(logo_path))
            scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(logo_label)

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

        # Create buttons
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

        # Footer with theme & language switchers
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(28, 16, 28, 28)
        footer_layout.setSpacing(16)

        # Theme + Language row
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
        for btn in self.buttons:
            btn.set_active(btn == clicked_button)
        index = self.buttons.index(clicked_button)
        if self.parent_window:
            self.parent_window.switch_page(index)


class QueuePage(QScrollArea):
    """Premium print queue page with print buttons"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setup_ui()

    def setup_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(32)

        # Page header
        header_layout = QHBoxLayout()

        header_text = QWidget()
        header_text_layout = QVBoxLayout(header_text)
        header_text_layout.setContentsMargins(0, 0, 0, 0)
        header_text_layout.setSpacing(8)

        self.page_title = QLabel()
        self.page_title.setObjectName("pageTitle")

        self.page_subtitle = QLabel()
        self.page_subtitle.setObjectName("pageSubtitle")

        header_text_layout.addWidget(self.page_title)
        header_text_layout.addWidget(self.page_subtitle)

        header_layout.addWidget(header_text)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Statistics cards
        stats_container = QWidget()
        stats_layout = QGridLayout(stats_container)
        stats_layout.setSpacing(24)
        stats_layout.setContentsMargins(0, 0, 0, 0)

        self.card_files = AnimatedStatCard("📁", t('queue_total_files'), "0", ("#2196f3", "#1976d2"))
        self.card_pages = AnimatedStatCard("📄", t('queue_total_pages'), "0", ("#9c27b0", "#7b1fa2"))
        self.card_time = AnimatedStatCard("⏱️", t('queue_estimated_time'), "0 min", ("#e91e63", "#c2185b"))
        self.card_status = AnimatedStatCard("✅", t('status_ready'), "Ready", ("#10b981", "#059669"))

        stats_layout.addWidget(self.card_files, 0, 0)
        stats_layout.addWidget(self.card_pages, 0, 1)
        stats_layout.addWidget(self.card_time, 0, 2)
        stats_layout.addWidget(self.card_status, 0, 3)

        layout.addWidget(stats_container)

        # Main content card
        content_card = QFrame()
        content_card.setObjectName("card")
        content_layout = QVBoxLayout(content_card)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(24)

        # Card header
        card_header = QHBoxLayout()

        self.card_title = QLabel()
        self.card_title.setObjectName("cardTitle")

        card_header.addWidget(self.card_title)
        card_header.addStretch()

        content_layout.addLayout(card_header)

        # Drag drop zone
        drop_zone = QFrame()
        drop_zone.setObjectName("glowCard")
        drop_zone.setMinimumHeight(180)
        drop_zone.setCursor(Qt.CursorShape.PointingHandCursor)

        drop_layout = QVBoxLayout(drop_zone)
        drop_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.setSpacing(16)

        drop_icon = QLabel("📎")
        drop_icon.setStyleSheet("font-size: 56px;")
        drop_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.drop_text = QLabel()
        self.drop_text.setStyleSheet("""
            color: rgba(176, 184, 196, 0.9);
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.3px;
        """)
        self.drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        drop_hint = QLabel("Supported: PDF files")
        drop_hint.setStyleSheet("""
            color: rgba(107, 114, 128, 0.7);
            font-size: 12px;
        """)
        drop_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        drop_layout.addWidget(drop_icon)
        drop_layout.addWidget(self.drop_text)
        drop_layout.addWidget(drop_hint)

        content_layout.addWidget(drop_zone)

        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)

        self.btn_add = QPushButton()
        self.btn_add.setObjectName("primaryButton")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.setMinimumHeight(50)
        self.btn_add.clicked.connect(self.add_sample_files)

        self.btn_clear = QPushButton()
        self.btn_clear.setObjectName("secondaryButton")
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear.setMinimumHeight(50)
        self.btn_clear.clicked.connect(self.clear_table)

        self.btn_remove = QPushButton()
        self.btn_remove.setObjectName("dangerButton")
        self.btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_remove.setMinimumHeight(50)

        buttons_layout.addWidget(self.btn_add, 2)
        buttons_layout.addWidget(self.btn_clear, 1)
        buttons_layout.addWidget(self.btn_remove, 1)

        content_layout.addLayout(buttons_layout)

        # Premium table with 5 columns (including Actions column)
        self.table = QTableWidget(0, 5)
        self.table.setMinimumHeight(350)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 120)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        content_layout.addWidget(self.table)

        # Printer configuration
        printer_card = QFrame()
        printer_card.setObjectName("card")
        printer_card.setStyleSheet("""
            QFrame#card {
                background: rgba(30, 35, 50, 0.5);
                padding: 20px;
            }
        """)

        printer_layout = QHBoxLayout(printer_card)
        printer_layout.setSpacing(16)

        printer_icon = QLabel("🖨️")
        printer_icon.setStyleSheet("font-size: 28px;")

        self.printer_label = QLabel()
        self.printer_label.setStyleSheet("""
            color: #ffffff;
            font-size: 14px;
            font-weight: 700;
        """)

        self.printer_combo = QComboBox()
        self.printer_combo.addItems(["Default Printer", "HP LaserJet Pro", "Canon PIXMA", "Epson EcoTank"])
        self.printer_combo.setMinimumWidth(280)

        printer_layout.addWidget(printer_icon)
        printer_layout.addWidget(self.printer_label)
        printer_layout.addWidget(self.printer_combo, 1)

        content_layout.addWidget(printer_card)

        # Print all button
        self.btn_print_all = QPushButton()
        self.btn_print_all.setObjectName("successButton")
        self.btn_print_all.setMinimumHeight(64)
        self.btn_print_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_print_all.setStyleSheet("""
            QPushButton#successButton {
                font-size: 18px;
                font-weight: 900;
                letter-spacing: 1.5px;
            }
        """)

        content_layout.addWidget(self.btn_print_all)

        layout.addWidget(content_card)

        # Pro tip card
        tip_card = QFrame()
        tip_card.setObjectName("glowCard")
        tip_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(30, 136, 229, 0.08),
                    stop:1 rgba(156, 39, 176, 0.05)
                );
                border-left: 4px solid qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #64b5f6,
                    stop:0.5 #9c27b0,
                    stop:1 #e91e63
                );
                border-radius: 16px;
                padding: 24px;
            }
        """)

        tip_layout = QHBoxLayout(tip_card)
        tip_layout.setSpacing(20)

        tip_icon = QLabel("💡")
        tip_icon.setStyleSheet("font-size: 32px;")

        tip_text_widget = QWidget()
        tip_text_layout = QVBoxLayout(tip_text_widget)
        tip_text_layout.setContentsMargins(0, 0, 0, 0)
        tip_text_layout.setSpacing(6)

        self.tip_title = QLabel()
        self.tip_title.setStyleSheet("""
            color: #64b5f6;
            font-weight: 800;
            font-size: 14px;
            letter-spacing: 0.5px;
        """)

        self.tip_text = QLabel()
        self.tip_text.setStyleSheet("""
            color: rgba(176, 184, 196, 0.9);
            font-size: 13px;
            font-weight: 500;
        """)
        self.tip_text.setWordWrap(True)

        tip_text_layout.addWidget(self.tip_title)
        tip_text_layout.addWidget(self.tip_text)

        tip_layout.addWidget(tip_icon)
        tip_layout.addWidget(tip_text_widget, 1)

        layout.addWidget(tip_card)
        layout.addStretch()

        self.setWidget(container)

        # Animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        container.setGraphicsEffect(self.opacity_effect)

        self.update_texts()

    def update_texts(self):
        self.page_title.setText(t('queue_title'))
        self.page_subtitle.setText(t('queue_subtitle'))
        self.card_title.setText(t('queue_files_in_queue'))
        self.drop_text.setText(t('queue_drag_drop'))
        self.btn_add.setText(f"➕  {t('queue_add_files')}")
        self.btn_clear.setText(f"🗑️  {t('queue_clear_all')}")
        self.btn_remove.setText(f"✖️  {t('queue_remove')}")
        self.printer_label.setText(t('queue_select_printer'))
        self.btn_print_all.setText(f"🖨️  {t('queue_print_all')}")
        self.tip_title.setText(f"💡 {t('queue_tip')}")
        self.tip_text.setText(t('queue_tip_text'))

        self.table.setHorizontalHeaderLabels([
            t('table_filename'), t('table_path'), t('table_pages'), t('table_status'), 'Actions'
        ])

    def add_sample_files(self):
        """Add sample files to table"""
        samples = [
            ("Invoice_2024.pdf", "C:/Documents/Invoices/", "5", t('status_ready')),
            ("Report_Q1.pdf", "C:/Documents/Reports/", "12", t('status_ready')),
            ("Contract_Draft.pdf", "C:/Documents/Legal/", "8", t('status_ready')),
        ]

        for filename, path, pages, status in samples:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(filename))
            self.table.setItem(row, 1, QTableWidgetItem(path))
            self.table.setItem(row, 2, QTableWidgetItem(pages))
            self.table.setItem(row, 3, QTableWidgetItem(status))

            # Add print button
            btn_print = QPushButton("🖨️ Print")
            btn_print.setObjectName("printButton")
            btn_print.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_print.clicked.connect(lambda checked, r=row: self.print_file(r))
            self.table.setCellWidget(row, 4, btn_print)

    def print_file(self, row):
        """Print individual file"""
        filename = self.table.item(row, 0).text()
        print(f"Printing: {filename}")
        # Update status
        self.table.setItem(row, 3, QTableWidgetItem(t('status_printing') + "..."))

    def clear_table(self):
        """Clear all files"""
        self.table.setRowCount(0)

    def animate_in(self):
        anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

        self.card_files.animate_in(0)
        self.card_pages.animate_in(150)
        self.card_time.animate_in(300)
        self.card_status.animate_in(450)


class PlaceholderPage(QWidget):
    """Premium placeholder page"""

    def __init__(self, title, subtitle, icon, parent=None):
        super().__init__(parent)
        self.title_text = title
        self.subtitle_text = subtitle
        self.icon = icon
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("font-size: 96px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel()
        self.title_label.setObjectName("pageTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("pageSubtitle")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.message = QLabel()
        self.message.setStyleSheet("""
            color: rgba(176, 184, 196, 0.8);
            font-size: 18px;
            font-weight: 600;
            margin-top: 24px;
        """)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon_label)
        layout.addSpacing(24)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.message)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.update_texts()

    def update_texts(self):
        self.title_label.setText(self.title_text)
        self.subtitle_label.setText(self.subtitle_text)
        self.message.setText(t('placeholder_coming_soon'))

    def animate_in(self):
        anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()


class MainWindow(QMainWindow):
    """Ultimate premium main window with theme switching"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(t('app_name'))
        self.setMinimumSize(1500, 950)
        self.is_dark_mode = True

        icon_path = Path(__file__).parent / "app-icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.setup_ui()
        self.load_styles()
        QTimer.singleShot(150, self.animate_initial_page)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = PremiumSidebar(self)
        main_layout.addWidget(self.sidebar)

        # Content
        content_container = QFrame()
        content_container.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()

        # Pages
        self.page_queue = QueuePage()
        self.page_scheduler = PlaceholderPage(t('scheduler_title'), t('scheduler_subtitle'), "⏰")
        self.page_history = PlaceholderPage(t('history_title'), t('history_subtitle'), "📊")
        self.page_settings = PlaceholderPage(t('settings_title'), t('settings_subtitle'), "⚙️")
        self.page_license = PlaceholderPage(t('license_title'), t('license_subtitle'), "🔑")
        self.page_about = PlaceholderPage(t('about_title'), t('about_subtitle'), "ℹ️")

        self.pages = [
            self.page_queue, self.page_scheduler, self.page_history,
            self.page_settings, self.page_license, self.page_about
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_container, 1)

    def load_styles(self):
        """Load theme stylesheet"""
        if self.is_dark_mode:
            qss_path = Path(__file__).parent / "styles_ultimate.qss"
        else:
            qss_path = Path(__file__).parent / "styles_ultimate_light.qss"

        if qss_path.exists():
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

    def switch_theme(self, is_dark):
        """Switch between dark and light themes"""
        self.is_dark_mode = is_dark
        self.load_styles()

    def switch_page(self, index):
        if index < len(self.pages):
            self.stack.setCurrentIndex(index)
            current_page = self.pages[index]
            if hasattr(current_page, 'animate_in'):
                current_page.animate_in()

    def animate_initial_page(self):
        self.page_queue.animate_in()

    def update_texts(self):
        self.setWindowTitle(t('app_name'))
        self.sidebar.update_texts()
        self.page_queue.update_texts()

        for i, page in enumerate(self.pages[1:], 1):
            if isinstance(page, PlaceholderPage):
                titles = [
                    (t('scheduler_title'), t('scheduler_subtitle')),
                    (t('history_title'), t('history_subtitle')),
                    (t('settings_title'), t('settings_subtitle')),
                    (t('license_title'), t('license_subtitle')),
                    (t('about_title'), t('about_subtitle'))
                ]
                if i-1 < len(titles):
                    page.title_text = titles[i-1][0]
                    page.subtitle_text = titles[i-1][1]
                    page.update_texts()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Print Manager")
    app.setOrganizationName("JG Software")
    app.setApplicationVersion("1.0.0")

    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
