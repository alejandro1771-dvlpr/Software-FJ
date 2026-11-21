
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

# 3. CLASE ABSTRACTA ENTIDAD

class Entidad(ABC):

    def __init__(self):
        self._id = str(uuid.uuid4())[:8].upper()
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def mostrar_informacion(self):
        pass

# 4. CLASE CLIENTE

class Cliente(Entidad):

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()

        self.__nombre = None
        self.__documento = None
        self.__correo = None
        self.__telefono = None

        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError(
                "El nombre debe tener al menos 3 caracteres."
            )
        self.__nombre = valor.strip().title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip()

        if not valor.isdigit() or len(valor) < 5:
            raise DatosInvalidosError(
                "El documento debe contener al menos 5 digitos."
            )
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise DatosInvalidosError("Correo invalido.")

        valor = valor.strip()

        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(
                "El correo electronico no tiene un formato valido."
            )

        self.__correo = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()

        if not valor.isdigit() or len(valor) < 7:
            raise DatosInvalidosError(
                "El telefono debe contener al menos 7 digitos."
            )

        self.__telefono = valor

    def mostrar_informacion(self):
        return (
            f"Cliente: {self.nombre} | "
            f"Documento: {self.documento} | "
            f"Correo: {self.correo} | "
            f"Telefono: {self.telefono}"
        )






