# 🚀 PDF Print Manager - Deployment Guide

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Windows)                         │
├─────────────────────────────────────────────────────────────┤
│  impresion_pdf.exe                                          │
│  - PowerShell compilado a EXE                               │
│  - Auto-update desde servidor                               │
│  - Validación de licencia con servidor                     │
│  - Impresión batch de PDFs                                  │
│  - Tracking de actividad                                    │
└─────────────────────────────────────────────────────────────┘
                             ↕ HTTP (Port 8001)
┌─────────────────────────────────────────────────────────────┐
│        SERVIDOR (DigitalOcean - 143.110.130.78)             │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Server (server_pdf.py)                             │
│  - Gestión de licencias                                     │
│  - Sistema de auto-update                                   │
│  - Log de actividad                                         │
│  - Tracking de trabajos de impresión                        │
│                                                              │
│  SQLite Database                                            │
│  - licenses (códigos de licencia)                           │
│  - license_activations (PCs activados)                      │
│  - activity (log de acciones)                               │
│  - print_jobs (historial de impresiones)                    │
│                                                              │
│  File Storage                                               │
│  - /opt/lagudi/impresion_pdf/updates/                       │
│    └── impresion_pdf.exe (última versión)                   │
│  - /opt/lagudi/impresion_pdf/installer/                     │
│    └── ImpresionPDF_Setup_v1.0.exe                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Requisitos Previos

### En tu máquina de desarrollo (Windows):
- PowerShell 5.1 o superior
- Módulo ps2exe: `Install-Module ps2exe -Scope CurrentUser`
- Python 3.10+ (para server_pdf.py)
- FastAPI: `pip install fastapi uvicorn`
- Git Bash (para scp)
- SSH configurado con llave privada para DigitalOcean
- Inno Setup (para crear instalador)

### En el servidor DigitalOcean:
- Ubuntu 20.04+ o Debian 11+
- Python 3.10+
- Acceso root o sudo
- Puerto 8001 abierto en firewall

---

## 🛠️ Setup Inicial del Servidor

### 1. Conectar al servidor

```bash
ssh -i ~/.ssh/jg_server_key root@143.110.130.78
```

### 2. Crear estructura de carpetas

```bash
mkdir -p /opt/lagudi/impresion_pdf/{updates,installer}
mkdir -p /opt/lagudi/server
```

### 3. Instalar dependencias Python

```bash
apt update
apt install -y python3 python3-pip python3-venv
pip3 install fastapi uvicorn[standard] python-multipart
```

### 4. Copiar server_pdf.py al servidor

```bash
# Desde tu máquina Windows (Git Bash):
scp -i ~/.ssh/jg_server_key server_pdf.py root@143.110.130.78:/opt/lagudi/server/
```

### 5. Instalar y configurar el servicio systemd

```bash
# Copiar archivo de servicio
scp -i ~/.ssh/jg_server_key jg-pdf-server.service root@143.110.130.78:/etc/systemd/system/

# En el servidor:
systemctl daemon-reload
systemctl enable jg-pdf-server
systemctl start jg-pdf-server
```

### 6. Verificar que el servicio está corriendo

```bash
systemctl status jg-pdf-server
journalctl -u jg-pdf-server -f  # Ver logs en tiempo real
```

### 7. Verificar conectividad

```bash
# Desde tu máquina:
curl http://143.110.130.78:8001/ping

# Debería responder:
# {"ok":true,"app":"impresion_pdf","version":"1.0","message":"PDF Print Manager Server running"}
```

---

## 🔨 Compilación y Publicación

### Flujo completo:

```cmd
1. Desarrolla en Print_PDFs.ps1
2. Actualiza versión en comentarios
3. Ejecuta: compile_pdf.bat
4. Prueba: dist\impresion_pdf.exe
5. Ejecuta: publish_pdf_update.bat
6. Actualiza APP_VERSION en server_pdf.py
7. Restart servicio: systemctl restart jg-pdf-server
```

### Comandos paso a paso:

```cmd
REM 1. Compilar
compile_pdf.bat

REM 2. Probar localmente
dist\impresion_pdf.exe

REM 3. Publicar al servidor
publish_pdf_update.bat

REM 4. SSH al servidor
ssh -i ~/.ssh/jg_server_key root@143.110.130.78

REM 5. En el servidor:
cd /opt/lagudi/server
nano server_pdf.py  # Actualizar APP_VERSION = "1.0"
systemctl restart jg-pdf-server
systemctl status jg-pdf-server
```

---

## 📦 Crear y Distribuir Instalador

### 1. Actualizar installer_pdf.iss

```iss
#define MyAppVersion "1.0"  ; Actualizar versión
```

### 2. Compilar con Inno Setup

```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_pdf.iss
```

### 3. Subir al servidor

```bash
scp -i ~/.ssh/jg_server_key installer\ImpresionPDF_Setup_v1.0.exe root@143.110.130.78:/opt/lagudi/impresion_pdf/installer/
```

### 4. Distribuir a usuarios

URL pública del instalador:
```
http://143.110.130.78:8001/download/installer
```

---

## 🔑 Gestión de Licencias

### Generar licencia (via API):

```bash
curl -X POST "http://143.110.130.78:8001/license/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "LFFG-PROD",
    "duration_days": 365,
    "notes": "Licencia anual producción"
  }'
```

Respuesta:
```json
{
  "ok": true,
  "license_code": "LFFG-ABCD-12345678-0365-A1B2C3D4",
  "client_id": "LFFG-PROD",
  "expiration_date": "2027-05-28T..."
}
```

### Ver todas las licencias:

```bash
curl http://143.110.130.78:8001/licenses
```

### Validar licencia:

```bash
curl -X POST "http://143.110.130.78:8001/license/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "license_code": "LFFG-ABCD-12345678-0365-A1B2C3D4",
    "pc_id": "PC-12345"
  }'
```

---

## 🔄 Sistema de Auto-Update

El cliente verifica automáticamente si hay nuevas versiones:

```powershell
# El .exe verifica en:
http://143.110.130.78:8001/app/version

# Si hay nueva versión, descarga desde:
http://143.110.130.78:8001/app/download
```

---

## 📊 Monitoreo y Logs

### Ver logs del servidor:

```bash
journalctl -u jg-pdf-server -f
```

### Ver actividad de usuarios:

```bash
curl http://143.110.130.78:8001/activity
```

### Ver historial de impresiones:

```bash
curl http://143.110.130.78:8001/print/history
```

### Verificar base de datos:

```bash
sqlite3 /opt/lagudi/impresion_pdf/impresion_pdf_data.db

sqlite> .tables
# licenses  license_activations  activity  print_jobs

sqlite> SELECT * FROM licenses;
sqlite> SELECT * FROM license_activations;
sqlite> .quit
```

---

## 🐛 Troubleshooting

### El servidor no responde:

```bash
# Verificar si el servicio está corriendo
systemctl status jg-pdf-server

# Ver logs de error
journalctl -u jg-pdf-server -n 100

# Restart servicio
systemctl restart jg-pdf-server
```

### Puerto 8001 no accesible:

```bash
# Verificar firewall
ufw status
ufw allow 8001/tcp
ufw reload

# Verificar que el servidor escucha en 8001
netstat -tulpn | grep 8001
```

### Base de datos corrupta:

```bash
# Backup
cp /opt/lagudi/impresion_pdf/impresion_pdf_data.db /opt/lagudi/impresion_pdf/impresion_pdf_data.db.backup

# Recrear
rm /opt/lagudi/impresion_pdf/impresion_pdf_data.db
systemctl restart jg-pdf-server
```

---

## 📞 Contacto

**Desarrollador:** Eng. Justo Torres  
**Empresa:** Lagudis Fresh Food Group  
**Email:** ghost.jgtv@gmail.com  
**Servidor:** 143.110.130.78:8001  

---

## 🔐 Seguridad

- ⚠️ Las licencias se validan con HMAC-SHA256
- ⚠️ Mantener SECRET_KEY privado en servidor y cliente
- ⚠️ Usar HTTPS en producción (agregar certificado SSL)
- ⚠️ Restringir acceso al puerto 8001 por IP si es posible

---

© 2026 Lagudis Fresh Food Group - All rights reserved
