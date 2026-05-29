@echo off
REM ============================================================================
REM Script de compilación para PDF Print Manager (Aplicación Python)
REM Author: Eng. Justo Torres - Lagudis Fresh Food Group
REM ============================================================================

echo.
echo ============================================================================
echo   COMPILANDO PDF PRINT MANAGER
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
cd pdf_print_manager
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Falló la instalación de dependencias
    cd ..
    pause
    exit /b 1
)

echo.
echo [2/4] Limpiando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist\PDF_Print_Manager.exe" del "dist\PDF_Print_Manager.exe"
if exist "PDF_Print_Manager.spec" del "PDF_Print_Manager.spec"

echo.
echo [3/4] Compilando con PyInstaller...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "PDF_Print_Manager" ^
    --icon "..\lagudi-logo.ico" ^
    --hidden-import "win32timezone" ^
    --hidden-import "PIL._tkinter_finder" ^
    main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] La compilación falló
    cd ..
    pause
    exit /b 1
)

echo.
echo [4/4] Copiando a carpeta principal...
copy /Y "dist\PDF_Print_Manager.exe" "..\dist\PDF_Print_Manager.exe" >nul

cd ..

echo.
echo ============================================================================
echo   COMPILACIÓN COMPLETADA EXITOSAMENTE
echo ============================================================================
echo.
echo Ejecutable creado: dist\PDF_Print_Manager.exe
echo.
dir "dist\PDF_Print_Manager.exe" | find "PDF_Print_Manager.exe"
echo.
echo ============================================================================
echo.
echo Para probar:
echo   dist\PDF_Print_Manager.exe
echo.
echo Para publicar al servidor:
echo   publish_app.bat
echo.
echo ============================================================================

pause
