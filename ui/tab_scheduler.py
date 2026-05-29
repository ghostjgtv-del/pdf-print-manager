"""
Scheduler Tab
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
"""

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from datetime import datetime, timedelta
from core.scheduler import PrintScheduler


class SchedulerTab(ctk.CTkFrame):
    """Print scheduler tab"""

    def __init__(self, parent, printer_manager, queue_tab):
        super().__init__(parent, fg_color="transparent")

        self.printer_manager = printer_manager
        self.queue_tab = queue_tab
        self.scheduler = PrintScheduler(printer_manager)

        # Start scheduler
        self.scheduler.start()

        # Create UI
        self.create_widgets()

        # Initial refresh
        self.refresh_jobs_list()

    def create_widgets(self):
        """Create UI widgets"""

        # Info banner
        info_frame = ctk.CTkFrame(self, fg_color="orange", corner_radius=8)
        info_frame.pack(fill="x", padx=10, pady=10)

        info_label = ctk.CTkLabel(
            info_frame,
            text="⚠️ The application must remain open for scheduled jobs to execute",
            font=ctk.CTkFont(size=12),
            text_color="white"
        )
        info_label.pack(pady=10, padx=15)

        # Create job section
        create_frame = ctk.CTkFrame(self)
        create_frame.pack(fill="x", padx=10, pady=(0, 10))

        title = ctk.CTkLabel(
            create_frame,
            text="Schedule New Job",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))

        # Import from queue button
        import_btn = ctk.CTkButton(
            create_frame,
            text="📋 Import Current Queue",
            command=self.import_from_queue,
            height=35
        )
        import_btn.pack(pady=5)

        # Job name
        name_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(name_frame, text="Name:", width=100, anchor="w").pack(side="left")
        self.name_entry = ctk.CTkEntry(name_frame, placeholder_text="E.g.: Daily print")
        self.name_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Date/Time pickers
        datetime_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        datetime_frame.pack(fill="x", padx=20, pady=5)

        # Date
        ctk.CTkLabel(datetime_frame, text="Date:", width=100, anchor="w").pack(side="left")
        self.date_entry = ctk.CTkEntry(datetime_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.date_entry.pack(side="left", padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Time
        ctk.CTkLabel(datetime_frame, text="Time:", width=60, anchor="w").pack(side="left", padx=(10, 0))
        self.time_entry = ctk.CTkEntry(datetime_frame, placeholder_text="HH:MM", width=80)
        self.time_entry.pack(side="left", padx=5)
        self.time_entry.insert(0, (datetime.now() + timedelta(minutes=30)).strftime("%H:%M"))

        # File count label
        self.file_count_label = ctk.CTkLabel(
            create_frame,
            text="0 files in queue",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.file_count_label.pack(pady=5)

        # Schedule button
        schedule_btn = ctk.CTkButton(
            create_frame,
            text="⏰ Schedule Job",
            command=self.schedule_job,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        schedule_btn.pack(pady=(10, 15))

        # Jobs list section
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        list_title = ctk.CTkLabel(
            list_frame,
            text="Scheduled Jobs",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        list_title.pack(pady=(15, 10))

        # Jobs table
        self.create_jobs_table(list_frame)

        # Bottom buttons
        button_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=15)

        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            command=self.refresh_jobs_list,
            width=120,
            height=35
        )
        refresh_btn.pack(side="left", padx=5)

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="✖️ Cancel Selected",
            command=self.cancel_selected,
            width=150,
            height=35,
            fg_color="darkred",
            hover_color="red"
        )
        cancel_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear Completed",
            command=self.clear_completed,
            width=150,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        clear_btn.pack(side="right", padx=5)

    def create_jobs_table(self, parent):
        """Create jobs list table"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Configure style
        style = tk.ttk.Style()
        style.configure(
            "Scheduler.Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0,
            font=('Segoe UI', 10)
        )
        style.map('Scheduler.Treeview', background=[('selected', '#1f6aa5')])

        # Columns
        columns = ('name', 'files', 'printer', 'scheduled', 'status')

        self.tree = tk.ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            style="Scheduler.Treeview",
            selectmode='browse'
        )

        # Headings
        self.tree.heading('name', text='Name')
        self.tree.heading('files', text='Files')
        self.tree.heading('printer', text='Printer')
        self.tree.heading('scheduled', text='Scheduled For')
        self.tree.heading('status', text='Status')

        # Column widths
        self.tree.column('name', width=200)
        self.tree.column('files', width=80, anchor='center')
        self.tree.column('printer', width=150)
        self.tree.column('scheduled', width=160)
        self.tree.column('status', width=120, anchor='center')

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def import_from_queue(self):
        """Import files from the print queue tab"""
        pending_jobs = self.queue_tab.queue.get_pending_jobs()

        if not pending_jobs:
            messagebox.showwarning("Empty Queue", "No files in print queue")
            return

        self.file_count_label.configure(
            text=f"{len(pending_jobs)} files imported from queue"
        )

        # Auto-fill name if empty
        if not self.name_entry.get():
            self.name_entry.insert(0, f"Job {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        messagebox.showinfo(
            "Queue Imported",
            f"Imported {len(pending_jobs)} files from print queue"
        )

    def schedule_job(self):
        """Schedule a new print job"""
        # Validate name
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a job name")
            return

        # Validate files
        pending_jobs = self.queue_tab.queue.get_pending_jobs()
        if not pending_jobs:
            messagebox.showerror("Error", "No files in queue to schedule")
            return

        # Validate date/time
        try:
            date_str = self.date_entry.get().strip()
            time_str = self.time_entry.get().strip()
            scheduled_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

            # Check if in the future
            if scheduled_time <= datetime.now():
                messagebox.showerror("Error", "Date and time must be in the future")
                return

        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format\nUse: YYYY-MM-DD and HH:MM")
            return

        # Get printer
        printer = self.queue_tab.printer_combo.get()
        if not printer or printer == "No printers":
            messagebox.showerror("Error", "Please select a valid printer")
            return

        # Get file paths
        filepaths = [job.filepath for job in pending_jobs]

        # Create scheduled job
        job = self.scheduler.add_job(
            name=name,
            filepaths=filepaths,
            printer=printer,
            scheduled_time=scheduled_time
        )

        messagebox.showinfo(
            "Job Scheduled",
            f"Job '{name}' will execute on {scheduled_time.strftime('%Y-%m-%d at %H:%M')}\n\n"
            f"Files: {len(filepaths)}\n"
            f"Printer: {printer}\n\n"
            f"⚠️ The application must remain open"
        )

        # Clear form
        self.name_entry.delete(0, 'end')
        self.file_count_label.configure(text="0 files in queue")

        # Refresh list
        self.refresh_jobs_list()

    def refresh_jobs_list(self):
        """Refresh the jobs list"""
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get all jobs
        jobs = self.scheduler.get_all_jobs()

        for job in jobs:
            status_map = {
                'Pending': '⏳ Pending',
                'Executing': '🖨️ Executing',
                'Completed': '✅ Completed',
                'Cancelled': '🚫 Cancelled',
                'Error': '❌ Error'
            }
            status_text = status_map.get(job.status, job.status)

            self.tree.insert('', 'end', values=(
                job.name,
                len(job.filepaths),
                job.printer,
                job.scheduled_time.strftime('%Y-%m-%d %H:%M'),
                status_text
            ), tags=(job.job_id,))

    def cancel_selected(self):
        """Cancel selected job"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a job")
            return

        # Get job ID from tags
        item = selection[0]
        tags = self.tree.item(item, 'tags')
        if not tags:
            return

        job_id = tags[0]

        # Confirm
        response = messagebox.askyesno(
            "Confirm Cancellation",
            "Are you sure you want to cancel this job?",
            icon=messagebox.WARNING
        )

        if response:
            if self.scheduler.cancel_job(job_id):
                messagebox.showinfo("Cancelled", "Job was cancelled successfully")
                self.refresh_jobs_list()
            else:
                messagebox.showerror("Error", "Could not cancel job")

    def clear_completed(self):
        """Clear completed and cancelled jobs"""
        self.scheduler.clear_completed_jobs()
        self.refresh_jobs_list()
        messagebox.showinfo("Cleared", "Completed and cancelled jobs were removed")
