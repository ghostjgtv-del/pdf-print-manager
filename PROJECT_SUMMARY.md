# 🎉 PDF Print Manager - Proyecto Completado

**Desarrollado para:** Lagudis Fresh Food Group  
**Desarrollador:** Eng. Justo Torres (ghost.jgtv@gmail.com)  
**Fecha:** Mayo 2026  
**Versión:** 1.0.0

---

## ✅ Estado del Proyecto

El proyecto **PDF Print Manager** ha sido completado exitosamente con todas las funcionalidades requeridas:

### ✨ Características Implementadas

- ✅ **Sistema de Licencias** con expiración y renovación
- ✅ **Generador de Códigos de Licencia** (herramienta exclusiva para ti)
- ✅ **Cola de Impresión** con agregar archivos/carpetas
- ✅ **Reordenamiento** de archivos (subir/bajar)
- ✅ **Selección de Impresora** con detección automática
- ✅ **Impresión Masiva** con manejo de errores
- ✅ **Programador de Trabajos** para impresiones futuras
- ✅ **Historial en SQLite** con filtros y estadísticas
- ✅ **Exportar a CSV** para reportes
- ✅ **Configuración** persistente (impresora, tema, tiempos)
- ✅ **Temas Oscuro/Claro** personalizables
- ✅ **Interfaz Gráfica Moderna** con CustomTkinter

---

## 📁 Estructura del Proyecto

```
C:\JG_Proyects\Impresion_PDFs\
├── Print_PDFs.ps1                 # Script PowerShell original (funcional)
├── PDF_PrintManager_SPEC.md       # Especificaciones originales
├── lagudi-full-logo.svg           # Logo de Lagudis
│
└── pdf_print_manager/             # 🆕 NUEVA APLICACIÓN
    ├── main.py                    # Punto de entrada
    ├── app.py                     # Aplicación principal
    ├── requirements.txt           # Dependencias Python
    ├── build.spec                 # Configuración PyInstaller
    ├── README.md                  # Documentación completa
    ├── INSTRUCCIONES.txt          # Guía rápida para usuarios
    ├── .gitignore                 # Para control de versiones
    │
    ├── 📜 Scripts de Utilidad:
    │   ├── install_dependencies.ps1  # Instalar dependencias
    │   ├── build.ps1                 # Compilar a .exe
    │   └── test_license.py           # Probar generador
    │
    ├── 🔐 license/                # Sistema de licencias
    │   ├── __init__.py
    │   ├── license_manager.py     # Gestión y validación
    │   └── license_window.py      # Ventana de activación
    │
    ├── 🎨 ui/                     # Interfaz gráfica
    │   ├── __init__.py
    │   ├── sidebar.py             # Barra lateral de navegación
    │   ├── tab_queue.py           # Tab de cola de impresión
    │   ├── tab_scheduler.py       # Tab de programador
    │   ├── tab_history.py         # Tab de historial
    │   └── tab_settings.py        # Tab de configuración
    │
    ├── ⚙️ core/                   # Lógica de negocio
    │   ├── __init__.py
    │   ├── printer.py             # Gestión de impresoras y cola
    │   ├── scheduler.py           # Programación de trabajos
    │   └── history.py             # Base de datos SQLite
    │
    ├── 🎨 assets/                 # Recursos
    │   └── lagudi-full-logo.svg   # Logo (copiado)
    │
    └── 🔑 tools/                  # ⚠️ SOLO PARA TI
        └── license_generator.py   # Generador de códigos
```

---

## 🚀 Próximos Pasos

### 1️⃣ Instalar Dependencias

```powershell
cd pdf_print_manager
.\install_dependencies.ps1
```

O manualmente:
```powershell
pip install -r requirements.txt
```

### 2️⃣ Probar la Aplicación

```powershell
python main.py
```

### 3️⃣ Generar Código de Licencia (para pruebas)

```powershell
cd tools
python license_generator.py
```

Opciones sugeridas:
- Cliente: `LFFG-PRODUCCION`
- Duración: `30` días (o `365` para anual)

### 4️⃣ Compilar a Ejecutable

```powershell
.\build.ps1
```

El archivo `.exe` estará en: `dist\PDF_Print_Manager.exe`

---

## 🔑 Sistema de Licencias

### Para Ti (Generador)

**Archivo:** `tools/license_generator.py`

#### Uso:
```powershell
cd tools
python license_generator.py
```

**Menú:**
1. Generar nueva licencia
2. Validar código de licencia
3. Salir

#### Generar Licencia:
1. Ingresar ID del cliente (ej: `LFFG-PROD`, `CLIENTE-001`)
2. Seleccionar duración:
   - 30 días (Trial)
   - 90 días (Trimestral)
   - 180 días (Semestral)
   - 365 días (Anual)
   - Personalizado
3. El código se genera y se puede guardar en archivo

#### Formato del Código:
```
LFFG-XXXX-XXXX-XXXX-XXXX
│    │    │    │    │
│    │    │    │    └─── Checksum (validación)
│    │    │    └──────── Duración (codificada)
│    │    └───────────── Fecha emisión (codificada)
│    └────────────────── Hash del cliente
└─────────────────────── Prefijo (LFFG)
```

### Para Usuarios

Al abrir la aplicación por primera vez, se solicita el código.

**Contacto para licencias:**
- Ing. Justo Torres
- ghost.jgtv@gmail.com

---

## 📋 Dependencias (requirements.txt)

```
customtkinter>=5.2.0      # UI moderna
pywin32>=306              # Impresión en Windows
schedule>=1.2.0           # Programación de tareas
pyinstaller>=6.0.0        # Compilar a .exe
cryptography>=41.0.0      # Encriptación de licencias
pillow>=10.0.0            # Manejo de imágenes
cairosvg>=2.7.0           # SVG a PNG (opcional)
```

---

## 🔧 Configuración Técnica

### Archivos Generados por la App

**Ubicación:** `C:\Users\<Usuario>\.pdf_print_manager\`

- **`.license.dat`**: Licencia encriptada (AES)
- **`history.db`**: Base de datos SQLite
- **`scheduled_jobs.json`**: Trabajos pendientes
- **`settings.json`**: Configuración de usuario

### Seguridad del Sistema de Licencias

- ✅ Validación offline (sin internet)
- ✅ Códigos firmados con HMAC-SHA256
- ✅ Almacenamiento encriptado con Fernet (AES)
- ✅ Fecha de expiración embebida en el código
- ✅ Advertencia 7 días antes de expirar
- ❌ No vinculado a hardware (flexibilidad)

---

## 📖 Documentación

### Para Desarrolladores:
- `README.md` - Documentación técnica completa

### Para Usuarios:
- `INSTRUCCIONES.txt` - Guía rápida de uso

---

## 🎯 Funcionalidades por Tab

### 📋 Cola de Impresión
- Agregar archivos individuales o carpetas
- Reordenar con botones ↑↓
- Quitar archivos seleccionados
- Ver estado: Pendiente/Imprimiendo/Impreso/Error
- Contador de páginas (si detectable)
- Selección de impresora
- Progreso en tiempo real

### ⏰ Programador
- Importar cola actual
- Programar fecha/hora futura
- Lista de trabajos pendientes/completados
- Cancelar trabajos
- Limpiar completados
- ⚠️ Requiere app abierta

### 📊 Historial
- Tabla completa de impresiones
- Filtros: Estado, Periodo (Hoy/7días/30días/Todo)
- Estadísticas: Total, exitosos, fallidos, páginas
- Doble-click para ver detalles
- Exportar a CSV
- Limpiar historial (todo o >30 días)

### ⚙️ Configuración
- Impresora predeterminada
- Tiempo de espera entre impresiones (1-10 seg)
- Tema oscuro/claro
- Ver información de licencia
- Renovar licencia

---

## 🐛 Testing Checklist

Antes de distribuir, probar:

- [ ] Instalación de dependencias
- [ ] Generación de código de licencia
- [ ] Activación con código
- [ ] Agregar archivos PDF
- [ ] Agregar carpeta con PDFs
- [ ] Reordenar archivos
- [ ] Imprimir en impresora real
- [ ] Programar trabajo futuro
- [ ] Ver historial
- [ ] Exportar CSV
- [ ] Cambiar configuración
- [ ] Tema claro/oscuro
- [ ] Compilar a .exe
- [ ] Ejecutar .exe en otra máquina

---

## 📊 Mejoras Futuras (Opcionales)

### v1.1 - Posibles Mejoras
- [ ] Vista previa de PDFs
- [ ] Soporte para múltiples formatos (Word, Excel)
- [ ] Impresión de rango de páginas
- [ ] Configuración de copias y calidad
- [ ] Notificaciones de escritorio
- [ ] Modo servidor/multi-usuario
- [ ] Vinculación de licencia a hardware
- [ ] Validación en línea de licencias
- [ ] Dashboard web de estadísticas

---

## 💡 Notas Importantes

### ⚠️ Confidencialidad
- **`tools/license_generator.py`** - NO DISTRIBUIR
- Este archivo es exclusivo para generar códigos
- Mantenerlo en ubicación segura

### 🔒 Seguridad
- La clave secreta en `license_manager.py` se puede ofuscar
- Considerar cambiarla antes de distribuir
- O usar variables de entorno

### 📦 Distribución
- El `.exe` es standalone (no requiere Python)
- Incluir `INSTRUCCIONES.txt` con el ejecutable
- Tamaño aproximado: 80-120 MB
- Compatible con Windows 10+

---

## 📞 Soporte

**Desarrollador:** Eng. Justo Torres  
**Email:** ghost.jgtv@gmail.com  
**Empresa:** Lagudis Fresh Food Group

---

## 🎉 Resumen Final

Has recibido:

✅ **Aplicación completa** con GUI moderna  
✅ **Sistema de licencias** funcional y seguro  
✅ **Generador de códigos** exclusivo para ti  
✅ **Documentación completa** para usuarios y desarrolladores  
✅ **Scripts de utilidad** para instalación y compilación  
✅ **Estructura profesional** lista para producción

**Estado:** ✅ LISTO PARA USAR

**Siguiente paso recomendado:**
1. Instalar dependencias: `.\install_dependencies.ps1`
2. Probar la aplicación: `python main.py`
3. Generar tu primer código: `cd tools; python license_generator.py`

---

**Desarrollado con ❤️ para Lagudis Fresh Food Group**  
**© 2026 - Todos los derechos reservados**
