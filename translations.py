"""
Multi-language support for PDF Print Manager
Author: Eng. Justo Torres
"""

TRANSLATIONS = {
    'en': {
        # Application
        'app_name': 'PDF Print Manager',
        'app_subtitle': 'Professional Batch Printing Solution',
        'version': 'Version',

        # Navigation
        'nav_queue': 'Print Queue',
        'nav_scheduler': 'Scheduler',
        'nav_history': 'History',
        'nav_settings': 'Settings',
        'nav_license': 'License',
        'nav_about': 'About',

        # Queue Page
        'queue_title': 'Print Queue',
        'queue_subtitle': 'Manage your PDF print jobs',
        'queue_add_files': '➕ Add Files',
        'queue_clear_all': '🗑️ Clear All',
        'queue_remove': '✖️ Remove',
        'queue_print_all': '🖨️ Print All',
        'queue_printer': 'Printer:',
        'queue_drag_drop_text': 'Drag & drop PDF files here or click Add Files',
        'queue_files_in_queue': 'Files in Queue',
        'queue_drag_drop': 'Drag & drop files here or use the button below',
        'queue_add_files': 'Add PDF Files',
        'queue_remove': 'Remove',
        'queue_clear_all': 'Clear All',
        'queue_print_all': 'PRINT ALL',
        'queue_printer_config': 'Printer Configuration',
        'queue_select_printer': 'Select Printer:',
        'queue_total_files': 'Total Files:',
        'queue_total_pages': 'Total Pages:',
        'queue_estimated_time': 'Estimated Time:',
        'queue_tip': 'Pro Tip',
        'queue_tip_text': 'You can schedule prints for later using the Scheduler tab',

        # Table Headers
        'table_filename': 'File Name',
        'table_path': 'Path',
        'table_pages': 'Pages',
        'table_status': 'Status',

        # Status
        'status_ready': 'Ready',
        'status_printing': 'Printing',
        'status_completed': 'Completed',
        'status_error': 'Error',
        'status_server': 'Server Status',
        'status_connected': 'Connected',
        'status_disconnected': 'Disconnected',

        # Scheduler
        'scheduler_title': 'Scheduler',
        'scheduler_subtitle': 'Schedule PDF print jobs for specific times',
        'scheduler_schedule_new': '➕ Schedule New Job',
        'scheduler_clear_completed': '🗑️ Clear Completed',
        'scheduler_job_name': 'Job Name',
        'scheduler_scheduled_time': 'Scheduled Time',
        'scheduler_files': 'Files',
        'scheduler_printer': 'Printer',
        'scheduler_status': 'Status',
        'scheduler_actions': 'Actions',
        'scheduler_cancel': 'Cancel',

        # History
        'history_title': 'Print History',
        'history_subtitle': 'View your print job history and statistics',
        'history_filter': 'Filter:',
        'history_all': 'All',
        'history_success': 'Success',
        'history_error': 'Error',
        'history_today': 'Today',
        'history_last_7_days': 'Last 7 days',
        'history_last_30_days': 'Last 30 days',
        'history_export_csv': '📊 Export CSV',
        'history_clear': '🗑️ Clear',
        'history_datetime': 'Date/Time',
        'history_filename': 'File Name',
        'history_printer': 'Printer',
        'history_pages': 'Pages',
        'history_status': 'Status',

        # Settings
        'settings_title': 'Settings',
        'settings_subtitle': 'Configure your application preferences',
        'settings_appearance': 'Appearance',
        'settings_language': 'Language:',
        'settings_theme': 'Theme:',
        'settings_dark': 'Dark',
        'settings_light': 'Light',
        'settings_english': 'English',
        'settings_spanish': 'Español',
        'settings_default_printer': 'Default Printer',
        'settings_default_printer_desc': 'Select the printer to be used by default:',
        'settings_print_settings': 'Print Settings',
        'settings_wait_time': 'Wait time between prints (seconds):',
        'settings_seconds': 'seconds',
        'settings_license': 'License',
        'settings_license_active': 'License active',
        'settings_license_inactive': 'No active license',
        'settings_renew_license': '🔑 Renew / Activate License',
        'settings_updates': 'Application Updates',
        'settings_current_version': 'Current Version:',
        'settings_check_updates': '🔍 Check for Updates',
        'settings_save': '💾 Save Settings',
        'settings_reset': '↺ Restore Defaults',

        # License
        'license_title': 'License',
        'license_subtitle': 'Manage your application license',
        'license_status': 'License Status',
        'license_active': 'License Active',
        'license_inactive': 'No Active License',
        'license_activate': '🔑 Activate New License',
        'license_refresh': '🔄 Refresh Status',
        'license_pc_info': 'PC Information',
        'license_pc_id': 'PC ID:',
        'license_pc_desc': 'Use this PC ID when requesting a license',
        'license_need': 'Need a License?',
        'license_contact': 'Contact:',
        'license_expires': 'Expires:',
        'license_days_remaining': 'Days Remaining:',
        'license_please_activate': 'Please activate a license to use this application',

        # About
        'about_title': 'About',
        'about_subtitle': 'Application information and credits',
        'about_app_name': 'PDF Print Manager',
        'about_version': 'Version 1.0.0',
        'about_description': 'Professional batch printing solution for managing PDF print jobs efficiently',
        'about_developer': 'Developer',
        'about_copyright': '© 2026 Eng. Justo Torres. All rights reserved.',

        # Buttons
        'btn_ok': 'OK',
        'btn_cancel': 'Cancel',
        'btn_apply': 'Apply',
        'btn_close': 'Close',
        'btn_save': 'Save',
        'btn_delete': 'Delete',
        'btn_edit': 'Edit',
        'btn_refresh': 'Refresh',
        'btn_export': 'Export',
        'btn_import': 'Import',
        'btn_print_action': 'Print',

        # Messages
        'msg_success': 'Success',
        'msg_error': 'Error',
        'msg_warning': 'Warning',
        'msg_info': 'Information',

        # Placeholders
        'placeholder_coming_soon': 'This feature is coming soon',
        'placeholder_in_development': 'Feature in development',
    },

    'es': {
        # Application
        'app_name': 'Gestor de Impresión PDF',
        'app_subtitle': 'Solución Profesional de Impresión por Lotes',
        'version': 'Versión',

        # Navigation
        'nav_queue': 'Cola de Impresión',
        'nav_scheduler': 'Programador',
        'nav_history': 'Historial',
        'nav_settings': 'Configuración',
        'nav_license': 'Licencia',
        'nav_about': 'Acerca de',

        # Queue Page
        'queue_title': 'Cola de Impresión',
        'queue_subtitle': 'Gestiona tus trabajos de impresión PDF',
        'queue_add_files': '➕ Agregar Archivos',
        'queue_clear_all': '🗑️ Limpiar Todo',
        'queue_remove': '✖️ Remover',
        'queue_print_all': '🖨️ Imprimir Todo',
        'queue_printer': 'Impresora:',
        'queue_drag_drop_text': 'Arrastra archivos PDF aquí o haz clic en Agregar Archivos',
        'queue_files_in_queue': 'Archivos en Cola',
        'queue_drag_drop': 'Arrastra archivos aquí o usa el botón',
        'queue_add_files': 'Agregar PDFs',
        'queue_remove': 'Remover',
        'queue_clear_all': 'Limpiar Todo',
        'queue_print_all': 'IMPRIMIR TODO',
        'queue_printer_config': 'Configuración de Impresora',
        'queue_select_printer': 'Seleccionar Impresora:',
        'queue_total_files': 'Total de Archivos:',
        'queue_total_pages': 'Páginas Totales:',
        'queue_estimated_time': 'Tiempo Estimado:',
        'queue_tip': 'Consejo Profesional',
        'queue_tip_text': 'Puedes programar impresiones para más tarde usando la pestaña Programador',

        # Table Headers
        'table_filename': 'Nombre del Archivo',
        'table_path': 'Ruta',
        'table_pages': 'Páginas',
        'table_status': 'Estado',

        # Status
        'status_ready': 'Listo',
        'status_printing': 'Imprimiendo',
        'status_completed': 'Completado',
        'status_error': 'Error',
        'status_server': 'Estado del Servidor',
        'status_connected': 'Conectado',
        'status_disconnected': 'Desconectado',

        # Scheduler
        'scheduler_title': 'Programador',
        'scheduler_subtitle': 'Programa trabajos de impresión PDF para momentos específicos',
        'scheduler_schedule_new': '➕ Programar Nuevo Trabajo',
        'scheduler_clear_completed': '🗑️ Limpiar Completados',
        'scheduler_job_name': 'Nombre del Trabajo',
        'scheduler_scheduled_time': 'Hora Programada',
        'scheduler_files': 'Archivos',
        'scheduler_printer': 'Impresora',
        'scheduler_status': 'Estado',
        'scheduler_actions': 'Acciones',
        'scheduler_cancel': 'Cancelar',

        # History
        'history_title': 'Historial de Impresión',
        'history_subtitle': 'Visualiza el historial de trabajos de impresión y estadísticas',
        'history_filter': 'Filtro:',
        'history_all': 'Todos',
        'history_success': 'Éxito',
        'history_error': 'Error',
        'history_today': 'Hoy',
        'history_last_7_days': 'Últimos 7 días',
        'history_last_30_days': 'Últimos 30 días',
        'history_export_csv': '📊 Exportar CSV',
        'history_clear': '🗑️ Limpiar',
        'history_datetime': 'Fecha/Hora',
        'history_filename': 'Nombre del Archivo',
        'history_printer': 'Impresora',
        'history_pages': 'Páginas',
        'history_status': 'Estado',

        # Settings
        'settings_title': 'Configuración',
        'settings_subtitle': 'Configura las preferencias de tu aplicación',
        'settings_appearance': 'Apariencia',
        'settings_language': 'Idioma:',
        'settings_theme': 'Tema:',
        'settings_dark': 'Oscuro',
        'settings_light': 'Claro',
        'settings_english': 'English',
        'settings_spanish': 'Español',
        'settings_default_printer': 'Impresora Predeterminada',
        'settings_default_printer_desc': 'Selecciona la impresora que se usará por defecto:',
        'settings_print_settings': 'Configuración de Impresión',
        'settings_wait_time': 'Tiempo de espera entre impresiones (segundos):',
        'settings_seconds': 'segundos',
        'settings_license': 'Licencia',
        'settings_license_active': 'Licencia activa',
        'settings_license_inactive': 'Sin licencia activa',
        'settings_renew_license': '🔑 Renovar / Activar Licencia',
        'settings_updates': 'Actualizaciones de la Aplicación',
        'settings_current_version': 'Versión Actual:',
        'settings_check_updates': '🔍 Buscar Actualizaciones',
        'settings_save': '💾 Guardar Configuración',
        'settings_reset': '↺ Restaurar Valores',

        # License
        'license_title': 'Licencia',
        'license_subtitle': 'Gestiona tu licencia de aplicación',
        'license_status': 'Estado de Licencia',
        'license_active': 'Licencia Activa',
        'license_inactive': 'Sin Licencia Activa',
        'license_activate': '🔑 Activar Nueva Licencia',
        'license_refresh': '🔄 Actualizar Estado',
        'license_pc_info': 'Información del PC',
        'license_pc_id': 'ID del PC:',
        'license_pc_desc': 'Usa este ID del PC al solicitar una licencia',
        'license_need': '¿Necesitas una Licencia?',
        'license_contact': 'Contacto:',
        'license_expires': 'Expira:',
        'license_days_remaining': 'Días Restantes:',
        'license_please_activate': 'Por favor activa una licencia para usar esta aplicación',

        # About
        'about_title': 'Acerca de',
        'about_subtitle': 'Información de la aplicación y créditos',
        'about_app_name': 'Gestor de Impresión PDF',
        'about_version': 'Versión 1.0.0',
        'about_description': 'Solución profesional de impresión por lotes para gestionar trabajos de impresión PDF eficientemente',
        'about_developer': 'Desarrollador',
        'about_copyright': '© 2026 Ing. Justo Torres. Todos los derechos reservados.',

        # Buttons
        'btn_ok': 'Aceptar',
        'btn_cancel': 'Cancelar',
        'btn_apply': 'Aplicar',
        'btn_close': 'Cerrar',
        'btn_save': 'Guardar',
        'btn_delete': 'Eliminar',
        'btn_edit': 'Editar',
        'btn_refresh': 'Actualizar',
        'btn_export': 'Exportar',
        'btn_import': 'Importar',
        'btn_print_action': 'Imprimir',

        # Messages
        'msg_success': 'Éxito',
        'msg_error': 'Error',
        'msg_warning': 'Advertencia',
        'msg_info': 'Información',

        # Placeholders
        'placeholder_coming_soon': 'Esta función estará disponible pronto',
        'placeholder_in_development': 'Función en desarrollo',
    }
}


class Translator:
    """Handle application translations"""

    def __init__(self, language='en'):
        self.language = language

    def set_language(self, language):
        """Change current language"""
        if language in TRANSLATIONS:
            self.language = language
            return True
        return False

    def get(self, key, language=None):
        """Get translated text"""
        lang = language or self.language
        return TRANSLATIONS.get(lang, {}).get(key, key)

    def __call__(self, key):
        """Shortcut for get()"""
        return self.get(key)


# Global translator instance
translator = Translator('en')
t = translator  # Shortcut
