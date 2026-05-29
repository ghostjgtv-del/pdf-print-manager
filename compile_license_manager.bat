@echo off
REM ============================================================================
REM Script de compilación para Lagudi License Manager
REM Author: Eng. Justo Torres - Lagudis Fresh Food Group
REM ============================================================================

echo.
echo ============================================================================
echo   COMPILANDO LAGUDI LICENSE MANAGER
echo   Lagudis Fresh Food Group
echo ============================================================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no está en PATH
    pause
    exit /b 1
)

echo [1/4] Instalando dependencias...
echo.
pip install -r requirements_license_manager.txt
pip install pyinstaller

if %errorlevel% neq 0 (
    echo [ERROR] Falló la instalación de dependencias
    pause
    exit /b 1
)

echo.
echo [2/4] Limpiando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist\license_manager.exe" del "dist\license_manager.exe"
if exist "license_manager.spec" del "license_manager.spec"

echo.
echo [3/4] Compilando con PyInstaller...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "Lagudi_License_Manager" ^
    --icon "lagudi-logo.ico" ^
    --add-data "lagudi-logo.ico;." ^
    --add-data "lagudi-logo.png;." ^
    --hidden-import "PIL._tkinter_finder" ^
    license_manager.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] La compilación falló
    pause
    exit /b 1
)

echo.
echo [4/4] Copiando recursos...
copy /Y "lagudi-logo.png" "dist\lagudi-logo.png" >nul
copy /Y "lagudi-logo.ico" "dist\lagudi-logo.ico" >nul

echo.
echo ============================================================================
echo   COMPILACIÓN COMPLETADA EXITOSAMENTE
echo ============================================================================
echo.
echo Ejecutable creado: dist\Lagudi_License_Manager.exe
echo.
dir "dist\Lagudi_License_Manager.exe" | find "Lagudi_License_Manager.exe"
echo.
echo ============================================================================
echo.
echo Para probar:
echo   dist\Lagudi_License_Manager.exe
echo.
echo ============================================================================

pause
