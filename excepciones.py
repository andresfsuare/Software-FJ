"""Excepciones personalizadas del sistema Software FJ."""

class SoftwareFJError(Exception):
    """Excepción base para errores controlados del sistema."""

class DatosInvalidosError(SoftwareFJError):
    """Datos de entrada inválidos."""

class ClienteInvalidoError(DatosInvalidosError):
    """Datos inválidos al registrar un cliente."""

class ServicioInvalidoError(DatosInvalidosError):
    """Datos inválidos al crear un servicio."""

class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio no está disponible para la operación solicitada."""

class ReservaInvalidaError(SoftwareFJError):
    """La reserva no puede crearse o procesarse."""

class EstadoReservaError(SoftwareFJError):
    """Operación no permitida por el estado actual de la reserva."""
