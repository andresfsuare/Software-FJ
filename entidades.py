"""Entidades principales y clase Cliente."""

from abc import ABC, abstractmethod
import re
from excepciones import ClienteInvalidoError

class Entidad(ABC):
    """Clase abstracta general para entidades identificables del sistema."""

    def __init__(self, identificador):
        identificador = str(identificador).strip() if identificador is not None else ""
        if not identificador:
            raise ValueError("El identificador no puede estar vacío.")
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        """Devuelve una descripción legible de la entidad."""

class Cliente(Entidad):
    """Cliente con datos encapsulados y validaciones."""

    def __init__(self, identificacion, nombre, correo, telefono):
        try:
            identificacion = str(identificacion).strip()
            nombre = str(nombre).strip()
            correo = str(correo).strip()
            telefono = str(telefono).strip()

            if not identificacion or len(identificacion) < 4:
                raise ClienteInvalidoError("La identificación debe tener al menos 4 caracteres.")
            if not nombre or not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]{2,}", nombre):
                raise ClienteInvalidoError("El nombre debe contener al menos 2 letras y solo caracteres válidos.")
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
                raise ClienteInvalidoError("El correo electrónico no tiene un formato válido.")
            if not re.fullmatch(r"\+?[0-9 -]{7,18}", telefono):
                raise ClienteInvalidoError("El teléfono debe contener entre 7 y 18 caracteres numéricos válidos.")

            super().__init__(identificacion)
            self.__nombre = nombre
            self.__correo = correo
            self.__telefono = telefono
        except ClienteInvalidoError:
            raise
        except Exception as exc:
            raise ClienteInvalidoError("No fue posible registrar el cliente.") from exc

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        return (f"Cliente {self.identificador}: {self.nombre} | "
                f"Correo: {self.correo} | Teléfono: {self.telefono}")
