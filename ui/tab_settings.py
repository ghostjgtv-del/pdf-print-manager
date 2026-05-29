"""
Settings Tab
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
"""

import customtkinter as ctk
from tkinter import messagebox
import json
from pathlib import Path


class SettingsTab(ctk.CTkFrame):
    """Application settings tab"""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        self.app = app
        self.settings_file = Path.home() / '.pdf_print_manager' / 'settings.json'
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)

        # Load settings
        self.settings = self.load_settings()

        # Create UI
        self.create_widgets()

    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            'default_printer': None,
            'default_folder': None,
            'theme': 'dark',
            'wait_time': 3
        }

        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    default_settings.update(saved_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")

        return default_settings

    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def create_widgets(self):
        """Create UI widgets"""

        # Title
        title = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(20, 20))

        # Scrollable settings container
        container = ctk.CTkScrollableFrame(self)
        container.pack(fill="both", expand=True, padx=50, pady=(0, 20))

        # Appearance section
        appearance_frame = self.create_section(container, "🎨 Appearance")

        ctk.CTkLabel(appearance_frame, text="Theme:", anchor="w").pack(fill="x", pady=(0, 5))

        self.theme_combo = ctk.CTkComboBox(
            appearance_frame,
            values=["dark", "light"],
            state="readonly",
            command=self.change_theme
        )
        self.theme_combo.set(self.settings.get('theme', 'dark'))
        self.theme_combo.pack(fill="x", pady=(0, 10))

        # Printer section
        printer_frame = self.create_section(container, "🖨️ Default Printer")

        ctk.CTkLabel(
            printer_frame,
            text="Select the printer to be used by default:",
            anchor="w",
            wraplength=400
        ).pack(fill="x", pady=(0, 10))

        # Get printers
        printers = self.app.printer_manager.get_printers()
        printer_values = printers if printers else ["No printers"]

        self.printer_combo = ctk.CTkComboBox(
            printer_frame,
            values=printer_values,
            state="readonly"
        )

        current_printer = self.settings.get('default_printer')
        if current_printer and current_printer in printers:
            self.printer_combo.set(current_printer)
        elif printers:
            self.printer_combo.set(printers[0])

        self.printer_combo.pack(fill="x", pady=(0, 10))

        # Print settings section
        print_frame = self.create_section(container, "🔧 Print Settings")

        ctk.CTkLabel(
            print_frame,
            text="Wait time between prints (seconds):",
            anchor="w",
            wraplength=400
        ).pack(fill="x", pady=(0, 10))

        self.wait_time_slider = ctk.CTkSlider(
            print_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            command=self.update_wait_time_label
        )
        self.wait_time_slider.set(self.settings.get('wait_time', 3))
        self.wait_time_slider.pack(fill="x", pady=(0, 5))

        self.wait_time_label = ctk.CTkLabel(
            print_frame,
            text=f"{int(self.wait_time_slider.get())} seconds",
            text_color="gray"
        )
        self.wait_time_label.pack(anchor="w")

        # License section
        license_frame = self.create_section(container, "📜 License")

        license_info = self.app.license_manager.get_license_info()

        if license_info and license_info['is_valid']:
            days = license_info['days_remaining']
            color = "green" if days > 7 else "orange"

            license_text = (
                f"✅ License active\n\n"
                f"Expires: {license_info['expires_at'].strftime('%Y-%m-%d')}\n"
                f"Days remaining: {days}"
            )

            license_label = ctk.CTkLabel(
                license_frame,
                text=license_text,
                justify="left",
                text_color=color
            )
            license_label.pack(pady=(0, 10))

        else:
            license_label = ctk.CTkLabel(
                license_frame,
                text="❌ No active license",
                justify="left",
                text_color="red"
            )
            license_label.pack(pady=(0, 10))

        renew_btn = ctk.CTkButton(
            license_frame,
            text="🔑 Renew / Activate License",
            command=self.app.show_license_window,
            height=35
        )
        renew_btn.pack(fill="x")

        # Updates section
        updates_frame = self.create_section(container, "🔄 Updates")

        from updater import Updater

        update_available, current, latest = Updater.check_for_updates()

        if update_available:
            update_text = f"🎉 Nueva versión disponible!\n\nVersión actual: {current}\nÚltima versión: {latest}"
            color = "green"
        else:
            update_text = f"✅ Estás usando la última versión\n\nVersión: {current}"
            color = "gray"

        update_label = ctk.CTkLabel(
            updates_frame,
            text=update_text,
            justify="left",
            text_color=color
        )
        update_label.pack(pady=(0, 10))

        check_update_btn = ctk.CTkButton(
            updates_frame,
            text="🔍 Buscar Actualizaciones",
            command=self.check_updates,
            height=35
        )
        check_update_btn.pack(fill="x")

        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(30, 15))

        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Settings",
            command=self.save_settings_clicked,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=5)

        reset_btn = ctk.CTkButton(
            button_frame,
            text="↺ Restore Defaults",
            command=self.reset_settings,
            height=45,
            fg_color="gray40",
            hover_color="gray30"
        )
        reset_btn.pack(side="right", fill="x", expand=True, padx=5)

    def create_section(self, parent, title):
        """Create a settings section"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="x", padx=15, pady=15)

        title_label = ctk.CTkLabel(
            section_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(anchor="w", pady=(15, 15), padx=15)

        content_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 15))

        return content_frame

    def update_wait_time_label(self, value):
        """Update wait time label"""
        self.wait_time_label.configure(text=f"{int(value)} seconds")

    def change_theme(self, choice):
        """Change application theme"""
        ctk.set_appearance_mode(choice)
        self.settings['theme'] = choice

    def save_settings_clicked(self):
        """Save settings button clicked"""
        # Update settings
        self.settings['default_printer'] = self.printer_combo.get()
        self.settings['theme'] = self.theme_combo.get()
        self.settings['wait_time'] = int(self.wait_time_slider.get())

        # Save to file
        if self.save_settings():
            messagebox.showinfo(
                "Settings Saved",
                "Settings were saved successfully"
            )

            # Apply to current session
            if self.settings['default_printer'] != "No printers":
                self.app.printer_manager.set_default_printer(self.settings['default_printer'])

        else:
            messagebox.showerror(
                "Error",
                "Could not save settings"
            )

    def reset_settings(self):
        """Reset settings to defaults"""
        response = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to restore default settings?",
            icon=messagebox.WARNING
        )

        if response:
            self.settings = {
                'default_printer': None,
                'default_folder': None,
                'theme': 'dark',
                'wait_time': 3
            }

            # Update UI
            self.theme_combo.set('dark')
            self.wait_time_slider.set(3)
            self.update_wait_time_label(3)

            # Save
            self.save_settings()

            messagebox.showinfo(
                "Restored",
                "Settings were restored to defaults"
            )

    def check_updates(self):
        """Check for application updates"""
        from updater import Updater

        update_available, current, latest = Updater.check_for_updates()

        if update_available:
            response = messagebox.askyesno(
                "Actualización Disponible",
                f"Nueva versión disponible!\n\n"
                f"Versión actual: {current}\n"
                f"Nueva versión: {latest}\n\n"
                f"¿Desea descargar e instalar la actualización ahora?\n"
                f"La aplicación se reiniciará automáticamente.",
                icon=messagebox.INFO
            )

            if response:
                # Create progress window
                progress_window = ctk.CTkToplevel(self.app)
                progress_window.title("Descargando Actualización")
                progress_window.geometry("400x150")
                progress_window.transient(self.app)
                progress_window.grab_set()

                # Center window
                progress_window.update_idletasks()
                x = (progress_window.winfo_screenwidth() // 2) - 200
                y = (progress_window.winfo_screenheight() // 2) - 75
                progress_window.geometry(f"+{x}+{y}")

                label = ctk.CTkLabel(
                    progress_window,
                    text="Descargando actualización...",
                    font=ctk.CTkFont(size=14)
                )
                label.pack(pady=(20, 10))

                progress_bar = ctk.CTkProgressBar(progress_window, width=300)
                progress_bar.pack(pady=10)
                progress_bar.set(0)

                progress_label = ctk.CTkLabel(progress_window, text="0%")
                progress_label.pack()

                def update_progress(value):
                    progress_bar.set(value / 100)
                    progress_label.configure(text=f"{value}%")
                    progress_window.update()

                # Download and install
                success, message = Updater.download_and_install_update(update_progress)

                progress_window.destroy()

                if success:
                    messagebox.showinfo("Actualización", message)
                    # App will be restarted by update script
                    self.app.quit()
                else:
                    messagebox.showerror("Error", message)
        else:
            messagebox.showinfo(
                "Actualización",
                f"Ya estás usando la última versión ({current})"
            )
