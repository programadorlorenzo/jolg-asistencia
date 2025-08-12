"""
Módulo de manejo de cámara para el Sistema de Asistencia JOLG
"""

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage


class CameraThread(QThread):
    """Hilo para manejar la captura de video de la cámara"""
    changePixmap = pyqtSignal(QImage)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, camera_id=0):
        super().__init__()
        self.camera_id = camera_id
        self.camera = None
        self.running = False
        self.current_frame = None
    
    def run(self):
        """Ejecuta la captura de video"""
        try:
            self.camera = cv2.VideoCapture(self.camera_id)
            if not self.camera.isOpened():
                self.error_occurred.emit("No se puede acceder a la cámara")
                return
            
            # Configurar resolución
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            self.running = True
            
            while self.running:
                ret, frame = self.camera.read()
                if ret:
                    self.current_frame = frame.copy()
                    # Convertir frame de BGR a RGB
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    
                    # Crear QImage
                    qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    self.changePixmap.emit(qt_image)
                else:
                    self.error_occurred.emit("Error leyendo de la cámara")
                    break
                    
        except Exception as e:
            self.error_occurred.emit(f"Error en cámara: {str(e)}")
    
    def get_current_frame(self):
        """Obtiene el frame actual"""
        return self.current_frame.copy() if self.current_frame is not None else None
    
    def capture_photo(self, filename):
        """Captura una foto y la guarda"""
        if self.current_frame is not None:
            try:
                cv2.imwrite(filename, self.current_frame)
                return True
            except Exception as e:
                self.error_occurred.emit(f"Error guardando foto: {str(e)}")
                return False
        return False
    
    def stop(self):
        """Detiene la captura de video"""
        self.running = False
        if self.camera:
            self.camera.release()
        self.quit()
        self.wait()  # Esperar a que termine el hilo


class CameraManager:
    """Administrador de cámara simplificado"""
    
    def __init__(self):
        self.camera_thread = None
    
    def start_camera(self, camera_id=0):
        """Inicia la cámara"""
        if self.camera_thread is None:
            self.camera_thread = CameraThread(camera_id)
        return self.camera_thread
    
    def stop_camera(self):
        """Detiene la cámara"""
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_thread = None
    
    def capture_photo(self, filename):
        """Captura una foto"""
        if self.camera_thread:
            return self.camera_thread.capture_photo(filename)
        return False
