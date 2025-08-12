"""
Módulo de interfaz de usuario para el Sistema de Asistencia JOLG
Diseño moderno y elegante
"""

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                           QPushButton, QLabel, QTextEdit, QLineEdit, QComboBox, QFrame,
                           QProgressBar, QMessageBox, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor


class ModernButton(QPushButton):
    """Botón con estilo moderno oscuro"""
    
    def __init__(self, text, color="#0078d4"):
        super().__init__(text)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;i
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: 600;
                min-height: 25px;
            }}
            QPushButton:hover {{
                background-color: {self._darker_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darkest_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #555555;
                color: #999999;
            }}
        """)
    
    def _darker_color(self, color):
        """Genera un color más oscuro"""
        colors = {
            "#0078d4": "#106ebe",
            "#28a745": "#1e7e34",
            "#dc3545": "#c82333",
            "#ffc107": "#e0a800"
        }
        return colors.get(color, "#333333")
    
    def _darkest_color(self, color):
        """Genera el color más oscuro"""
        colors = {
            "#0078d4": "#005a9e",
            "#28a745": "#155724",
            "#dc3545": "#bd2130",
            "#ffc107": "#d39e00"
        }
        return colors.get(color, "#222222")


class ModernComboBox(QComboBox):
    """ComboBox con estilo oscuro moderno"""
    
    def __init__(self, items=None, placeholder="Seleccionar..."):
        super().__init__()
        self.placeholder = placeholder
        
        # Agregar placeholder como primer item
        if placeholder:
            self.addItem(placeholder)
            
        if items:
            self.addItems(items)
        
        # Conectar evento para manejar placeholder
        self.currentIndexChanged.connect(self.handle_selection)
            
        self.setStyleSheet("""
            QComboBox {
                border: 2px solid #444444;
                border-radius: 12px;
                padding: 15px 20px;
                font-size: 16px;
                background-color: #2d2d2d;
                color: white;
                min-width: 250px;
                min-height: 25px;
            }
            QComboBox:focus {
                border-color: #0078d4;
                outline: none;
            }
            QComboBox:hover {
                border-color: #666666;
                background-color: #3d3d3d;
            }
            QComboBox::drop-down {
                border: none;
                width: 40px;
                background-color: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid white;
                margin-right: 15px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #444444;
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #0078d4;
                selection-color: white;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 12px;
                border-bottom: 1px solid #444444;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #3d3d3d;
            }
        """)

    def handle_selection(self, index):
        """Maneja la selección del ComboBox para el placeholder"""
        if hasattr(self, 'placeholder') and self.placeholder:
            if index == 0 and self.itemText(0) == self.placeholder:
                # Si selecciona el placeholder, mantener la selección pero no como válida
                return
    
    def get_selected_value(self):
        """Obtiene el valor seleccionado, excluyendo el placeholder"""
        current_text = self.currentText()
        if hasattr(self, 'placeholder') and current_text == self.placeholder:
            return None
        return current_text


class ModernTextArea(QTextEdit):
    """Área de texto con estilo oscuro moderno"""
    
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMaximumHeight(100)
        self.setStyleSheet("""
            QTextEdit {
                border: 2px solid #444444;
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 13px;
                background-color: #2d2d2d;
                color: white;
            }
            QTextEdit:focus {
                border-color: #0078d4;
                outline: none;
            }
            QTextEdit:hover {
                border-color: #666666;
                background-color: #3d3d3d;
            }
        """)


class CameraFrame(QFrame):
    """Frame de cámara con estilo oscuro moderno"""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: 2px solid #444444;
                border-radius: 15px;
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
                color: #0078d4;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                min-height: 260px;
            }
        """)
        
        layout.addWidget(self.camera_label)
        self.setLayout(layout)


class StatusBar(QFrame):
    """Barra de estado oscura moderna"""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-top: 1px solid #444444;
                padding: 8px;
            }
        """)
        self.setMaximumHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)
        
        self.status_label = QLabel("Listo para registrar asistencia")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #0078d4;
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
                background-color: #2d2d2d;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
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
            "info": "#0078d4"
        }
        
        color = colors.get(status_type, "#0078d4")
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
        self.setWindowTitle('ASISTENCIA JOLG - Sistema de Registro')
        self.setGeometry(100, 100, 1100, 750)
        self.setMinimumSize(900, 650)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 0)
        main_layout.setSpacing(20)
        central_widget.setLayout(main_layout)
        
        # Contenido principal (sin header)
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
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #0078d4, stop: 1 #005a9e);
                border-radius: 15px;
                min-height: 100px;
                max-height: 100px;
            }
        """)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(40, 25, 40, 25)
        
        # Título principal grande y visible
        title_label = QLabel("ASISTENCIA JOLG")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                letter-spacing: 2px;
            }
        """)
        
        # Subtítulo
        subtitle_label = QLabel("Sistema de Registro de Personal")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: normal;
            }
        """)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(8)
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
                background-color: #1e1e1e;
                border: 2px solid #444444;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        controls_frame.setMaximumWidth(380)
        controls_frame.setMinimumWidth(380)
        
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(25)
        controls_layout.setContentsMargins(25, 25, 25, 25)
        
        # Título del panel
        panel_title = QLabel("ASISTENCIA JOLG")
        panel_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #0078d4;
                margin-bottom: 20px;
                padding: 15px 0px;
                text-align: center;
            }
        """)
        panel_title.setAlignment(Qt.AlignCenter)
        controls_layout.addWidget(panel_title)
        
        # ComboBox sin label (con placeholder incorporado)
        self.personal_id_combo = ModernComboBox(["TIENDA1", "TIENDA2", "TIENDA3"], "Seleccionar Personal ID")
        controls_layout.addWidget(self.personal_id_combo)
        
        # TextArea sin label (con placeholder incorporado)
        self.observaciones_input = ModernTextArea("Escriba observaciones opcionales...")
        controls_layout.addWidget(self.observaciones_input)
        
        # Espaciado
        controls_layout.addSpacing(20)
        
        # Botón registrar con nuevo color
        self.btn_registrar = ModernButton("📸 REGISTRAR ASISTENCIA", "#28a745")
        self.btn_registrar.setMinimumHeight(60)
        controls_layout.addWidget(self.btn_registrar)
        
        # Disclaimer
        disclaimer = QLabel("⚠️ IMPORTANTE: Registre su asistencia a primera hora del día")
        disclaimer.setStyleSheet("""
            QLabel {
                color: #ffc107;
                font-size: 12px;
                font-weight: 600;
                margin-top: 15px;
                margin-bottom: 10px;
                padding: 10px;
                background-color: rgba(255, 193, 7, 0.1);
                border: 1px solid #ffc107;
                border-radius: 8px;
                text-align: center;
            }
        """)
        disclaimer.setAlignment(Qt.AlignCenter)
        disclaimer.setWordWrap(True)
        controls_layout.addWidget(disclaimer)
        
        # Spacer
        controls_layout.addStretch()
        
        controls_frame.setLayout(controls_layout)
        layout.addWidget(controls_frame, 1)
    
    def setup_styles(self):
        """Configura los estilos globales oscuros"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: white;
            }
            QLabel {
                color: #cccccc;
                font-size: 14px;
            }
        """)
    
    def get_camera_label(self):
        """Retorna el label de la cámara para actualizaciones"""
        return self.camera_frame.camera_label
    
    def get_personal_id(self):
        """Obtiene el ID personal seleccionado"""
        return self.personal_id_combo.get_selected_value()
    
    def get_observaciones(self):
        """Obtiene las observaciones ingresadas"""
        return self.observaciones_input.toPlainText().strip()
    
    def clear_inputs(self):
        """Limpia los campos de entrada"""
        self.observaciones_input.clear()
        # No reseteamos el combo porque el usuario puede querer el mismo
    
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
