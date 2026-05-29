@echo off
REM ============================================================================
REM Script para publicar PDF Print Manager al servidor DigitalOcean
REM Author: Eng. Justo Torres - Lagudis Fresh Food Group
REM ============================================================================

echo.
echo ============================================================================
echo   PUBLICAR PDF PRINT MANAGER AL SERVIDOR
echo   Lagudis Fresh Food Group
echo ============================================================================
echo.

REM Verificar que el ejecutable existe
if not exist "dist\PDF_Print_Manager.exe" (
    echo [ERROR] No se encuentra dist\PDF_Print_Manager.exe
    echo Ejecuta primero: compile_app.bat
    pause
    exit /b 1
)

echo [1/2] Subiendo ejecutable al servidor...
echo        Servidor: 143.110.130.78
echo        Puerto: 8001
echo        Ruta: /opt/lagudi/impresion_pdf/updates/
echo.

REM Renombrar para mantener compatibilidad
bash -c "scp -i ~/.ssh/jg_server_key dist/PDF_Print_Manager.exe root@143.110.130.78:/opt/lagudi/impresion_pdf/updates/impresion_pdf.exe"

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] No se pudo subir via SCP
    echo.
    echo SOLUCION ALTERNATIVA:
    echo   1. Sube manualmente dist\PDF_Print_Manager.exe al servidor
    echo   2. Usando FileZilla, WinSCP o similar
    echo   3. Ruta destino: /opt/lagudi/impresion_pdf/updates/impresion_pdf.exe
    echo.
    pause
) else (
    echo.
    echo [OK] Archivo subido exitosamente
)

echo.
echo [2/2] Verificando en servidor...
curl -s http://143.110.130.78:8001/app/version

echo.
echo.
echo ============================================================================
echo   ACTUALIZACION PUBLICADA
echo ============================================================================
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Actualizar APP_VERSION en server_pdf.py si cambió la versión
echo 2. Hacer commit y push a GitHub
echo 3. Hacer pull en el servidor
echo.
echo Comandos:
echo   git add .
echo   git commit -m "Update PDF Print Manager"
echo   git push origin main
echo.
echo   ssh -i ~/.ssh/jg_server_key root@143.110.130.78
echo   cd /opt/lagudi/pdf-print-manager
echo   git pull
echo   systemctl restart jg-pdf-server
echo.
echo ============================================================================

pause
