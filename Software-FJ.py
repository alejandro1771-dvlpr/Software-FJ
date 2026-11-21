
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

#5. CLASE ABSTRACTA SERVICIO

class Servicio(Entidad, ABC):

    def __init__(self, nombre, tarifa, capacidad=10):
        super().__init__()

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("Nombre de servicio invalido.")

        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)):
            raise DatosInvalidosError("La tarifa debe ser numerica.")

        if tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser positiva.")

        if isinstance(capacidad, bool) or not isinstance(capacidad, int):
            raise DatosInvalidosError("La capacidad debe ser entera.")

        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser positiva.")

        self._nombre = nombre.strip()
        self._tarifa = float(tarifa)
        self._capacidad = capacidad
        self._reservas_activas = 0

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._reservas_activas < self._capacidad

    def ocupar(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no tiene disponibilidad."
            )

        self._reservas_activas += 1

    def liberar(self):
        if self._reservas_activas <= 0:
            raise OperacionNoPermitidaError(
                "No existen reservas activas para liberar."
            )

        self._reservas_activas -= 1

    @abstractmethod
    def calcular_costo_base(self, duracion, **parametros):
        pass

    @abstractmethod
    def validar_parametros(self, duracion, **parametros):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

 # Sobrecarga simulada mediante argumentos opcionales.
    # Permite calcular costos con o sin impuestos y descuentos.

def calcular_costo(
        self, duracion, *args, impuesto=0, descuento=0, **parametros
    ):

        # Variantes:
        # calcular_costo(2)
        # calcular_costo(2, 19)
        # calcular_costo(2, 19, 10)
        # calcular_costo(2, impuesto=19, descuento=10)

        if len(args) > 2:
            raise DatosInvalidosError(
                "Cantidad incorrecta de argumentos adicionales."
            )

        if len(args) >= 1:
            if impuesto != 0:
                raise DatosInvalidosError(
                    "El impuesto se especifico dos veces."
                )
            impuesto = args[0]

        if len(args) == 2:
            if descuento != 0:
                raise DatosInvalidosError(
                    "El descuento se especifico dos veces."
                )
            descuento = args[1]

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise DatosInvalidosError("Impuesto invalido.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise DatosInvalidosError("Descuento invalido.")

        if not 0 <= impuesto <= 100:
            raise DatosInvalidosError(
                "El impuesto debe estar entre 0 y 100."
            )

        if not 0 <= descuento <= 100:
            raise DatosInvalidosError(
                "El descuento debe estar entre 0 y 100."
            )

        self.validar_parametros(duracion, **parametros)

        base = self.calcular_costo_base(duracion, **parametros)

        if base < 0:
            raise DatosInvalidosError("Calculo base inconsistente.")

        subtotal = base * (1 - descuento / 100)
        total = subtotal * (1 + impuesto / 100)

        return round(total, 2)

    def mostrar_informacion(self):
        return (
            f"Servicio: {self.nombre} | "
            f"Tarifa: ${self.tarifa:,.2f}"
        )

# 6. SERVICIO ESPECIALIZADO: RESERVA DE SALAS

class ReservaSala(Servicio):

    def __init__(self, nombre, tarifa, capacidad=5):
        super().__init__(nombre, tarifa, capacidad)

    def validar_parametros(self, duracion, **parametros):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidosError("Duracion de sala invalida.")

        if duracion <= 0 or duracion > 12:
            raise DatosInvalidosError(
                "La duracion debe estar entre 0 y 12 horas."
            )

        personas = parametros.get("personas", 1)

        if isinstance(personas, bool) or not isinstance(personas, int):
            raise DatosInvalidosError("Cantidad de personas invalida.")

        if personas < 1 or personas > 50:
            raise DatosInvalidosError(
                "La sala admite entre 1 y 50 personas."
            )

    def calcular_costo_base(self, duracion, **parametros):
        self.validar_parametros(duracion, **parametros)
        personas = parametros.get("personas", 1)

        recargo = 1.20 if personas > 20 else 1

        return self.tarifa * duracion * recargo

    def describir_servicio(self):
        return "Reserva de salas para reuniones y capacitaciones."

