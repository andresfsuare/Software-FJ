
"""Clase Reserva y operaciones de su ciclo de vida."""

from datetime import datetime
from enum import Enum
import math

from excepciones import ReservaInvalidaError, EstadoReservaError


class EstadoReserva(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva:
    """Representa una reserva de un cliente para un servicio."""

    _siguiente_id = 1

    def __init__(
        self, cliente, servicio, duracion,
        impuesto=0.19, descuento=0.0
    ):
        # Importaciones locales para evitar dependencias circulares.
        from entidades import Cliente
        from servicios import Servicio

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "La reserva requiere un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "La reserva requiere un servicio válido."
            )

        try:
            duracion = float(duracion)
            impuesto = float(impuesto)
            descuento = float(descuento)
        except (TypeError, ValueError) as exc:
            raise ReservaInvalidaError(
                "La duración, el impuesto y el descuento "
                "deben ser numéricos."
            ) from exc

        if not all(
            math.isfinite(valor)
            for valor in (duracion, impuesto, descuento)
        ):
            raise ReservaInvalidaError(
                "Los valores de la reserva deben ser finitos."
            )

        if duracion <= 0:
            raise ReservaInvalidaError(
                "La duración debe ser mayor que cero."
            )

        if not 0 <= impuesto <= 1:
            raise ReservaInvalidaError(
                "El impuesto debe estar entre 0 y 1."
            )

        if not 0 <= descuento <= 1:
            raise ReservaInvalidaError(
                "El descuento debe estar entre 0 y 1."
            )

        self.identificador = f"RES-{Reserva._siguiente_id:04d}"
        Reserva._siguiente_id += 1

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.impuesto = impuesto
        self.descuento = descuento
        self.estado = EstadoReserva.PENDIENTE
        self.fecha_creacion = datetime.now().isoformat(
            timespec="seconds"
        )
        self.costo = None

    def confirmar(self):
        """Calcula el costo y confirma una reserva pendiente."""

        if self.estado != EstadoReserva.PENDIENTE:
            raise EstadoReservaError(
                f"No se puede confirmar una reserva en estado "
                f"{self.estado.value}."
            )

        # El estado solo cambia si el cálculo termina correctamente.
        costo_calculado = self.servicio.calcular_costo(
            self.duracion,
            self.impuesto,
            self.descuento
        )

        self.costo = costo_calculado
        self.estado = EstadoReserva.CONFIRMADA

        return self.costo

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""

        if self.estado not in (
            EstadoReserva.PENDIENTE,
            EstadoReserva.CONFIRMADA
        ):
            raise EstadoReservaError(
                f"No se puede cancelar una reserva en estado "
                f"{self.estado.value}."
            )

        self.estado = EstadoReserva.CANCELADA
        return f"Reserva {self.identificador} cancelada."

    def procesar(self):
        """Procesa una reserva que ya fue confirmada."""

        if self.estado != EstadoReserva.CONFIRMADA:
            raise EstadoReservaError(
                "Solo se pueden procesar reservas confirmadas."
            )

        self.estado = EstadoReserva.PROCESADA
        return f"Reserva {self.identificador} procesada."

    def mostrar_informacion(self):
        """Devuelve los datos principales de la reserva."""

        if self.costo is not None:
            costo = f"${self.costo:.2f}"
        else:
            costo = "Pendiente de cálculo"

        return (
            f"{self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion:g} | "
            f"Estado: {self.estado.value} | "
            f"Costo: {costo}"
        )
