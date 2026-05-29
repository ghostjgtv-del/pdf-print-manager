# 📦 Build Instructions - PDF Print Manager

## Método 1: Usar el script automático (RECOMENDADO)

### ✅ Más fácil y rápido

1. **Doble clic** en `build_exe.bat`
2. Espera a que termine (1-3 minutos)
3. El .exe estará en la carpeta `dist\`

```
dist\
└── PDF_Print_Manager.exe  ← Aquí está tu ejecutable
```

---

## Método 2: Comando manual simple

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
pyinstaller --onefile --windowed --name="PDF_Print_Manager" pdf_print_manager/main.py
```

---

## Método 3: Usando el archivo .spec (avanzado)

Si necesitas más control:

```bash
pyinstaller PDF_Print_Manager.spec
```

---

## 📋 Requisitos previos

- Python 3.10 o superior
- PyInstaller instalado: `pip install pyinstaller`
- Todas las dependencias instaladas: `pip install -r pdf_print_manager/requirements.txt`

---

## 🎯 Resultado esperado

Después de compilar:

```
dist\
└── PDF_Print_Manager.exe  (aproximadamente 50-80 MB)
```

### El .exe incluye:
- ✅ Python embebido
- ✅ Todas las librerías (customtkinter, pywin32, PyPDF2, etc.)
- ✅ Tu código de aplicación
- ✅ Todo lo necesario para funcionar

### NO incluye:
- ❌ Settings del usuario (se crean al usar la app)
- ❌ Licencias (cada usuario activa la suya)

---

## 🚀 Distribución

### Para distribuir a usuarios:

1. **Copia** `PDF_Print_Manager.exe` de la carpeta `dist\`
2. **Envía** el .exe + el archivo de licencia
3. **Instrucciones** para el usuario:
   - Ejecutar el .exe
   - Activar con el código de licencia
   - ¡Listo!

### Ubicación de datos en la máquina del usuario:

```
C:\Users\[usuario]\.pdf_print_manager\
├── settings.json      (configuración)
└── .license.dat       (licencia encriptada)
```

---

## ⚙️ Opciones adicionales

### Agregar ícono personalizado:

1. Coloca `icon.ico` en la raíz del proyecto
2. Usa: `pyinstaller --icon=icon.ico ...`

### Crear instalador:

Usa **Inno Setup** o **NSIS** para crear un instalador profesional.

---

## 🐛 Solución de problemas

### Error: "Module not found"
```bash
pip install -r pdf_print_manager/requirements.txt
```

### El .exe es muy grande
- Normal: 50-80 MB es esperado
- Incluye Python + todas las librerías
- Para reducir: usa `--onedir` en lugar de `--onefile`

### Error al ejecutar el .exe
- Verifica que todas las dependencias estén en requirements.txt
- Prueba en modo `--console` para ver errores

---

## 📞 Soporte

**Desarrollador:** Eng. Justo Torres  
**Empresa:** Lagudis Fresh Food Group  
**Email:** ghost.jgtv@gmail.com

---

© 2026 Lagudis Fresh Food Group - All rights reserved
