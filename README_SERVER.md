# 📄 PDF Print Manager - Server Architecture

**Lagudis Fresh Food Group**  
**Author:** Eng. Justo Torres  
**Email:** ghost.jgtv@gmail.com

---

## 🎯 Overview

Sistema cliente-servidor para impresión batch de PDFs con:
- ✅ Gestión centralizada de licencias
- ✅ Auto-update automático
- ✅ Tracking de actividad y trabajos de impresión
- ✅ Arquitectura similar a Warehouse_List

---

## 🏗️ Arquitectura

```
Cliente (Windows)          →  Servidor (DigitalOcean)
─────────────────────────────────────────────────────
impresion_pdf.exe              server_pdf.py
  │                              │
  ├─ Impresión PDFs              ├─ FastAPI Server (Port 8001)
  ├─ Auto-update                 ├─ SQLite Database
  ├─ Validación licencia         ├─ License Management
  └─ Tracking actividad          └─ Activity Logging
```

---

## 📁 Estructura de Archivos

### Desarrollo (Local):
```
C:\JG_Proyects\Impresion_PDFs\
├── Print_PDFs.ps1                  # Aplicación principal PowerShell
├── server_pdf.py                   # Servidor FastAPI
├── compile_pdf.bat                 # Compilar PS1 → EXE
├── publish_pdf_update.bat          # Publicar al servidor
├── installer_pdf.iss               # Inno Setup installer
├── jg-pdf-server.service           # Systemd service
├── lagudi-logo.ico                 # Icono de la app
├── lagudi-logo.png                 # Logo embebido
├── DEPLOYMENT.md                   # Guía de deployment
└── README_SERVER.md                # Este archivo
```

### Producción (Servidor):
```
/opt/lagudi/
├── server/
│   └── server_pdf.py               # FastAPI server
├── impresion_pdf/
│   ├── updates/
│   │   └── impresion_pdf.exe       # Última versión para auto-update
│   ├── installer/
│   │   └── ImpresionPDF_Setup_v1.0.exe
│   └── impresion_pdf_data.db       # SQLite database
```

---

## 🚀 Quick Start

### 1. Setup Inicial del Servidor

```bash
# SSH al servidor
ssh -i ~/.ssh/jg_server_key root@143.110.130.78

# Crear carpetas
mkdir -p /opt/lagudi/impresion_pdf/{updates,installer}
mkdir -p /opt/lagudi/server

# Instalar dependencias
pip3 install fastapi uvicorn

# Copiar server_pdf.py
# (desde tu máquina Windows con Git Bash)
scp -i ~/.ssh/jg_server_key server_pdf.py root@143.110.130.78:/opt/lagudi/server/

# Instalar servicio
scp -i ~/.ssh/jg_server_key jg-pdf-server.service root@143.110.130.78:/etc/systemd/system/
systemctl daemon-reload
systemctl enable jg-pdf-server
systemctl start jg-pdf-server

# Verificar
curl http://143.110.130.78:8001/ping
```

### 2. Compilar y Publicar

```cmd
REM En tu máquina Windows:
compile_pdf.bat           # Compila PS1 → EXE
publish_pdf_update.bat    # Sube al servidor
```

### 3. Crear Instalador

```cmd
REM Compilar con Inno Setup:
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_pdf.iss

REM Subir al servidor:
scp -i ~/.ssh/jg_server_key installer\ImpresionPDF_Setup_v1.0.exe root@143.110.130.78:/opt/lagudi/impresion_pdf/installer/
```

---

## 🔑 API Endpoints

### Health Check
```
GET /ping
```

### Licenses
```
POST /license/generate    # Generar licencia
POST /license/validate    # Validar licencia
GET  /licenses            # Listar todas las licencias
```

### Activity
```
POST /log                 # Log de actividad
GET  /activity            # Ver actividad
```

### Print Jobs
```
POST /print/log           # Registrar trabajo de impresión
GET  /print/history       # Historial de impresiones
```

### Auto-Update
```
GET /app/version          # Versión actual disponible
GET /app/download         # Descargar .exe actualizado
GET /download/installer   # Descargar instalador
```

---

## 📋 Endpoints del Servidor

| Endpoint | Puerto | Descripción |
|----------|--------|-------------|
| `/ping` | 8001 | Health check |
| `/license/generate` | 8001 | Generar licencia |
| `/license/validate` | 8001 | Validar licencia |
| `/app/version` | 8001 | Versión app |
| `/app/download` | 8001 | Descargar .exe |

---

## 🗄️ Base de Datos (SQLite)

### Tablas:

1. **licenses**
   - Códigos de licencia generados
   - Cliente, fechas, duración

2. **license_activations**
   - PCs que han activado licencias
   - Tracking de uso

3. **activity**
   - Log de actividad de usuarios
   - Acciones, timestamps

4. **print_jobs**
   - Historial de trabajos de impresión
   - Usuario, impresora, archivos, resultados

---

## 🔄 Flujo de Auto-Update

```
1. Cliente inicia → Verifica versión local
2. Consulta /app/version al servidor
3. Si hay nueva versión:
   - Descarga desde /app/download
   - Reemplaza .exe actual
   - Reinicia aplicación
```

---

## 📊 Monitoreo

```bash
# Ver logs del servidor
journalctl -u jg-pdf-server -f

# Ver licencias activas
curl http://143.110.130.78:8001/licenses | jq

# Ver actividad reciente
curl http://143.110.130.78:8001/activity | jq

# Ver trabajos de impresión
curl http://143.110.130.78:8001/print/history | jq
```

---

## 🛠️ Comandos Útiles

### Servidor:
```bash
systemctl status jg-pdf-server      # Estado
systemctl restart jg-pdf-server     # Reiniciar
systemctl stop jg-pdf-server        # Detener
journalctl -u jg-pdf-server -f      # Ver logs
```

### Base de datos:
```bash
sqlite3 /opt/lagudi/impresion_pdf/impresion_pdf_data.db
```

### Firewall:
```bash
ufw allow 8001/tcp                  # Abrir puerto
ufw status                          # Ver reglas
```

---

## 📞 Soporte

**Desarrollador:** Eng. Justo Torres  
**Email:** ghost.jgtv@gmail.com  
**Servidor:** 143.110.130.78:8001  

---

## 📖 Documentación

- [DEPLOYMENT.md](DEPLOYMENT.md) - Guía completa de deployment
- [INSTRUCTIONS.txt](pdf_print_manager/INSTRUCTIONS.txt) - Manual de usuario

---

## 🔐 Seguridad

- Licencias con HMAC-SHA256
- SECRET_KEY debe mantenerse privado
- Considerar HTTPS en producción
- Restringir acceso por IP si es posible

---

© 2026 Lagudis Fresh Food Group - All rights reserved
