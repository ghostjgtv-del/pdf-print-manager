"""
Script para aplicar traducciones y colores adaptativos a todas las páginas
"""

import re
from pathlib import Path

def fix_page_titles(content, page_key):
    """Reemplaza títulos hardcodeados con objectNames y traducciones"""

    # Patrones comunes para títulos
    patterns = [
        (r'title = QLabel\("(.+?)"\)\s*title\.setStyleSheet\("color: #FFFFFF',
         f'self.title_label = QLabel(t("{page_key}_title"))\n        self.title_label.setObjectName("pageTitle")'),

        (r'subtitle = QLabel\("(.+?)"\)\s*subtitle\.setStyleSheet\("color: #94A3B8',
         f'self.subtitle_label = QLabel(t("{page_key}_subtitle"))\n        self.subtitle_label.setObjectName("pageSubtitle")'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Fix addWidget references
    content = content.replace('title_layout.addWidget(title)', 'title_layout.addWidget(self.title_label)')
    content = content.replace('title_section.addWidget(title)', 'title_section.addWidget(self.title_label)')
    content = content.replace('layout.addWidget(title)', 'layout.addWidget(self.title_label)')

    content = content.replace('title_layout.addWidget(subtitle)', 'title_layout.addWidget(self.subtitle_label)')
    content = content.replace('title_section.addWidget(subtitle)', 'title_section.addWidget(self.subtitle_label)')
    content = content.replace('layout.addWidget(subtitle)', 'layout.addWidget(self.subtitle_label)')

    return content

def add_update_texts_method(content, update_code):
    """Agrega método update_texts si no existe"""
    if 'def update_texts(self):' in content:
        return content

    # Buscar def animate_in y agregar update_texts antes
    animate_pattern = r'(\s+def animate_in\(self\):.*?pass)'
    replacement = f'{update_code}\n\n\\1'
    content = re.sub(animate_pattern, replacement, content, flags=re.DOTALL)

    return content

# Lista de páginas para actualizar
pages_to_fix = {
    'tab_history_pyqt.py': {
        'key': 'history',
        'update_texts': '''    def update_texts(self):
        """Update all text labels when language changes"""
        if hasattr(self, 'title_label'):
            self.title_label.setText("📊 " + t("history_title"))
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(t("history_subtitle"))'''
    },
    'tab_settings_pyqt.py': {
        'key': 'settings',
        'update_texts': '''    def update_texts(self):
        """Update all text labels when language changes"""
        # Rebuild page for Settings
        container = self.widget()
        if container:
            container.deleteLater()
        self.setup_ui()'''
    },
    'tab_license_pyqt.py': {
        'key': 'license',
        'update_texts': '''    def update_texts(self):
        """Update all text labels when language changes"""
        # Rebuild page for License
        self.refresh_status()'''
    },
    'tab_about_pyqt.py': {
        'key': 'about',
        'update_texts': '''    def update_texts(self):
        """Update all text labels when language changes"""
        # Rebuild page for About
        container = self.widget()
        if container:
            container.deleteLater()
        self.setup_ui()'''
    }
}

ui_dir = Path('C:/JG_Proyects/Impresion_PDFs/ui')

for filename, config in pages_to_fix.items():
    file_path = ui_dir / filename
    if not file_path.exists():
        print(f"Skipping {filename} - file not found")
        continue

    print(f"Processing {filename}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Aplicar fixes
    content = fix_page_titles(content, config['key'])
    content = add_update_texts_method(content, config['update_texts'])

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Updated {filename}")

print("\n✅ All pages updated!")
