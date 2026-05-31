"""
PDF Print Manager - PyQt6 Professional Demo
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
Date: May 2026
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QScrollArea, QStackedWidget,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QProgressBar, QFileDialog, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, QPoint,
    pyqtProperty, QSequentialAnimationGroup, QParallelAnimationGroup
)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QPalette, QColor
from pathlib import Path


class AnimatedWidget(QWidget):
    """Widget with fade-in animation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 0.0
        self.setWindowOpacity(0.0)

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    opacity = pyqtProperty(float, get_opacity, set_opacity)

    def fade_in(self, duration=400):
        """Fade in animation"""
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()


class SidebarButton(QPushButton):
    """Custom sidebar navigation button with icon and text"""

    def __init__(self, icon_text, text, parent=None):
        super().__init__(parent)
        self.icon_text = icon_text
        self.button_text = text
        self.is_active = False

        self.setText(f"{icon_text} {text}")
        self.setObjectName("navButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Set fixed height for consistency
        self.setMinimumHeight(56)
        self.setMaximumHeight(56)

    def set_active(self, active):
        """Set button as active/inactive"""
        self.is_active = active
        self.setProperty("active", "true" if active else "false")
        self.style().unpolish(self)
        self.style().polish(self)


class PDFPrintManagerDemo(QMainWindow):
    """Main application window - Professional Demo"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Print Manager - Lagudis Fresh Food Group")
        self.setMinimumSize(1400, 800)

        # Set window icon
        icon_path = Path(__file__).parent / "app-icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Load styles
        self.load_styles()

        # Create UI
        self.setup_ui()

        # Center window
        self.center_window()

        # Start with Queue tab
        self.show_page(0)

        # Fade in main window
        QTimer.singleShot(100, self.fade_in_window)

    def load_styles(self):
        """Load QSS stylesheet"""
        qss_path = Path(__file__).parent / "styles.qss"
        if qss_path.exists():
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

    def setup_ui(self):
        """Setup the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout (horizontal: sidebar + content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Create content area
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentArea")
        main_layout.addWidget(self.content_stack, 1)

        # Create pages
        self.create_pages()

    def create_sidebar(self):
        """Create the sidebar with navigation"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(280)
        sidebar.setMaximumWidth(280)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo section
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 30, 20, 20)
        logo_layout.setSpacing(0)

        # Logo image
        logo_label = QLabel()
        logo_pixmap = QPixmap(str(Path(__file__).parent / "logo-app.png"))
        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(
                180, 60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_layout.addWidget(logo_label)
            logo_layout.addSpacing(15)

        # Title
        title = QLabel("PDF PRINT\nMANAGER")
        title.setObjectName("sidebarTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        logo_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("LAGUDIS FRESH FOOD GROUP")
        subtitle.setObjectName("sidebarSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        logo_layout.addWidget(subtitle)

        layout.addWidget(logo_container)

        # Separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator)

        # Navigation buttons
        self.nav_buttons = []

        nav_items = [
            ("📄", "Cola de Impresión"),
            ("⏰", "Programador"),
            ("📊", "Historial"),
            ("⚙️", "Configuración"),
            ("🔑", "Licencia"),
            ("ℹ️", "Acerca de")
        ]

        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 20, 0, 0)
        nav_layout.setSpacing(0)

        for icon, text in nav_items:
            btn = SidebarButton(icon, text)
            btn.clicked.connect(lambda checked, idx=len(self.nav_buttons): self.show_page(idx))
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()
        layout.addWidget(nav_container, 1)

        # Status section at bottom
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #252b3b;
                border-radius: 12px;
                padding: 15px;
                margin: 16px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        status_layout.setSpacing(8)

        status_title = QLabel("Estado del Servidor")
        status_title.setStyleSheet("color: #b0b8c4; font-size: 12px; font-weight: 600;")
        status_layout.addWidget(status_title)

        status_indicator = QLabel("● Conectado")
        status_indicator.setStyleSheet("color: #10b981; font-size: 13px; font-weight: 600;")
        status_layout.addWidget(status_indicator)

        server_label = QLabel("143.110.130.78:8001")
        server_label.setStyleSheet("color: #6b7280; font-size: 11px;")
        status_layout.addWidget(server_label)

        layout.addWidget(status_frame)

        return sidebar

    def create_pages(self):
        """Create content pages"""
        # Queue Page (Demo completa)
        queue_page = self.create_queue_page()
        self.content_stack.addWidget(queue_page)

        # Other pages (placeholders con fade-in)
        for i in range(5):
            placeholder = self.create_placeholder_page(
                ["Programador de Tareas", "Historial de Impresiones",
                 "Configuración", "Información de Licencia", "Acerca de"][i]
            )
            self.content_stack.addWidget(placeholder)

    def create_queue_page(self):
        """Create the Queue page with animations"""
        page = AnimatedWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        # Header
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        title = QLabel("📄 Cola de Impresión")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)

        subtitle = QLabel("Gestiona tus trabajos de impresión en batch")
        subtitle.setObjectName("pageSubtitle")
        header_layout.addWidget(subtitle)

        layout.addWidget(header_widget)

        # Action bar
        action_bar = self.create_action_bar()
        layout.addWidget(action_bar)

        # Main content: Split view
        content_layout = QHBoxLayout()
        content_layout.setSpacing(24)

        # Left: File list card
        file_card = self.create_file_list_card()
        content_layout.addWidget(file_card, 2)

        # Right: Printer settings card
        printer_card = self.create_printer_card()
        content_layout.addWidget(printer_card, 1)

        layout.addLayout(content_layout)

        return page

    def create_action_bar(self):
        """Create action bar with buttons"""
        action_bar = QFrame()
        action_bar.setObjectName("card")

        layout = QHBoxLayout(action_bar)
        layout.setContentsMargins(20, 16, 20, 16)

        # Add files button
        add_btn = QPushButton("📁 Agregar PDFs")
        add_btn.setObjectName("primaryButton")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.add_files_demo)
        layout.addWidget(add_btn)

        # Remove button
        remove_btn = QPushButton("🗑️ Remover")
        remove_btn.setObjectName("secondaryButton")
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(remove_btn)

        # Clear button
        clear_btn = QPushButton("🧹 Limpiar Todo")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(clear_btn)

        layout.addStretch()

        # Print button
        print_btn = QPushButton("🖨️ IMPRIMIR TODO")
        print_btn.setObjectName("successButton")
        print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        print_btn.setMinimumWidth(200)
        print_btn.clicked.connect(self.start_print_demo)
        layout.addWidget(print_btn)

        return action_bar

    def create_file_list_card(self):
        """Create file list card with table"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Card title
        title = QLabel("Archivos en Cola")
        title.setObjectName("cardTitle")
        layout.addWidget(title)

        subtitle = QLabel("Arrastra archivos aquí o usa el botón 'Agregar PDFs'")
        subtitle.setObjectName("cardSubtitle")
        layout.addWidget(subtitle)

        # Table
        self.file_table = QTableWidget(0, 4)
        self.file_table.setHorizontalHeaderLabels([
            "Nombre del Archivo", "Ruta", "Páginas", "Estado"
        ])
        self.file_table.horizontalHeader().setStretchLastSection(True)
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.file_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.file_table.setAlternatingRowColors(True)
        self.file_table.verticalHeader().setVisible(False)
        self.file_table.setMinimumHeight(300)

        # Add demo data
        self.add_demo_files()

        layout.addWidget(self.file_table)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        return card

    def create_printer_card(self):
        """Create printer selection card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("Configuración de Impresora")
        title.setObjectName("cardTitle")
        layout.addWidget(title)

        # Printer selection
        printer_label = QLabel("Impresora:")
        printer_label.setStyleSheet("color: #b0b8c4; font-size: 13px; font-weight: 600;")
        layout.addWidget(printer_label)

        self.printer_combo = QComboBox()
        self.printer_combo.addItems([
            "Microsoft Print to PDF",
            "HP LaserJet Pro",
            "Canon PIXMA",
            "Epson EcoTank"
        ])
        self.printer_combo.setCurrentIndex(0)
        layout.addWidget(self.printer_combo)

        layout.addSpacing(10)

        # Stats
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setSpacing(12)

        stats_data = [
            ("Total de archivos:", "0"),
            ("Páginas totales:", "0"),
            ("Tiempo estimado:", "0 min")
        ]

        for label_text, value_text in stats_data:
            stat_row = QWidget()
            stat_layout = QHBoxLayout(stat_row)
            stat_layout.setContentsMargins(0, 0, 0, 0)

            label = QLabel(label_text)
            label.setStyleSheet("color: #b0b8c4; font-size: 13px;")
            stat_layout.addWidget(label)

            stat_layout.addStretch()

            value = QLabel(value_text)
            value.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 600;")
            stat_layout.addWidget(value)

            stats_layout.addWidget(stat_row)

        layout.addWidget(stats_widget)

        layout.addStretch()

        # Info box
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 136, 229, 0.1);
                border: 1px solid #1e88e5;
                border-radius: 10px;
                padding: 16px;
            }
        """)
        info_layout = QVBoxLayout(info_box)
        info_layout.setSpacing(8)

        info_title = QLabel("💡 Consejo")
        info_title.setStyleSheet("color: #64b5f6; font-size: 13px; font-weight: 600;")
        info_layout.addWidget(info_title)

        info_text = QLabel(
            "Puedes programar impresiones para más tarde "
            "usando la pestaña 'Programador'"
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #b0b8c4; font-size: 12px; line-height: 1.4;")
        info_layout.addWidget(info_text)

        layout.addWidget(info_box)

        return card

    def create_placeholder_page(self, title_text):
        """Create placeholder page for other tabs"""
        page = AnimatedWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel(title_text)
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Esta sección estará disponible en la versión completa")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        # Placeholder card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        placeholder_label = QLabel("🚀")
        placeholder_label.setStyleSheet("font-size: 64px;")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(placeholder_label)

        text = QLabel("Función en desarrollo")
        text.setStyleSheet("color: #b0b8c4; font-size: 16px; margin-top: 20px;")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(text)

        layout.addWidget(card, 1)

        return page

    def add_demo_files(self):
        """Add demo files to table"""
        demo_files = [
            ("Reporte_Ventas_2026.pdf", "C:/Documents/Reportes/", "15", "Listo"),
            ("Factura_001234.pdf", "C:/Documents/Facturas/", "3", "Listo"),
            ("Cotización_Cliente_A.pdf", "C:/Documents/Cotizaciones/", "8", "Listo"),
        ]

        for file_data in demo_files:
            self.add_file_to_table(*file_data)

    def add_file_to_table(self, name, path, pages, status):
        """Add a file row to table"""
        row = self.file_table.rowCount()
        self.file_table.insertRow(row)

        self.file_table.setItem(row, 0, QTableWidgetItem(name))
        self.file_table.setItem(row, 1, QTableWidgetItem(path))
        self.file_table.setItem(row, 2, QTableWidgetItem(pages))

        status_item = QTableWidgetItem(f"✓ {status}")
        status_item.setForeground(QColor("#10b981"))
        self.file_table.setItem(row, 3, status_item)

    def show_page(self, index):
        """Show a specific page with animation"""
        # Update button states
        for i, btn in enumerate(self.nav_buttons):
            btn.set_active(i == index)

        # Switch page
        self.content_stack.setCurrentIndex(index)

        # Trigger fade-in animation
        current_widget = self.content_stack.currentWidget()
        if isinstance(current_widget, AnimatedWidget):
            current_widget.fade_in(300)

    def add_files_demo(self):
        """Demo: Add files"""
        # Simulate file dialog
        demo_file = ("Nuevo_Documento.pdf", "C:/Documents/", "5", "Listo")
        self.add_file_to_table(*demo_file)

        # Animate the row
        self.animate_new_row()

    def animate_new_row(self):
        """Animate newly added row"""
        # This would animate the last row
        pass

    def start_print_demo(self):
        """Demo: Start printing"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Animate progress
        self.animate_progress()

    def animate_progress(self):
        """Animate progress bar"""
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.progress_animation.setDuration(3000)
        self.progress_animation.setStartValue(0)
        self.progress_animation.setEndValue(100)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.progress_animation.finished.connect(self.print_complete)
        self.progress_animation.start()

    def print_complete(self):
        """Called when print animation completes"""
        QTimer.singleShot(1000, lambda: self.progress_bar.setVisible(False))

    def center_window(self):
        """Center window on screen"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def fade_in_window(self):
        """Fade in the entire window"""
        self.setWindowOpacity(0.0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(600)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()


def main():
    """Run the demo application"""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("PDF Print Manager")
    app.setOrganizationName("Lagudis Fresh Food Group")

    # Set font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and show window
    window = PDFPrintManagerDemo()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
