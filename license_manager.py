"""
Lagudi License Manager
Sistema de gestión de licencias para PDF Print Manager
Author: Eng. Justo Torres - Lagudis Fresh Food Group
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
import pyperclip
from PIL import Image

# Configuración del tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Configuración del servidor
SERVER_URL = "http://143.110.130.78:8001"

class LicenseManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("Lagudi License Manager - PDF Print Manager")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # Colores personalizados Lagudis
        self.colors = {
            "primary": "#1e88e5",      # Azul Lagudis
            "secondary": "#0d47a1",    # Azul oscuro
            "success": "#43a047",      # Verde
            "warning": "#fb8c00",      # Naranja
            "danger": "#e53935",       # Rojo
            "dark": "#1a1a1a",         # Fondo oscuro
            "card": "#2b2b2b",         # Tarjetas
            "text": "#ffffff",         # Texto principal
            "text_secondary": "#b0b0b0" # Texto secundario
        }

        # Configurar el grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear sidebar
        self.create_sidebar()

        # Crear área principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Vista por defecto
        self.current_view = None
        self.show_generate_view()

    def create_sidebar(self):
        """Crear sidebar con navegación"""
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.colors["card"])
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)

        # Logo y título
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="ew")

        title_label = ctk.CTkLabel(
            logo_frame,
            text="🔑 LICENSE\nMANAGER",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["primary"]
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="Lagudis Fresh Food Group",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_secondary"]
        )
        subtitle_label.pack(pady=(5, 0))

        # Separador
        separator = ctk.CTkFrame(sidebar, height=2, fg_color=self.colors["primary"])
        separator.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # Botones de navegación
        btn_generate = ctk.CTkButton(
            sidebar,
            text="📝 Generar Licencia",
            command=self.show_generate_view,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            corner_radius=10
        )
        btn_generate.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        btn_list = ctk.CTkButton(
            sidebar,
            text="📋 Ver Licencias",
            command=self.show_list_view,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            hover_color=self.colors["card"],
            border_width=2,
            border_color=self.colors["primary"],
            corner_radius=10
        )
        btn_list.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        btn_validate = ctk.CTkButton(
            sidebar,
            text="✓ Validar Licencia",
            command=self.show_validate_view,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            hover_color=self.colors["card"],
            border_width=2,
            border_color=self.colors["primary"],
            corner_radius=10
        )
        btn_validate.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Estado del servidor
        self.server_status_frame = ctk.CTkFrame(sidebar, fg_color=self.colors["dark"], corner_radius=10)
        self.server_status_frame.grid(row=7, column=0, padx=20, pady=20, sticky="ew")

        status_title = ctk.CTkLabel(
            self.server_status_frame,
            text="Estado del Servidor",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["text_secondary"]
        )
        status_title.pack(pady=(10, 5))

        self.server_status_label = ctk.CTkLabel(
            self.server_status_frame,
            text="● Verificando...",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["warning"]
        )
        self.server_status_label.pack(pady=(0, 10))

        # Verificar estado del servidor
        self.check_server_status()

    def check_server_status(self):
        """Verificar si el servidor está disponible"""
        try:
            response = requests.get(f"{SERVER_URL}/ping", timeout=3)
            if response.status_code == 200:
                self.server_status_label.configure(
                    text="● Conectado",
                    text_color=self.colors["success"]
                )
            else:
                self.server_status_label.configure(
                    text="● Error",
                    text_color=self.colors["danger"]
                )
        except:
            self.server_status_label.configure(
                text="● Sin conexión",
                text_color=self.colors["danger"]
            )

    def clear_main_frame(self):
        """Limpiar el frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_generate_view(self):
        """Vista para generar nuevas licencias"""
        self.clear_main_frame()
        self.current_view = "generate"

        # Título
        title = ctk.CTkLabel(
            self.main_frame,
            text="📝 Generar Nueva Licencia",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Frame del formulario
        form_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["card"], corner_radius=15)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        form_frame.grid_columnconfigure(0, weight=1)

        # Contenedor con padding
        content = ctk.CTkFrame(form_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)

        # Client ID
        ctk.CTkLabel(
            content,
            text="ID del Cliente",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.client_id_entry = ctk.CTkEntry(
            content,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Ej: LFFG-PROD-001"
        )
        self.client_id_entry.pack(fill="x", pady=(0, 20))

        # Duración
        ctk.CTkLabel(
            content,
            text="Duración (días)",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        duration_frame = ctk.CTkFrame(content, fg_color="transparent")
        duration_frame.pack(fill="x", pady=(0, 20))

        self.duration_entry = ctk.CTkEntry(
            duration_frame,
            height=45,
            width=200,
            font=ctk.CTkFont(size=14),
            placeholder_text="365"
        )
        self.duration_entry.pack(side="left", padx=(0, 10))

        # Botones rápidos
        btn_30 = ctk.CTkButton(
            duration_frame,
            text="30 días",
            width=80,
            height=45,
            command=lambda: self.duration_entry.delete(0, "end") or self.duration_entry.insert(0, "30")
        )
        btn_30.pack(side="left", padx=5)

        btn_365 = ctk.CTkButton(
            duration_frame,
            text="1 año",
            width=80,
            height=45,
            command=lambda: self.duration_entry.delete(0, "end") or self.duration_entry.insert(0, "365")
        )
        btn_365.pack(side="left", padx=5)

        btn_1095 = ctk.CTkButton(
            duration_frame,
            text="3 años",
            width=80,
            height=45,
            command=lambda: self.duration_entry.delete(0, "end") or self.duration_entry.insert(0, "1095")
        )
        btn_1095.pack(side="left", padx=5)

        # Notas
        ctk.CTkLabel(
            content,
            text="Notas (opcional)",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.notes_entry = ctk.CTkTextbox(
            content,
            height=100,
            font=ctk.CTkFont(size=14)
        )
        self.notes_entry.pack(fill="x", pady=(0, 30))

        # Botón generar
        generate_btn = ctk.CTkButton(
            content,
            text="🔑 GENERAR LICENCIA",
            height=60,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors["success"],
            hover_color="#2e7d32",
            command=self.generate_license
        )
        generate_btn.pack(fill="x")

        # Frame de resultado (oculto inicialmente)
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["dark"], corner_radius=15)
        self.result_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        self.result_frame.grid_remove()

    def generate_license(self):
        """Generar una nueva licencia"""
        client_id = self.client_id_entry.get().strip()
        duration = self.duration_entry.get().strip()
        notes = self.notes_entry.get("1.0", "end-1c").strip()

        # Validaciones
        if not client_id:
            messagebox.showerror("Error", "El ID del cliente es requerido")
            return

        if not duration or not duration.isdigit():
            messagebox.showerror("Error", "La duración debe ser un número válido")
            return

        # Datos para el servidor
        data = {
            "client_id": client_id,
            "duration_days": int(duration),
            "notes": notes if notes else f"Licencia generada el {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        }

        try:
            response = requests.post(f"{SERVER_URL}/license/generate", json=data)

            if response.status_code == 200:
                result = response.json()
                self.show_license_result(result)
            else:
                messagebox.showerror("Error", f"Error al generar licencia: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")

    def show_license_result(self, result):
        """Mostrar el resultado de la licencia generada"""
        # Limpiar resultado anterior
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.result_frame.grid()

        content = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)

        # Título
        title = ctk.CTkLabel(
            content,
            text="✅ Licencia Generada Exitosamente",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors["success"]
        )
        title.pack(pady=(0, 20))

        # Código de licencia
        license_frame = ctk.CTkFrame(content, fg_color=self.colors["card"], corner_radius=10)
        license_frame.pack(fill="x", pady=(0, 15))

        license_content = ctk.CTkFrame(license_frame, fg_color="transparent")
        license_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            license_content,
            text="Código de Licencia:",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        ).pack(anchor="w")

        license_code = result.get("license_code", "")
        license_label = ctk.CTkLabel(
            license_content,
            text=license_code,
            font=ctk.CTkFont(size=16, weight="bold", family="Consolas"),
            text_color=self.colors["primary"]
        )
        license_label.pack(anchor="w", pady=(5, 10))

        # Botón copiar
        copy_btn = ctk.CTkButton(
            license_content,
            text="📋 Copiar al Portapapeles",
            height=40,
            command=lambda: self.copy_to_clipboard(license_code),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"]
        )
        copy_btn.pack(fill="x")

        # Información adicional
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(fill="x")

        info_items = [
            ("Cliente:", result.get("client_id", "")),
            ("Válida hasta:", result.get("expiration_date", "")[:10])
        ]

        for label, value in info_items:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_secondary"],
                width=120,
                anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(side="left")

    def copy_to_clipboard(self, text):
        """Copiar texto al portapapeles"""
        try:
            pyperclip.copy(text)
            messagebox.showinfo("Éxito", "Código copiado al portapapeles")
        except:
            # Fallback a tkinter clipboard
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Éxito", "Código copiado al portapapeles")

    def show_list_view(self):
        """Vista para listar todas las licencias"""
        self.clear_main_frame()
        self.current_view = "list"

        # Título
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        title_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            title_frame,
            text="📋 Licencias Generadas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")

        refresh_btn = ctk.CTkButton(
            title_frame,
            text="🔄 Actualizar",
            width=120,
            height=40,
            command=self.load_licenses
        )
        refresh_btn.grid(row=0, column=1, sticky="e")

        # Frame de la tabla
        table_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["card"], corner_radius=15)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Crear Treeview con estilo
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=self.colors["dark"],
            foreground=self.colors["text"],
            fieldbackground=self.colors["dark"],
            borderwidth=0,
            font=("Segoe UI", 11),
            rowheight=35
        )
        style.configure(
            "Treeview.Heading",
            background=self.colors["secondary"],
            foreground=self.colors["text"],
            borderwidth=0,
            font=("Segoe UI", 12, "bold")
        )
        style.map("Treeview", background=[("selected", self.colors["primary"])])

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)

        # Treeview
        columns = ("ID Cliente", "Código", "Creada", "Expira", "Días", "Activaciones")
        self.licenses_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )

        scrollbar.configure(command=self.licenses_tree.yview)

        # Configurar columnas
        self.licenses_tree.heading("ID Cliente", text="ID Cliente")
        self.licenses_tree.heading("Código", text="Código de Licencia")
        self.licenses_tree.heading("Creada", text="Fecha Creación")
        self.licenses_tree.heading("Expira", text="Fecha Expiración")
        self.licenses_tree.heading("Días", text="Días")
        self.licenses_tree.heading("Activaciones", text="Activaciones")

        self.licenses_tree.column("ID Cliente", width=150)
        self.licenses_tree.column("Código", width=280)
        self.licenses_tree.column("Creada", width=120)
        self.licenses_tree.column("Expira", width=120)
        self.licenses_tree.column("Días", width=80, anchor="center")
        self.licenses_tree.column("Activaciones", width=120, anchor="center")

        self.licenses_tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Bind doble click para copiar
        self.licenses_tree.bind("<Double-1>", self.on_license_double_click)

        # Cargar licencias
        self.load_licenses()

    def load_licenses(self):
        """Cargar lista de licencias desde el servidor"""
        try:
            response = requests.get(f"{SERVER_URL}/licenses")

            if response.status_code == 200:
                licenses = response.json()

                # Limpiar tabla
                for item in self.licenses_tree.get_children():
                    self.licenses_tree.delete(item)

                # Agregar licencias
                for lic in licenses:
                    self.licenses_tree.insert("", "end", values=(
                        lic.get("client_id", ""),
                        lic.get("license_code", ""),
                        lic.get("created_at", "")[:10],
                        lic.get("expiration_date", "")[:10],
                        lic.get("duration_days", ""),
                        lic.get("activation_count", 0)
                    ))
            else:
                messagebox.showerror("Error", "No se pudieron cargar las licencias")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")

    def on_license_double_click(self, event):
        """Copiar código de licencia al hacer doble click"""
        selection = self.licenses_tree.selection()
        if selection:
            item = self.licenses_tree.item(selection[0])
            license_code = item["values"][1]
            self.copy_to_clipboard(license_code)

    def show_validate_view(self):
        """Vista para validar licencias"""
        self.clear_main_frame()
        self.current_view = "validate"

        # Título
        title = ctk.CTkLabel(
            self.main_frame,
            text="✓ Validar Licencia",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Frame del formulario
        form_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["card"], corner_radius=15)
        form_frame.grid(row=1, column=0, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)

        content = ctk.CTkFrame(form_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)

        # Código de licencia
        ctk.CTkLabel(
            content,
            text="Código de Licencia",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.validate_license_entry = ctk.CTkEntry(
            content,
            height=45,
            font=ctk.CTkFont(size=14, family="Consolas"),
            placeholder_text="LFFG-XXXX-XXXXXXXX-XXXX-XXXXXXXX"
        )
        self.validate_license_entry.pack(fill="x", pady=(0, 20))

        # PC ID
        ctk.CTkLabel(
            content,
            text="PC ID (opcional)",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.validate_pc_entry = ctk.CTkEntry(
            content,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="PC-12345"
        )
        self.validate_pc_entry.pack(fill="x", pady=(0, 30))

        # Botón validar
        validate_btn = ctk.CTkButton(
            content,
            text="✓ VALIDAR LICENCIA",
            height=60,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            command=self.validate_license
        )
        validate_btn.pack(fill="x")

        # Frame de resultado
        self.validate_result_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["dark"], corner_radius=15)
        self.validate_result_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        self.validate_result_frame.grid_remove()

    def validate_license(self):
        """Validar una licencia"""
        license_code = self.validate_license_entry.get().strip()
        pc_id = self.validate_pc_entry.get().strip() or "VALIDATION-TEST"

        if not license_code:
            messagebox.showerror("Error", "El código de licencia es requerido")
            return

        data = {
            "license_code": license_code,
            "pc_id": pc_id
        }

        try:
            response = requests.post(f"{SERVER_URL}/license/validate", json=data)
            result = response.json()

            self.show_validation_result(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")

    def show_validation_result(self, result):
        """Mostrar resultado de validación"""
        # Limpiar resultado anterior
        for widget in self.validate_result_frame.winfo_children():
            widget.destroy()

        self.validate_result_frame.grid()

        content = ctk.CTkFrame(self.validate_result_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)

        # Estado
        is_valid = result.get("valid", False)
        message = result.get("message", "")

        if is_valid:
            icon = "✅"
            color = self.colors["success"]
            status_text = "Licencia Válida"
        else:
            icon = "❌"
            color = self.colors["danger"]
            status_text = "Licencia Inválida"

        title = ctk.CTkLabel(
            content,
            text=f"{icon} {status_text}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color
        )
        title.pack(pady=(0, 10))

        message_label = ctk.CTkLabel(
            content,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"],
            wraplength=600
        )
        message_label.pack()

        # Información adicional si es válida
        if is_valid and "license_info" in result:
            info = result["license_info"]

            info_frame = ctk.CTkFrame(content, fg_color=self.colors["card"], corner_radius=10)
            info_frame.pack(fill="x", pady=(20, 0))

            info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
            info_content.pack(fill="x", padx=20, pady=15)

            info_items = [
                ("Cliente:", info.get("client_id", "")),
                ("Expira:", info.get("expiration_date", "")[:10]),
                ("Días restantes:", str(info.get("days_remaining", 0)))
            ]

            for label, value in info_items:
                row = ctk.CTkFrame(info_content, fg_color="transparent")
                row.pack(fill="x", pady=5)

                ctk.CTkLabel(
                    row,
                    text=label,
                    font=ctk.CTkFont(size=13),
                    text_color=self.colors["text_secondary"],
                    width=150,
                    anchor="w"
                ).pack(side="left")

                ctk.CTkLabel(
                    row,
                    text=value,
                    font=ctk.CTkFont(size=13, weight="bold")
                ).pack(side="left")


if __name__ == "__main__":
    app = LicenseManagerApp()
    app.mainloop()
