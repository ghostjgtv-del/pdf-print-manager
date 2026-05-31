@echo off
REM ============================================================================
REM PDF Print Manager - Build Script
REM Author: Eng. Justo Torres
REM ============================================================================

echo.
echo ============================================================================
echo PDF PRINT MANAGER - BUILD SCRIPT
echo ============================================================================
echo.

REM Limpiar builds anteriores
echo [1/5] Limpiando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "PDF_Print_Manager.exe" del /q "PDF_Print_Manager.exe"
echo      OK - Limpieza completada
echo.

REM Verificar que PyInstaller está instalado
echo [2/5] Verificando PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo      INSTALANDO PyInstaller...
    pip install pyinstaller
)
echo      OK - PyInstaller disponible
echo.

REM Compilar con PyInstaller
echo [3/5] Compilando aplicacion con PyInstaller...
pyinstaller --clean build_installer.spec
if errorlevel 1 (
    echo      ERROR - Fallo la compilacion
    pause
    exit /b 1
)
echo      OK - Compilacion exitosa
echo.

REM Mover ejecutable a raiz
echo [4/5] Organizando archivos...
if exist "dist\PDF_Print_Manager.exe" (
    move "dist\PDF_Print_Manager.exe" "PDF_Print_Manager.exe"
    echo      OK - Ejecutable movido a raiz
) else (
    echo      ERROR - No se encontro el ejecutable
    pause
    exit /b 1
)
echo.

REM Limpiar archivos temporales
echo [5/5] Limpiando archivos temporales...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo      OK - Limpieza completada
echo.

echo ============================================================================
echo BUILD COMPLETADO EXITOSAMENTE
echo ============================================================================
echo.
echo Ejecutable generado: PDF_Print_Manager.exe
echo.
pause
