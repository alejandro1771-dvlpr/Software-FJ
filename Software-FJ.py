
"""
=========================================================
 SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ
=========================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging
import os
import uuid

# 1. CONFIGURACION DE REGISTROS Y LOGS

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    eventos = logging.FileHandler(
        "logs/eventos.log", encoding="utf-8"
    )
    eventos.setLevel(logging.INFO)
    eventos.setFormatter(formato)

    errores = logging.FileHandler(
        "logs/errores.log", encoding="utf-8"
    )
    errores.setLevel(logging.ERROR)
    errores.setFormatter(formato)

    logger.addHandler(eventos)
    logger.addHandler(errores)

# 2. EXCEPCIONES PERSONALIZADAS

class SoftwareFJError(Exception):
    """Excepcion general del sistema."""
    pass


class DatosInvalidosError(SoftwareFJError):
    """Datos incorrectos o incompletos."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio no tiene disponibilidad."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Error durante la gestion de una reserva."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Operacion incompatible con el estado actual."""
    pass


class ProcesamientoError(SoftwareFJError):
    """Error durante el procesamiento de una operacion."""
    pass
