"""
Print Queue Tab (PyQt6)
Author: Eng. Justo Torres
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QFileDialog, QMessageBox,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QColor

from translations import translator, t
from core.printer import PrinterManager


class AnimatedStatCard(QFrame):
    """Animated statistic card"""

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

        header_layout = QHBoxLayout()
        header_layout.setSpacing(14)

        self.icon_label = QLabel(self.icon)
        self.icon_label.setStyleSheet(f"""
            font-size: 40px;
            color: {self.gradient_colors[0]};
        """)

        title_container = QVBoxLayout()
        title_container.setSpacing(4)

        self.title_label = QLabel(self.title_text)
        self.title_label.setStyleSheet("""
            color: #8A99AD;
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

        self.trend_label = QLabel("📈 +0%")
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

    def update_value(self, value):
        """Update the card value"""
        self.value_label.setText(str(value))

    def animate_in(self, delay=0):
        """Animate card entrance"""
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_anim.setDuration(800)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        if delay > 0:
            QTimer.singleShot(delay, fade_anim.start)
        else:
            fade_anim.start()


class QueuePage(QWidget):
    """Print queue management page - Zero Scroll Design"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.print_manager = PrinterManager()
        self.pdf_files = []

        self.setAcceptDrops(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Compact header - No excessive spacing
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        self.page_title = QLabel()
        self.page_title.setObjectName("pageTitle")
        self.page_title.setStyleSheet("font-size: 28px; font-weight: 900; color: #FFFFFF; margin: 0px;")

        self.page_subtitle = QLabel()
        self.page_subtitle.setObjectName("pageSubtitle")
        self.page_subtitle.setStyleSheet("font-size: 13px; color: #94A3B8; margin: 0px;")

        header_text = QVBoxLayout()
        header_text.setSpacing(4)
        header_text.setContentsMargins(0, 0, 0, 0)
        header_text.addWidget(self.page_title)
        header_text.addWidget(self.page_subtitle)

        header_layout.addLayout(header_text)
        header_layout.addStretch()

        # Compact stats in header
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.card_files = AnimatedStatCard("📁", t('queue_total_files'), "0", ("#2563EB", "#1D4ED8"))
        self.card_pages = AnimatedStatCard("📄", t('queue_total_pages'), "0", ("#8B5CF6", "#7C3AED"))
        self.card_time = AnimatedStatCard("⏱️", t('queue_estimated_time'), "0 min", ("#EC4899", "#DB2777"))

        self.card_files.setMaximumHeight(70)
        self.card_pages.setMaximumHeight(70)
        self.card_time.setMaximumHeight(70)

        stats_layout.addWidget(self.card_files)
        stats_layout.addWidget(self.card_pages)
        stats_layout.addWidget(self.card_time)

        header_layout.addLayout(stats_layout)
        layout.addLayout(header_layout)

        # Horizontal toolbar - Buttons + Printer Selector
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(12)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)

        # Action buttons - Compact
        self.btn_add = QPushButton()
        self.btn_add.setObjectName("primaryButton")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.setFixedHeight(40)
        self.btn_add.clicked.connect(self.add_files)

        self.btn_clear = QPushButton()
        self.btn_clear.setObjectName("secondaryButton")
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear.setFixedHeight(40)
        self.btn_clear.clicked.connect(self.clear_queue)

        self.btn_remove = QPushButton()
        self.btn_remove.setObjectName("dangerButton")
        self.btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_remove.setFixedHeight(40)
        self.btn_remove.clicked.connect(self.remove_selected)

        toolbar_layout.addWidget(self.btn_add)
        toolbar_layout.addWidget(self.btn_clear)
        toolbar_layout.addWidget(self.btn_remove)
        toolbar_layout.addSpacing(24)

        # Printer selector inline
        printer_icon = QLabel("🖨️")
        printer_icon.setStyleSheet("font-size: 20px;")

        self.printer_label = QLabel()
        self.printer_label.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")

        self.printer_combo = QComboBox()
        self.printer_combo.setMinimumWidth(200)
        self.printer_combo.setFixedHeight(40)
        self.load_printers()

        toolbar_layout.addWidget(printer_icon)
        toolbar_layout.addWidget(self.printer_label)
        toolbar_layout.addWidget(self.printer_combo)
        toolbar_layout.addStretch()

        # Print All button on far right
        self.btn_print_all = QPushButton()
        self.btn_print_all.setObjectName("successButton")
        self.btn_print_all.setFixedHeight(40)
        self.btn_print_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_print_all.clicked.connect(self.print_all)

        toolbar_layout.addWidget(self.btn_print_all)

        layout.addLayout(toolbar_layout)

        # Table with print buttons
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
        self.printer_combo.setMinimumWidth(280)
        self.load_printers()

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
        self.btn_print_all.clicked.connect(self.print_all)

        content_layout.addWidget(self.btn_print_all)

        layout.addWidget(content_card)

        # Pro tip card
        tip_card = QFrame()
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
        """Update all text labels"""
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
            t('table_filename'), t('table_path'), t('table_pages'),
            t('table_status'), 'Actions'
        ])

    def load_printers(self):
        """Load available printers"""
        printers = self.print_manager.get_printers()
        self.printer_combo.clear()
        self.printer_combo.addItems(printers)

    def add_files(self):
        """Open file dialog to add PDF files"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF Files",
            "",
            "PDF Files (*.pdf)"
        )

        if files:
            for file_path in files:
                self.add_file_to_queue(file_path)

    def add_file_to_queue(self, file_path):
        """Add a file to the queue"""
        if file_path in self.pdf_files:
            return

        self.pdf_files.append(file_path)

        # Get file info
        filename = Path(file_path).name
        directory = str(Path(file_path).parent)
        pages = self.print_manager.get_pdf_page_count(file_path)

        # Add to table
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(filename))
        self.table.setItem(row, 1, QTableWidgetItem(directory))
        self.table.setItem(row, 2, QTableWidgetItem(str(pages)))
        self.table.setItem(row, 3, QTableWidgetItem(t('status_ready')))

        # Add print button
        btn_print = QPushButton("🖨️ Print")
        btn_print.setObjectName("printButton")
        btn_print.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_print.clicked.connect(lambda checked, r=row: self.print_file(r))
        self.table.setCellWidget(row, 4, btn_print)

        self.update_stats()

    def remove_selected(self):
        """Remove selected files from queue"""
        selected_rows = set(item.row() for item in self.table.selectedItems())
        for row in sorted(selected_rows, reverse=True):
            if row < len(self.pdf_files):
                self.pdf_files.pop(row)
            self.table.removeRow(row)

        self.update_stats()

    def clear_queue(self):
        """Clear all files from queue"""
        self.pdf_files.clear()
        self.table.setRowCount(0)
        self.update_stats()

    def print_file(self, row):
        """Print individual file"""
        if row >= len(self.pdf_files):
            return

        file_path = self.pdf_files[row]
        printer = self.printer_combo.currentText()

        # Update status
        self.table.setItem(row, 3, QTableWidgetItem(t('status_printing')))

        # Print
        success = self.print_manager.print_pdf(file_path, printer)

        if success:
            self.table.setItem(row, 3, QTableWidgetItem(t('status_completed')))
        else:
            self.table.setItem(row, 3, QTableWidgetItem(t('status_error')))

    def print_all(self):
        """Print all files in queue"""
        if not self.pdf_files:
            QMessageBox.warning(self, "No Files", "Please add PDF files to the queue first.")
            return

        printer = self.printer_combo.currentText()

        for row, file_path in enumerate(self.pdf_files):
            self.print_file(row)

        QMessageBox.information(self, "Print Complete", "All files have been sent to the printer.")

    def update_stats(self):
        """Update statistics cards"""
        total_files = len(self.pdf_files)
        total_pages = sum(self.print_manager.get_pdf_page_count(f) for f in self.pdf_files)
        est_time = total_pages * 0.5  # 0.5 min per page estimate

        self.card_files.update_value(str(total_files))
        self.card_pages.update_value(str(total_pages))
        self.card_time.update_value(f"{est_time:.1f} min")

    def animate_in(self):
        """Animate page entrance"""
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

    def dragEnterEvent(self, event):
        """Handle drag enter"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle file drop"""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.pdf'):
                self.add_file_to_queue(file_path)
