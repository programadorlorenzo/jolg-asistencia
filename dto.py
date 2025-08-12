"""
Data Transfer Objects (DTO) para la API de Asistencia JOLG
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AsistenciaDTO:
    """
    DTO para enviar datos de asistencia a la API
    
    Estructura que se envía a la API en formato JSON:
    {
        "observaciones": "string",
        "usuarioJolg": "string",
        "timestamp": "2024-01-01T12:00:00.000Z"
    }
    """
    observaciones: str
    usuarioJolg: str
    timestamp: Optional[str] = None
    
    def to_dict(self):
        """Convierte el DTO a diccionario para JSON"""
        return {
            "observaciones": self.observaciones,
            "usuarioJolg": self.usuarioJolg,
            "timestamp": self.timestamp or datetime.now().isoformat()
        }


@dataclass
class AsistenciaLocalDTO:
    """
    DTO para almacenamiento local de asistencia
    Incluye campos adicionales para gestión local
    """
    observaciones: str
    usuarioJolg: str
    timestamp: str
    foto: Optional[str] = None
    enviado: bool = False
    
    def to_api_dto(self) -> AsistenciaDTO:
        """Convierte a DTO para API"""
        return AsistenciaDTO(
            observaciones=self.observaciones,
            usuarioJolg=self.usuarioJolg,
            timestamp=self.timestamp
        )
