# ✅ Setup Checklist - PDF Print Manager con DigitalOcean

---

## 📋 Archivos Creados

### Servidor y Backend:
- [x] `server_pdf.py` - FastAPI server con licencias y auto-update (Puerto 8001)
- [x] `jg-pdf-server.service` - Systemd service para DigitalOcean

### Scripts de Compilación:
- [x] `compile_pdf.bat` - Compila Print_PDFs.ps1 → impresion_pdf.exe
- [x] `publish_pdf_update.bat` - Sube .exe al servidor

### Instalador:
- [x] `installer_pdf.iss` - Inno Setup script para crear instalador

### Documentación:
- [x] `DEPLOYMENT.md` - Guía completa de deployment
- [x] `README_SERVER.md` - Overview de arquitectura
- [x] `SETUP_CHECKLIST.md` - Este archivo

---

## 🎯 Configuración Confirmada

| Item | Valor | Status |
|------|-------|--------|
| Servidor | 143.110.130.78 | ✅ |
| Puerto | 8001 | ✅ |
| Ruta servidor | /opt/lagudi/impresion_pdf/ | ✅ |
| Servicio | jg-pdf-server.service | ✅ |
| Nombre app | Impresion PDFs | ✅ |
| Ejecutable | impresion_pdf.exe | ✅ |
| Icono | lagudi-logo.ico | ✅ |
| Logo | lagudi-logo.png | ✅ |
| Versión inicial | 1.0 | ✅ |

---

## 🚀 Pasos para Desplegar

### FASE 1: Setup del Servidor DigitalOcean

```bash
# 1. Conectar al servidor
ssh -i ~/.ssh/jg_server_key root@143.110.130.78

# 2. Crear estructura de carpetas
mkdir -p /opt/lagudi/impresion_pdf/{updates,installer}
mkdir -p /opt/lagudi/server

# 3. Instalar dependencias
apt update
apt install -y python3 python3-pip
pip3 install fastapi uvicorn[standard] python-multipart

# 4. Copiar server_pdf.py (desde Windows con Git Bash)
scp -i ~/.ssh/jg_server_key server_pdf.py root@143.110.130.78:/opt/lagudi/server/

# 5. Instalar servicio systemd
scp -i ~/.ssh/jg_server_key jg-pdf-server.service root@143.110.130.78:/etc/systemd/system/

# 6. Habilitar y arrancar servicio
systemctl daemon-reload
systemctl enable jg-pdf-server
systemctl start jg-pdf-server
systemctl status jg-pdf-server

# 7. Configurar firewall
ufw allow 8001/tcp
ufw reload

# 8. Verificar
curl http://143.110.130.78:8001/ping
```

**Resultado esperado:**
```json
{
  "ok": true,
  "app": "impresion_pdf",
  "version": "1.0",
  "message": "PDF Print Manager Server running"
}
```

---

### FASE 2: Compilar Aplicación

```cmd
REM 1. Verificar archivos necesarios
dir Print_PDFs.ps1
dir lagudi-logo.ico
dir lagudi-logo.png

REM 2. Instalar ps2exe (solo primera vez)
powershell -Command "Install-Module ps2exe -Scope CurrentUser -Force"

REM 3. Compilar
compile_pdf.bat

REM 4. Verificar resultado
dir dist\impresion_pdf.exe
```

---

### FASE 3: Publicar Primera Versión

```cmd
REM 1. Subir .exe al servidor
publish_pdf_update.bat

REM 2. Verificar que llegó
curl http://143.110.130.78:8001/app/version
```

---

### FASE 4: Crear Instalador

```cmd
REM 1. Abrir Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_pdf.iss

REM 2. Verificar que se creó
dir installer\ImpresionPDF_Setup_v1.0.exe

REM 3. Subir al servidor
scp -i ~/.ssh/jg_server_key installer\ImpresionPDF_Setup_v1.0.exe root@143.110.130.78:/opt/lagudi/impresion_pdf/installer/

REM 4. Verificar descarga pública
curl -O http://143.110.130.78:8001/download/installer
```

---

## 🔑 Probar Sistema de Licencias

### 1. Generar licencia de prueba:

```bash
curl -X POST "http://143.110.130.78:8001/license/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "TEST-001",
    "duration_days": 30,
    "notes": "Licencia de prueba"
  }'
```

### 2. Copiar el license_code de la respuesta

### 3. Validar licencia:

```bash
curl -X POST "http://143.110.130.78:8001/license/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "license_code": "LFFG-XXXX-XXXXXXXX-XXXX-XXXXXXXX",
    "pc_id": "TEST-PC"
  }'
```

### 4. Ver todas las licencias:

```bash
curl http://143.110.130.78:8001/licenses | jq
```

---

## 📊 Verificación de Funcionamiento

### Checklist de Pruebas:

- [ ] Server responde en puerto 8001
- [ ] `/ping` retorna ok: true
- [ ] `/app/version` retorna versión correcta
- [ ] `/app/download` descarga el .exe
- [ ] `/download/installer` descarga el instalador
- [ ] `/license/generate` crea licencias
- [ ] `/license/validate` valida correctamente
- [ ] impresion_pdf.exe se ejecuta sin errores
- [ ] El instalador crea shortcuts correctos
- [ ] Auto-update funciona
- [ ] Logs del servidor son accesibles

---

## 🐛 Troubleshooting Rápido

### Puerto 8001 no accesible:
```bash
ufw allow 8001/tcp
ufw reload
netstat -tulpn | grep 8001
```

### Servicio no arranca:
```bash
journalctl -u jg-pdf-server -n 50
systemctl restart jg-pdf-server
```

### .exe no compila:
```powershell
Install-Module ps2exe -Scope CurrentUser -Force
Get-Module -ListAvailable ps2exe
```

---

## 📞 Contactos y URLs

| Recurso | URL/Comando |
|---------|-------------|
| Server Health | http://143.110.130.78:8001/ping |
| App Version | http://143.110.130.78:8001/app/version |
| Download .exe | http://143.110.130.78:8001/app/download |
| Download Installer | http://143.110.130.78:8001/download/installer |
| SSH Server | ssh -i ~/.ssh/jg_server_key root@143.110.130.78 |
| Developer | ghost.jgtv@gmail.com |

---

## 🎉 Siguiente Paso

Una vez completado el checklist, el sistema estará listo para:
1. Distribuir instalador a usuarios
2. Generar licencias según necesidad
3. Auto-update automático de clientes
4. Monitoreo centralizado de uso

---

**Estado:** ✅ Configuración completa  
**Versión:** 1.0  
**Fecha:** Mayo 2026  
**Empresa:** Lagudis Fresh Food Group  

---

© 2026 Lagudis Fresh Food Group - All rights reserved
