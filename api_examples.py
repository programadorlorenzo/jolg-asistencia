"""
Ejemplos de configuración y uso de la API para el Sistema de Asistencia JOLG
"""

import requests
import json
from datetime import datetime


# Ejemplo 1: Configuración básica de la API
API_CONFIG = {
    "url": "https://api.ejemplo.com/asistencia",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer tu-token-aqui"  # Si usa autenticación
    }
}


# Ejemplo 2: DTO que se envía a la API
def crear_dto_asistencia(usuario_jolg, observaciones=""):
    """Crea un DTO de asistencia para enviar a la API"""
    return {
        "observaciones": observaciones,
        "usuarioJolg": usuario_jolg,
        "timestamp": datetime.now().isoformat()
    }


# Ejemplo 3: Función para enviar asistencia a la API
def enviar_asistencia_api(usuario_jolg, observaciones=""):
    """
    Envía una asistencia a la API
    
    Args:
        usuario_jolg (str): Usuario JOLG
        observaciones (str): Observaciones opcionales
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        dto = crear_dto_asistencia(usuario_jolg, observaciones)
        
        response = requests.post(
            API_CONFIG["url"],
            json=dto,
            headers=API_CONFIG["headers"],
            timeout=10
        )
        
        response.raise_for_status()
        
        return True, "Asistencia enviada exitosamente"
        
    except requests.exceptions.RequestException as e:
        return False, f"Error de conexión: {str(e)}"
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"


# Ejemplo 4: Simulación de API para pruebas locales
def simular_api_local():
    """
    Simula una API local para pruebas
    Usar con flask o fastapi para pruebas
    """
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/asistencia', methods=['POST'])
    def registrar_asistencia():
        try:
            data = request.get_json()
            
            # Validar campos requeridos
            if not data.get('usuarioJolg'):
                return jsonify({"error": "usuarioJolg es requerido"}), 400
            
            # Simular guardado en base de datos
            print(f"Asistencia recibida: {data}")
            
            return jsonify({
                "success": True,
                "message": "Asistencia registrada",
                "id": "12345"
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app


# Ejemplo 5: Configuración para diferentes entornos
CONFIGS = {
    "desarrollo": {
        "url": "http://localhost:5000/asistencia",
        "timeout": 30
    },
    "pruebas": {
        "url": "https://api-test.empresa.com/asistencia",
        "timeout": 15
    },
    "produccion": {
        "url": "https://api.empresa.com/asistencia",
        "timeout": 10
    }
}


def obtener_config(entorno="desarrollo"):
    """Obtiene la configuración según el entorno"""
    return CONFIGS.get(entorno, CONFIGS["desarrollo"])


# Ejemplo 6: Prueba de conexión con la API
def probar_conexion_api(url):
    """
    Prueba la conexión con la API
    
    Args:
        url (str): URL de la API
    
    Returns:
        bool: True si la conexión es exitosa
    """
    try:
        # Intentar un GET al endpoint base
        response = requests.get(url.replace('/asistencia', '/health'), timeout=5)
        return response.status_code == 200
    except:
        try:
            # Si no hay endpoint health, probar con OPTIONS
            response = requests.options(url, timeout=5)
            return response.status_code in [200, 204, 405]
        except:
            return False


# Ejemplo 7: Uso en la aplicación principal
if __name__ == "__main__":
    # Ejemplo de uso
    print("=== Prueba de API ===")
    
    # Configurar para desarrollo
    config = obtener_config("desarrollo")
    API_CONFIG.update(config)
    
    # Probar conexión
    if probar_conexion_api(API_CONFIG["url"]):
        print("✅ API accesible")
    else:
        print("❌ API no accesible")
    
    # Probar envío
    success, message = enviar_asistencia_api(
        usuario_jolg="user123",
        observaciones="Prueba desde script"
    )
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")


# Ejemplo 8: Configuración avanzada con autenticación
API_CONFIG_AVANZADA = {
    "url": "https://api.empresa.com/v1/asistencia",
    "headers": {
        "Content-Type": "application/json",
        "User-Agent": "SistemaAsistenciaJOLG/1.0",
        "X-API-Key": "tu-api-key-aqui"
    },
    "auth": {
        "type": "bearer",  # o "basic"
        "token": "tu-token-jwt-aqui"
    },
    "timeout": 10,
    "retries": 3
}
