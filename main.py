#!/usr/bin/env python3
"""
Sistema de Asistencia JOLG - Aplicación Principal
Versión modularizada y optimizada
"""

import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap

# Importar módulos locales
from ui_module import AsistenciaUI
from camera_module import CameraManager
from api_module import AsistenciaWorker, LocalStorage


class AsistenciaApp:
    """Aplicación principal del sistema de asistencia"""
    
    def __init__(self):
        self.ui = AsistenciaUI()
        self.camera_manager = CameraManager()
        self.local_storage = LocalStorage()
        self.current_worker = None
        
        self.setup_connections()
        self.setup_camera()
        self.create_directories()
    
    def create_directories(self):
        """Crea directorios necesarios"""
        os.makedirs("fotos", exist_ok=True)
        os.makedirs("temp", exist_ok=True)
    
    def setup_connections(self):
        """Configura las conexiones de señales"""
        self.ui.btn_registrar.clicked.connect(self.registrar_asistencia)
    
    def setup_camera(self):
        """Configura e inicia la cámara"""
        try:
            print("Iniciando configuración de cámara...")
            camera_thread = self.camera_manager.start_camera()
            camera_thread.changePixmap.connect(self.update_camera_image)
            camera_thread.error_occurred.connect(self.handle_camera_error)
            print("Iniciando hilo de cámara...")
            camera_thread.start()
            print("Hilo de cámara iniciado")
            
        except Exception as e:
            print(f"Error en setup_camera: {e}")
            self.ui.update_status(f"Error iniciando cámara: {str(e)}", "error")
    
    def update_camera_image(self, qt_image):
        """Actualiza la imagen de la cámara en la UI"""
        try:
            pixmap = QPixmap.fromImage(qt_image)
            camera_label = self.ui.get_camera_label()
            scaled_pixmap = pixmap.scaled(
                camera_label.size(),
                aspectRatioMode=1,
                transformMode=1  # Smooth transformation
            )
            camera_label.setPixmap(scaled_pixmap)
            
            # Solo mostrar esto una vez
            if not hasattr(self, '_camera_started'):
                print("✅ Cámara funcionando correctamente")
                self.ui.update_status("Cámara lista", "success")
                self._camera_started = True
                
        except Exception as e:
            print(f"Error actualizando imagen: {e}")
    
    def handle_camera_error(self, error_message):
        """Maneja errores de la cámara"""
        self.ui.update_status(f"Error de cámara: {error_message}", "error")
        self.ui.show_message("Error de Cámara", error_message, "error")
    
    def registrar_asistencia(self):
        """Registra la asistencia del usuario"""
        # Validar campos
        personal_id = self.ui.get_personal_id()
        if not personal_id or not personal_id.isdigit():
            self.ui.show_message("Error", "Por favor ingrese un ID de personal válido", "warning")
            return
        
        observaciones = self.ui.get_observaciones()
        
        # Verificar que hay una imagen de cámara
        if not self.camera_manager.camera_thread or not self.camera_manager.camera_thread.current_frame is not None:
            self.ui.show_message("Error", "No hay imagen de cámara disponible", "error")
            return
        
        # Deshabilitar botón durante el proceso
        self.ui.set_register_enabled(False)
        self.ui.show_progress("Iniciando registro...")
        
        try:
            # Capturar foto
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            foto_filename = f"asistencia_{personal_id}_{timestamp}.jpg"
            foto_path = os.path.join("fotos", foto_filename)
            
            # Guardar foto
            if self.camera_manager.capture_photo(foto_path):
                self.ui.update_status("Foto capturada, enviando...", "info")
                
                # Guardar localmente primero
                self.local_storage.save_record(
                    int(personal_id), 
                    observaciones, 
                    foto_path, 
                    sent=False
                )
                
                # Iniciar proceso de envío en segundo plano
                self.current_worker = AsistenciaWorker(
                    int(personal_id),
                    observaciones,
                    foto_path
                )
                
                self.current_worker.progress.connect(self.ui.update_status)
                self.current_worker.finished.connect(self.handle_registro_finished)
                self.current_worker.start()
                
            else:
                self.ui.hide_progress()
                self.ui.set_register_enabled(True)
                self.ui.update_status("Error capturando foto", "error")
                self.ui.show_message("Error", "No se pudo capturar la foto", "error")
                
        except Exception as e:
            self.ui.hide_progress()
            self.ui.set_register_enabled(True)
            self.ui.update_status(f"Error inesperado: {str(e)}", "error")
            self.ui.show_message("Error", f"Error inesperado: {str(e)}", "error")
    
    def handle_registro_finished(self, success, message):
        """Maneja el resultado del registro de asistencia"""
        self.ui.hide_progress()
        self.ui.set_register_enabled(True)
        
        if success:
            self.ui.update_status("✅ Asistencia registrada exitosamente", "success")
            self.ui.show_message("Éxito", message, "information")
            self.ui.clear_inputs()
        else:
            self.ui.update_status(f"❌ Error: {message}", "error")
            self.ui.show_message("Error", f"Error registrando asistencia:\n{message}", "error")
        
        # Limpiar worker
        if self.current_worker:
            self.current_worker.deleteLater()
            self.current_worker = None
    
    def show(self):
        """Muestra la aplicación"""
        self.ui.show()
    
    def close(self):
        """Cierra la aplicación y limpia recursos"""
        if self.current_worker:
            self.current_worker.quit()
            self.current_worker.wait()
        
        self.camera_manager.stop_camera()
        self.ui.close()


def main():
    """Función principal"""
    try:
        # Crear aplicación
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # Estilo moderno
        
        # Configurar aplicación
        app.setApplicationName("Sistema de Asistencia JOLG")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("Consorcio Lorenzo")
        
        # Crear y mostrar ventana principal
        asistencia_app = AsistenciaApp()
        asistencia_app.show()
        
        # Ejecutar aplicación
        result = app.exec_()
        
        # Limpiar recursos
        asistencia_app.close()
        
        return result
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Ejecute 'python install.py' para instalar las dependencias")
        input("Presione Enter para salir...")
        return 1
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        input("Presione Enter para salir...")
        return 1


if __name__ == '__main__':
    sys.exit(main())
