"""
Print Queue Tab (PyQt6) - FIXED VERSION
Author: Eng. Justo Torres
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QFileDialog, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QColor, QDragEnterEvent, QDropEvent, QIcon

from translations import translator, t
from core.printer import PrinterManager
from core.history import HistoryManager


class NoScrollComboBox(QComboBox):
    """ComboBox that ignores mouse wheel events"""
    def wheelEvent(self, event):
        event.ignore()


class DropZoneWidget(QFrame):
    """Widget específico para Drag & Drop de archivos PDF"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.setAcceptDrops(True)  # SOLO esta zona acepta drops
        self.setObjectName("dropZone")
        self.setFixedHeight(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Solo acepta archivos PDF arrastrados dentro de esta zona"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            # Verificar que al menos un archivo sea PDF
            if any(url.toLocalFile().lower().endswith('.pdf') for url in urls):
                event.acceptProposedAction()
            else:
                event.ignore()  # Cursor de "no permitido"
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Procesa archivos PDF soltados SOLO dentro de esta zona"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]

        if pdf_files and self.parent_widget:
            for pdf_file in pdf_files:
                self.parent_widget.add_file_to_queue(pdf_file)
            event.acceptProposedAction()
        else:
            event.ignore()


class AnimatedStatCard(QFrame):
    """Compact statistic card"""

    def __init__(self, icon, title, value, color, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setFixedHeight(70)
        self.setFixedWidth(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        # Icon and value
        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 24px; color: {color};")

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"font-size: 22px; font-weight: 900; color: {color};")

        top_layout.addWidget(icon_label)
        top_layout.addWidget(self.value_label)
        top_layout.addStretch()

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #8A99AD; font-size: 10px; font-weight: 600;")

        layout.addLayout(top_layout)
        layout.addWidget(title_label)

    def update_value(self, value):
        self.value_label.setText(str(value))


class QueuePage(QWidget):
    """Print queue management page"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.print_manager = PrinterManager()
        self.history_manager = HistoryManager()
        self.pdf_files = []
        # NO activar drag & drop global - solo en la zona específica
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        # Title
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        self.title_label = QLabel(t("queue_title"))
        self.title_label.setObjectName("pageTitle")

        self.subtitle_label = QLabel(t("queue_subtitle"))
        self.subtitle_label.setObjectName("pageSubtitle")

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        # Stats
        self.card_files = AnimatedStatCard("📁", "FILES", "0", "#2563EB")
        self.card_pages = AnimatedStatCard("📄", "PAGES", "0", "#8B5CF6")
        self.card_time = AnimatedStatCard("⏱️", "TIME", "0m", "#EC4899")

        header_layout.addWidget(self.card_files)
        header_layout.addWidget(self.card_pages)
        header_layout.addWidget(self.card_time)

        layout.addLayout(header_layout)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.btn_add = QPushButton(t("queue_add_files"))
        self.btn_add.setObjectName("primaryButton")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.setFixedHeight(38)
        self.btn_add.clicked.connect(self.add_files)
        toolbar.addWidget(self.btn_add)

        self.btn_clear = QPushButton(t("queue_clear_all"))
        self.btn_clear.setObjectName("secondaryButton")
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear.setFixedHeight(38)
        self.btn_clear.clicked.connect(self.clear_queue)
        toolbar.addWidget(self.btn_clear)

        self.btn_remove = QPushButton(t("queue_remove"))
        self.btn_remove.setObjectName("dangerButton")
        self.btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_remove.setFixedHeight(38)
        self.btn_remove.clicked.connect(self.remove_selected)
        toolbar.addWidget(self.btn_remove)

        toolbar.addSpacing(20)

        # Printer selector
        printer_icon = QLabel("🖨️")
        printer_icon.setStyleSheet("font-size: 18px;")
        toolbar.addWidget(printer_icon)

        self.printer_label = QLabel(t("queue_printer"))
        self.printer_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")
        toolbar.addWidget(self.printer_label)

        self.printer_combo = NoScrollComboBox()
        self.printer_combo.setMinimumWidth(180)
        self.printer_combo.setFixedHeight(38)
        self.load_printers()
        toolbar.addWidget(self.printer_combo)

        toolbar.addStretch()

        self.btn_print_all = QPushButton(t("queue_print_all"))
        self.btn_print_all.setObjectName("successButton")
        self.btn_print_all.setFixedHeight(38)
        self.btn_print_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_print_all.clicked.connect(self.print_all)
        toolbar.addWidget(self.btn_print_all)

        layout.addLayout(toolbar)

        # Content card
        content_card = QFrame()
        content_card.setObjectName("mainCard")
        content_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        content_layout = QVBoxLayout(content_card)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(10)

        # Drop zone - Widget específico con drag & drop restringido
        drop_zone = DropZoneWidget(self)  # Usar clase personalizada

        drop_layout = QHBoxLayout(drop_zone)
        drop_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.setSpacing(10)

        drop_icon = QLabel("📎")
        drop_icon.setStyleSheet("font-size: 28px;")
        drop_layout.addWidget(drop_icon)

        self.drop_text = QLabel(t("queue_drag_drop_text"))
        self.drop_text.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")
        drop_layout.addWidget(self.drop_text)

        content_layout.addWidget(drop_zone)

        # Table
        self.table = QTableWidget(0, 5)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setHorizontalHeaderLabels(['Filename', 'Path', 'Pages', 'Status', 'Actions'])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Column sizing
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Filename
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Path
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)     # Pages
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)     # Status
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)     # Actions

        self.table.setColumnWidth(2, 80)   # Pages
        self.table.setColumnWidth(3, 120)  # Status
        self.table.setColumnWidth(4, 100)  # Actions - ancho para texto

        # Center align headers for fixed columns
        for col in [2, 3, 4]:
            item = self.table.horizontalHeaderItem(col)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== ALTURA DE FILAS Y EVENTOS DE CLIC =====
        self.table.verticalHeader().setDefaultSectionSize(38)  # Altura de filas
        self.table.verticalHeader().setVisible(False)  # Ocultar números de fila

        # Conectar eventos de clic y hover en celda para detectar acciones
        self.table.cellClicked.connect(self.detectar_clic_acciones)
        self.table.cellEntered.connect(self.handle_cell_hover)

        content_layout.addWidget(self.table)

        layout.addWidget(content_card)

        # Footer
        footer = QLabel("Developed by Eng. Justo Torres • ghost.jgtv@gmail.com")
        footer.setStyleSheet("color: #64748B; font-size: 10px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def load_printers(self):
        printers = self.print_manager.get_printers()
        self.printer_combo.clear()
        self.printer_combo.addItems(printers if printers else ["No printers"])

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)")
        if files:
            for file_path in files:
                self.add_file_to_queue(file_path)

    def add_file_to_queue(self, file_path):
        if file_path in self.pdf_files:
            return

        self.pdf_files.append(file_path)
        filename = Path(file_path).name
        directory = str(Path(file_path).parent)
        pages = self.print_manager.get_pdf_page_count(file_path)

        row = self.table.rowCount()
        self.table.insertRow(row)

        # Filename and Path - left aligned
        self.table.setItem(row, 0, QTableWidgetItem(filename))
        self.table.setItem(row, 1, QTableWidgetItem(directory))

        # Pages - center aligned
        pages_item = QTableWidgetItem(str(pages))
        pages_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 2, pages_item)

        # Status - center aligned
        status_item = QTableWidgetItem("Ready")
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 3, status_item)

        # ===== COLUMNA ACTIONS: TEXTO NATIVO COMO LINK INTERACTIVO =====
        # Texto según idioma
        action_text = f"[ {t('btn_print_action')} ]"
        item_print = QTableWidgetItem(action_text)
        item_print.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Forzar color azul y negrita directamente en el item
        item_print.setForeground(QColor("#2563EB"))
        font = item_print.font()
        font.setBold(True)
        font.setPointSize(10)
        item_print.setFont(font)

        # Que no sea editable
        item_print.setFlags(item_print.flags() & ~Qt.ItemFlag.ItemIsEditable)

        # Insertar en la tabla
        self.table.setItem(row, 4, item_print)

        self.update_stats()

    def remove_selected(self):
        selected_rows = set(item.row() for item in self.table.selectedItems())
        for row in sorted(selected_rows, reverse=True):
            if row < len(self.pdf_files):
                self.pdf_files.pop(row)
            self.table.removeRow(row)
        self.update_stats()

    def clear_queue(self):
        self.pdf_files.clear()
        self.table.setRowCount(0)
        self.update_stats()

    def print_file(self, row):
        if row >= len(self.pdf_files):
            return

        file_path = self.pdf_files[row]
        printer = self.printer_combo.currentText()
        filename = Path(file_path).name

        self.table.setItem(row, 3, QTableWidgetItem("Printing..."))
        success = self.print_manager.print_pdf(file_path, printer)
        pages = self.print_manager.get_pdf_page_count(file_path)

        if success:
            self.table.setItem(row, 3, QTableWidgetItem("✅ Completed"))
            self.history_manager.add_entry(filename, file_path, printer, pages, "Success")
        else:
            self.table.setItem(row, 3, QTableWidgetItem("❌ Error"))
            self.history_manager.add_entry(filename, file_path, printer, pages, "Error", "Print job failed")

    def print_all(self):
        if not self.pdf_files:
            QMessageBox.warning(self, "No Files", "Please add PDF files to the queue first.")
            return

        for row in range(len(self.pdf_files)):
            self.print_file(row)

        QMessageBox.information(self, "Print Complete", "All files have been sent to the printer.")

    def update_stats(self):
        total_files = len(self.pdf_files)
        total_pages = sum(self.print_manager.get_pdf_page_count(f) for f in self.pdf_files)
        est_time = int(total_pages * 0.5)

        self.card_files.update_value(str(total_files))
        self.card_pages.update_value(str(total_pages))
        self.card_time.update_value(f"{est_time}m")

    def detectar_clic_acciones(self, row, col):
        """Detecta clics en la columna Actions y ejecuta la impresión"""
        COLUMNA_ACTIONS_INDEX = 4  # Índice de la columna Actions
        if col == COLUMNA_ACTIONS_INDEX:
            # Ejecutar impresión de la fila clickeada
            self.print_file(row)

    def handle_cell_hover(self, row, col):
        """Cambia el color del texto cuando el mouse pasa por encima de la columna Actions"""
        COLUMNA_ACTIONS_INDEX = 4
        if col == COLUMNA_ACTIONS_INDEX:
            item = self.table.item(row, col)
            if item:
                # Color hover más oscuro
                item.setForeground(QColor("#1D4ED8"))
                self.table.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            # Restaurar colores normales en todas las celdas de Actions
            for r in range(self.table.rowCount()):
                action_item = self.table.item(r, COLUMNA_ACTIONS_INDEX)
                if action_item:
                    action_item.setForeground(QColor("#2563EB"))
            self.table.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    # Drag & drop ahora está manejado por DropZoneWidget - no se necesita aquí

    def animate_in(self):
        pass

    def refresh_for_theme(self):
        """Refresh UI when theme changes - Queue is a QWidget, colors are set in QSS"""
        # For QWidget pages, we don't need to rebuild - just let QSS handle it
        pass

    def update_texts(self):
        """Update all text labels when language changes"""
        self.title_label.setText(t("queue_title"))
        self.subtitle_label.setText(t("queue_subtitle"))
        self.btn_add.setText(t("queue_add_files"))
        self.btn_clear.setText(t("queue_clear_all"))
        self.btn_remove.setText(t("queue_remove"))
        self.btn_print_all.setText(t("queue_print_all"))
        self.printer_label.setText(t("queue_printer"))
        self.drop_text.setText(t("queue_drag_drop_text"))
        # Update table headers if needed
        if hasattr(self, 'table'):
            self.table.setHorizontalHeaderLabels([
                t("table_filename"),
                t("table_path"),
                t("table_pages"),
                t("table_status"),
                'Actions'
            ])
