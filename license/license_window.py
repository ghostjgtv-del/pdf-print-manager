"""
License Activation Window
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from .license_manager import LicenseManager
import os
from pathlib import Path
import re


class LicenseWindow(ctk.CTkToplevel):
    """License activation window"""

    def __init__(self, parent, on_success_callback=None):
        super().__init__(parent)

        self.manager = LicenseManager()
        self.on_success_callback = on_success_callback

        # Window configuration
        self.title("PDF Print Manager - License Activation")
        self.geometry("600x550")
        self.resizable(False, False)

        # Make it modal
        self.transient(parent)
        self.grab_set()

        # Center window
        self.center_window()

        # Create UI
        self.create_widgets()

        # Check if license exists
        self.check_existing_license()

    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create UI widgets"""

        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Logo placeholder
        logo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        logo_frame.pack(pady=(0, 10))

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="📄",
            font=ctk.CTkFont(size=60)
        )
        logo_label.pack()

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="PDF Print Manager",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="License Activation",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 20))

        # Status frame
        self.status_frame = ctk.CTkFrame(main_frame)
        self.status_frame.pack(fill="x", pady=(0, 20))

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="⚠️ This application requires a valid license",
            font=ctk.CTkFont(size=12),
            wraplength=500
        )
        self.status_label.pack(pady=10)

        # License code input
        input_label = ctk.CTkLabel(
            main_frame,
            text="License Code:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        input_label.pack(anchor="w", pady=(0, 5))

        self.license_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="LFFG-XXXX-XXXX-XXXX-XXXX",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.license_entry.pack(fill="x", pady=(0, 10))

        # Load from file button
        load_file_button = ctk.CTkButton(
            main_frame,
            text="📁 Load from File",
            command=self.load_from_file,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        load_file_button.pack(fill="x", pady=(0, 15))

        # Activate button
        self.activate_button = ctk.CTkButton(
            main_frame,
            text="Activate License",
            command=self.activate_license,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.activate_button.pack(fill="x", pady=(0, 20))

        # Separator
        separator = ctk.CTkFrame(main_frame, height=2)
        separator.pack(fill="x", pady=15)

        # Contact information
        contact_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        contact_frame.pack()

        contact_title = ctk.CTkLabel(
            contact_frame,
            text="To acquire or renew your license, contact:",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        contact_title.pack(pady=(0, 8))

        contact_info = ctk.CTkLabel(
            contact_frame,
            text="Eng. Justo Torres\nLagudis Fresh Food Group\nghost.jgtv@gmail.com",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        contact_info.pack()

        # Footer
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=(15, 0))

        footer_label = ctk.CTkLabel(
            footer_frame,
            text="© 2026 Lagudis Fresh Food Group - All rights reserved",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        footer_label.pack()

    def check_existing_license(self):
        """Check if there's an existing license"""
        is_valid, message, days_remaining = self.manager.load_license()

        if is_valid:
            if days_remaining <= 7:
                self.status_label.configure(
                    text=f"⚠️ {message}",
                    text_color="orange"
                )
            else:
                self.status_label.configure(
                    text=f"✅ {message}",
                    text_color="green"
                )

                # If license is valid and has more than 7 days, offer to continue
                response = messagebox.askyesno(
                    "Valid License",
                    f"{message}\n\nDo you want to enter a new license anyway?",
                    parent=self
                )

                if not response:
                    self.on_activation_success()
        else:
            self.status_label.configure(
                text=f"❌ {message}",
                text_color="red"
            )

    def load_from_file(self):
        """Load license code from a file"""
        filepath = filedialog.askopenfilename(
            title="Select License File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            parent=self
        )

        if not filepath:
            return

        try:
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract license code using regex
            # Look for pattern: LFFG-XXXX-XXXX-XXXX-XXXX
            pattern = r'LFFG-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{8}'
            match = re.search(pattern, content)

            if match:
                license_code = match.group(0)

                # Clear current entry and insert the code
                self.license_entry.delete(0, 'end')
                self.license_entry.insert(0, license_code)

                messagebox.showinfo(
                    "License Loaded",
                    f"License code loaded successfully!\n\nCode: {license_code[:20]}...",
                    parent=self
                )
            else:
                messagebox.showerror(
                    "Invalid File",
                    "No valid license code found in the file.\n\n"
                    "Please select a valid license file.",
                    parent=self
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to read file:\n{str(e)}",
                parent=self
            )

    def activate_license(self):
        """Activate the license"""
        license_code = self.license_entry.get().strip()

        if not license_code:
            messagebox.showerror(
                "Error",
                "Please enter a license code",
                parent=self
            )
            return

        # Disable button during validation
        self.activate_button.configure(state="disabled", text="Validating...")
        self.update()

        # Validate and save
        success, message = self.manager.save_license(license_code)

        # Re-enable button
        self.activate_button.configure(state="normal", text="Activate License")

        if success:
            messagebox.showinfo(
                "Activation Successful",
                f"✅ {message}\n\nThe application is ready to use!",
                parent=self
            )
            self.on_activation_success()
        else:
            messagebox.showerror(
                "Activation Error",
                f"❌ {message}\n\nPlease verify the code and try again.",
                parent=self
            )

    def on_activation_success(self):
        """Called when activation is successful"""
        if self.on_success_callback:
            self.on_success_callback()
        self.destroy()


class LicenseInfoWindow(ctk.CTkToplevel):
    """Window to display license information"""

    def __init__(self, parent):
        super().__init__(parent)

        self.manager = LicenseManager()

        # Window configuration
        self.title("License Information")
        self.geometry("500x450")
        self.resizable(False, False)

        # Make it modal
        self.transient(parent)
        self.grab_set()

        # Center window
        self.center_window()

        # Create UI
        self.create_widgets()

    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create UI widgets"""

        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="PDF Print Manager v1.0",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Developer info
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))

        dev_info = [
            ("Developed by:", "Eng. Justo Torres"),
            ("Company:", "Lagudis Fresh Food Group"),
            ("Contact:", "ghost.jgtv@gmail.com"),
            ("Version:", "1.0.0"),
            ("Date:", "May 2026")
        ]

        for label, value in dev_info:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=10)

            label_widget = ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=120,
                anchor="w"
            )
            label_widget.pack(side="left")

            value_widget = ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            value_widget.pack(side="left", fill="x", expand=True)

        # Separator
        separator = ctk.CTkFrame(main_frame, height=2)
        separator.pack(fill="x", pady=15)

        # License info
        license_info = self.manager.get_license_info()

        license_frame = ctk.CTkFrame(main_frame)
        license_frame.pack(fill="x", pady=(0, 20))

        license_title = ctk.CTkLabel(
            license_frame,
            text="License Information",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        license_title.pack(pady=(10, 10))

        if license_info and license_info['is_valid']:
            status_color = "green" if license_info['days_remaining'] > 7 else "orange"
            status_text = "✅ Active" if license_info['days_remaining'] > 7 else "⚠️ Expiring soon"

            # Mask license code - show only last segment after last dash
            license_code = license_info['code']
            if '-' in license_code:
                last_segment = license_code.split('-')[-1]
                masked_code = f"****-****-********-****-{last_segment}"
            else:
                masked_code = "****-****-********-****-****"

            license_data = [
                ("Status:", status_text, status_color),
                ("Code:", masked_code, "white"),
                ("Activated:", license_info['activated_at'].strftime('%Y-%m-%d'), "white"),
                ("Expires:", license_info['expires_at'].strftime('%Y-%m-%d'), "white"),
                ("Days remaining:", str(license_info['days_remaining']), status_color)
            ]

            for label, value, color in license_data:
                row = ctk.CTkFrame(license_frame, fg_color="transparent")
                row.pack(fill="x", pady=3, padx=10)

                label_widget = ctk.CTkLabel(
                    row,
                    text=label,
                    font=ctk.CTkFont(size=11),
                    width=120,
                    anchor="w"
                )
                label_widget.pack(side="left")

                value_widget = ctk.CTkLabel(
                    row,
                    text=value,
                    font=ctk.CTkFont(size=11),
                    text_color=color,
                    anchor="w"
                )
                value_widget.pack(side="left")

        else:
            no_license_label = ctk.CTkLabel(
                license_frame,
                text="❌ No active license",
                font=ctk.CTkFont(size=12),
                text_color="red"
            )
            no_license_label.pack(pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        renew_button = ctk.CTkButton(
            button_frame,
            text="Renew License",
            command=self.open_license_activation,
            height=35
        )
        renew_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.destroy,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        close_button.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Footer
        footer_label = ctk.CTkLabel(
            main_frame,
            text="© 2026 Lagudis Fresh Food Group - All rights reserved",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        footer_label.pack(side="bottom", pady=(15, 0))

    def open_license_activation(self):
        """Open license activation window"""
        self.destroy()
        # The parent will handle opening the activation window
        if hasattr(self.master, 'show_license_window'):
            self.master.show_license_window()
