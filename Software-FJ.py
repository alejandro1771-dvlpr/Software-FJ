
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

# 7. SERVICIO ESPECIALIZADO: ALQUILER DE EQUIPOS

class AlquilerEquipo(Servicio):

    def __init__(self, nombre, tarifa, capacidad=10):
        super().__init__(nombre, tarifa, capacidad)

    def validar_parametros(self, duracion, **parametros):

        if isinstance(duracion, bool) or not isinstance(duracion, int):
            raise DatosInvalidosError(
                "La duracion del alquiler debe ser un numero entero."
            )

        if duracion < 1 or duracion > 30:
            raise DatosInvalidosError(
                "El alquiler debe durar entre 1 y 30 dias."
            )

        cantidad = parametros.get("cantidad", 1)

        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise DatosInvalidosError("Cantidad de equipos invalida.")

        if cantidad < 1 or cantidad > 20:
            raise DatosInvalidosError(
                "La cantidad debe estar entre 1 y 20 equipos."
            )

    def calcular_costo_base(self, duracion, **parametros):
        self.validar_parametros(duracion, **parametros)
        cantidad = parametros.get("cantidad", 1)

        return self.tarifa * duracion * cantidad

    def describir_servicio(self):
        return "Alquiler de computadores y equipos tecnologicos."

# 8. SERVICIO ESPECIALIZADO: ASESORIAS

class AsesoriaEspecializada(Servicio):

    def __init__(self, nombre, tarifa, capacidad=8):
        super().__init__(nombre, tarifa, capacidad)

    def validar_parametros(self, duracion, **parametros):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidosError("Duracion de asesoria invalida.")

        if duracion <= 0 or duracion > 8:
            raise DatosInvalidosError(
                "La asesoria debe durar entre 0 y 8 horas."
            )

        especialidad = parametros.get("especialidad")

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError(
                "Debe indicar la especialidad de la asesoria."
            )

    def calcular_costo_base(self, duracion, **parametros):
        self.validar_parametros(duracion, **parametros)

        especialidad = parametros["especialidad"].lower()

        recargos = {
            "software": 1.20,
            "seguridad": 1.35,
            "redes": 1.15,
            "general": 1.00
        }

        if especialidad not in recargos:
            raise DatosInvalidosError(
                "Especialidad no reconocida."
            )

        return self.tarifa * duracion * recargos[especialidad]

    def describir_servicio(self):
        return "Asesorias profesionales en tecnologia y sistemas."

# 9. CLASE RESERVA

class Reserva(Entidad):

    def __init__(self, cliente, servicio, duracion, **parametros):
        super().__init__()

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente no es valido.")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio no es valido.")

        servicio.validar_parametros(duracion, **parametros)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._parametros = parametros.copy()
        self._estado = "PENDIENTE"
        self._costo = 0.0

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):

        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self._servicio.ocupar()
        self._estado = "CONFIRMADA"

        logger.info(
            "Reserva %s confirmada para %s",
            self.id, self._cliente.nombre
        )

    def cancelar(self):

        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                "Solo se pueden cancelar reservas confirmadas."
            )

        self._servicio.liberar()
        self._estado = "CANCELADA"

        logger.info("Reserva %s cancelada.", self.id)

    def procesar(self, impuesto=19, descuento=0):

        try:
            if self._estado != "CONFIRMADA":
                raise ReservaInvalidaError(
                    "La reserva debe estar confirmada para procesarse."
                )

            self._costo = self._servicio.calcular_costo(
                self._duracion,
                impuesto=impuesto,
                descuento=descuento,
                **self._parametros
            )

            if self._costo < 0:
                raise DatosInvalidosError(
                    "El resultado del costo no puede ser negativo."
                )

            logger.info(
                "Reserva %s procesada. Total: $%.2f",
                self.id, self._costo
            )

            return self._costo

        except Exception as error:
            logger.exception(
                "Error procesando reserva %s", self.id
            )

            # Encadenamiento de excepciones.
            raise ProcesamientoError(
                f"No fue posible procesar la reserva {self.id}."
            ) from error

        finally:
            logger.info(
                "Finalizo intento de procesamiento de reserva %s",
                self.id
            )

    def mostrar_informacion(self):

        return (
            f"Reserva: {self.id}\n"
            f"Cliente: {self._cliente.nombre}\n"
            f"Servicio: {self._servicio.nombre}\n"
            f"Duracion: {self._duracion}\n"
            f"Estado: {self._estado}\n"
            f"Costo: ${self._costo:,.2f}"
        )

# 10. CLASE PRINCIPAL DEL SISTEMA

class SistemaSoftwareFJ:

    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        logger.info("Sistema Software FJ iniciado.")

    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Objeto cliente incorrecto.")

        documento = cliente.documento

        if any(c.documento == documento for c in self.__clientes):
            raise DatosInvalidosError(
                "Ya existe un cliente con ese documento."
            )

        self.__clientes.append(cliente)

        logger.info(
            "Cliente registrado: %s", cliente.nombre
        )

        return cliente

    def registrar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Servicio no valido.")

        if any(s.id == servicio.id for s in self.__servicios):
            raise DatosInvalidosError("El servicio ya esta registrado.")

        self.__servicios.append(servicio)

        logger.info(
            "Servicio registrado: %s", servicio.nombre
        )

        return servicio

    def crear_reserva(self, cliente, servicio, duracion, **parametros):

        if cliente not in self.__clientes:
            raise ReservaInvalidaError(
                "El cliente no esta registrado."
            )

        if servicio not in self.__servicios:
            raise ReservaInvalidaError(
                "El servicio no esta registrado."
            )

        reserva = Reserva(
            cliente, servicio, duracion, **parametros
        )

        self.__reservas.append(reserva)

        logger.info("Reserva creada: %s", reserva.id)

        return reserva

    def listar_clientes(self):
        return self.__clientes.copy()

    def listar_servicios(self):
        return self.__servicios.copy()

    def listar_reservas(self):
        return self.__reservas.copy()

    def mostrar_resumen(self):

        print("\n========== RESUMEN SOFTWARE FJ ==========")
        print("Clientes registrados:", len(self.__clientes))
        print("Servicios registrados:", len(self.__servicios))
        print("Reservas creadas:", len(self.__reservas))

        print("\n--- CLIENTES ---")
        for cliente in self.__clientes:
            print(cliente.mostrar_informacion())

        print("\n--- SERVICIOS ---")
        for servicio in self.__servicios:
            print(servicio.mostrar_informacion())
            print(servicio.describir_servicio())

        print("\n--- RESERVAS ---")
        for reserva in self.__reservas:
            print(reserva.mostrar_informacion())
            print("----------------------------------")

# 11. FUNCION PARA MANEJO CONTROLADO DE ERRORES

def ejecutar_operacion(descripcion, operacion):

    print(f"\n>>> {descripcion}")

    try:
        resultado = operacion()

    except SoftwareFJError as error:
        logger.exception("Error controlado: %s", descripcion)
        print("ERROR CONTROLADO:", error)

    except Exception as error:
        logger.exception("Error inesperado: %s", descripcion)
        print("ERROR INESPERADO:", error)

    else:
        logger.info("Operacion exitosa: %s", descripcion)
        print("Operacion realizada correctamente.")

        if resultado is not None:
            print(resultado)

    finally:
        print("Operacion finalizada. El sistema continua activo.")

# 12. SIMULACION DE OPERACIONES

def ejecutar_demostracion():

    sistema = SistemaSoftwareFJ()

    print("\n")
    print("=" * 55)
    print("       SISTEMA INTEGRAL SOFTWARE FJ")
    print("       DEMOSTRACION DE FUNCIONAMIENTO")
    print("=" * 55)

    # -----------------------------------------------
    # OPERACION 1: REGISTRO DE CLIENTE VALIDO
    # -----------------------------------------------

    cliente1 = Cliente(
        "Carlos Ramirez",
        "1020304050",
        "carlos@gmail.com",
        "3001234567"
    )

    ejecutar_operacion(
        "Operacion 1: Registrar cliente valido",
        lambda: sistema.registrar_cliente(cliente1).mostrar_informacion()
    )

    # -----------------------------------------------
    # OPERACION 2: CLIENTE CON CORREO INVALIDO
    # -----------------------------------------------

    ejecutar_operacion(
        "Operacion 2: Registrar cliente con correo incorrecto",
        lambda: Cliente(
            "Maria Lopez",
            "2030405060",
            "correo_invalido",
            "3101234567"
        )
    )

    # -----------------------------------------------
    # OPERACION 3: REGISTRO DE SEGUNDO CLIENTE
    # -----------------------------------------------

    cliente2 = Cliente(
        "Laura Torres",
        "3040506070",
        "laura@gmail.com",
        "3201234567"
    )

    ejecutar_operacion(
        "Operacion 3: Registrar segundo cliente",
        lambda: sistema.registrar_cliente(cliente2).nombre
    )

    # -----------------------------------------------
    # OPERACION 4: CREAR SERVICIO DE SALAS
    # -----------------------------------------------

    sala = ReservaSala("Sala de reuniones", 50000, 2)

    ejecutar_operacion(
        "Operacion 4: Crear servicio de salas",
        lambda: sistema.registrar_servicio(sala).nombre
    )

    # -----------------------------------------------
    # OPERACION 5: CREAR SERVICIO DE EQUIPOS
    # -----------------------------------------------

    equipo = AlquilerEquipo("Computador portatil", 80000, 5)

    ejecutar_operacion(
        "Operacion 5: Crear servicio de equipos",
        lambda: sistema.registrar_servicio(equipo).nombre
    )

    # -----------------------------------------------
    # OPERACION 6: CREAR SERVICIO DE ASESORIAS
    # -----------------------------------------------

    asesoria = AsesoriaEspecializada(
        "Asesoria tecnologica", 100000, 3
    )

    ejecutar_operacion(
        "Operacion 6: Crear servicio de asesoria",
        lambda: sistema.registrar_servicio(asesoria).nombre
    )

    # -----------------------------------------------
    # OPERACION 7: CREAR SERVICIO INVALIDO
    # -----------------------------------------------

    ejecutar_operacion(
        "Operacion 7: Crear servicio con tarifa negativa",
        lambda: ReservaSala("Sala invalida", -5000)
    )

    # -----------------------------------------------
    # OPERACION 8: RESERVA CORRECTA DE SALA
    # -----------------------------------------------

    reserva1 = sistema.crear_reserva(
        cliente1, sala, 3, personas=15
    )

    ejecutar_operacion(
        "Operacion 8: Confirmar y procesar reserva de sala",
        lambda: (
            reserva1.confirmar(),
            reserva1.procesar(impuesto=19, descuento=10)
        )
    )

    # -----------------------------------------------
    # OPERACION 9: RESERVA CORRECTA DE EQUIPOS
    # -----------------------------------------------

    reserva2 = sistema.crear_reserva(
        cliente2, equipo, 2, cantidad=2
    )

    ejecutar_operacion(
        "Operacion 9: Confirmar y procesar alquiler de equipos",
        lambda: (
            reserva2.confirmar(),
            reserva2.procesar(impuesto=19)
        )
    )

    # -----------------------------------------------
    # OPERACION 10: RESERVA CORRECTA DE ASESORIA
    # -----------------------------------------------

    reserva3 = sistema.crear_reserva(
        cliente1,
        asesoria,
        2,
        especialidad="software"
    )

    ejecutar_operacion(
        "Operacion 10: Confirmar y procesar asesoria",
        lambda: (
            reserva3.confirmar(),
            reserva3.procesar(impuesto=19)
        )
    )

    # -----------------------------------------------
    # OPERACION 11: RESERVA CON DURACION INVALIDA
    # -----------------------------------------------

    ejecutar_operacion(
        "Operacion 11: Crear reserva con duracion incorrecta",
        lambda: sistema.crear_reserva(
            cliente1, sala, -5, personas=10
        )
    )

    # -----------------------------------------------
    # OPERACION 12: CLIENTE NO REGISTRADO
    # -----------------------------------------------

    cliente_no_registrado = Cliente(
        "Pedro Gomez",
        "4050607080",
        "pedro@gmail.com",
        "3151234567"
    )

    ejecutar_operacion(
        "Operacion 12: Reserva con cliente no registrado",
        lambda: sistema.crear_reserva(
            cliente_no_registrado, sala, 2, personas=5
        )
    )

    # -----------------------------------------------
    # OPERACION 13: CANCELACION DE RESERVA
    # -----------------------------------------------

    ejecutar_operacion(
        "Operacion 13: Cancelar reserva confirmada",
        lambda: reserva2.cancelar()
    )

    # -----------------------------------------------
    # OPERACION 14: INTENTO DE CANCELACION INCORRECTA
    # -----------------------------------------------

    ejecutar_operacion(
        "Operacion 14: Cancelar reserva ya cancelada",
        lambda: reserva2.cancelar()
    )

    # -----------------------------------------------
    # OPERACION 15: PROCESAR RESERVA PENDIENTE
    # -----------------------------------------------

    reserva4 = sistema.crear_reserva(
        cliente2, sala, 2, personas=10
    )

    ejecutar_operacion(
        "Operacion 15: Procesar reserva sin confirmar",
        lambda: reserva4.procesar()
    )

    # -----------------------------------------------
    # OPERACION 16: CALCULO CON SOBRECARGA
    # -----------------------------------------------

    ejecutar_operacion(
        "Operacion 16: Calcular costo con impuestos y descuento",
        lambda: (
            f"Costo normal: ${sala.calcular_costo(2):,.2f}\n"
            f"Con impuesto: ${sala.calcular_costo(2, 19):,.2f}\n"
            f"Con impuesto y descuento: "
            f"${sala.calcular_costo(2, 19, 10):,.2f}"
        )
    )

    # -----------------------------------------------
    # OPERACION 17: VALIDACION DE ARGUMENTOS
    # -----------------------------------------------

    ejecutar_operacion(
        "Operacion 17: Calculo con impuesto incorrecto",
        lambda: sala.calcular_costo(2, impuesto=150)
    )

    # -----------------------------------------------
    # OPERACION 18: SERVICIO SIN DISPONIBILIDAD
    # -----------------------------------------------

    sala_llena = ReservaSala("Sala de capacidad limitada", 40000, 1)

    sistema.registrar_servicio(sala_llena)

    reserva_llena = sistema.crear_reserva(
        cliente1, sala_llena, 2, personas=10
    )
    reserva_llena.confirmar()

    reserva_extra = sistema.crear_reserva(
        cliente2, sala_llena, 2, personas=10
    )

    ejecutar_operacion(
        "Operacion 18: Intentar reservar sala sin disponibilidad",
        lambda: reserva_extra.confirmar()
    )

 # RESUMEN FINAL

 sistema.mostrar_resumen()

    print("\n")
    print("=" * 55)
    print("SIMULACION FINALIZADA")
    print("El sistema continuo funcionando ante los errores.")
    print("Revise los archivos logs/eventos.log y logs/errores.log")
    print("=" * 55)

    return sistema

# 13. MENU INTERACTIVO DE CONSOLA

def menu_interactivo(sistema):

    while True:

        print("\n========== MENU SOFTWARE FJ ==========")
        print("1. Registrar cliente")
        print("2. Consultar clientes")
        print("3. Consultar servicios")
        print("4. Crear reserva de sala")
        print("5. Crear reserva de equipos")
        print("6. Crear reserva de asesoria")
        print("7. Consultar reservas")
        print("8. Cancelar reserva")
        print("9. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        try:

            if opcion == "1":

                nombre = input("Nombre: ")
                documento = input("Documento: ")
                correo = input("Correo: ")
                telefono = input("Telefono: ")

                cliente = Cliente(
                    nombre, documento, correo, telefono
                )

                sistema.registrar_cliente(cliente)
                print("Cliente registrado:", cliente.nombre)

            elif opcion == "2":

                for cliente in sistema.listar_clientes():
                    print(cliente.mostrar_informacion())

            elif opcion == "3":

                for servicio in sistema.listar_servicios():
                    print(servicio.mostrar_informacion())
                    print(servicio.describir_servicio())

            elif opcion in ("4", "5", "6"):

                clientes = sistema.listar_clientes()
                servicios = sistema.listar_servicios()

                if not clientes or not servicios:
                    raise DatosInvalidosError(
                        "Debe existir al menos un cliente y un servicio."
                    )

                for i, cliente in enumerate(clientes):
                    print(i, cliente.nombre)

                indice_cliente = int(input("Seleccione cliente: "))

                if not 0 <= indice_cliente < len(clientes):
                    raise DatosInvalidosError("Cliente no encontrado.")

                cliente = clientes[indice_cliente]

                servicios_filtrados = []

                for servicio in servicios:
                    if (
                        opcion == "4" and isinstance(servicio, ReservaSala)
                    ) or (
                        opcion == "5" and isinstance(servicio, AlquilerEquipo)
                    ) or (
                        opcion == "6" and isinstance(
                            servicio, AsesoriaEspecializada
                        )
                    ):
                        servicios_filtrados.append(servicio)

                if not servicios_filtrados:
                    raise DatosInvalidosError(
                        "No hay servicios de ese tipo registrados."
                    )

                for i, servicio in enumerate(servicios_filtrados):
                    print(i, servicio.nombre)

                indice_servicio = int(input("Seleccione servicio: "))

                if not 0 <= indice_servicio < len(servicios_filtrados):
                    raise DatosInvalidosError("Servicio no encontrado.")

                servicio = servicios_filtrados[indice_servicio]
                duracion = float(input("Duracion: "))

                parametros = {}

                if isinstance(servicio, ReservaSala):
                    parametros["personas"] = int(
                        input("Cantidad de personas: ")
                    )

                elif isinstance(servicio, AlquilerEquipo):
                    parametros["cantidad"] = int(
                        input("Cantidad de equipos: ")
                    )

                elif isinstance(servicio, AsesoriaEspecializada):
                    parametros["especialidad"] = input(
                        "Especialidad (software, seguridad, redes, general): "
                    )

                reserva = sistema.crear_reserva(
                    cliente, servicio, duracion, **parametros
                )

                reserva.confirmar()
                total = reserva.procesar()

                print("Reserva confirmada.")
                print("Total a pagar: $", total)

            elif opcion == "7":

                for reserva in sistema.listar_reservas():
                    print(reserva.mostrar_informacion())
                    print("------------------------")

            elif opcion == "8":

                reservas = sistema.listar_reservas()

                for i, reserva in enumerate(reservas):
                    print(i, reserva.id, reserva.estado)

                indice = int(input("Seleccione reserva: "))

                if not 0 <= indice < len(reservas):
                    raise DatosInvalidosError("Reserva no encontrada.")

                reservas[indice].cancelar()
                print("Reserva cancelada correctamente.")

            elif opcion == "9":
                print("Gracias por utilizar Software FJ.")
                logger.info("Sesion de consola finalizada.")
                break

            else:
                raise DatosInvalidosError(
                    "Seleccione una opcion valida del 1 al 9."
                )

        except (SoftwareFJError, ValueError) as error:
            logger.exception("Error en el menu interactivo.")
            print("No se pudo completar la operacion:", error)

        except Exception as error:
            logger.exception("Error inesperado en el menu.")
            print("Error inesperado:", error)

        finally:
            print("\nSistema Software FJ activo.")

# 14. PUNTO DE ENTRADA DEL PROGRAMA

if __name__ == "__main__":

    try:

        sistema = ejecutar_demostracion()

        print("\n¿Desea ingresar al menu interactivo?")
        respuesta = input("Escriba SI o NO: ").strip().upper()

        if respuesta == "SI":
            menu_interactivo(sistema)

    except Exception as error:

        logger.exception("Error critico en la aplicacion.")

        print("Se detecto un error general:", error)
        print("Consulte el archivo logs/errores.log.")

    finally:

        logger.info("Finalizacion de la ejecucion principal.")
        print("\nSoftware FJ: ejecucion finalizada.")
