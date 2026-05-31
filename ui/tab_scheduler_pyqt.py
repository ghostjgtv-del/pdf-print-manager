"""
Scheduler Tab (PyQt6) - Full Implementation
Author: Eng. Justo Torres
"""

from datetime import datetime, timedelta
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QDateTimeEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QFileDialog, QDialog, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtGui import QColor

from core.scheduler import PrintScheduler
from core.printer import PrinterManager
from translations import translator, t


class NoScrollComboBox(QComboBox):
    """ComboBox that ignores mouse wheel events"""
    def wheelEvent(self, event):
        event.ignore()


class AddScheduledJobDialog(QDialog):
    """Dialog for creating a new scheduled job"""

    def __init__(self, scheduler, printer_manager, parent=None):
        super().__init__(parent)
        self.scheduler = scheduler
        self.printer_manager = printer_manager
        self.selected_files = []

        self.setWindowTitle("Schedule New Print Job")
        self.setModal(True)
        self.setMinimumSize(600, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Schedule New Print Job")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1e88e5;")
        layout.addWidget(title)

        # Job name
        name_label = QLabel("Job Name:")
        name_label.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")
        layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Weekly Reports")
        self.name_input.setMinimumHeight(40)
        layout.addWidget(self.name_input)

        # Files section
        files_label = QLabel("PDF Files:")
        files_label.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")
        layout.addWidget(files_label)

        files_row = QHBoxLayout()

        self.files_count_label = QLabel("No files selected")
        self.files_count_label.setStyleSheet("color: #94A3B8; font-size: 12px;")
        files_row.addWidget(self.files_count_label)

        files_row.addStretch()

        btn_add_files = QPushButton("📁 Select Files")
        btn_add_files.setMinimumHeight(35)
        btn_add_files.clicked.connect(self.select_files)
        files_row.addWidget(btn_add_files)

        layout.addLayout(files_row)

        # Printer selection
        printer_label = QLabel("Printer:")
        printer_label.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")
        layout.addWidget(printer_label)

        self.printer_combo = NoScrollComboBox()
        self.printer_combo.setMinimumHeight(40)
        printers = self.printer_manager.get_printers()
        if printers:
            self.printer_combo.addItems(printers)
        else:
            self.printer_combo.addItem("No printers found")
        layout.addWidget(self.printer_combo)

        # Date and time
        datetime_label = QLabel("Schedule Date & Time:")
        datetime_label.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")
        layout.addWidget(datetime_label)

        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setMinimumHeight(40)
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        # Set minimum to current time
        self.datetime_edit.setMinimumDateTime(QDateTime.currentDateTime())
        # Set default to 1 hour from now
        self.datetime_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        layout.addWidget(self.datetime_edit)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()

        btn_schedule = QPushButton("✅ Schedule Job")
        btn_schedule.setObjectName("successButton")
        btn_schedule.setMinimumHeight(45)
        btn_schedule.clicked.connect(self.schedule_job)
        button_layout.addWidget(btn_schedule)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("secondaryButton")
        btn_cancel.setMinimumHeight(45)
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)

        layout.addLayout(button_layout)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF files",
            "",
            "PDF files (*.pdf)"
        )

        if files:
            self.selected_files = files
            self.files_count_label.setText(f"{len(files)} file(s) selected")
            self.files_count_label.setStyleSheet("color: #10B981; font-size: 12px; font-weight: 600;")

    def schedule_job(self):
        # Validate inputs
        job_name = self.name_input.text().strip()
        if not job_name:
            QMessageBox.warning(self, "Error", "Please enter a job name")
            return

        if not self.selected_files:
            QMessageBox.warning(self, "Error", "Please select at least one PDF file")
            return

        printer = self.printer_combo.currentText()
        if printer == "No printers found":
            QMessageBox.warning(self, "Error", "No printer available")
            return

        # Get scheduled time
        scheduled_dt = self.datetime_edit.dateTime().toPyDateTime()

        # Validate time is in the future
        if scheduled_dt <= datetime.now():
            QMessageBox.warning(self, "Error", "Scheduled time must be in the future")
            return

        # Create the scheduled job
        try:
            job = self.scheduler.add_job(
                name=job_name,
                filepaths=self.selected_files,
                printer=printer,
                scheduled_time=scheduled_dt
            )

            QMessageBox.information(
                self,
                "Job Scheduled",
                f"Job '{job_name}' scheduled for {scheduled_dt.strftime('%Y-%m-%d %H:%M')}"
            )

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to schedule job:\n{str(e)}")


class SchedulerPage(QWidget):
    """Scheduler page for managing scheduled print jobs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.printer_manager = PrinterManager()
        self.scheduler = PrintScheduler(self.printer_manager)

        # Start the scheduler
        self.scheduler.start()

        self.setup_ui()
        self.refresh_jobs()

        # Auto-refresh every 30 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_jobs)
        self.timer.start(30000)  # 30 seconds

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()

        title_section = QVBoxLayout()
        title_section.setSpacing(2)

        self.title_label = QLabel("⏰ " + t("scheduler_title"))
        self.title_label.setObjectName("pageTitle")
        title_section.addWidget(self.title_label)

        self.subtitle_label = QLabel(t("scheduler_subtitle"))
        self.subtitle_label.setObjectName("pageSubtitle")
        title_section.addWidget(self.subtitle_label)

        header.addLayout(title_section)
        header.addStretch()

        layout.addLayout(header)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.btn_new = QPushButton(t("scheduler_schedule_new"))
        self.btn_new.setObjectName("primaryButton")
        self.btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new.setFixedHeight(38)
        self.btn_new.clicked.connect(self.show_add_dialog)
        toolbar.addWidget(self.btn_new)

        self.btn_clear = QPushButton(t("scheduler_clear_completed"))
        self.btn_clear.setObjectName("secondaryButton")
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear.setFixedHeight(38)
        self.btn_clear.clicked.connect(self.clear_completed)
        toolbar.addWidget(self.btn_clear)

        toolbar.addStretch()

        btn_refresh = QPushButton("🔄")
        btn_refresh.setObjectName("primaryButton")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFixedHeight(38)
        btn_refresh.setFixedWidth(38)
        btn_refresh.clicked.connect(self.refresh_jobs)
        toolbar.addWidget(btn_refresh)

        layout.addLayout(toolbar)

        # Stats card
        stats_card = QFrame()
        stats_card.setObjectName("card")
        stats_card.setFixedHeight(60)
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(16, 12, 16, 12)

        self.stats_label = QLabel("Loading...")
        self.stats_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")
        stats_layout.addWidget(self.stats_label)

        layout.addWidget(stats_card)

        # Table card
        content_card = QFrame()
        content_card.setObjectName("mainCard")
        content_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        content_layout = QVBoxLayout(content_card)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget(0, 6)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setHorizontalHeaderLabels([
            t("scheduler_job_name"),
            t("scheduler_scheduled_time"),
            t("scheduler_files"),
            t("scheduler_printer"),
            t("scheduler_status"),
            t("scheduler_actions")
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)
        self.table.verticalHeader().setVisible(False)

        content_layout.addWidget(self.table)

        layout.addWidget(content_card)

        # Footer
        footer = QLabel("Developed by Eng. Justo Torres • ghost.jgtv@gmail.com")
        footer.setStyleSheet("color: #64748B; font-size: 10px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def show_add_dialog(self):
        dialog = AddScheduledJobDialog(self.scheduler, self.printer_manager, self)
        if dialog.exec():
            self.refresh_jobs()

    def refresh_jobs(self):
        self.table.setRowCount(0)

        try:
            jobs = self.scheduler.get_all_jobs()

            # Sort by scheduled time
            jobs.sort(key=lambda j: j.scheduled_time, reverse=True)

            for job in jobs:
                row = self.table.rowCount()
                self.table.insertRow(row)

                # Job name
                self.table.setItem(row, 0, QTableWidgetItem(job.name))

                # Scheduled time
                time_str = job.scheduled_time.strftime('%Y-%m-%d %H:%M')
                self.table.setItem(row, 1, QTableWidgetItem(time_str))

                # File count
                file_count = QTableWidgetItem(str(len(job.filepaths)))
                file_count.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 2, file_count)

                # Printer
                self.table.setItem(row, 3, QTableWidgetItem(job.printer))

                # Status
                status_colors = {
                    'Pending': '#3B82F6',
                    'Completed': '#10B981',
                    'Cancelled': '#6B7280',
                    'Error': '#DC2626',
                    'Executing': '#F59E0B'
                }

                status_icons = {
                    'Pending': '⏳',
                    'Completed': '✅',
                    'Cancelled': '❌',
                    'Error': '⚠️',
                    'Executing': '⚙️'
                }

                status_text = f"{status_icons.get(job.status, '')} {job.status}"
                status_item = QTableWidgetItem(status_text)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                status_item.setForeground(QColor(status_colors.get(job.status, '#94A3B8')))
                self.table.setItem(row, 4, status_item)

                # Actions button
                if job.status == "Pending":
                    btn_cancel = QPushButton("Cancel")
                    btn_cancel.setObjectName("dangerButton")
                    btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn_cancel.clicked.connect(lambda checked, jid=job.job_id: self.cancel_job(jid))
                    self.table.setCellWidget(row, 5, btn_cancel)
                else:
                    label = QLabel("-")
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setStyleSheet("color: #64748B;")
                    self.table.setCellWidget(row, 5, label)

            self.update_stats()

        except Exception as e:
            print(f"Error refreshing jobs: {e}")

    def update_stats(self):
        try:
            jobs = self.scheduler.get_all_jobs()

            pending = len([j for j in jobs if j.status == "Pending"])
            completed = len([j for j in jobs if j.status == "Completed"])
            failed = len([j for j in jobs if j.status == "Error"])

            stats_text = f"📊 Total: {len(jobs)} jobs  |  ⏳ Pending: {pending}  |  ✅ Completed: {completed}  |  ⚠️ Failed: {failed}"
            self.stats_label.setText(stats_text)

        except Exception as e:
            print(f"Error updating stats: {e}")
            self.stats_label.setText("Error loading statistics")

    def cancel_job(self, job_id):
        reply = QMessageBox.question(
            self,
            "Confirm Cancellation",
            "Are you sure you want to cancel this scheduled job?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.scheduler.cancel_job(job_id):
                    QMessageBox.information(self, "Success", "Job cancelled successfully")
                    self.refresh_jobs()
                else:
                    QMessageBox.warning(self, "Error", "Could not cancel job")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to cancel job:\n{str(e)}")

    def clear_completed(self):
        reply = QMessageBox.question(
            self,
            "Confirm Clear",
            "Remove all completed and cancelled jobs from the list?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.scheduler.clear_completed_jobs()
                QMessageBox.information(self, "Success", "Completed jobs cleared")
                self.refresh_jobs()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to clear jobs:\n{str(e)}")

    def animate_in(self):
        pass

    def update_texts(self):
        """Update all text labels when language changes"""
        self.title_label.setText("⏰ " + t("scheduler_title"))
        self.subtitle_label.setText(t("scheduler_subtitle"))
        self.btn_new.setText(t("scheduler_schedule_new"))
        self.btn_clear.setText(t("scheduler_clear_completed"))
        self.table.setHorizontalHeaderLabels([
            t("scheduler_job_name"),
            t("scheduler_scheduled_time"),
            t("scheduler_files"),
            t("scheduler_printer"),
            t("scheduler_status"),
            t("scheduler_actions")
        ])
        self.refresh_jobs()  # Refresh to update button labels

    def closeEvent(self, event):
        """Stop scheduler when page is closed"""
        if hasattr(self, 'timer'):
            self.timer.stop()
        if hasattr(self, 'scheduler'):
            self.scheduler.stop()
        event.accept()
