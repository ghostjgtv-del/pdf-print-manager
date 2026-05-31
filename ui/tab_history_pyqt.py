"""
History Tab (PyQt6) - FIXED VERSION with visible content
Author: Eng. Justo Torres
"""

from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QFileDialog, QDialog, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from translations import translator, t
from core.history import HistoryManager


class NoScrollComboBox(QComboBox):
    """ComboBox that ignores mouse wheel events"""
    def wheelEvent(self, event):
        event.ignore()


class PrintDetailsDialog(QDialog):
    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.setWindowTitle("Print Details")
        self.setMinimumSize(500, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("Print Job Details")
        title.setStyleSheet("font-size: 18px; font-weight: 900; color: #1e88e5;")
        layout.addWidget(title)

        details_frame = QFrame()
        details_frame.setObjectName("card")
        details_layout = QVBoxLayout(details_frame)
        details_layout.setContentsMargins(16, 16, 16, 16)
        details_layout.setSpacing(12)

        details = [
            ("📅 Date/Time:", self.entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')),
            ("📄 File Name:", self.entry['filename']),
            ("📁 Path:", self.entry['filepath']),
            ("🖨️ Printer:", self.entry['printer']),
            ("📃 Pages:", str(self.entry['pages']) if self.entry['pages'] > 0 else "Unknown"),
            ("✅ Status:", "Success" if self.entry['status'] == 'Success' else "Error")
        ]

        for label_text, value_text in details:
            row = QHBoxLayout()
            row.setSpacing(10)
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 13px; font-weight: 700; color: rgba(176, 184, 196, 0.95); min-width: 100px;")
            value = QLabel(value_text)
            value.setStyleSheet("font-size: 13px; color: rgba(176, 184, 196, 0.85);")
            value.setWordWrap(True)
            row.addWidget(label)
            row.addWidget(value, 1)
            details_layout.addLayout(row)

        layout.addWidget(details_frame)

        if self.entry.get('error_message'):
            error_frame = QFrame()
            error_frame.setStyleSheet("background: rgba(220, 38, 38, 0.1); border: 1px solid #DC2626; border-radius: 6px; padding: 12px;")
            error_layout = QVBoxLayout(error_frame)
            error_label = QLabel(f"❌ Error message:\n{self.entry['error_message']}")
            error_label.setStyleSheet("color: #DC2626; font-size: 12px;")
            error_label.setWordWrap(True)
            error_layout.addWidget(error_label)
            layout.addWidget(error_frame)

        layout.addStretch()

        btn_close = QPushButton("Close")
        btn_close.setObjectName("primaryButton")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setMinimumHeight(40)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)


class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.history_manager = HistoryManager()
        self.setup_ui()
        self.refresh_history()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()

        title_section = QVBoxLayout()
        title_section.setSpacing(2)

        title = QLabel("📊 " + t("history_title"))
        title.setObjectName("pageTitle")
        title_section.addWidget(title)

        subtitle = QLabel(t("history_subtitle"))
        subtitle.setObjectName("pageSubtitle")
        title_section.addWidget(subtitle)

        header.addLayout(title_section)
        header.addStretch()

        layout.addLayout(header)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        filter_label = QLabel("📊 Filter:")
        filter_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")
        toolbar.addWidget(filter_label)

        self.status_combo = NoScrollComboBox()
        self.status_combo.addItems(["All", "Success", "Error"])
        self.status_combo.setFixedHeight(38)
        self.status_combo.currentTextChanged.connect(lambda: self.refresh_history())
        toolbar.addWidget(self.status_combo)

        self.period_combo = NoScrollComboBox()
        self.period_combo.addItems(["Today", "Last 7 days", "Last 30 days", "All"])
        self.period_combo.setCurrentText("Last 7 days")
        self.period_combo.setFixedHeight(38)
        self.period_combo.currentTextChanged.connect(lambda: self.refresh_history())
        toolbar.addWidget(self.period_combo)

        toolbar.addStretch()

        btn_export = QPushButton("📊  Export CSV")
        btn_export.setObjectName("secondaryButton")
        btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_export.setFixedHeight(38)
        btn_export.clicked.connect(self.export_csv)
        toolbar.addWidget(btn_export)

        btn_clear = QPushButton("🗑️  Clear")
        btn_clear.setObjectName("dangerButton")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setFixedHeight(38)
        btn_clear.clicked.connect(self.clear_history)
        toolbar.addWidget(btn_clear)

        btn_refresh = QPushButton("🔄")
        btn_refresh.setObjectName("primaryButton")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFixedHeight(38)
        btn_refresh.setFixedWidth(38)
        btn_refresh.clicked.connect(self.refresh_history)
        toolbar.addWidget(btn_refresh)

        layout.addLayout(toolbar)

        # Stats card
        stats_card = QFrame()
        stats_card.setObjectName("card")
        stats_card.setFixedHeight(60)
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(16, 12, 16, 12)

        self.stats_label = QLabel("Loading statistics...")
        self.stats_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")
        stats_layout.addWidget(self.stats_label)

        layout.addWidget(stats_card)

        # Table card
        content_card = QFrame()
        content_card.setObjectName("mainCard")
        content_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        content_layout = QVBoxLayout(content_card)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget(0, 5)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setHorizontalHeaderLabels(['Date/Time', 'File Name', 'Printer', 'Pages', 'Status'])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 160)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 100)
        self.table.verticalHeader().setVisible(False)
        self.table.doubleClicked.connect(self.show_details)

        content_layout.addWidget(self.table)

        layout.addWidget(content_card)

        # Footer
        footer = QLabel("Developed by Eng. Justo Torres • ghost.jgtv@gmail.com")
        footer.setStyleSheet("color: #64748B; font-size: 10px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def get_date_range(self):
        period = self.period_combo.currentText()
        if period == "Today":
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), None
        elif period == "Last 7 days":
            return datetime.now() - timedelta(days=7), None
        elif period == "Last 30 days":
            return datetime.now() - timedelta(days=30), None
        else:
            return None, None

    def refresh_history(self):
        self.table.setRowCount(0)
        status = self.status_combo.currentText()
        status_filter = None if status == "All" else status
        date_from, date_to = self.get_date_range()

        try:
            entries = self.history_manager.get_history(limit=1000, status_filter=status_filter, date_from=date_from, date_to=date_to)

            for entry in entries:
                row = self.table.rowCount()
                self.table.insertRow(row)

                timestamp_str = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                self.table.setItem(row, 0, QTableWidgetItem(timestamp_str))
                self.table.setItem(row, 1, QTableWidgetItem(entry['filename']))
                self.table.setItem(row, 2, QTableWidgetItem(entry['printer']))

                pages_str = str(entry['pages']) if entry['pages'] > 0 else "-"
                pages_item = QTableWidgetItem(pages_str)
                pages_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 3, pages_item)

                status_text = "✅ Success" if entry['status'] == 'Success' else "❌ Error"
                status_item = QTableWidgetItem(status_text)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                status_item.setForeground(QColor("#10B981" if entry['status'] == 'Success' else "#DC2626"))
                self.table.setItem(row, 4, status_item)

                self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, entry['id'])

        except Exception as e:
            print(f"Error loading history: {e}")

        self.update_statistics()

    def update_statistics(self):
        try:
            stats = self.history_manager.get_statistics()
            if stats:
                success_rate = 0
                if stats['total_prints'] > 0:
                    success_rate = (stats['successful_prints'] / stats['total_prints']) * 100
                stats_text = f"📊 Total: {stats['total_prints']} prints  |  ✅ Successful: {stats['successful_prints']}  |  ❌ Failed: {stats['failed_prints']}  |  📄 Pages: {stats['total_pages']}  |  📈 Success rate: {success_rate:.1f}%"
                self.stats_label.setText(stats_text)
            else:
                self.stats_label.setText("No history data available")
        except Exception as e:
            print(f"Error updating statistics: {e}")
            self.stats_label.setText("Error loading statistics")

    def show_details(self):
        row = self.table.currentRow()
        if row < 0:
            return
        entry_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        try:
            entries = self.history_manager.get_history(limit=99999)
            entry = next((e for e in entries if e['id'] == entry_id), None)
            if entry:
                dialog = PrintDetailsDialog(entry, self)
                dialog.exec()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load details:\n{str(e)}")

    def export_csv(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save history as CSV",
            f"print_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV files (*.csv);;All files (*.*)"
        )
        if not filepath:
            return
        date_from, date_to = self.get_date_range()
        try:
            success = self.history_manager.export_to_csv(filepath, date_from, date_to)
            if success:
                QMessageBox.information(self, "Export Successful", f"History was exported to:\n{filepath}")
            else:
                QMessageBox.critical(self, "Error", "Could not export history")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed:\n{str(e)}")

    def clear_history(self):
        reply = QMessageBox.question(
            self, "Confirm Clear",
            "What do you want to delete?\n\n• Yes - Delete all history\n• No - Delete only old records (>30 days)\n• Cancel - Don't delete anything",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Cancel:
            return
        try:
            if reply == QMessageBox.StandardButton.Yes:
                if self.history_manager.clear_history():
                    QMessageBox.information(self, "Completed", "All history was deleted")
                    self.refresh_history()
                else:
                    QMessageBox.critical(self, "Error", "Could not delete history")
            else:
                date_before = datetime.now() - timedelta(days=30)
                if self.history_manager.clear_history(date_before):
                    QMessageBox.information(self, "Completed", "Old records were deleted")
                    self.refresh_history()
                else:
                    QMessageBox.critical(self, "Error", "Could not delete history")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Operation failed:\n{str(e)}")

    def animate_in(self):
        pass
