"""
Servicio de Perfiles de Entrenamiento
Define diferentes tipos de entrenamientos con patrones de intensidad variables
"""
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class IntensityPoint:
    """Punto de intensidad en el entrenamiento"""
    time_percent: float  # Porcentaje del tiempo total (0-100)
    intensity: float     # Intensidad 0.0 (reposo) a 1.0 (máximo)
    hr_percent: float    # Porcentaje de FC máxima (0-100)

    def get_heart_rate(self, age: int) -> int:
        """Calcula BPM basado en edad y porcentaje de FC máxima"""
        max_hr = 220 - age
        resting_hr = 70
        target_hr = resting_hr + (max_hr - resting_hr) * (self.hr_percent / 100)
        return int(target_hr)


@dataclass
class WorkoutProfile:
    """Perfil completo de un tipo de entrenamiento"""
    name: str
    description: str
    icon: str
    intensity_points: List[IntensityPoint]
    avg_calories_30min: int  # Calorías promedio en 30 min
    difficulty: str  # 'Fácil', 'Moderado', 'Intenso', 'Muy Intenso'

    def get_intensity_at_time(self, elapsed_minutes: float, total_minutes: float) -> IntensityPoint:
        """
        Obtiene la intensidad en un momento específico del entrenamiento

        Args:
            elapsed_minutes: Minutos transcurridos
            total_minutes: Duración total del entrenamiento

        Returns:
            Punto de intensidad interpolado
        """
        if total_minutes == 0:
            return self.intensity_points[0]

        # Calcular porcentaje de tiempo transcurrido
        time_percent = (elapsed_minutes / total_minutes) * 100
        time_percent = min(100, max(0, time_percent))

        # Encontrar puntos de intensidad alrededor del tiempo actual
        before_point = self.intensity_points[0]
        after_point = self.intensity_points[-1]

        for i, point in enumerate(self.intensity_points):
            if point.time_percent <= time_percent:
                before_point = point
                if i + 1 < len(self.intensity_points):
                    after_point = self.intensity_points[i + 1]
                else:
                    after_point = point
            else:
                after_point = point
                break

        # Interpolar entre los dos puntos
        if before_point.time_percent == after_point.time_percent:
            return before_point

        # Interpolación lineal
        t = (time_percent - before_point.time_percent) / (after_point.time_percent - before_point.time_percent)

        interpolated_intensity = before_point.intensity + t * (after_point.intensity - before_point.intensity)
        interpolated_hr_percent = before_point.hr_percent + t * (after_point.hr_percent - before_point.hr_percent)

        return IntensityPoint(
            time_percent=time_percent,
            intensity=interpolated_intensity,
            hr_percent=interpolated_hr_percent
        )

    def get_chart_data(self) -> Tuple[List[float], List[float]]:
        """
        Obtiene datos para graficar el perfil de intensidad

        Returns:
            (tiempos, intensidades) para graficar
        """
        times = [p.time_percent for p in self.intensity_points]
        intensities = [p.intensity * 100 for p in self.intensity_points]
        return times, intensities


# ============================================================================
# PERFILES DE ENTRENAMIENTO PREDEFINIDOS
# ============================================================================

WORKOUT_PROFILES = {
    'caminata': WorkoutProfile(
        name='Caminata Ligera',
        description='Actividad de baja intensidad, ideal para principiantes o recuperación',
        icon='🚶',
        difficulty='Fácil',
        avg_calories_30min=120,
        intensity_points=[
            IntensityPoint(0, 0.20, 40),    # Inicio suave
            IntensityPoint(10, 0.30, 45),   # Calentamiento
            IntensityPoint(50, 0.35, 50),   # Ritmo constante
            IntensityPoint(90, 0.30, 45),   # Enfriamiento
            IntensityPoint(100, 0.20, 40),  # Final suave
        ]
    ),

    'trote': WorkoutProfile(
        name='Trote Moderado',
        description='Carrera suave y constante, intensidad moderada',
        icon='🏃',
        difficulty='Moderado',
        avg_calories_30min=250,
        intensity_points=[
            IntensityPoint(0, 0.30, 50),    # Calentamiento caminando
            IntensityPoint(10, 0.50, 65),   # Inicio del trote
            IntensityPoint(20, 0.60, 70),   # Ritmo de trote
            IntensityPoint(80, 0.60, 70),   # Mantener ritmo
            IntensityPoint(90, 0.45, 60),   # Reducir velocidad
            IntensityPoint(100, 0.30, 50),  # Enfriamiento
        ]
    ),

    'correr': WorkoutProfile(
        name='Carrera Intensa',
        description='Carrera a ritmo alto, quema máxima de calorías',
        icon='🏃‍♂️',
        difficulty='Intenso',
        avg_calories_30min=400,
        intensity_points=[
            IntensityPoint(0, 0.40, 55),    # Calentamiento activo
            IntensityPoint(10, 0.65, 75),   # Aumentar a carrera
            IntensityPoint(20, 0.80, 85),   # Ritmo intenso
            IntensityPoint(70, 0.80, 85),   # Mantener intensidad
            IntensityPoint(85, 0.70, 75),   # Reducción gradual
            IntensityPoint(95, 0.50, 65),   # Pre-enfriamiento
            IntensityPoint(100, 0.35, 55),  # Enfriamiento final
        ]
    ),

    'hiit': WorkoutProfile(
        name='HIIT - Intervalos',
        description='Intervalos de alta intensidad alternados con recuperación',
        icon='⚡',
        difficulty='Muy Intenso',
        avg_calories_30min=450,
        intensity_points=[
            IntensityPoint(0, 0.35, 50),    # Calentamiento
            IntensityPoint(10, 0.50, 65),   # Preparación
            # Intervalos: alta-baja-alta-baja...
            IntensityPoint(15, 0.90, 90),   # Sprint 1
            IntensityPoint(20, 0.40, 55),   # Recuperación 1
            IntensityPoint(25, 0.90, 90),   # Sprint 2
            IntensityPoint(30, 0.40, 55),   # Recuperación 2
            IntensityPoint(35, 0.90, 90),   # Sprint 3
            IntensityPoint(40, 0.40, 55),   # Recuperación 3
            IntensityPoint(45, 0.90, 90),   # Sprint 4
            IntensityPoint(50, 0.40, 55),   # Recuperación 4
            IntensityPoint(55, 0.90, 90),   # Sprint 5
            IntensityPoint(60, 0.40, 55),   # Recuperación 5
            IntensityPoint(65, 0.90, 90),   # Sprint 6
            IntensityPoint(70, 0.40, 55),   # Recuperación 6
            IntensityPoint(75, 0.90, 90),   # Sprint final
            IntensityPoint(85, 0.50, 65),   # Enfriamiento activo
            IntensityPoint(95, 0.35, 50),   # Enfriamiento
            IntensityPoint(100, 0.25, 45),  # Final
        ]
    ),

    'piramide': WorkoutProfile(
        name='Pirámide Progresiva',
        description='Incremento progresivo de intensidad hasta el pico, luego descenso',
        icon='🔺',
        difficulty='Intenso',
        avg_calories_30min=380,
        intensity_points=[
            IntensityPoint(0, 0.30, 50),    # Base
            IntensityPoint(15, 0.50, 65),   # Subida nivel 1
            IntensityPoint(30, 0.65, 75),   # Subida nivel 2
            IntensityPoint(45, 0.80, 85),   # Subida nivel 3
            IntensityPoint(50, 0.90, 90),   # PICO
            IntensityPoint(60, 0.80, 85),   # Bajada nivel 3
            IntensityPoint(75, 0.65, 75),   # Bajada nivel 2
            IntensityPoint(90, 0.50, 65),   # Bajada nivel 1
            IntensityPoint(100, 0.30, 50),  # Base final
        ]
    ),

    'resistencia': WorkoutProfile(
        name='Resistencia Constante',
        description='Mantiene intensidad media-alta durante todo el entrenamiento',
        icon='💪',
        difficulty='Moderado',
        avg_calories_30min=320,
        intensity_points=[
            IntensityPoint(0, 0.35, 50),    # Calentamiento
            IntensityPoint(10, 0.55, 70),   # Subir a ritmo
            IntensityPoint(20, 0.70, 75),   # Intensidad de trabajo
            IntensityPoint(80, 0.70, 75),   # Mantener constante
            IntensityPoint(90, 0.55, 65),   # Reducir
            IntensityPoint(100, 0.35, 50),  # Enfriamiento
        ]
    ),
}


def get_workout_profile(profile_name: str) -> WorkoutProfile:
    """
    Obtiene un perfil de entrenamiento por nombre

    Args:
        profile_name: Nombre del perfil

    Returns:
        Perfil de entrenamiento
    """
    return WORKOUT_PROFILES.get(profile_name.lower(), WORKOUT_PROFILES['trote'])


def list_workout_profiles() -> List[Tuple[str, WorkoutProfile]]:
    """
    Lista todos los perfiles disponibles

    Returns:
        Lista de (nombre, perfil)
    """
    return [(name, profile) for name, profile in WORKOUT_PROFILES.items()]


def get_recommended_heart_rate(
    profile_name: str,
    elapsed_minutes: float,
    total_minutes: float,
    user_age: int
) -> int:
    """
    Obtiene la frecuencia cardíaca recomendada para un momento específico

    Args:
        profile_name: Nombre del perfil de entrenamiento
        elapsed_minutes: Minutos transcurridos
        total_minutes: Duración total
        user_age: Edad del usuario

    Returns:
        BPM recomendado
    """
    profile = get_workout_profile(profile_name)
    intensity = profile.get_intensity_at_time(elapsed_minutes, total_minutes)
    return intensity.get_heart_rate(user_age)
