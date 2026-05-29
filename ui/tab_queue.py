"""
Print Queue Tab
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import subprocess
import json
from pathlib import Path
from typing import Optional
from core.printer import PrintQueue, PrinterManager


class QueueTab(ctk.CTkFrame):
    """Print Queue management tab"""

    def __init__(self, parent, printer_manager: PrinterManager, history_manager):
        super().__init__(parent, fg_color="transparent")

        self.printer_manager = printer_manager
        self.history_manager = history_manager
        self.queue = PrintQueue()
        self.is_printing = False
        self.settings_file = Path.home() / '.pdf_print_manager' / 'settings.json'

        # Create UI
        self.create_widgets()

        # Refresh printers and load saved default
        self.refresh_printer_list()
        self.load_saved_printer()

    def create_widgets(self):
        """Create all UI widgets"""

        # Top toolbar (grid layout for better responsiveness)
        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=10, pady=10)
        toolbar.grid_columnconfigure(3, weight=1)  # Spacer column expands

        # Left side buttons - use grid for better control
        btn_frame_left = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame_left.grid(row=0, column=0, sticky="w", padx=5)

        # Add Files button
        self.add_files_btn = ctk.CTkButton(
            btn_frame_left,
            text="➕ Add Files",
            command=self.add_files,
            width=140,
            height=35
        )
        self.add_files_btn.pack(side="left", padx=3)

        # Add Folder button
        self.add_folder_btn = ctk.CTkButton(
            btn_frame_left,
            text="📁 Add Folder",
            command=self.add_folder,
            width=140,
            height=35
        )
        self.add_folder_btn.pack(side="left", padx=3)

        # Clear button
        self.clear_btn = ctk.CTkButton(
            btn_frame_left,
            text="🗑️ Clear Queue",
            command=self.clear_queue,
            width=130,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        self.clear_btn.pack(side="left", padx=3)

        # Right side - printer controls
        printer_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        printer_frame.grid(row=0, column=4, sticky="e", padx=5)

        # Printer label
        printer_label = ctk.CTkLabel(printer_frame, text="Printer:", font=ctk.CTkFont(size=14, weight="bold"))
        printer_label.pack(side="left", padx=(0, 8))

        # Printer selector
        self.printer_combo = ctk.CTkComboBox(
            printer_frame,
            values=["Loading..."],
            width=380,
            height=35,
            state="readonly",
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=12)
        )
        self.printer_combo.pack(side="left", padx=3)

        # Refresh printers button
        refresh_btn = ctk.CTkButton(
            printer_frame,
            text="🔄",
            command=self.refresh_printer_list,
            width=45,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        refresh_btn.pack(side="left", padx=3)

        # Printer settings button
        settings_btn = ctk.CTkButton(
            printer_frame,
            text="⚙️ Settings",
            command=self.open_printer_properties,
            width=100,
            height=35,
            fg_color="gray40",
            hover_color="gray30",
            font=ctk.CTkFont(size=11)
        )
        settings_btn.pack(side="left", padx=3)

        # Queue list frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Queue table (using Treeview)
        self.create_queue_table(list_frame)

        # Bottom controls
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Left side - reorder buttons
        reorder_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        reorder_frame.pack(side="left")

        self.move_up_btn = ctk.CTkButton(
            reorder_frame,
            text="↑ Move Up",
            command=self.move_up,
            width=100,
            height=35
        )
        self.move_up_btn.pack(side="left", padx=5)

        self.move_down_btn = ctk.CTkButton(
            reorder_frame,
            text="↓ Move Down",
            command=self.move_down,
            width=100,
            height=35
        )
        self.move_down_btn.pack(side="left", padx=5)

        self.remove_btn = ctk.CTkButton(
            reorder_frame,
            text="✖️ Remove",
            command=self.remove_selected,
            width=100,
            height=35,
            fg_color="darkred",
            hover_color="red"
        )
        self.remove_btn.pack(side="left", padx=5)

        # Right side - print button and progress
        right_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        right_frame.pack(side="right")

        # Progress label
        self.progress_label = ctk.CTkLabel(
            right_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(side="left", padx=10)

        # Print button
        self.print_btn = ctk.CTkButton(
            right_frame,
            text="🖨️ Print All",
            command=self.start_printing,
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.print_btn.pack(side="right", padx=5)

    def create_queue_table(self, parent):
        """Create the queue table using Treeview"""
        # Create frame for table and scrollbar
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Create Treeview
        self.style = tk.ttk.Style()
        self.style.theme_use("default")

        # Configure colors based on current theme
        self.configure_table_theme()

        # Store table frame for later theme updates
        self.table_frame = table_frame

        # Columns
        columns = ('filename', 'path', 'pages', 'status')

        self.tree = tk.ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            style="Queue.Treeview",
            selectmode='extended'  # Allow multiple selection
        )

        # Define headings
        self.tree.heading('filename', text='File Name')
        self.tree.heading('path', text='Path')
        self.tree.heading('pages', text='Pages')
        self.tree.heading('status', text='Status')

        # Define column widths
        self.tree.column('filename', width=250, minwidth=150)
        self.tree.column('path', width=350, minwidth=200)
        self.tree.column('pages', width=80, minwidth=60, anchor='center')
        self.tree.column('status', width=120, minwidth=80, anchor='center')

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def configure_table_theme(self):
        """Configure table colors based on current theme"""
        # Get current appearance mode
        appearance_mode = ctk.get_appearance_mode().lower()

        if appearance_mode == "light":
            # Light theme colors
            bg_color = "#ffffff"
            fg_color = "#000000"
            field_bg = "#f0f0f0"
            selected_bg = "#0078d4"
            heading_bg = "#e0e0e0"
            heading_fg = "#000000"
        else:
            # Dark theme colors
            bg_color = "#2b2b2b"
            fg_color = "white"
            field_bg = "#2b2b2b"
            selected_bg = "#1f6aa5"
            heading_bg = "#1f6aa5"
            heading_fg = "white"

        self.style.configure(
            "Queue.Treeview",
            background=bg_color,
            foreground=fg_color,
            fieldbackground=field_bg,
            borderwidth=0,
            font=('Segoe UI', 11),
            rowheight=28
        )
        self.style.configure(
            "Queue.Treeview.Heading",
            font=('Segoe UI', 12, 'bold'),
            background=heading_bg,
            foreground=heading_fg
        )
        self.style.map('Queue.Treeview', background=[('selected', selected_bg)])

    def refresh_queue_table(self):
        """Refresh the queue table display"""
        # Update theme colors
        self.configure_table_theme()

        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add jobs
        for job in self.queue.jobs:
            pages_text = str(job.page_count) if job.page_count > 0 else "?"

            # Status with emoji
            status_map = {
                'Pending': '⏳ Pending',
                'Printing': '🖨️ Printing',
                'Printed': '✅ Printed',
                'Error': '❌ Error'
            }
            status_text = status_map.get(job.status, job.status)

            self.tree.insert('', 'end', values=(
                job.filename,
                job.filepath,
                pages_text,
                status_text
            ))

        # Update counter
        pending_count = self.queue.get_pending_count()
        total_count = self.queue.get_job_count()
        self.progress_label.configure(text=f"{pending_count} pending of {total_count}")

    def add_files(self):
        """Add individual PDF files"""
        filepaths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if filepaths:
            self.queue.add_files(list(filepaths))
            self.refresh_queue_table()
            messagebox.showinfo("Files Added", f"Added {len(filepaths)} files to queue")

    def add_folder(self):
        """Add all PDFs from a folder"""
        folder_path = filedialog.askdirectory(title="Select folder with PDFs")

        if folder_path:
            # Ask if recursive
            recursive = messagebox.askyesno(
                "Include Subfolders",
                "Do you want to include PDFs from subfolders too?",
                default=messagebox.NO
            )

            added_jobs = self.queue.add_folder(folder_path, recursive=recursive)

            if added_jobs:
                self.refresh_queue_table()
                messagebox.showinfo("Folder Added", f"Added {len(added_jobs)} files from folder")
            else:
                messagebox.showwarning("No Files", "No PDF files found in the selected folder")

    def clear_queue(self):
        """Clear the entire queue"""
        if self.queue.get_job_count() == 0:
            return

        response = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to clear the entire queue?",
            icon=messagebox.WARNING
        )

        if response:
            self.queue.clear()
            self.refresh_queue_table()

    def move_up(self):
        """Move selected item(s) up"""
        selection = self.tree.selection()
        if not selection:
            return

        # Only allow moving single items
        if len(selection) > 1:
            messagebox.showinfo("Info", "Please select only one item to move")
            return

        index = self.tree.index(selection[0])
        if self.queue.move_up(index):
            self.refresh_queue_table()
            # Re-select the item at new position
            new_selection = self.tree.get_children()[index - 1]
            self.tree.selection_set(new_selection)
            self.tree.see(new_selection)

    def move_down(self):
        """Move selected item(s) down"""
        selection = self.tree.selection()
        if not selection:
            return

        # Only allow moving single items
        if len(selection) > 1:
            messagebox.showinfo("Info", "Please select only one item to move")
            return

        index = self.tree.index(selection[0])
        if self.queue.move_down(index):
            self.refresh_queue_table()
            # Re-select the item at new position
            new_selection = self.tree.get_children()[index + 1]
            self.tree.selection_set(new_selection)
            self.tree.see(new_selection)

    def remove_selected(self):
        """Remove selected item(s) - supports multiple selection"""
        selection = self.tree.selection()
        if not selection:
            return

        # Confirm deletion
        count = len(selection)
        if count > 1:
            response = messagebox.askyesno(
                "Confirm",
                f"Remove {count} selected files from queue?",
                icon=messagebox.WARNING
            )
            if not response:
                return

        # Get indices and sort in reverse order to delete from end to start
        indices = [self.tree.index(item) for item in selection]
        indices.sort(reverse=True)

        # Remove jobs
        for index in indices:
            self.queue.remove_job(index)

        self.refresh_queue_table()

    def refresh_printer_list(self):
        """Refresh the printer dropdown"""
        self.printer_manager.refresh_printers()
        printers = self.printer_manager.get_printers()

        if printers:
            self.printer_combo.configure(values=printers)
            default = self.printer_manager.get_default_printer()
            if default:
                self.printer_combo.set(default)
            else:
                self.printer_combo.set(printers[0])
        else:
            self.printer_combo.configure(values=["No printers"])
            self.printer_combo.set("No printers")

    def load_saved_printer(self):
        """Load saved default printer from settings"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    saved_printer = settings.get('default_printer')

                    if saved_printer and saved_printer != "No printers":
                        printers = self.printer_manager.get_printers()
                        if saved_printer in printers:
                            self.printer_combo.set(saved_printer)
        except Exception as e:
            print(f"Error loading saved printer: {e}")

    def open_printer_properties(self):
        """Open Windows printer properties dialog"""
        printer = self.printer_combo.get()
        if printer == "No printers" or not printer:
            messagebox.showwarning(
                "No Printer Selected",
                "Please select a printer first"
            )
            return

        try:
            # Open printer properties using Windows rundll32
            # This opens the printer preferences dialog where users can set duplex, quality, etc.
            subprocess.Popen([
                'rundll32',
                'printui.dll,PrintUIEntry',
                '/e',  # Display printer properties
                f'/n{printer}'
            ])

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to open printer properties:\n{str(e)}\n\n"
                f"You can also access printer settings through Windows Control Panel."
            )

    def start_printing(self):
        """Start printing selected jobs or all pending jobs if none selected"""
        # Check if any items are selected
        selection = self.tree.selection()

        if selection:
            # Print only selected items
            indices = [self.tree.index(item) for item in selection]
            jobs_to_print = [self.queue.jobs[i] for i in indices if self.queue.jobs[i].status == "Pending"]

            if not jobs_to_print:
                messagebox.showwarning("No Pending Files", "Selected files have already been printed or are in error state")
                return

            print_msg = f"Print {len(jobs_to_print)} selected file(s) to"
        else:
            # Print all pending jobs
            jobs_to_print = self.queue.get_pending_jobs()

            if not jobs_to_print:
                messagebox.showwarning("Empty Queue", "No pending files to print")
                return

            print_msg = f"Print all {len(jobs_to_print)} file(s) to"

        printer = self.printer_combo.get()
        if printer == "No printers" or not printer:
            messagebox.showerror("Error", "Please select a valid printer")
            return

        # Confirm
        response = messagebox.askyesno(
            "Confirm Print",
            f"{print_msg} '{printer}'?",
            icon=messagebox.QUESTION
        )

        if not response:
            return

        # Store jobs to print
        pending_jobs = jobs_to_print

        # Disable buttons
        self.is_printing = True
        self.print_btn.configure(state="disabled", text="⏳ Printing...")
        self.add_files_btn.configure(state="disabled")
        self.add_folder_btn.configure(state="disabled")

        # Start printing in background
        def on_progress(current, total, job):
            self.after(0, lambda: self._update_progress(current, total, job))

        def on_complete(successful, failed, errors):
            self.after(0, lambda: self._on_print_complete(successful, failed, errors))

        self.printer_manager.print_multiple_async(
            pending_jobs,
            printer,
            wait_seconds=3,
            progress_callback=on_progress,
            completion_callback=on_complete
        )

    def _update_progress(self, current, total, job):
        """Update progress display (called from print thread)"""
        self.progress_label.configure(
            text=f"Printing {current}/{total}: {job.filename}"
        )
        self.refresh_queue_table()

        # Log to history
        if job.status == "Printed":
            self.history_manager.add_entry(
                filename=job.filename,
                filepath=job.filepath,
                printer=self.printer_combo.get(),
                pages=job.page_count,
                status="Success"
            )
        elif job.status == "Error":
            self.history_manager.add_entry(
                filename=job.filename,
                filepath=job.filepath,
                printer=self.printer_combo.get(),
                pages=job.page_count,
                status="Error",
                error_message=job.error_message
            )

    def _on_print_complete(self, successful, failed, errors):
        """Called when printing is complete"""
        self.is_printing = False

        # Re-enable buttons
        self.print_btn.configure(state="normal", text="🖨️ Print All")
        self.add_files_btn.configure(state="normal")
        self.add_folder_btn.configure(state="normal")

        # Show results
        message = f"Printing completed:\n\n"
        message += f"✅ Successful: {successful}\n"
        message += f"❌ Failed: {failed}\n"

        if errors:
            message += "\nErrors:\n"
            for error in errors[:5]:  # Show first 5 errors
                message += f"  • {error}\n"
            if len(errors) > 5:
                message += f"  ... and {len(errors) - 5} more"

        if failed > 0:
            messagebox.showwarning("Printing Completed with Errors", message)
        else:
            messagebox.showinfo("Printing Successful", message)

        self.refresh_queue_table()
