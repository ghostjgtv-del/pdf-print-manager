"""
Sidebar Navigation
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
"""

import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    """Left sidebar with navigation buttons"""

    def __init__(self, parent, on_tab_change):
        super().__init__(parent, width=200, corner_radius=0, fg_color=("gray90", "gray14"))

        self.on_tab_change = on_tab_change
        self.current_tab = "queue"

        # Logo/Title section
        self.create_header()

        # Navigation buttons
        self.create_nav_buttons()

        # Footer
        self.create_footer()

    def create_header(self):
        """Create header with logo and title"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=20, padx=20)

        # Logo emoji (will be replaced with actual logo if available)
        logo_label = ctk.CTkLabel(
            header_frame,
            text="📄",
            font=ctk.CTkFont(size=48)
        )
        logo_label.pack()

        title_label = ctk.CTkLabel(
            header_frame,
            text="PDF Print\nManager",
            font=ctk.CTkFont(size=16, weight="bold"),
            justify="center"
        )
        title_label.pack(pady=(10, 0))

    def create_nav_buttons(self):
        """Create navigation buttons"""
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=10, pady=20)

        # Navigation items
        nav_items = [
            ("queue", "📋 Print Queue", "queue"),
            ("scheduler", "⏰ Scheduler", "scheduler"),
            ("history", "📊 History", "history"),
            ("settings", "⚙️ Settings", "settings")
        ]

        self.nav_buttons = {}

        for key, label, command_param in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=label,
                command=lambda p=command_param: self.select_tab(p),
                height=45,
                corner_radius=8,
                anchor="w",
                font=ctk.CTkFont(size=13)
            )
            btn.pack(fill="x", pady=5)
            self.nav_buttons[key] = btn

        # Set initial selection
        self.update_button_styles()

    def create_footer(self):
        """Create footer with info"""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=20, padx=20)

        # About button - same style as nav buttons
        self.about_btn = ctk.CTkButton(
            footer_frame,
            text="ℹ️ About",
            command=self.show_about,
            height=40,
            corner_radius=8,
            fg_color=("gray80", "gray25"),
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            font=ctk.CTkFont(size=13)
        )
        self.about_btn.pack(fill="x")

        # Version label
        version_label = ctk.CTkLabel(
            footer_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60")
        )
        version_label.pack(pady=(10, 0))

    def select_tab(self, tab_name):
        """Handle tab selection"""
        if tab_name != self.current_tab:
            self.current_tab = tab_name
            self.update_button_styles()
            if self.on_tab_change:
                self.on_tab_change(tab_name)

    def update_button_styles(self):
        """Update button styles based on selection"""
        for key, btn in self.nav_buttons.items():
            if key == self.current_tab:
                # Selected button - darker/more prominent
                btn.configure(
                    fg_color=("#1f6aa5", "#1f6aa5"),
                    text_color=("white", "white"),
                    hover_color=("#144870", "#144870")
                )
            else:
                # Unselected button
                btn.configure(
                    fg_color=("gray80", "gray25"),
                    text_color=("gray10", "gray90"),
                    hover_color=("gray70", "gray30")
                )

    def show_about(self):
        """Show about/license info window"""
        if self.on_tab_change:
            self.on_tab_change("about")
