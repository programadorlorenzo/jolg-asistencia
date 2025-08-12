@echo off
echo ========================================
echo    INSTALADOR ALTERNATIVO - NSIS
echo ========================================

REM Crear script NSIS
echo !include "MUI2.nsh" > installer_nsis.nsi
echo. >> installer_nsis.nsi
echo Name "Asistencia JOLG" >> installer_nsis.nsi
echo OutFile "setup_output\AsistenciaJOLG_Setup_v1.0.0.exe" >> installer_nsis.nsi
echo InstallDir "$PROGRAMFILES64\AsistenciaJOLG" >> installer_nsis.nsi
echo RequestExecutionLevel admin >> installer_nsis.nsi
echo. >> installer_nsis.nsi
echo !define MUI_WELCOMEPAGE_TITLE "Asistencia JOLG v1.0.0" >> installer_nsis.nsi
echo !define MUI_WELCOMEPAGE_TEXT "Sistema de registro de asistencia para personal.$\r$\n$\r$\nEste asistente le guiará durante la instalación." >> installer_nsis.nsi
echo !insertmacro MUI_PAGE_WELCOME >> installer_nsis.nsi
echo !insertmacro MUI_PAGE_LICENSE "README.txt" >> installer_nsis.nsi
echo !insertmacro MUI_PAGE_DIRECTORY >> installer_nsis.nsi
echo !insertmacro MUI_PAGE_INSTFILES >> installer_nsis.nsi
echo !insertmacro MUI_PAGE_FINISH >> installer_nsis.nsi
echo !insertmacro MUI_UNPAGE_WELCOME >> installer_nsis.nsi
echo !insertmacro MUI_UNPAGE_CONFIRM >> installer_nsis.nsi
echo !insertmacro MUI_UNPAGE_INSTFILES >> installer_nsis.nsi
echo !insertmacro MUI_UNPAGE_FINISH >> installer_nsis.nsi
echo !insertmacro MUI_LANGUAGE "Spanish" >> installer_nsis.nsi
echo. >> installer_nsis.nsi
echo Section "MainSection" SEC01 >> installer_nsis.nsi
echo   SetOutPath "$INSTDIR" >> installer_nsis.nsi
echo   File "distribucion\AsistenciaJOLG.exe" >> installer_nsis.nsi
echo   File "distribucion\README.txt" >> installer_nsis.nsi
echo   CreateDirectory "$INSTDIR\fotos" >> installer_nsis.nsi
echo   CreateDirectory "$INSTDIR\temp" >> installer_nsis.nsi
echo   CreateShortCut "$DESKTOP\Asistencia JOLG.lnk" "$INSTDIR\AsistenciaJOLG.exe" >> installer_nsis.nsi
echo   CreateDirectory "$SMPROGRAMS\Asistencia JOLG" >> installer_nsis.nsi
echo   CreateShortCut "$SMPROGRAMS\Asistencia JOLG\Asistencia JOLG.lnk" "$INSTDIR\AsistenciaJOLG.exe" >> installer_nsis.nsi
echo   WriteUninstaller "$INSTDIR\uninstall.exe" >> installer_nsis.nsi
echo SectionEnd >> installer_nsis.nsi
echo. >> installer_nsis.nsi
echo Section "Uninstall" >> installer_nsis.nsi
echo   Delete "$INSTDIR\AsistenciaJOLG.exe" >> installer_nsis.nsi
echo   Delete "$INSTDIR\README.txt" >> installer_nsis.nsi
echo   Delete "$INSTDIR\uninstall.exe" >> installer_nsis.nsi
echo   RMDir /r "$INSTDIR\fotos" >> installer_nsis.nsi
echo   RMDir /r "$INSTDIR\temp" >> installer_nsis.nsi
echo   RMDir "$INSTDIR" >> installer_nsis.nsi
echo   Delete "$DESKTOP\Asistencia JOLG.lnk" >> installer_nsis.nsi
echo   RMDir /r "$SMPROGRAMS\Asistencia JOLG" >> installer_nsis.nsi
echo SectionEnd >> installer_nsis.nsi

echo Script NSIS creado: installer_nsis.nsi
echo.
echo Para compilar necesitas NSIS instalado desde: https://nsis.sourceforge.io/
echo.

REM Crear instalador ZIP como alternativa inmediata
echo [ALTERNATIVA] Creando paquete ZIP distribuible...
if not exist "setup_output" mkdir "setup_output"

REM Usar PowerShell para crear ZIP
powershell -Command "Compress-Archive -Path 'distribucion\*' -DestinationPath 'setup_output\AsistenciaJOLG_Portable_v1.0.0.zip' -Force"

if exist "setup_output\AsistenciaJOLG_Portable_v1.0.0.zip" (
    echo ✅ Paquete ZIP creado: setup_output\AsistenciaJOLG_Portable_v1.0.0.zip
    echo.
    echo INSTRUCCIONES PARA DISTRIBUCIÓN ZIP:
    echo 1. Descomprimir en cualquier carpeta
    echo 2. Ejecutar AsistenciaJOLG.exe
    echo 3. No requiere instalación
    echo.
) else (
    echo ❌ Error creando ZIP
)

echo ========================================
echo    RESUMEN DE OPCIONES DISPONIBLES
echo ========================================
echo.
echo 1. PAQUETE ZIP (LISTO) ✅
echo    - Archivo: setup_output\AsistenciaJOLG_Portable_v1.0.0.zip
echo    - Uso: Descomprimir y ejecutar
echo    - Tamaño: ~30-50 MB
echo.
echo 2. INSTALADOR EXE (REQUIERE HERRAMIENTAS):
echo.
echo    a) INNO SETUP (RECOMENDADO - GRATUITO)
echo       - Descarga: https://jrsoftware.org/isdl.php
echo       - Archivo listo: setup_script.iss
echo       - Comando: crear_instalador.bat
echo.
echo    b) NSIS (ALTERNATIVO - GRATUITO) 
echo       - Descarga: https://nsis.sourceforge.io/
echo       - Archivo listo: installer_nsis.nsi
echo       - Compilar manualmente
echo.
echo    c) ADVANCED INSTALLER (PROFESIONAL)
echo       - Descarga: https://www.advancedinstaller.com/
echo       - Version gratuita limitada
echo.
echo ========================================
pause
