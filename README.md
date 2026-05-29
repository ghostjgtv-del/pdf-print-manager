# 📄 PDF Print Manager

Sistema cliente-servidor para impresión batch de PDFs con gestión centralizada de licencias y auto-update.

**Lagudis Fresh Food Group**  
**Desarrollado por:** Eng. Justo Torres (ghost.jgtv@gmail.com)

---

## 🏗️ Arquitectura

```
Cliente (Windows)              Servidor (DigitalOcean)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PDF_Print_Manager.exe     →    server_pdf.py
  │                              │
  ├─ Impresión PDFs              ├─ FastAPI Server (Puerto 8001)
  ├─ Auto-update                 ├─ SQLite Database
  ├─ Validación licencia         ├─ License Management
  └─ Tracking actividad          └─ Activity Logging
```

**Servidor:** 143.110.130.78:8001

---

## 📁 Estructura del Proyecto

```
C:\JG_Proyects\Impresion_PDFs\
│
├── 📱 Aplicación Cliente
│   ├── main.py                    # Punto de entrada
│   ├── app.py                     # Ventana principal
│   ├── updater.py                 # Sistema de auto-update
│   │
│   ├── core/                      # Lógica de negocio
│   │   ├── printer.py             # Gestión de impresoras
│   │   ├── history.py             # Historial de trabajos
│   │   └── scheduler.py           # Programación de tareas
│   │
│   ├── ui/                        # Interfaz de usuario
│   │   ├── tab_queue.py           # Cola de impresión
│   │   ├── tab_history.py         # Historial
│   │   ├── tab_scheduler.py       # Programador
│   │   ├── tab_settings.py        # Configuración
│   │   └── sidebar.py             # Barra lateral
│   │
│   └── license/                   # Sistema de licencias
│       ├── license_manager.py     # Validación con servidor
│       └── license_window.py      # UI de activación
│
├── 🔧 Herramientas
│   ├── server_pdf.py              # Servidor FastAPI
│   ├── license_manager.py         # Generador de licencias
│   │
│   ├── compile_app.bat            # Compilar aplicación
│   ├── compile_license_manager.bat # Compilar generador
│   ├── publish_app.bat            # Publicar al servidor
│   │
│   └── installer_pdf.iss          # Instalador Inno Setup
│
├── 📦 Ejecutables
│   └── dist/
│       ├── PDF_Print_Manager.exe  # Aplicación (36 MB)
│       └── Lagudi_License_Manager.exe # Generador (35 MB)
│
├── 📚 Documentación
│   ├── README.md                  # Este archivo
│   ├── DEPLOYMENT.md              # Guía de deployment
│   ├── SETUP_POWERSHELL.md        # Guía PowerShell
│   └── SETUP_CHECKLIST.md         # Checklist de setup
│
└── 🔧 Configuración
    ├── requirements.txt           # Dependencias Python
    ├── .gitignore                 # Archivos ignorados
    └── jg-pdf-server.service      # Servicio systemd
```

---

## 🚀 Quick Start

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

### Compilar Aplicación

```bash
# Compilar PDF Print Manager
.\compile_app.bat

# Compilar License Manager
.\compile_license_manager.bat
```

### Deployment al Servidor

```bash
# Publicar actualización
.\publish_app.bat

# O manualmente:
scp -i ~/.ssh/jg_server_key dist/PDF_Print_Manager.exe root@143.110.130.78:/opt/lagudi/impresion_pdf/updates/impresion_pdf.exe
```

---

## 🔑 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/ping` | GET | Health check |
| `/license/generate` | POST | Generar licencia |
| `/license/validate` | POST | Validar licencia |
| `/licenses` | GET | Listar licencias |
| `/app/version` | GET | Versión disponible |
| `/app/download` | GET | Descargar .exe |
| `/download/installer` | GET | Descargar instalador |
| `/log` | POST | Log de actividad |
| `/activity` | GET | Ver actividad |
| `/print/log` | POST | Registrar impresión |
| `/print/history` | GET | Historial de impresiones |

---

## 📦 Instalación del Servidor

Ver guía completa en [DEPLOYMENT.md](DEPLOYMENT.md)

**Instalación rápida:**

```bash
# Clonar repo en el servidor
cd /opt/lagudi
git clone https://github.com/ghostjgtv-del/pdf-print-manager.git

# Instalar dependencias
pip3 install --break-system-packages fastapi uvicorn[standard] python-multipart

# Configurar servicio
cd pdf-print-manager
cp jg-pdf-server.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable jg-pdf-server
systemctl start jg-pdf-server

# Crear estructura de carpetas
mkdir -p /opt/lagudi/impresion_pdf/{updates,installer}

# Abrir puerto
ufw allow 8001/tcp
ufw reload
```

---

## 🔄 Flujo de Trabajo

### Actualizar aplicación:

1. Editar código en `core/`, `ui/`, etc.
2. Compilar: `.\compile_app.bat`
3. Publicar: `.\publish_app.bat`
4. Commit y push a GitHub
5. Pull en servidor y restart servicio

### Generar licencia:

1. Ejecutar: `dist\Lagudi_License_Manager.exe`
2. Llenar formulario
3. Copiar código generado
4. Entregar a cliente

---

## 🧪 Testing

```bash
# Health check
curl http://143.110.130.78:8001/ping

# Ver versión
curl http://143.110.130.78:8001/app/version

# Ver logs del servidor
ssh -i ~/.ssh/jg_server_key root@143.110.130.78
journalctl -u jg-pdf-server -f
```

---

## 🔐 Seguridad

- Licencias validadas con HMAC-SHA256
- `SECRET_KEY` debe mantenerse privado
- Considerar HTTPS en producción
- Restringir acceso por IP si es posible

---

## 📞 Contacto

**Desarrollador:** Eng. Justo Torres  
**Email:** ghost.jgtv@gmail.com  
**Empresa:** Lagudis Fresh Food Group  
**Servidor:** 143.110.130.78:8001  
**GitHub:** https://github.com/ghostjgtv-del/pdf-print-manager

---

© 2026 Lagudis Fresh Food Group
