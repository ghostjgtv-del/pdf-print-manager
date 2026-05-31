@echo off
REM ============================================================================
REM PDF Print Manager - Git Push Script
REM Author: Eng. Justo Torres
REM ============================================================================

echo.
echo ============================================================================
echo PDF PRINT MANAGER - GIT PUSH
echo ============================================================================
echo.

REM Verificar si hay repositorio Git
if not exist ".git" (
    echo [INIT] Inicializando repositorio Git...
    git init
    git branch -M main
    echo      OK - Repositorio inicializado
    echo.
)

REM Agregar todos los cambios
echo [1/4] Agregando archivos al staging...
git add .
echo      OK - Archivos agregados
echo.

REM Crear commit
echo [2/4] Creando commit...
git commit -m "Build v1.0.0 - Fixed Actions column with native text implementation

- Replaced widget-based buttons with native QTableWidgetItem
- Implemented click events for print actions
- Added hover effects for interactive feedback
- Fixed row height issues (38px)
- Complete Spanish/English translation support
- Logo improvements with gradient backgrounds
- Light/Dark theme complete support

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

if errorlevel 1 (
    echo      NOTA - No hay cambios para commitear
) else (
    echo      OK - Commit creado
)
echo.

REM Agregar remote si no existe
echo [3/4] Verificando remote...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo      CONFIGURE EL REMOTE MANUALMENTE:
    echo      git remote add origin https://github.com/TU_USUARIO/pdf-print-manager.git
    pause
    exit /b 1
) else (
    echo      OK - Remote configurado
)
echo.

REM Push al repositorio
echo [4/4] Subiendo al repositorio...
git push -u origin main
if errorlevel 1 (
    echo      ERROR - Fallo el push
    pause
    exit /b 1
)
echo      OK - Push completado
echo.

echo ============================================================================
echo GIT PUSH COMPLETADO EXITOSAMENTE
echo ============================================================================
echo.
pause
