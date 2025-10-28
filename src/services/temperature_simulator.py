"""
Simulador de Temperatura Corporal
Simula lecturas realistas de temperatura corporal durante el ejercicio
"""
import random
import time
from typing import Optional


class TemperatureSimulator:
    """Simula temperatura corporal durante el ejercicio de forma realista"""

    def __init__(
        self,
        base_temp: float = 36.5,
        min_temp: float = 36.0,
        max_temp: float = 39.5
    ):
        """
        Inicializa el simulador

        Args:
            base_temp: Temperatura corporal base en reposo
            min_temp: Temperatura mínima posible
            max_temp: Temperatura máxima durante ejercicio intenso
        """
        self.base_temp = base_temp
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.current_temp = base_temp
        self.exercise_time = 0  # segundos

    def get_temperature(
        self,
        heart_rate: int,
        duration_minutes: float,
        intensity: str = "medium"
    ) -> float:
        """
        Simula lectura de temperatura basada en parámetros de ejercicio

        Relación fisiológica: La temperatura corporal aumenta directamente
        con la frecuencia cardíaca durante el ejercicio debido al incremento
        en metabolismo y producción de calor muscular.

        Args:
            heart_rate: Frecuencia cardíaca actual (ppm)
            duration_minutes: Duración del ejercicio hasta ahora (minutos)
            intensity: Intensidad del ejercicio (low, medium, high)

        Returns:
            Temperatura corporal simulada en °C
        """
        # Factor de intensidad
        intensity_factors = {
            'low': 0.3,
            'medium': 0.5,
            'high': 0.8
        }
        intensity_factor = intensity_factors.get(intensity, 0.5)

        # RELACIÓN DIRECTA CON BPM (mejorada)
        # Temperatura aumenta proporcionalmente con FC
        # Rango típico: 60-180 BPM → temperatura 36.5-38.5°C

        hr_factor = 0
        if heart_rate > 60:
            # Factor más agresivo para mejor sincronización
            hr_factor = (heart_rate - 60) / 120.0  # Normalizado 0-1 (antes /160)
            # Esto hace que a 180 BPM el factor sea 1.0 en vez de 0.75

        # Incremento por tiempo de ejercicio
        # La temperatura tarda ~10-15 min en estabilizarse durante ejercicio
        time_factor = min(duration_minutes / 15.0, 1.0)  # Reducido de 20 a 15 min

        # Calcular temperatura objetivo con mayor peso al BPM
        # El BPM ahora tiene ~70% de influencia vs 30% del tiempo
        temp_increase = hr_factor * 3.0 * (0.7 + 0.3 * time_factor) * intensity_factor
        target_temp = self.base_temp + temp_increase

        # Limitar al rango válido
        target_temp = max(self.min_temp, min(target_temp, self.max_temp))

        # Simular variación natural reducida (±0.08°C para menos ruido)
        variation = random.uniform(-0.08, 0.08)
        simulated_temp = target_temp + variation

        # Asegurar que esté en rango válido
        simulated_temp = max(self.min_temp, min(simulated_temp, self.max_temp))

        # Actualizar temperatura actual con transición más rápida
        # Factor aumentado de 0.3 a 0.4 para mejor seguimiento del BPM
        self.current_temp = self._smooth_transition(self.current_temp, simulated_temp, factor=0.4)

        return round(self.current_temp, 1)

    def _smooth_transition(self, current: float, target: float, factor: float = 0.3) -> float:
        """
        Crea transición suave entre temperatura actual y objetivo

        Args:
            current: Temperatura actual
            target: Temperatura objetivo
            factor: Factor de suavizado (0-1)

        Returns:
            Nueva temperatura
        """
        return current + (target - current) * factor

    def reset(self):
        """Resetea el simulador a temperatura base"""
        self.current_temp = self.base_temp
        self.exercise_time = 0

    def get_realistic_reading(
        self,
        heart_rate: int,
        elapsed_minutes: float,
        user_age: int,
        user_weight: float
    ) -> float:
        """
        Obtiene lectura realista considerando más factores

        Args:
            heart_rate: Frecuencia cardíaca
            elapsed_minutes: Minutos transcurridos
            user_age: Edad del usuario
            user_weight: Peso del usuario

        Returns:
            Temperatura simulada
        """
        # Ajuste por edad (personas mayores tienden a tener temp más baja)
        age_adjustment = 0
        if user_age > 50:
            age_adjustment = -0.2
        elif user_age < 25:
            age_adjustment = 0.1

        # Ajuste por peso (más masa = más calor generado)
        weight_adjustment = 0
        if user_weight > 90:
            weight_adjustment = 0.2
        elif user_weight < 60:
            weight_adjustment = -0.1

        # Determinar intensidad automáticamente por FC
        if heart_rate < 100:
            intensity = "low"
        elif heart_rate < 150:
            intensity = "medium"
        else:
            intensity = "high"

        base_temp = self.get_temperature(heart_rate, elapsed_minutes, intensity)
        adjusted_temp = base_temp + age_adjustment + weight_adjustment

        # Asegurar rango válido
        return max(self.min_temp, min(adjusted_temp, self.max_temp))


class TemperatureSensor:
    """Interfaz para sensor de temperatura (simula lectura de hardware)"""

    def __init__(self):
        self.simulator = TemperatureSimulator()
        self.is_connected = True

    def read_temperature(
        self,
        heart_rate: int,
        elapsed_minutes: float,
        user_age: int,
        user_weight: float
    ) -> Optional[float]:
        """
        Lee temperatura del sensor (simulado)

        Args:
            heart_rate: Frecuencia cardíaca actual
            elapsed_minutes: Minutos de ejercicio
            user_age: Edad del usuario
            user_weight: Peso del usuario

        Returns:
            Temperatura o None si no hay conexión
        """
        if not self.is_connected:
            return None

        # Simular pequeño delay de lectura
        time.sleep(0.05)

        return self.simulator.get_realistic_reading(
            heart_rate=heart_rate,
            elapsed_minutes=elapsed_minutes,
            user_age=user_age,
            user_weight=user_weight
        )

    def calibrate(self, base_temp: float):
        """Calibra el sensor con temperatura base del usuario"""
        self.simulator.base_temp = base_temp
        self.simulator.current_temp = base_temp

    def check_connection(self) -> bool:
        """Verifica si el sensor está conectado"""
        return self.is_connected

    def disconnect(self):
        """Simula desconexión del sensor"""
        self.is_connected = False

    def connect(self):
        """Simula reconexión del sensor"""
        self.is_connected = True
