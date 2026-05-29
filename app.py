"""
Main Application Window
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
Date: May 2026
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import json
from pathlib import Path

# Core modules
from core.printer import PrinterManager
from core.history import HistoryManager
from license.license_manager import LicenseManager
from license.license_window import LicenseWindow, LicenseInfoWindow

# UI modules
from ui.sidebar import Sidebar
from ui.tab_queue import QueueTab
from ui.tab_scheduler import SchedulerTab
from ui.tab_history import HistoryTab
from ui.tab_settings import SettingsTab


class PDFPrintManagerApp(ctk.CTk):
    """Main application window"""

    def __init__(self):
        super().__init__()

        # Load saved theme
        saved_theme = self.load_saved_theme()
        ctk.set_appearance_mode(saved_theme)
        ctk.set_default_color_theme("blue")

        # Window configuration
        self.title("PDF Print Manager - Lagudis Fresh Food Group")
        self.geometry("1500x850")
        self.minsize(1300, 750)

        # Initialize managers
        self.license_manager = LicenseManager()
        self.printer_manager = PrinterManager()
        self.history_manager = HistoryManager()

        # Check license before showing UI
        if not self.check_license():
            self.withdraw()  # Hide main window
            self.show_license_window(required=True)
        else:
            self.create_ui()
            self.center_window()

    def load_saved_theme(self):
        """Load saved theme from settings"""
        try:
            settings_file = Path.home() / '.pdf_print_manager' / 'settings.json'
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return settings.get('theme', 'dark')
        except:
            pass
        return 'dark'

    def check_license(self):
        """Check if license is valid"""
        is_valid, message, days_remaining = self.license_manager.load_license()

        if not is_valid:
            return False

        # Show warning if expiring soon
        if days_remaining <= 7:
            messagebox.showwarning(
                "License Expiring Soon",
                f"{message}\n\nPlease contact:\nEng. Justo Torres\nghost.jgtv@gmail.com"
            )

        return True

    def show_license_window(self, required=False):
        """Show license activation window"""
        def on_success():
            if required:
                # License was activated, now show main window
                self.deiconify()
                self.create_ui()
                self.center_window()
                # Mark that license was successfully activated
                self.license_activated = True

        self.license_activated = False
        license_window = LicenseWindow(self, on_success_callback=on_success)

        if required:
            # Wait for window to close
            self.wait_window(license_window)

            # If license was not activated, exit
            if not self.license_activated:
                messagebox.showerror(
                    "License Required",
                    "The application requires a valid license to function.\n\n"
                    "Contact:\nEng. Justo Torres\nghost.jgtv@gmail.com"
                )
                self.quit()
                sys.exit(1)

    def create_ui(self):
        """Create the main UI"""
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, on_tab_change=self.change_tab)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Main content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Create tabs (but don't show them yet)
        self.tabs = {}
        self.current_tab = None

        # Initialize with queue tab
        self.change_tab("queue")

    def change_tab(self, tab_name):
        """Change the active tab"""
        # Handle special case for about
        if tab_name == "about":
            LicenseInfoWindow(self)
            return

        # If tab doesn't exist, create it
        if tab_name not in self.tabs:
            if tab_name == "queue":
                self.tabs[tab_name] = QueueTab(
                    self.content_frame,
                    self.printer_manager,
                    self.history_manager
                )
            elif tab_name == "scheduler":
                # Queue tab must exist first for scheduler
                if "queue" not in self.tabs:
                    self.tabs["queue"] = QueueTab(
                        self.content_frame,
                        self.printer_manager,
                        self.history_manager
                    )

                self.tabs[tab_name] = SchedulerTab(
                    self.content_frame,
                    self.printer_manager,
                    self.tabs["queue"]
                )
            elif tab_name == "history":
                self.tabs[tab_name] = HistoryTab(
                    self.content_frame,
                    self.history_manager
                )
            elif tab_name == "settings":
                self.tabs[tab_name] = SettingsTab(
                    self.content_frame,
                    self
                )

        # Hide current tab
        if self.current_tab and self.current_tab in self.tabs:
            self.tabs[self.current_tab].pack_forget()

        # Show new tab
        if tab_name in self.tabs:
            self.tabs[tab_name].pack(fill="both", expand=True)
            self.current_tab = tab_name

    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def on_closing(self):
        """Handle window closing"""
        # Stop scheduler if it's running
        if "scheduler" in self.tabs:
            self.tabs["scheduler"].scheduler.stop()

        # Ask for confirmation if printing
        if "queue" in self.tabs and self.tabs["queue"].is_printing:
            response = messagebox.askyesno(
                "Printing in Progress",
                "There is a print job in progress. Are you sure you want to exit?",
                icon=messagebox.WARNING
            )

            if not response:
                return

        self.quit()

    def run(self):
        """Run the application"""
        # Set closing protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start main loop
        self.mainloop()
