@echo off
echo ========================================
echo    CREANDO INSTALADOR ASISTENCIA JOLG
echo ========================================

REM Verificar que existe el ejecutable
if not exist "distribucion\AsistenciaJOLG.exe" (
    echo ❌ ERROR: No se encuentra el ejecutable
    echo Ejecute primero: crear_ejecutable.bat
    pause
    exit /b 1
)

echo.
echo [1/4] Verificando archivos de distribución...
echo ✅ AsistenciaJOLG.exe encontrado
echo.

REM Verificar si Inno Setup está instalado
set "INNO_PATH="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
) else (
    echo ❌ ERROR: Inno Setup no está instalado
    echo.
    echo OPCIONES DISPONIBLES:
    echo.
    echo 1. INNO SETUP (GRATUITO - RECOMENDADO)
    echo    - Descarga: https://jrsoftware.org/isdl.php
    echo    - Instalar version 6.x
    echo    - Reiniciar este script
    echo.
    echo 2. ADVANCED INSTALLER (PROFESIONAL)
    echo    - Descarga: https://www.advancedinstaller.com/
    echo    - Versión gratuita disponible
    echo.
    echo 3. WIX TOOLSET (TÉCNICO)
    echo    - Descarga: https://wixtoolset.org/
    echo    - Requiere conocimientos de XML
    echo.
    pause
    exit /b 1
)

echo [2/4] Inno Setup encontrado en: %INNO_PATH%
echo.

REM Crear directorio de salida
if not exist "setup_output" mkdir "setup_output"

echo [3/4] Compilando instalador con Inno Setup...
echo.

REM Compilar el instalador
"%INNO_PATH%" "setup_script.iss"

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Falló la compilación del instalador
    pause
    exit /b 1
)

echo.
echo [4/4] Verificando archivos generados...

if exist "setup_output\AsistenciaJOLG_Setup_v1.0.0.exe" (
    echo ✅ Instalador creado exitosamente!
    echo.
    echo ========================================
    echo    INSTALADOR CREADO EXITOSAMENTE
    echo ========================================
    echo.
    echo Archivo generado:
    echo - setup_output\AsistenciaJOLG_Setup_v1.0.0.exe
    echo.
    echo CARACTERÍSTICAS DEL INSTALADOR:
    echo - ✅ Interfaz profesional en español/inglés
    echo - ✅ Instalación en Archivos de Programa
    echo - ✅ Accesos directos en menú inicio/escritorio
    echo - ✅ Desinstalador automático
    echo - ✅ Creación de carpetas necesarias
    echo - ✅ Permisos de administrador
    echo.
    echo DISTRIBUCIÓN:
    echo - Tamaño: ~50-80 MB (incluye todas las dependencias)
    echo - Compatible: Windows 7/8/10/11 (64-bit)
    echo - Sin dependencias externas
    echo.
) else (
    echo ❌ ERROR: No se generó el instalador
)

echo ========================================
pause
