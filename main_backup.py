#!/usr/bin/env python3
"""
Sistema de Asistencia JOLG
Aplicación PyQt5 para registrar asistencia con cámara web
"""

import sys
import cv2
import json
import os
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QPushButton, QLabel, QTextEdit, QMessageBox,
                           QLineEdit, QGroupBox, QGridLayout)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QFont
import requests


class CameraThread(QThread):
    """Hilo para manejar la captura de video de la cámara"""
    changePixmap = pyqtSignal(QImage)
    
    def __init__(self):
        super().__init__()
        self.camera = None
        self.running = False
    
    def run(self):
        """Ejecuta la captura de video"""
        self.camera = cv2.VideoCapture(0)
        self.running = True
        
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                # Convertir frame de BGR a RGB
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                
                # Crear QImage
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.changePixmap.emit(qt_image)
    
    def stop(self):
        """Detiene la captura de video"""
        self.running = False
        if self.camera:
            self.camera.release()
        self.quit()


class AsistenciaManager:
    """Maneja el almacenamiento local y envío a API"""
    
    def __init__(self):
        self.local_file = "asistencia_local.json"
        self.api_url = "https://api.example.com/asistencia"  # Cambiar por tu API real
    
    def guardar_local(self, observaciones, usuario_jolg, foto_path=None):
        """Guarda la asistencia localmente"""
        timestamp = datetime.now().isoformat()
        
        registro = {
            "timestamp": timestamp,
            "observaciones": observaciones,
            "usuarioJolg": usuario_jolg,
            "foto": foto_path,
            "enviado": False
        }
        
        # Cargar registros existentes
        registros = []
        if os.path.exists(self.local_file):
            try:
                with open(self.local_file, 'r', encoding='utf-8') as f:
                    registros = json.load(f)
            except:
                registros = []
        
        # Agregar nuevo registro
        registros.append(registro)
        
        # Guardar todos los registros
        with open(self.local_file, 'w', encoding='utf-8') as f:
            json.dump(registros, f, indent=2, ensure_ascii=False)
        
        return registro
    
    def enviar_a_api(self, registro):
        """Envía el registro a la API"""
        try:
            # DTO para la API
            dto = {
                "observaciones": registro["observaciones"],
                "usuarioJolg": registro["usuarioJolg"],
                "timestamp": registro["timestamp"]
            }
            
            response = requests.post(self.api_url, json=dto, timeout=10)
            response.raise_for_status()
            
            # Marcar como enviado
            self.marcar_como_enviado(registro["timestamp"])
            return True, "Enviado exitosamente"
            
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def marcar_como_enviado(self, timestamp):
        """Marca un registro como enviado"""
        if not os.path.exists(self.local_file):
            return
        
        try:
            with open(self.local_file, 'r', encoding='utf-8') as f:
                registros = json.load(f)
            
            for registro in registros:
                if registro["timestamp"] == timestamp:
                    registro["enviado"] = True
                    break
            
            with open(self.local_file, 'w', encoding='utf-8') as f:
                json.dump(registros, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def obtener_pendientes(self):
        """Obtiene registros pendientes de envío"""
        if not os.path.exists(self.local_file):
            return []
        
        try:
            with open(self.local_file, 'r', encoding='utf-8') as f:
                registros = json.load(f)
            return [r for r in registros if not r.get("enviado", False)]
        except:
            return []


class AsistenciaApp(QMainWindow):
    """Aplicación principal de asistencia"""
    
    def __init__(self):
        super().__init__()
        self.asistencia_manager = AsistenciaManager()
        self.camera_thread = None
        self.current_frame = None
        self.initUI()
        self.setup_camera()
    
    def initUI(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle('Sistema de Asistencia JOLG')
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Panel izquierdo - Cámara
        camera_group = QGroupBox("Cámara")
        camera_layout = QVBoxLayout()
        
        self.camera_label = QLabel("Iniciando cámara...")
        self.camera_label.setMinimumSize(400, 300)
        self.camera_label.setStyleSheet("border: 2px solid gray; background-color: black;")
        camera_layout.addWidget(self.camera_label)
        
        camera_group.setLayout(camera_layout)
        main_layout.addWidget(camera_group)
        
        # Panel derecho - Controles
        controls_group = QGroupBox("Registro de Asistencia")
        controls_layout = QVBoxLayout()
        
        # Campo Usuario JOLG
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Usuario JOLG:"))
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Ingrese su usuario JOLG")
        user_layout.addWidget(self.usuario_input)
        controls_layout.addLayout(user_layout)
        
        # Campo Observaciones
        controls_layout.addWidget(QLabel("Observaciones:"))
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(100)
        self.observaciones_input.setPlaceholderText("Ingrese observaciones (opcional)")
        controls_layout.addWidget(self.observaciones_input)
        
        # Botón registrar
        self.btn_registrar = QPushButton("📸 Registrar Asistencia")
        self.btn_registrar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.btn_registrar.clicked.connect(self.registrar_asistencia)
        controls_layout.addWidget(self.btn_registrar)
        
        # Botón enviar pendientes
        self.btn_enviar = QPushButton("🌐 Enviar Pendientes a API")
        self.btn_enviar.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 12px;
                padding: 8px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.btn_enviar.clicked.connect(self.enviar_pendientes)
        controls_layout.addWidget(self.btn_enviar)
        
        # Estado
        self.status_label = QLabel("Listo para registrar asistencia")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        controls_layout.addWidget(self.status_label)
        
        controls_group.setLayout(controls_layout)
        main_layout.addWidget(controls_group)
    
    def setup_camera(self):
        """Configura e inicia la cámara"""
        self.camera_thread = CameraThread()
        self.camera_thread.changePixmap.connect(self.update_image)
        self.camera_thread.start()
    
    def update_image(self, qt_image):
        """Actualiza la imagen de la cámara"""
        self.current_frame = qt_image
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.camera_label.size(), aspectRatioMode=1)
        self.camera_label.setPixmap(scaled_pixmap)
    
    def registrar_asistencia(self):
        """Registra la asistencia"""
        usuario = self.usuario_input.text().strip()
        observaciones = self.observaciones_input.toPlainText().strip()
        
        if not usuario:
            QMessageBox.warning(self, "Error", "Por favor ingrese el usuario JOLG")
            return
        
        if not self.current_frame:
            QMessageBox.warning(self, "Error", "No hay imagen de cámara disponible")
            return
        
        try:
            # Guardar foto
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            foto_filename = f"foto_{usuario}_{timestamp}.jpg"
            foto_path = os.path.join("fotos", foto_filename)
            
            # Crear directorio si no existe
            os.makedirs("fotos", exist_ok=True)
            
            # Convertir QImage a formato que OpenCV pueda guardar
            w = self.current_frame.width()
            h = self.current_frame.height()
            
            # Convertir QImage a array numpy
            ptr = self.current_frame.bits()
            ptr.setsize(h * w * 3)
            arr = np.frombuffer(ptr, np.uint8).reshape((h, w, 3))
            
            # Convertir RGB a BGR para OpenCV
            bgr_image = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            cv2.imwrite(foto_path, bgr_image)
            
            # Guardar registro localmente
            registro = self.asistencia_manager.guardar_local(
                observaciones, usuario, foto_path
            )
            
            # Intentar enviar inmediatamente
            enviado, mensaje = self.asistencia_manager.enviar_a_api(registro)
            
            if enviado:
                self.status_label.setText("✅ Asistencia registrada y enviada")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                QMessageBox.information(self, "Éxito", 
                    f"Asistencia registrada correctamente para {usuario}")
            else:
                self.status_label.setText("⚠️ Registrado localmente (sin conexión)")
                self.status_label.setStyleSheet("color: orange; font-weight: bold;")
                QMessageBox.warning(self, "Guardado Local", 
                    f"Asistencia guardada localmente. Error de conexión: {mensaje}")
            
            # Limpiar campos
            self.observaciones_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar asistencia: {str(e)}")
            self.status_label.setText("❌ Error al registrar")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
    
    def enviar_pendientes(self):
        """Envía registros pendientes a la API"""
        pendientes = self.asistencia_manager.obtener_pendientes()
        
        if not pendientes:
            QMessageBox.information(self, "Info", "No hay registros pendientes para enviar")
            return
        
        enviados = 0
        for registro in pendientes:
            enviado, mensaje = self.asistencia_manager.enviar_a_api(registro)
            if enviado:
                enviados += 1
        
        if enviados > 0:
            QMessageBox.information(self, "Éxito", 
                f"Se enviaron {enviados} de {len(pendientes)} registros")
            self.status_label.setText(f"✅ {enviados} registros enviados")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            QMessageBox.warning(self, "Error", 
                "No se pudo enviar ningún registro. Verifique la conexión.")
    
    def closeEvent(self, event):
        """Maneja el cierre de la aplicación"""
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_thread.wait()
        event.accept()


def main():
    """Función principal"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    window = AsistenciaApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Ejecute 'python install.py' para instalar las dependencias")
        input("Presione Enter para salir...")
    except Exception as e:
        print(f"Error inesperado: {e}")
        input("Presione Enter para salir...")
