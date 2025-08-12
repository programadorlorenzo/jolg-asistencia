"""
Módulo de interfaz de usuario para el Sistema de Asistencia JOLG
Diseño moderno y elegante
"""

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                           QPushButton, QLabel, QTextEdit, QLineEdit, QFrame,
                           QProgressBar, QMessageBox, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor


class ModernButton(QPushButton):
    """Botón con estilo moderno"""
    
    def __init__(self, text, color="#4CAF50"):
        super().__init__(text)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {self._darker_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darkest_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
    
    def _darker_color(self, color):
        """Genera un color más oscuro"""
        colors = {
            "#4CAF50": "#45a049",
            "#2196F3": "#1976D2", 
            "#FF9800": "#F57C00",
            "#f44336": "#d32f2f"
        }
        return colors.get(color, "#333333")
    
    def _darkest_color(self, color):
        """Genera el color más oscuro"""
        colors = {
            "#4CAF50": "#3d8b40",
            "#2196F3": "#1565C0",
            "#FF9800": "#E65100", 
            "#f44336": "#b71c1c"
        }
        return colors.get(color, "#222222")


class ModernInput(QLineEdit):
    """Input con estilo moderno"""
    
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #bdbdbd;
            }
        """)


class ModernTextArea(QTextEdit):
    """Área de texto con estilo moderno"""
    
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMaximumHeight(80)
        self.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                background-color: white;
            }
            QTextEdit:focus {
                border-color: #2196F3;
                outline: none;
            }
            QTextEdit:hover {
                border-color: #bdbdbd;
            }
        """)


class CameraFrame(QFrame):
    """Frame de cámara con estilo moderno"""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
            }
        """)
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.camera_label = QLabel("Iniciando cámara...")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("""
            QLabel {
                background-color: #000000;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                min-height: 260px;
            }
        """)
        
        layout.addWidget(self.camera_label)
        self.setLayout(layout)


class StatusBar(QFrame):
    """Barra de estado moderna"""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-top: 1px solid #e0e0e0;
                padding: 8px;
            }
        """)
        self.setMaximumHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)
        
        self.status_label = QLabel("Listo para registrar asistencia")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #28a745;
                font-weight: 600;
                font-size: 14px;
            }
        """)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                text-align: center;
                height: 20px;
                background-color: #e0e0e0;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 4px;
            }
        """)
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def set_status(self, message, status_type="info"):
        """Establece el mensaje de estado"""
        colors = {
            "success": "#28a745",
            "error": "#dc3545", 
            "warning": "#ffc107",
            "info": "#17a2b8"
        }
        
        color = colors.get(status_type, "#28a745")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-weight: 600;
                font-size: 14px;
            }}
        """)
        self.status_label.setText(message)
    
    def show_progress(self):
        """Muestra la barra de progreso"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminado
    
    def hide_progress(self):
        """Oculta la barra de progreso"""
        self.progress_bar.setVisible(False)


class AsistenciaUI(QMainWindow):
    """Interfaz principal moderna y elegante"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_styles()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle('Sistema de Asistencia JOLG')
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 0)
        main_layout.setSpacing(20)
        central_widget.setLayout(main_layout)
        
        # Header
        self.create_header(main_layout)
        
        # Contenido principal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        
        # Panel izquierdo - Cámara
        self.camera_frame = CameraFrame()
        content_layout.addWidget(self.camera_frame, 2)
        
        # Panel derecho - Controles
        self.create_controls_panel(content_layout)
        
        main_layout.addLayout(content_layout)
        
        # Barra de estado
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)
    
    def create_header(self, layout):
        """Crea el header de la aplicación"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2196F3;
                border-radius: 12px;
                min-height: 80px;
                max-height: 80px;
            }
        """)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(30, 20, 30, 20)
        
        title_label = QLabel("Sistema de Asistencia JOLG")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        
        subtitle_label = QLabel("Registro de asistencia con cámara")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
            }
        """)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
    
    def create_controls_panel(self, layout):
        """Crea el panel de controles"""
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        controls_frame.setMaximumWidth(350)
        controls_frame.setMinimumWidth(350)
        
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(20)
        controls_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título del panel
        panel_title = QLabel("Registro de Asistencia")
        panel_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
        """)
        controls_layout.addWidget(panel_title)
        
        # Campo Personal ID
        self.personal_id_input = ModernInput("Ingrese su ID de personal")
        controls_layout.addWidget(QLabel("ID Personal:"))
        controls_layout.addWidget(self.personal_id_input)
        
        # Campo Observaciones
        controls_layout.addWidget(QLabel("Observaciones:"))
        self.observaciones_input = ModernTextArea("Observaciones opcionales...")
        controls_layout.addWidget(self.observaciones_input)
        
        # Botones
        self.btn_registrar = ModernButton("📸 Registrar Asistencia", "#4CAF50")
        self.btn_registrar.setMinimumHeight(50)
        controls_layout.addWidget(self.btn_registrar)
        
        # Spacer
        controls_layout.addStretch()
        
        controls_frame.setLayout(controls_layout)
        layout.addWidget(controls_frame, 1)
    
    def setup_styles(self):
        """Configura los estilos globales"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
        """)
    
    def get_camera_label(self):
        """Retorna el label de la cámara para actualizaciones"""
        return self.camera_frame.camera_label
    
    def get_personal_id(self):
        """Obtiene el ID personal ingresado"""
        return self.personal_id_input.text().strip()
    
    def get_observaciones(self):
        """Obtiene las observaciones ingresadas"""
        return self.observaciones_input.toPlainText().strip()
    
    def clear_inputs(self):
        """Limpia los campos de entrada"""
        self.observaciones_input.clear()
    
    def set_register_enabled(self, enabled):
        """Habilita/deshabilita el botón de registro"""
        self.btn_registrar.setEnabled(enabled)
    
    def show_message(self, title, message, message_type="information"):
        """Muestra un mensaje al usuario"""
        if message_type == "information":
            QMessageBox.information(self, title, message)
        elif message_type == "warning":
            QMessageBox.warning(self, title, message)
        elif message_type == "error":
            QMessageBox.critical(self, title, message)
    
    def update_status(self, message, status_type="info"):
        """Actualiza el estado en la barra inferior"""
        self.status_bar.set_status(message, status_type)
    
    def show_progress(self, message="Procesando..."):
        """Muestra progreso"""
        self.status_bar.show_progress()
        self.status_bar.set_status(message, "info")
    
    def hide_progress(self):
        """Oculta progreso"""
        self.status_bar.hide_progress()
