"""
History Tab
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
from datetime import datetime, timedelta


class HistoryTab(ctk.CTkFrame):
    """Print history tab"""

    def __init__(self, parent, history_manager):
        super().__init__(parent, fg_color="transparent")

        self.history_manager = history_manager

        # Create UI
        self.create_widgets()

        # Initial load
        self.refresh_history()

    def create_widgets(self):
        """Create UI widgets"""

        # Toolbar
        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=10, pady=10)

        # Filter section
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(filter_frame, text="Filter:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)

        # Status filter
        ctk.CTkLabel(filter_frame, text="Status:").pack(side="left", padx=(15, 5))
        self.status_combo = ctk.CTkComboBox(
            filter_frame,
            values=["All", "Success", "Error"],
            width=120,
            state="readonly",
            command=lambda _: self.refresh_history()
        )
        self.status_combo.set("All")
        self.status_combo.pack(side="left", padx=5)

        # Date filter
        ctk.CTkLabel(filter_frame, text="Period:").pack(side="left", padx=(15, 5))
        self.period_combo = ctk.CTkComboBox(
            filter_frame,
            values=["Today", "Last 7 days", "Last 30 days", "All"],
            width=150,
            state="readonly",
            command=lambda _: self.refresh_history()
        )
        self.period_combo.set("Last 7 days")
        self.period_combo.pack(side="left", padx=5)

        # Buttons
        button_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        button_frame.pack(side="right")

        export_btn = ctk.CTkButton(
            button_frame,
            text="📊 Export CSV",
            command=self.export_csv,
            width=130,
            height=35
        )
        export_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_history,
            width=100,
            height=35,
            fg_color="darkred",
            hover_color="red"
        )
        clear_btn.pack(side="left", padx=5)

        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄",
            command=self.refresh_history,
            width=40,
            height=35
        )
        refresh_btn.pack(side="left", padx=5)

        # Statistics frame
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Loading statistics...",
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        self.stats_label.pack(pady=10, padx=15, anchor="w")

        # History table
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.create_history_table(table_frame)

    def create_history_table(self, parent):
        """Create history table"""
        # Configure style
        style = tk.ttk.Style()
        style.configure(
            "History.Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0,
            font=('Segoe UI', 10),
            rowheight=25
        )
        style.map('History.Treeview', background=[('selected', '#1f6aa5')])

        # Columns
        columns = ('timestamp', 'filename', 'printer', 'pages', 'status')

        self.tree = tk.ttk.Treeview(
            parent,
            columns=columns,
            show='headings',
            style="History.Treeview",
            selectmode='browse'
        )

        # Headings
        self.tree.heading('timestamp', text='Date/Time')
        self.tree.heading('filename', text='File Name')
        self.tree.heading('printer', text='Printer')
        self.tree.heading('pages', text='Pages')
        self.tree.heading('status', text='Status')

        # Column widths
        self.tree.column('timestamp', width=160)
        self.tree.column('filename', width=300)
        self.tree.column('printer', width=200)
        self.tree.column('pages', width=80, anchor='center')
        self.tree.column('status', width=120, anchor='center')

        # Scrollbars
        vsb = ctk.CTkScrollbar(parent, command=self.tree.yview)
        hsb = ctk.CTkScrollbar(parent, orientation="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Double-click to show details
        self.tree.bind('<Double-Button-1>', self.show_details)

    def get_date_range(self):
        """Get date range based on period selection"""
        period = self.period_combo.get()

        if period == "Today":
            date_from = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return date_from, None
        elif period == "Last 7 days":
            date_from = datetime.now() - timedelta(days=7)
            return date_from, None
        elif period == "Last 30 days":
            date_from = datetime.now() - timedelta(days=30)
            return date_from, None
        else:  # All
            return None, None

    def refresh_history(self):
        """Refresh history table"""
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get filters
        status = self.status_combo.get()
        status_filter = None if status == "All" else status

        date_from, date_to = self.get_date_range()

        # Load history
        entries = self.history_manager.get_history(
            limit=1000,
            status_filter=status_filter,
            date_from=date_from,
            date_to=date_to
        )

        # Populate table
        for entry in entries:
            timestamp_str = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            pages_str = str(entry['pages']) if entry['pages'] > 0 else "-"

            status_map = {
                'Success': '✅ Success',
                'Error': '❌ Error'
            }
            status_text = status_map.get(entry['status'], entry['status'])

            # Store entry ID in tags
            self.tree.insert('', 'end', values=(
                timestamp_str,
                entry['filename'],
                entry['printer'],
                pages_str,
                status_text
            ), tags=(entry['id'],))

        # Update statistics
        self.update_statistics()

    def update_statistics(self):
        """Update statistics display"""
        stats = self.history_manager.get_statistics()

        if stats:
            success_rate = 0
            if stats['total_prints'] > 0:
                success_rate = (stats['successful_prints'] / stats['total_prints']) * 100

            stats_text = (
                f"📊 Total: {stats['total_prints']} prints  |  "
                f"✅ Successful: {stats['successful_prints']}  |  "
                f"❌ Failed: {stats['failed_prints']}  |  "
                f"📄 Pages: {stats['total_pages']}  |  "
                f"📈 Success rate: {success_rate:.1f}%"
            )
            self.stats_label.configure(text=stats_text)
        else:
            self.stats_label.configure(text="No history data")

    def show_details(self, event):
        """Show details of selected entry"""
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.tree.item(item, 'values')
        tags = self.tree.item(item, 'tags')

        if not tags:
            return

        entry_id = tags[0]

        # Get full entry details
        entries = self.history_manager.get_history(limit=99999)
        entry = next((e for e in entries if e['id'] == entry_id), None)

        if not entry:
            return

        # Create details window
        details_window = ctk.CTkToplevel(self)
        details_window.title("Print Details")
        details_window.geometry("500x400")
        details_window.transient(self)
        details_window.grab_set()

        # Center window
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (250)
        y = (details_window.winfo_screenheight() // 2) - (200)
        details_window.geometry(f'+{x}+{y}')

        # Content
        content = ctk.CTkFrame(details_window)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            content,
            text="Print Details",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(0, 20))

        # Details
        details = [
            ("Date/Time:", entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')),
            ("File Name:", entry['filename']),
            ("Path:", entry['filepath']),
            ("Printer:", entry['printer']),
            ("Pages:", str(entry['pages']) if entry['pages'] > 0 else "Unknown"),
            ("Status:", "✅ Success" if entry['status'] == 'Success' else "❌ Error")
        ]

        for label, value in details:
            row = ctk.CTkFrame(content, fg_color="transparent")
            row.pack(fill="x", pady=5)

            label_widget = ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=100,
                anchor="w"
            )
            label_widget.pack(side="left")

            value_widget = ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=12),
                anchor="w",
                wraplength=350
            )
            value_widget.pack(side="left", fill="x", expand=True)

        # Error message if any
        if entry.get('error_message'):
            error_frame = ctk.CTkFrame(content, fg_color="darkred", corner_radius=8)
            error_frame.pack(fill="x", pady=(15, 0))

            error_label = ctk.CTkLabel(
                error_frame,
                text=f"Error message:\n{entry['error_message']}",
                font=ctk.CTkFont(size=11),
                justify="left",
                wraplength=400
            )
            error_label.pack(pady=10, padx=10)

        # Close button
        close_btn = ctk.CTkButton(
            content,
            text="Close",
            command=details_window.destroy,
            height=40
        )
        close_btn.pack(side="bottom", pady=(20, 0))

    def export_csv(self):
        """Export history to CSV"""
        # Ask for file path
        filepath = filedialog.asksaveasfilename(
            title="Save history as CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"print_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        if not filepath:
            return

        # Get date range
        date_from, date_to = self.get_date_range()

        # Export
        success = self.history_manager.export_to_csv(filepath, date_from, date_to)

        if success:
            messagebox.showinfo(
                "Export Successful",
                f"History was exported to:\n{filepath}"
            )
        else:
            messagebox.showerror(
                "Error",
                "Could not export history"
            )

    def clear_history(self):
        """Clear history with confirmation"""
        response = messagebox.askyesnocancel(
            "Confirm Clear",
            "What do you want to delete?\n\n"
            "Yes - Delete all history\n"
            "No - Delete only old records (>30 days)\n"
            "Cancel - Don't delete anything",
            icon=messagebox.WARNING
        )

        if response is None:  # Cancel
            return

        if response:  # Yes - clear all
            if self.history_manager.clear_history():
                messagebox.showinfo("Completed", "All history was deleted")
                self.refresh_history()
            else:
                messagebox.showerror("Error", "Could not delete history")
        else:  # No - clear old
            date_before = datetime.now() - timedelta(days=30)
            if self.history_manager.clear_history(date_before):
                messagebox.showinfo("Completed", "Old records were deleted")
                self.refresh_history()
            else:
                messagebox.showerror("Error", "Could not delete history")
