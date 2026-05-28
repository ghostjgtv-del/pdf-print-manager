@echo off
REM ============================================================================
REM Script de compilación para PDF Print Manager
REM Compila Print_PDFs.ps1 a impresion_pdf.exe
REM Author: Eng. Justo Torres - Lagudis Fresh Food Group
REM ============================================================================
REM
REM Este script compila Print_PDFs.ps1 a impresion_pdf.exe usando ps2exe
REM con todos los recursos necesarios incluidos.
REM
REM Requisitos:
REM   - PowerShell 5.1 o superior
REM   - Módulo ps2exe: Install-Module ps2exe -Scope CurrentUser
REM
REM ============================================================================

echo.
echo ============================================================================
echo   COMPILANDO PDF PRINT MANAGER
echo   Lagudis Fresh Food Group
echo ============================================================================
echo.

REM Verificar que los archivos necesarios existen
if not exist "Print_PDFs.ps1" (
    echo [ERROR] No se encuentra Print_PDFs.ps1
    pause
    exit /b 1
)

if not exist "lagudi-logo.ico" (
    echo [ERROR] No se encuentra lagudi-logo.ico
    pause
    exit /b 1
)

if not exist "lagudi-logo.png" (
    echo [ERROR] No se encuentra lagudi-logo.png
    pause
    exit /b 1
)

echo [1/4] Archivos verificados OK
echo.

REM Crear carpeta dist si no existe
if not exist "dist" mkdir dist

echo [2/4] Verificando módulo ps2exe...
echo.
powershell -Command "if (-not (Get-Module -ListAvailable -Name ps2exe)) { Write-Host '[INSTALANDO] Módulo ps2exe...' -ForegroundColor Yellow; Install-Module ps2exe -Scope CurrentUser -Force }"

echo.
echo [3/4] Compilando PowerShell a EXE...
echo.

REM Compilar con ps2exe
powershell -Command "Import-Module ps2exe; Invoke-ps2exe -inputFile 'Print_PDFs.ps1' -outputFile 'dist\impresion_pdf.exe' -iconFile 'lagudi-logo.ico' -title 'PDF Print Manager' -description 'Lagudis Fresh Food Group - PDF Batch Printing Tool' -company 'Lagudis Fresh Food Group' -product 'PDF Print Manager' -copyright '(c) 2026 Lagudis Fresh Food Group' -version '1.0.0.0' -noConsole -requireAdmin"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] La compilación falló
    echo.
    echo Posibles soluciones:
    echo   1. Instalar ps2exe: Install-Module ps2exe -Scope CurrentUser
    echo   2. Verificar que PowerShell 5.1+ está instalado
    pause
    exit /b 1
)

REM Copiar recursos necesarios a dist
echo.
echo [4/4] Copiando recursos...
copy /Y "lagudi-logo.png" "dist\lagudi-logo.png" >nul
copy /Y "lagudi-logo.ico" "dist\lagudi-logo.ico" >nul

echo.
echo ============================================================================
echo   COMPILACIÓN COMPLETADA EXITOSAMENTE
echo ============================================================================
echo.
echo Ejecutable creado: dist\impresion_pdf.exe
echo Tamaño aproximado:
dir "dist\impresion_pdf.exe" | find "impresion_pdf.exe"
echo.
echo Recursos incluidos:
echo   - lagudi-logo.png
echo   - lagudi-logo.ico
echo.
echo ============================================================================
echo.
echo Para probar:
echo   dist\impresion_pdf.exe
echo.
echo Para publicar al servidor:
echo   run: publish_update.bat
echo.
echo ============================================================================

pause
