@echo off
echo ================================
echo  Sistema de Asistencia JOLG v2.0
echo ================================
echo.

cd /d %~dp0

echo Verificando entorno virtual...
if not exist ".venv" (
    echo Error: Entorno virtual no encontrado.
    echo.
    echo Ejecutando instalador automatico...
    python install.py
    if errorlevel 1 (
        echo Error en la instalacion.
        pause
        exit /b 1
    )
)

echo Verificando dependencias...
.venv\Scripts\python.exe -c "import PyQt5, cv2, requests, numpy" 2>nul
if errorlevel 1 (
    echo Instalando dependencias faltantes...
    .venv\Scripts\pip.exe install -r requirements.txt
)

echo.
echo Iniciando Sistema de Asistencia JOLG...
echo.
.venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo Error al ejecutar la aplicacion.
    echo ========================================
    echo Posibles soluciones:
    echo 1. Verificar que la camara este conectada
    echo 2. Cerrar otras apps que usen la camara
    echo 3. Ejecutar como administrador
    echo 4. Verificar conexion a internet
    echo.
    echo Para obtener mas informacion ejecute:
    echo   python test.py
    echo.
    pause
)
