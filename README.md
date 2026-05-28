# 📄 PDF Print Manager

Sistema cliente-servidor para impresión batch de PDFs con gestión centralizada de licencias y auto-update.

**Lagudis Fresh Food Group**  
**Desarrollado por:** Eng. Justo Torres (ghost.jgtv@gmail.com)

---

## 🏗️ Arquitectura

```
Cliente (Windows)              Servidor (DigitalOcean)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
impresion_pdf.exe         →    server_pdf.py
  │                              │
  ├─ Impresión PDFs              ├─ FastAPI Server (Puerto 8001)
  ├─ Auto-update                 ├─ SQLite Database
  ├─ Validación licencia         ├─ License Management
  └─ Tracking actividad          └─ Activity Logging
```

**Servidor:** 143.110.130.78:8001

---

## 🚀 Quick Start

### Desarrollo Local

```bash
# Compilar aplicación
.\compile_pdf.bat

# Publicar al servidor
.\publish_pdf_update.bat

# Crear instalador
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_pdf.iss
```

### Deployment al Servidor

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones completas de setup del servidor.

```bash
# SSH al servidor
ssh -i ~/.ssh/jg_server_key root@143.110.130.78

# Pull de actualizaciones
cd /opt/lagudi/server
git pull origin main

# Restart servicio
systemctl restart jg-pdf-server
```

---

## 📁 Estructura del Proyecto

```
.
├── server_pdf.py              # FastAPI server backend
├── Print_PDFs.ps1             # Aplicación cliente PowerShell
├── compile_pdf.bat            # Compilar PS1 → EXE
├── publish_pdf_update.bat     # Publicar al servidor
├── installer_pdf.iss          # Inno Setup installer script
├── jg-pdf-server.service      # Systemd service
├── lagudi-logo.ico            # Icono de la aplicación
├── DEPLOYMENT.md              # Guía completa de deployment
├── SETUP_POWERSHELL.md        # Guía para PowerShell
└── README_SERVER.md           # Documentación de arquitectura
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

**Requisitos:**
- Ubuntu 20.04+ / Debian 11+
- Python 3.10+
- Puerto 8001 abierto

**Instalación rápida:**
```bash
# Clonar repo en el servidor
cd /opt/lagudi/server
git clone <repo-url> .

# Instalar dependencias
pip3 install --break-system-packages fastapi uvicorn[standard] python-multipart

# Configurar servicio
cp jg-pdf-server.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable jg-pdf-server
systemctl start jg-pdf-server

# Abrir puerto
ufw allow 8001/tcp
ufw reload
```

---

## 🔄 Flujo de Trabajo

### Actualizar aplicación:

1. Editar `Print_PDFs.ps1`
2. Incrementar versión
3. Commit y push a GitHub
4. Compilar: `.\compile_pdf.bat`
5. Publicar: `.\publish_pdf_update.bat`
6. Actualizar `APP_VERSION` en `server_pdf.py`
7. Commit, push y pull en servidor
8. Restart: `systemctl restart jg-pdf-server`

### Actualizar solo el servidor:

1. Editar `server_pdf.py`
2. Commit y push a GitHub
3. En el servidor:
   ```bash
   cd /opt/lagudi/server
   git pull origin main
   systemctl restart jg-pdf-server
   ```

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

---

© 2026 Lagudis Fresh Food Group
