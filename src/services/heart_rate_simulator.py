"""
Simulador de Frecuencia Cardíaca
Simula BPM de forma realista durante el ejercicio basado en el tiempo transcurrido
"""
import random
import time
from typing import Optional
import sys
from pathlib import Path

# Asegurar que src esté en el path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TRAINING_CONFIG


class HeartRateSimulator:
    """Simula frecuencia cardíaca durante el ejercicio de forma realista"""

    def __init__(
        self,
        resting_hr: int = None,
        age: int = 25,
        fitness_level: str = "medium"
    ):
        """
        Inicializa el simulador de FC

        Args:
            resting_hr: FC en reposo (si no se proporciona, se calcula)
            age: Edad del usuario
            fitness_level: Nivel de fitness (low, medium, high)
        """
        self.age = age
        self.fitness_level = fitness_level

        # FC en reposo según fitness
        if resting_hr is None:
            fitness_factors = {'low': 75, 'medium': 70, 'high': 60}
            self.resting_hr = fitness_factors.get(fitness_level, 70)
        else:
            self.resting_hr = resting_hr

        # FC máxima teórica (220 - edad)
        self.max_hr = 220 - age

        # FC objetivo para diferentes intensidades
        self.warmup_hr = int(self.resting_hr + (self.max_hr - self.resting_hr) * 0.5)
        self.moderate_hr = int(self.resting_hr + (self.max_hr - self.resting_hr) * 0.6)
        self.vigorous_hr = int(self.resting_hr + (self.max_hr - self.resting_hr) * 0.75)

        self.current_hr = self.resting_hr
        self.last_update_time = 0

    def get_heart_rate(self, elapsed_minutes: float, intensity: str = "auto") -> int:
        """
        Obtiene FC simulada basada en tiempo de ejercicio

        Args:
            elapsed_minutes: Minutos transcurridos de ejercicio
            intensity: Intensidad del ejercicio (auto, low, medium, high)

        Returns:
            Frecuencia cardíaca simulada
        """
        if intensity == "auto":
            # Determinar intensidad automáticamente según el tiempo
            intensity = self._auto_detect_intensity(elapsed_minutes)

        target_hr = self._get_target_hr(intensity, elapsed_minutes)

        # Simular variación natural (±5 bpm)
        variation = random.randint(-5, 5)
        simulated_hr = target_hr + variation

        # Limitar a rangos válidos
        simulated_hr = max(TRAINING_CONFIG['heart_rate']['min'],
                          min(simulated_hr, TRAINING_CONFIG['heart_rate']['max']))

        # Transición suave
        self.current_hr = self._smooth_transition(self.current_hr, simulated_hr)

        return int(self.current_hr)

    def _auto_detect_intensity(self, elapsed_minutes: float) -> str:
        """
        Detecta intensidad automáticamente basada en el tiempo

        Patrón típico de entrenamiento:
        - 0-5 min: Calentamiento (low)
        - 5-25 min: Ejercicio moderado-intenso (medium-high)
        - 25-30 min: Enfriamiento (low-medium)

        Args:
            elapsed_minutes: Minutos transcurridos

        Returns:
            Nivel de intensidad
        """
        if elapsed_minutes < 3:
            return "low"  # Calentamiento inicial
        elif elapsed_minutes < 5:
            return "medium"  # Transición
        elif elapsed_minutes < 20:
            return "high"  # Ejercicio intenso
        elif elapsed_minutes < 25:
            return "medium"  # Comenzando enfriamiento
        else:
            return "low"  # Enfriamiento final

    def _get_target_hr(self, intensity: str, elapsed_minutes: float) -> int:
        """
        Obtiene FC objetivo según intensidad

        Args:
            intensity: Nivel de intensidad
            elapsed_minutes: Minutos transcurridos

        Returns:
            FC objetivo
        """
        if intensity == "low":
            # Durante calentamiento, FC aumenta gradualmente
            if elapsed_minutes < 3:
                progress = elapsed_minutes / 3.0
                return int(self.resting_hr + (self.warmup_hr - self.resting_hr) * progress)
            else:
                return self.warmup_hr

        elif intensity == "medium":
            return self.moderate_hr

        elif intensity == "high":
            return self.vigorous_hr

        return self.moderate_hr

    def _smooth_transition(self, current: float, target: float, factor: float = 0.3) -> float:
        """
        Crea transición suave entre FC actual y objetivo

        Args:
            current: FC actual
            target: FC objetivo
            factor: Factor de suavizado (0-1)

        Returns:
            Nueva FC
        """
        return current + (target - current) * factor


class BiometricSensor:
    """
    Conector para sensores biométricos externos
    Puede conectarse a dispositivos reales o usar simulación
    """

    def __init__(self, use_simulation: bool = True):
        """
        Inicializa el sensor biométrico

        Args:
            use_simulation: Si True, usa simulación. Si False, intenta conectar hardware
        """
        self.use_simulation = use_simulation
        self.is_connected = False
        self.hr_simulator = None
        self.device_info = None

        if use_simulation:
            self._init_simulation()
        else:
            self._init_hardware()

    def _init_simulation(self):
        """Inicializa modo de simulación"""
        self.hr_simulator = HeartRateSimulator()
        self.is_connected = True
        self.device_info = {
            'type': 'simulator',
            'name': 'Simulador Virtual',
            'capabilities': ['heart_rate', 'temperature']
        }

    def _init_hardware(self):
        """
        Inicializa conexión con hardware real
        PLACEHOLDER para futura implementación
        """
        # TODO: Implementar conexión Bluetooth/ANT+
        # Por ahora, fallback a simulación
        print("⚠️ Hardware no implementado aún. Usando simulación...")
        self._init_simulation()

    def calibrate(self, resting_hr: int = None, age: int = 25, fitness_level: str = "medium"):
        """
        Calibra el sensor con datos del usuario

        Args:
            resting_hr: FC en reposo del usuario
            age: Edad del usuario
            fitness_level: Nivel de fitness
        """
        if self.use_simulation:
            self.hr_simulator = HeartRateSimulator(resting_hr, age, fitness_level)

    def read_heart_rate(self, elapsed_minutes: float) -> Optional[int]:
        """
        Lee frecuencia cardíaca del sensor

        Args:
            elapsed_minutes: Minutos de ejercicio

        Returns:
            Frecuencia cardíaca o None si no hay conexión
        """
        if not self.is_connected:
            return None

        if self.use_simulation:
            return self.hr_simulator.get_heart_rate(elapsed_minutes)
        else:
            # TODO: Leer de hardware real
            return None

    def read_temperature(self, heart_rate: int, elapsed_minutes: float, user_age: int, user_weight: float) -> Optional[float]:
        """
        Lee temperatura del sensor (por ahora usa simulación existente)

        Args:
            heart_rate: FC actual
            elapsed_minutes: Minutos transcurridos
            user_age: Edad del usuario
            user_weight: Peso del usuario

        Returns:
            Temperatura o None
        """
        if not self.is_connected:
            return None

        # Importar simulador de temperatura
        from services.temperature_simulator import TemperatureSensor

        temp_sensor = TemperatureSensor()
        return temp_sensor.read_temperature(
            heart_rate=heart_rate,
            elapsed_minutes=elapsed_minutes,
            user_age=user_age,
            user_weight=user_weight
        )

    def get_device_info(self) -> dict:
        """Obtiene información del dispositivo conectado"""
        return self.device_info if self.device_info else {
            'type': 'none',
            'name': 'Sin conexión',
            'capabilities': []
        }

    def disconnect(self):
        """Desconecta el sensor"""
        self.is_connected = False
        self.device_info = None

    def reconnect(self):
        """Intenta reconectar el sensor"""
        if self.use_simulation:
            self._init_simulation()
        else:
            self._init_hardware()


# Alias para compatibilidad
HeartRateSensor = BiometricSensor
