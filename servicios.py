
"""Servicios abstractos y servicios concretos de Software FJ."""

from abc import ABC, abstractmethod
import math

from entidades import Entidad
from excepciones import (
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)


class Servicio(Entidad, ABC):
    """Clase abstracta base para los servicios de Software FJ."""

    def __init__(self, codigo, nombre, tarifa_base, disponible=True):
        super().__init__(codigo)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError(
                "El nombre del servicio no puede estar vacío."
            )

        try:
            tarifa_base = float(tarifa_base)
        except (TypeError, ValueError) as exc:
            raise ServicioInvalidoError(
                "La tarifa base debe ser numérica."
            ) from exc

        if not math.isfinite(tarifa_base) or tarifa_base < 0:
            raise ServicioInvalidoError(
                "La tarifa debe ser finita y no negativa."
            )

        if not isinstance(disponible, bool):
            raise ServicioInvalidoError(
                "La disponibilidad debe ser True o False."
            )

        self._nombre = nombre.strip()
        self._tarifa_base = tarifa_base
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def validar_disponibilidad(self):
        """Comprueba que el servicio pueda utilizarse."""
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no está disponible."
            )

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """Calcula el costo final del servicio."""

    @abstractmethod
    def describir(self):
        """Describe las características del servicio."""

    def mostrar_informacion(self):
        return self.describir()

    def _calcular(self, duracion, impuesto=0.0, descuento=0.0):
        """Valida los parámetros y calcula el costo final."""

        self.validar_disponibilidad()

        try:
            duracion = float(duracion)
            impuesto = float(impuesto)
            descuento = float(descuento)
        except (TypeError, ValueError) as exc:
            raise ServicioInvalidoError(
                "Duración, impuesto y descuento deben ser numéricos."
            ) from exc

        if not all(
            math.isfinite(valor)
            for valor in (duracion, impuesto, descuento)
        ):
            raise ServicioInvalidoError(
                "Los parámetros deben ser números finitos."
            )

        if duracion <= 0:
            raise ServicioInvalidoError(
                "La duración debe ser mayor que cero."
            )

        if not 0 <= impuesto <= 1:
            raise ServicioInvalidoError(
                "El impuesto debe estar entre 0 y 1."
            )

        if not 0 <= descuento <= 1:
            raise ServicioInvalidoError(
                "El descuento debe estar entre 0 y 1."
            )

        subtotal = self.tarifa_base * duracion
        subtotal_descuento = subtotal * (1 - descuento)
        total = subtotal_descuento * (1 + impuesto)

        if not math.isfinite(total):
            raise ServicioInvalidoError(
                "El cálculo produjo un costo no válido."
            )

        return round(total, 2)

    # Variantes del cálculo de costos mediante parámetros opcionales.
    def calcular_costo_basico(self, duracion):
        """Calcula el costo sin impuesto ni descuento."""
        return self.calcular_costo(duracion)

    def calcular_costo_con_impuesto(self, duracion, impuesto):
        """Calcula el costo aplicando un impuesto."""
        return self.calcular_costo(
            duracion, impuesto=impuesto
        )

    def calcular_costo_con_descuento(
        self, duracion, descuento
    ):
        """Calcula el costo aplicando un descuento."""
        return self.calcular_costo(
            duracion, descuento=descuento
        )


class ServicioSala(Servicio):
    """Servicio de alquiler de salas por hora."""

    def __init__(
        self, codigo, nombre, tarifa_hora, capacidad,
        disponible=True
    ):
        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, int)
            or capacidad <= 0
        ):
            raise ServicioInvalidoError(
                "La capacidad debe ser un entero positivo."
            )

        super().__init__(
            codigo, nombre, tarifa_hora, disponible
        )
        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def calcular_costo(
        self, duracion, impuesto=0.0, descuento=0.0
    ):
        return self._calcular(
            duracion, impuesto, descuento
        )

    def describir(self):
        return (
            f"Sala '{self.nombre}' | "
            f"${self.tarifa_base:.2f}/hora | "
            f"Capacidad: {self.capacidad}"
        )


class ServicioEquipo(Servicio):
    """Servicio de alquiler de equipos por día."""

    def __init__(
        self, codigo, nombre, tarifa_dia, cantidad,
        disponible=True
    ):
        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ServicioInvalidoError(
                "La cantidad de equipos debe ser un entero positivo."
            )

        super().__init__(
            codigo, nombre, tarifa_dia, disponible
        )
        self._cantidad = cantidad

    @property
    def cantidad(self):
        return self._cantidad

    def calcular_costo(
        self, duracion, impuesto=0.0, descuento=0.0
    ):
        return self._calcular(
            duracion, impuesto, descuento
        )

    def describir(self):
        return (
            f"Alquiler de equipo '{self.nombre}' | "
            f"${self.tarifa_base:.2f}/día | "
            f"Unidades: {self.cantidad}"
        )


class ServicioAsesoria(Servicio):
    """Servicio de asesoría especializada por hora."""

    def __init__(
        self, codigo, nombre, tarifa_hora, especialidad,
        disponible=True
    ):
        if (
            not isinstance(especialidad, str)
            or not especialidad.strip()
        ):
            raise ServicioInvalidoError(
                "La especialidad no puede estar vacía."
            )

        super().__init__(
            codigo, nombre, tarifa_hora, disponible
        )
        self._especialidad = especialidad.strip()

    @property
    def especialidad(self):
        return self._especialidad

    def calcular_costo(
        self, duracion, impuesto=0.0, descuento=0.0
    ):
        return self._calcular(
            duracion, impuesto, descuento
        )

    def describir(self):
        return (
            f"Asesoría '{self.nombre}' | "
            f"${self.tarifa_base:.2f}/hora | "
            f"Especialidad: {self.especialidad}"
        )
