"""
Módulo de servicios
Contiene servicios para entrenamiento en tiempo real
"""
import sys
from pathlib import Path

# Asegurar que src esté en el path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.timer_service import TimerService, IntervalTimer
from services.temperature_simulator import TemperatureSimulator, TemperatureSensor
from services.ai_coach import AICoachService
from services.heart_rate_simulator import HeartRateSimulator, BiometricSensor
from services.training_session import TrainingSession

__all__ = [
    'TimerService',
    'IntervalTimer',
    'TemperatureSimulator',
    'TemperatureSensor',
    'AICoachService',
    'HeartRateSimulator',
    'BiometricSensor',
    'TrainingSession'
]
