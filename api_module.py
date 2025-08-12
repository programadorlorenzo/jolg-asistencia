"""
Módulo de manejo de API para el Sistema de Asistencia JOLG
"""

import os
import requests
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal


class APIClient:
    """Cliente para manejar las llamadas a la API"""
    
    def __init__(self):
        self.base_url = "https://backend-admin.consorciolorenzo.com"
        self.upload_endpoint = f"{self.base_url}/files/file"
        self.asistencia_endpoint = f"{self.base_url}/asistencias_jolg"
        self.timeout = 30
    
    def upload_file(self, file_path):
        """
        Sube un archivo al servidor
        
        Args:
            file_path (str): Ruta del archivo a subir
            
        Returns:
            tuple: (success: bool, result: str or dict)
        """
        try:
            if not os.path.exists(file_path):
                return False, "Archivo no encontrado"
            
            with open(file_path, 'rb') as file:
                files = {
                    'file': (os.path.basename(file_path), file, 'image/jpeg')
                }
                
                headers = {
                    'accept': '*/*'
                }
                
                response = requests.put(
                    self.upload_endpoint,
                    files=files,
                    headers=headers,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                
                # Asumir que el servidor retorna la ruta del archivo
                if response.text:
                    return True, response.text.strip('"')  # Remover comillas si las hay
                else:
                    return True, response.json() if response.content else "files/uploaded"
                    
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def register_asistencia(self, personal_id, observaciones, foto_ruta, fecha_hora=None):
        """
        Registra asistencia en el servidor
        
        Args:
            personal_id (str): ID del personal (TIENDA1, TIENDA2, TIENDA3)
            observaciones (str): Observaciones
            foto_ruta (str): Ruta de la foto subida
            fecha_hora (str): Fecha y hora de registro
            
        Returns:
            tuple: (success: bool, result: str or dict)
        """
        try:
            if fecha_hora is None:
                # Formato ISO 8601 con timezone UTC
                fecha_hora = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "Z"
            
            # Convertir personalID a número según la tienda
            personal_id_map = {
                "TIENDA1": 1,
                "TIENDA2": 2, 
                "TIENDA3": 3
            }
            
            personal_id_num = personal_id_map.get(personal_id, 1)
            
            data = {
                "personalID": personal_id_num,  # Ahora es número
                "observaciones": observaciones if observaciones else "",
                "fotoRuta": foto_ruta,
                "fechaHoraRegistro": fecha_hora
            }
            
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            print(f"DEBUG: Enviando datos: {data}")  # Para debug
            
            response = requests.post(
                self.asistencia_endpoint,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            
            print(f"DEBUG: Response status: {response.status_code}")  # Para debug
            print(f"DEBUG: Response body: {response.text}")  # Para debug
            
            response.raise_for_status()
            return True, response.json() if response.content else "Asistencia registrada"
            
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"


class AsistenciaWorker(QThread):
    """Worker thread para manejar el registro de asistencia sin bloquear la UI"""
    
    finished = pyqtSignal(bool, str)  # success, message
    progress = pyqtSignal(str)  # status message
    
    def __init__(self, personal_id, observaciones, foto_path):
        super().__init__()
        self.personal_id = personal_id
        self.observaciones = observaciones
        self.foto_path = foto_path
        self.api_client = APIClient()
    
    def run(self):
        """Ejecuta el proceso de registro de asistencia"""
        try:
            # Paso 1: Subir archivo
            self.progress.emit("Subiendo foto...")
            success, result = self.api_client.upload_file(self.foto_path)
            
            if not success:
                self.finished.emit(False, f"Error subiendo foto: {result}")
                return
            
            foto_ruta = result
            self.progress.emit("Foto subida exitosamente...")
            
            # Paso 2: Registrar asistencia
            self.progress.emit("Registrando asistencia...")
            success, result = self.api_client.register_asistencia(
                self.personal_id,
                self.observaciones,
                foto_ruta
            )
            
            if success:
                self.finished.emit(True, "Asistencia registrada exitosamente")
            else:
                self.finished.emit(False, f"Error registrando asistencia: {result}")
                
        except Exception as e:
            self.finished.emit(False, f"Error inesperado: {str(e)}")


class LocalStorage:
    """Maneja el almacenamiento local de registros"""
    
    def __init__(self, storage_file="asistencia_local.json"):
        self.storage_file = storage_file
    
    def save_record(self, personal_id, observaciones, foto_path, sent=False):
        """Guarda un registro localmente"""
        import json
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "personalID": personal_id,
            "observaciones": observaciones,
            "foto_path": foto_path,
            "sent": sent
        }
        
        records = self.load_records()
        records.append(record)
        
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def load_records(self):
        """Carga registros desde archivo local"""
        import json
        
        if not os.path.exists(self.storage_file):
            return []
        
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def get_pending_records(self):
        """Obtiene registros pendientes de envío"""
        records = self.load_records()
        return [r for r in records if not r.get('sent', False)]
    
    def mark_as_sent(self, timestamp):
        """Marca un registro como enviado"""
        import json
        
        records = self.load_records()
        for record in records:
            if record.get('timestamp') == timestamp:
                record['sent'] = True
                break
        
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
