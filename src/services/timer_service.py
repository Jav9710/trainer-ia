"""
Servicio de Cronómetro
Gestiona el tiempo de entrenamiento con funciones de inicio, pausa y detención
"""
import time
from datetime import datetime, timedelta
from typing import Optional


class TimerService:
    """Servicio para gestionar cronómetro de entrenamiento"""

    def __init__(self):
        """Inicializa el cronómetro"""
        self.start_time: Optional[datetime] = None
        self.pause_time: Optional[datetime] = None
        self.total_paused_seconds: float = 0.0
        self.is_running: bool = False
        self.is_paused: bool = False
        self.is_stopped: bool = False

    def start(self):
        """Inicia el cronómetro"""
        if not self.is_running:
            self.start_time = datetime.now()
            self.is_running = True
            self.is_paused = False
            self.is_stopped = False
            self.total_paused_seconds = 0.0

    def pause(self):
        """Pausa el cronómetro"""
        if self.is_running and not self.is_paused:
            self.pause_time = datetime.now()
            self.is_paused = True

    def resume(self):
        """Reanuda el cronómetro después de una pausa"""
        if self.is_running and self.is_paused and self.pause_time:
            pause_duration = (datetime.now() - self.pause_time).total_seconds()
            self.total_paused_seconds += pause_duration
            self.pause_time = None
            self.is_paused = False

    def stop(self):
        """Detiene el cronómetro completamente"""
        if self.is_running:
            if self.is_paused and self.pause_time:
                # Si estaba en pausa, sumar ese tiempo
                pause_duration = (datetime.now() - self.pause_time).total_seconds()
                self.total_paused_seconds += pause_duration
            self.is_running = False
            self.is_paused = False
            self.is_stopped = True

    def reset(self):
        """Reinicia el cronómetro a cero"""
        self.start_time = None
        self.pause_time = None
        self.total_paused_seconds = 0.0
        self.is_running = False
        self.is_paused = False
        self.is_stopped = False

    def get_elapsed_seconds(self) -> float:
        """
        Obtiene segundos transcurridos (excluyendo tiempo en pausa)

        Returns:
            Segundos transcurridos
        """
        if not self.start_time:
            return 0.0

        if self.is_paused and self.pause_time:
            # Si está en pausa, calcular hasta el momento de la pausa
            elapsed = (self.pause_time - self.start_time).total_seconds()
            return elapsed - self.total_paused_seconds
        elif self.is_running:
            # Si está corriendo, calcular hasta ahora
            elapsed = (datetime.now() - self.start_time).total_seconds()
            return elapsed - self.total_paused_seconds
        elif self.is_stopped:
            # Si está detenido, retornar tiempo total al momento de detener
            if self.pause_time:
                elapsed = (self.pause_time - self.start_time).total_seconds()
            else:
                elapsed = (datetime.now() - self.start_time).total_seconds()
            return elapsed - self.total_paused_seconds

        return 0.0

    def get_elapsed_minutes(self) -> float:
        """
        Obtiene minutos transcurridos

        Returns:
            Minutos transcurridos
        """
        return self.get_elapsed_seconds() / 60.0

    def get_formatted_time(self) -> str:
        """
        Obtiene tiempo formateado como HH:MM:SS

        Returns:
            String con formato de tiempo
        """
        total_seconds = int(self.get_elapsed_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_status(self) -> str:
        """
        Obtiene estado actual del cronómetro

        Returns:
            Estado: 'stopped', 'running', 'paused'
        """
        if not self.is_running and not self.is_stopped:
            return "stopped"
        elif self.is_paused:
            return "paused"
        elif self.is_running:
            return "running"
        else:
            return "stopped"

    def is_active(self) -> bool:
        """Verifica si el cronómetro está activo (corriendo o en pausa)"""
        return self.is_running

    def get_progress_info(self, target_minutes: int) -> dict:
        """
        Obtiene información de progreso

        Args:
            target_minutes: Minutos objetivo

        Returns:
            Diccionario con información de progreso
        """
        elapsed_minutes = self.get_elapsed_minutes()
        progress_percent = min((elapsed_minutes / target_minutes) * 100, 100.0)
        remaining_minutes = max(target_minutes - elapsed_minutes, 0.0)

        return {
            'elapsed_seconds': self.get_elapsed_seconds(),
            'elapsed_minutes': elapsed_minutes,
            'formatted_time': self.get_formatted_time(),
            'progress_percent': progress_percent,
            'remaining_minutes': remaining_minutes,
            'target_minutes': target_minutes,
            'is_complete': progress_percent >= 100.0
        }


class IntervalTimer(TimerService):
    """Cronómetro con soporte para intervalos (útil para HIIT)"""

    def __init__(self, interval_seconds: int = 60):
        """
        Inicializa cronómetro de intervalos

        Args:
            interval_seconds: Duración de cada intervalo en segundos
        """
        super().__init__()
        self.interval_seconds = interval_seconds
        self.intervals_completed = 0

    def get_current_interval(self) -> int:
        """
        Obtiene número del intervalo actual

        Returns:
            Número de intervalo (empezando en 1)
        """
        if not self.is_running:
            return 0

        elapsed = self.get_elapsed_seconds()
        current_interval = int(elapsed // self.interval_seconds) + 1
        return current_interval

    def get_interval_progress(self) -> dict:
        """
        Obtiene progreso del intervalo actual

        Returns:
            Diccionario con info del intervalo
        """
        elapsed = self.get_elapsed_seconds()
        current_interval = self.get_current_interval()
        seconds_in_interval = elapsed % self.interval_seconds
        interval_progress = (seconds_in_interval / self.interval_seconds) * 100

        return {
            'current_interval': current_interval,
            'seconds_in_interval': seconds_in_interval,
            'interval_progress_percent': interval_progress,
            'seconds_until_next': self.interval_seconds - seconds_in_interval
        }
