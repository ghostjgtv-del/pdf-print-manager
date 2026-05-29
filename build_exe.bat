@echo off
REM ========================================
REM PDF Print Manager - Build Script
REM Author: Eng. Justo Torres
REM ========================================

echo.
echo ========================================
echo  Building PDF Print Manager v1.0
echo  Lagudis Fresh Food Group
echo ========================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Limpiar builds anteriores
echo [1/4] Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "PDF_Print_Manager.spec" del /q "PDF_Print_Manager.spec"

echo [2/4] Creating executable...
pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name="PDF_Print_Manager" ^
    --add-data="pdf_print_manager;pdf_print_manager" ^
    --hidden-import=win32timezone ^
    --hidden-import=PyPDF2 ^
    --hidden-import=cryptography ^
    --hidden-import=customtkinter ^
    --collect-all=customtkinter ^
    pdf_print_manager/main.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo  ERROR: Build failed!
    echo ========================================
    pause
    exit /b 1
)

echo [3/4] Cleaning up temporary files...
rmdir /s /q "build"
del /q "PDF_Print_Manager.spec"

echo [4/4] Build complete!
echo.
echo ========================================
echo  SUCCESS!
echo ========================================
echo.
echo  Executable created at:
echo  %cd%\dist\PDF_Print_Manager.exe
echo.
echo  File size:
dir "dist\PDF_Print_Manager.exe" | find "PDF_Print_Manager.exe"
echo.
echo ========================================

pause
