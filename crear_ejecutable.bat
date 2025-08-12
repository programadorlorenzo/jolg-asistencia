@echo off
echo ========================================
echo    CREANDO EJECUTABLE ASISTENCIA JOLG
echo ========================================

REM Limpiar builds anteriores
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo [1/3] Limpiando archivos anteriores...
echo.

REM Crear ejecutable usando la configuración personalizada
echo [2/3] Creando ejecutable con PyInstaller...
pyinstaller build_config.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Falló la creación del ejecutable
    pause
    exit /b 1
)

echo.
echo [3/3] Creando carpeta de distribución...

REM Crear carpeta de distribución con todo lo necesario
if not exist "distribucion" mkdir "distribucion"
copy "dist\AsistenciaJOLG.exe" "distribucion\"

REM Crear carpetas necesarias
if not exist "distribucion\fotos" mkdir "distribucion\fotos"
if not exist "distribucion\temp" mkdir "distribucion\temp"

REM Crear archivo README
echo Sistema de Asistencia JOLG > "distribucion\README.txt"
echo ========================= >> "distribucion\README.txt"
echo. >> "distribucion\README.txt"
echo Instrucciones de uso: >> "distribucion\README.txt"
echo 1. Ejecutar AsistenciaJOLG.exe >> "distribucion\README.txt"
echo 2. Seleccionar Personal ID >> "distribucion\README.txt"
echo 3. Agregar observaciones (opcional) >> "distribucion\README.txt"
echo 4. Presionar "REGISTRAR ASISTENCIA" >> "distribucion\README.txt"
echo. >> "distribucion\README.txt"
echo Carpetas: >> "distribucion\README.txt"
echo - fotos: Se guardan las fotos capturadas >> "distribucion\README.txt"
echo - temp: Archivos temporales >> "distribucion\README.txt"

echo.
echo ✅ ÉXITO: Ejecutable creado en carpeta 'distribucion'
echo.
echo Archivos generados:
echo - distribucion\AsistenciaJOLG.exe (Aplicación principal)
echo - distribucion\fotos\ (Carpeta para fotos)
echo - distribucion\temp\ (Carpeta temporal)
echo - distribucion\README.txt (Instrucciones)
echo.
echo ========================================
echo    PROCESO COMPLETADO EXITOSAMENTE
echo ========================================
pause
