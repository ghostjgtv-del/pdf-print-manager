# 🚀 Setup del Servidor - Guía PowerShell

---

## 🎯 Qué se ejecuta donde:

```
┌─────────────────────────────────────────────┐
│  TU MÁQUINA WINDOWS (PowerShell)            │
│  - Conectar al servidor (SSH)               │
│  - Copiar archivos (SCP)                    │
│  - Compilar .exe                            │
│  - Crear instalador                         │
└─────────────────────────────────────────────┘
              ↓ SSH ↓
┌─────────────────────────────────────────────┐
│  SERVIDOR DIGITALOCEAN (Bash/Linux)         │
│  - Crear carpetas (mkdir)                   │
│  - Instalar Python (apt)                    │
│  - Iniciar servicio (systemctl)             │
└─────────────────────────────────────────────┘
```

---

## 📋 FASE 1: Desde PowerShell en tu PC

### 1.1 Verificar SSH Key

```powershell
# Verificar que tienes la llave SSH
Test-Path ~/.ssh/jg_server_key

# Si no existe, copia tu llave ahí
```

### 1.2 Conectar al Servidor

```powershell
# Desde PowerShell:
ssh -i ~/.ssh/jg_server_key root@143.110.130.78
```

**Ahora estás DENTRO del servidor (Linux/Bash)**

---

## 📋 FASE 2: Dentro del Servidor (Bash)

Una vez conectado por SSH, ejecuta estos comandos **en el servidor**:

```bash
# Crear estructura de carpetas
mkdir -p /opt/lagudi/impresion_pdf/updates
mkdir -p /opt/lagudi/impresion_pdf/installer
mkdir -p /opt/lagudi/server

# Instalar dependencias Python
apt update
apt install -y python3 python3-pip python3-venv

# Instalar FastAPI
pip3 install fastapi uvicorn[standard] python-multipart

# Verificar instalación
python3 --version
pip3 list | grep fastapi
```

### Salir del servidor:
```bash
exit
```

---

## 📋 FASE 3: Copiar Archivos desde PowerShell

```powershell
# Volver a PowerShell en tu máquina Windows

# Navegar a la carpeta del proyecto
cd C:\JG_Proyects\Impresion_PDFs

# Copiar server_pdf.py al servidor
scp -i ~/.ssh/jg_server_key server_pdf.py root@143.110.130.78:/opt/lagudi/server/

# Copiar servicio systemd
scp -i ~/.ssh/jg_server_key jg-pdf-server.service root@143.110.130.78:/etc/systemd/system/

# Verificar que se copiaron
ssh -i ~/.ssh/jg_server_key root@143.110.130.78 "ls -la /opt/lagudi/server/"
ssh -i ~/.ssh/jg_server_key root@143.110.130.78 "ls -la /etc/systemd/system/jg-pdf-server.service"
```

---

## 📋 FASE 4: Configurar Servicio (desde PowerShell)

```powershell
# Ejecutar comandos remotos desde PowerShell:

# Recargar systemd
ssh -i ~/.ssh/jg_server_key root@143.110.130.78 "systemctl daemon-reload"

# Habilitar servicio
ssh -i ~/.ssh/jg_server_key root@143.110.130.78 "systemctl enable jg-pdf-server"

# Iniciar servicio
ssh -i ~/.ssh/jg_server_key root@143.110.130.78 "systemctl start jg-pdf-server"

# Ver estado
ssh -i ~/.ssh/jg_server_key root@143.110.130.78 "systemctl status jg-pdf-server"

# Configurar firewall
ssh -i ~/.ssh/jg_server_key root@143.110.130.78 "ufw allow 8001/tcp && ufw reload"
```

---

## 📋 FASE 5: Verificar desde PowerShell

```powershell
# Test de conectividad
curl http://143.110.130.78:8001/ping

# Debería responder:
# {"ok":true,"app":"impresion_pdf","version":"1.0","message":"PDF Print Manager Server running"}

# Ver versión de la app
curl http://143.110.130.78:8001/app/version

# Ver logs del servidor (requiere SSH)
ssh -i ~/.ssh/jg_server_key root@143.110.130.78 "journalctl -u jg-pdf-server -n 50"
```

---

## 🔨 Compilación (PowerShell)

```powershell
# En tu máquina Windows:
cd C:\JG_Proyects\Impresion_PDFs

# Compilar
.\compile_pdf.bat

# Publicar al servidor
.\publish_pdf_update.bat
```

---

## 📦 Crear Instalador (PowerShell)

```powershell
# Compilar con Inno Setup
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_pdf.iss

# Verificar que se creó
Test-Path "installer\ImpresionPDF_Setup_v1.0.exe"

# Subir al servidor
scp -i ~/.ssh/jg_server_key "installer\ImpresionPDF_Setup_v1.0.exe" root@143.110.130.78:/opt/lagudi/impresion_pdf/installer/

# Verificar URL pública
curl http://143.110.130.78:8001/download/installer -o test_installer.exe
```

---

## 🎯 Script PowerShell Todo-en-Uno

```powershell
# Guardar como: setup_server.ps1

$ServerIP = "143.110.130.78"
$SSHKey = "~/.ssh/jg_server_key"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " Setup PDF Print Manager Server" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Crear carpetas en servidor
Write-Host "[1/6] Creando estructura de carpetas..." -ForegroundColor Yellow
ssh -i $SSHKey root@$ServerIP "mkdir -p /opt/lagudi/impresion_pdf/{updates,installer} && mkdir -p /opt/lagudi/server"

# Paso 2: Instalar dependencias
Write-Host "[2/6] Instalando dependencias Python..." -ForegroundColor Yellow
ssh -i $SSHKey root@$ServerIP "apt update && apt install -y python3 python3-pip && pip3 install fastapi uvicorn[standard] python-multipart"

# Paso 3: Copiar archivos
Write-Host "[3/6] Copiando archivos al servidor..." -ForegroundColor Yellow
scp -i $SSHKey server_pdf.py root@${ServerIP}:/opt/lagudi/server/
scp -i $SSHKey jg-pdf-server.service root@${ServerIP}:/etc/systemd/system/

# Paso 4: Configurar servicio
Write-Host "[4/6] Configurando servicio systemd..." -ForegroundColor Yellow
ssh -i $SSHKey root@$ServerIP "systemctl daemon-reload && systemctl enable jg-pdf-server && systemctl start jg-pdf-server"

# Paso 5: Configurar firewall
Write-Host "[5/6] Configurando firewall..." -ForegroundColor Yellow
ssh -i $SSHKey root@$ServerIP "ufw allow 8001/tcp && ufw reload"

# Paso 6: Verificar
Write-Host "[6/6] Verificando instalación..." -ForegroundColor Yellow
$response = curl -s http://${ServerIP}:8001/ping | ConvertFrom-Json

if ($response.ok) {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host " INSTALACION EXITOSA" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Servidor: http://${ServerIP}:8001" -ForegroundColor Green
    Write-Host "Estado: $($response.message)" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR: El servidor no responde correctamente" -ForegroundColor Red
    Write-Host ""
}

Write-Host "Ver logs:"
Write-Host "  ssh -i $SSHKey root@$ServerIP 'journalctl -u jg-pdf-server -f'" -ForegroundColor Cyan
Write-Host ""
```

### Ejecutar el script:

```powershell
.\setup_server.ps1
```

---

## 🐛 Troubleshooting PowerShell

### SSH no funciona:
```powershell
# Verificar conectividad
Test-NetConnection -ComputerName 143.110.130.78 -Port 22

# Verificar permisos de la llave
icacls ~/.ssh/jg_server_key
```

### SCP no funciona:
```powershell
# Alternativa: usar SFTP
# O instalar OpenSSH:
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

### Curl no disponible:
```powershell
# Usar Invoke-WebRequest:
Invoke-WebRequest -Uri "http://143.110.130.78:8001/ping" | Select-Object -Expand Content
```

---

## 📞 Resumen

**TU MÁQUINA (PowerShell):**
- Conectar con `ssh`
- Copiar con `scp`
- Compilar con `.\compile_pdf.bat`
- Verificar con `curl`

**SERVIDOR (Bash - después de SSH):**
- Comandos Linux: `mkdir`, `apt`, `systemctl`
- Se ejecutan después de `ssh -i ~/.ssh/jg_server_key root@143.110.130.78`

---

© 2026 Lagudis Fresh Food Group
