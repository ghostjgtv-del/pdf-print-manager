@echo off
REM ============================================================================
REM Script para publicar nueva versión de PDF Print Manager al servidor
REM Author: Eng. Justo Torres - Lagudis Fresh Food Group
REM ============================================================================
REM
REM Este script:
REM   1. Detecta la versión actual en Print_PDFs.ps1
REM   2. Compila el .exe
REM   3. Sube el .exe al servidor DigitalOcean (143.110.130.78:8001)
REM   4. Te recuerda actualizar server_pdf.py y hacer restart del servicio
REM
REM ============================================================================

echo.
echo ============================================================================
echo   PUBLICAR NUEVA VERSION - PDF PRINT MANAGER
echo   Lagudis Fresh Food Group
echo ============================================================================
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "Print_PDFs.ps1" (
    echo [ERROR] No se encuentra Print_PDFs.ps1
    echo Ejecuta este script desde C:\JG_Proyects\Impresion_PDFs\
    pause
    exit /b 1
)

REM Detectar versión del comentario en el script
echo [1/4] Detectando version...
findstr /C:"Version" Print_PDFs.ps1 > temp_version.txt 2>nul
set /p VERSION_LINE=<temp_version.txt
del temp_version.txt 2>nul

REM Extraer número de versión (ajustar según formato)
REM Si no encuentra versión, usar 1.0 por defecto
set NEW_VERSION=1.0
if defined VERSION_LINE (
    for /f "tokens=2 delims=:" %%a in ("%VERSION_LINE%") do set NEW_VERSION=%%a
    set NEW_VERSION=%NEW_VERSION: =%
)

echo       Version: %NEW_VERSION%
echo.

REM Compilar con compile_pdf.bat
echo [2/4] Compilando .exe...
call compile_pdf.bat

if %errorlevel% neq 0 (
    echo [ERROR] Falló la compilación
    pause
    exit /b 1
)

echo.
echo [3/4] Subiendo al servidor DigitalOcean...
echo        Servidor: 143.110.130.78
echo        Puerto: 8001
echo        Ruta: /opt/lagudi/impresion_pdf/updates/
echo.

REM Subir usando SCP (requiere configuración de SSH)
bash -c "scp -i ~/.ssh/jg_server_key dist/impresion_pdf.exe root@143.110.130.78:/opt/lagudi/impresion_pdf/updates/impresion_pdf.exe"

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] No se pudo subir via SCP
    echo.
    echo SOLUCION ALTERNATIVA:
    echo   1. Sube manualmente dist\impresion_pdf.exe al servidor
    echo   2. Usando FileZilla, WinSCP o similar
    echo   3. Ruta destino: /opt/lagudi/impresion_pdf/updates/
    echo.
    pause
) else (
    echo.
    echo [OK] Archivo subido exitosamente
)

echo.
echo [4/4] Verificando en servidor...
curl -s http://143.110.130.78:8001/app/version

echo.
echo.
echo ============================================================================
echo   VERSION %NEW_VERSION% LISTA PARA DISTRIBUCION
echo ============================================================================
echo.
echo PASOS MANUALES SIGUIENTES:
echo.
echo 1. Actualizar APP_VERSION en server_pdf.py a "%NEW_VERSION%"
echo    Ubicacion: C:\JG_Proyects\Impresion_PDFs\server_pdf.py
echo    Linea 59: APP_VERSION = "%NEW_VERSION%"
echo.
echo 2. Hacer commit y push a GitHub:
echo    cd C:\JG_Proyects\Impresion_PDFs
echo    git add server_pdf.py dist/impresion_pdf.exe
echo    git commit -m "Update PDF Print Manager to v%NEW_VERSION%"
echo    git push origin main
echo.
echo 3. Actualizar el servidor (via SSH):
echo    ssh -i ~/.ssh/jg_server_key root@143.110.130.78
echo    cd /opt/lagudi/pdf-print-manager
echo    git pull
echo    systemctl restart jg-pdf-server
echo.
echo 4. Verificar que el servidor responde:
echo    curl http://143.110.130.78:8001/ping
echo    curl http://143.110.130.78:8001/app/version
echo.
echo ============================================================================
echo.
echo Para crear el instalador:
echo   1. Actualizar version en installer_pdf.iss
echo   2. Compilar con Inno Setup
echo   3. Subir a /opt/lagudi/impresion_pdf/installer/
echo.
echo ============================================================================

pause
