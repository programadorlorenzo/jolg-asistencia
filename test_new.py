#!/usr/bin/env python3
"""
Script de prueba mejorado para verificar el Sistema de Asistencia JOLG
"""

import sys
import os
import requests
from datetime import datetime

def test_dependencies():
    """Prueba que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    dependencies = [
        ("PyQt5", "PyQt5"),
        ("OpenCV", "cv2"),
        ("Requests", "requests"),
        ("NumPy", "numpy")
    ]
    
    all_ok = True
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - No instalado")
            all_ok = False
    
    return all_ok


def test_camera():
    """Prueba que la cámara esté disponible"""
    print("\n📷 Verificando cámara...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("  ❌ No se puede acceder a la cámara")
            return False
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            h, w = frame.shape[:2]
            print(f"  ✅ Cámara funcionando - Resolución: {w}x{h}")
            return True
        else:
            print("  ❌ No se puede leer desde la cámara")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_api_connection():
    """Prueba la conexión con la API"""
    print("\n🌐 Verificando conexión API...")
    
    base_url = "https://backend-admin.consorciolorenzo.com"
    
    try:
        # Probar conexión básica
        response = requests.get(base_url, timeout=5)
        print(f"  ✅ Servidor accesible - Status: {response.status_code}")
        return True
        
    except requests.exceptions.ConnectionError:
        print("  ❌ No se puede conectar al servidor")
        return False
    except requests.exceptions.Timeout:
        print("  ❌ Timeout de conexión")
        return False
    except Exception as e:
        print(f"  ⚠️ Error de conexión: {e}")
        return False


def test_modules():
    """Prueba los módulos personalizados"""
    print("\n📦 Verificando módulos del sistema...")
    
    modules = [
        ("UI Module", "ui_module"),
        ("Camera Module", "camera_module"), 
        ("API Module", "api_module")
    ]
    
    all_ok = True
    for name, module in modules:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError as e:
            print(f"  ❌ {name} - Error: {e}")
            all_ok = False
        except Exception as e:
            print(f"  ⚠️ {name} - Advertencia: {e}")
    
    return all_ok


def test_file_structure():
    """Verifica la estructura de archivos"""
    print("\n📁 Verificando estructura de archivos...")
    
    required_files = [
        "main.py",
        "ui_module.py", 
        "camera_module.py",
        "api_module.py",
        "config.json",
        "requirements.txt"
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - No encontrado")
            all_ok = False
    
    return all_ok


def create_test_directories():
    """Crea directorios de prueba"""
    print("\n📂 Creando directorios...")
    
    directories = ["fotos", "temp", "logs"]
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"  ✅ {directory}/")
        except Exception as e:
            print(f"  ❌ Error creando {directory}: {e}")


def run_quick_ui_test():
    """Ejecuta una prueba rápida de la UI"""
    print("\n🖥️ Prueba rápida de interfaz...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui_module import AsistenciaUI
        
        # Crear aplicación sin mostrar ventana
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Crear UI
        ui = AsistenciaUI()
        print("  ✅ UI creada correctamente")
        
        # No mostrar la ventana, solo verificar que se puede crear
        ui.close()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en UI: {e}")
        return False


def main():
    """Función principal de pruebas"""
    print("=" * 50)
    print("🧪 PRUEBAS DEL SISTEMA DE ASISTENCIA JOLG")
    print("=" * 50)
    
    tests = [
        ("Dependencias", test_dependencies),
        ("Estructura de archivos", test_file_structure),
        ("Módulos del sistema", test_modules),
        ("Cámara", test_camera),
        ("Conexión API", test_api_connection),
        ("Interfaz de usuario", run_quick_ui_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error en prueba '{test_name}': {e}")
            results.append((test_name, False))
    
    # Crear directorios
    create_test_directories()
    
    # Resumen de resultados
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n📊 Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
        print("\n📋 Siguiente paso:")
        print("   python main.py")
    else:
        print(f"\n⚠️ {total - passed} prueba(s) fallaron. Revise los errores arriba.")
        print("\n🔧 Soluciones comunes:")
        print("   - Ejecutar: python install.py")
        print("   - Verificar conexión a internet")
        print("   - Verificar cámara conectada")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
