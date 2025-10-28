"""
Servicio de Sesión de Entrenamiento
Coordina cronómetro, sensor de temperatura, predicción de calorías y coach IA
"""
from typing import Optional, Dict, List
from datetime import datetime
import time
import sys
from pathlib import Path
import random
import threading

# Asegurar que src esté en el path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.timer_service import TimerService
from services.temperature_simulator import TemperatureSensor
from services.ai_coach import AICoachService
from services.heart_rate_simulator import BiometricSensor
from calculations import CaloriePredictionService
from models import FeaturePreparator, ModelPredictor, model_manager
from config import TRAINING_CONFIG


class TrainingSession:
    """Gestiona una sesión completa de entrenamiento en tiempo real"""

    def __init__(
        self,
        user_data: Dict,
        target_duration_minutes: int,
        model_name: str = "MLP",
        ai_coach_api_key: Optional[str] = None,
        language: str = "Español",
        enable_tts: bool = False,
        tts_voice_gender: str = "Femenina",
        workout_profile: str = "trote"
    ):
        """
        Inicializa sesión de entrenamiento

        Args:
            user_data: Datos del usuario (nombre, apellidos, sexo, edad, peso, estatura)
            target_duration_minutes: Duración objetivo del entrenamiento
            model_name: Nombre del modelo ML a usar
            ai_coach_api_key: API key para el coach IA (opcional)
            language: Idioma del asistente (Español, English, Français)
            enable_tts: Habilitar Text-to-Speech
            tts_voice_gender: Género de voz (Femenina, Masculina)
            workout_profile: Perfil de entrenamiento (caminata, trote, carrera, hiit, piramide, resistencia)
        """
        # Datos del usuario
        self.user_data = user_data
        self.target_duration_minutes = target_duration_minutes
        self.model_name = model_name
        self.language = language
        self.enable_tts = enable_tts
        self.tts_voice_gender = tts_voice_gender
        self.workout_profile = workout_profile

        # Servicios
        self.timer = TimerService()
        self.biometric_sensor = BiometricSensor(use_simulation=True)
        self.temperature_sensor = TemperatureSensor()
        self.ai_coach = AICoachService(api_key=ai_coach_api_key, language=language)

        # Servicio TTS (si está habilitado)
        self.tts_service = None
        if enable_tts:
            try:
                # Intentar usar TTS mejorado primero
                from services.tts_service_improved import get_improved_tts_service
                self.tts_service = get_improved_tts_service(language, tts_voice_gender)
            except ImportError:
                # Fallback al TTS básico
                from services.tts_service import get_tts_service
                self.tts_service = get_tts_service(language, tts_voice_gender)

        # Calibrar sensor biométrico
        self.biometric_sensor.calibrate(
            resting_hr=user_data.get('pulsaciones', 70),
            age=user_data['edad'],
            fitness_level="medium"
        )

        # Servicio de predicción
        self.prediction_service = CaloriePredictionService(
            model_manager=model_manager,
            feature_preparator=FeaturePreparator,
            model_predictor=ModelPredictor
        )

        # Estado de la sesión
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.heart_rate_readings: List[int] = []
        self.temperature_readings: List[float] = []
        self.calorie_readings: List[float] = []
        self.timestamps: List[float] = []

        # Calorías objetivo (estimación inicial)
        self.target_calories = self._estimate_target_calories()
        self.current_calories = 0.0
        self.last_prediction_time = 0.0
        self.last_coach_message_time = 0.0

        # Coach messages history
        self.coach_messages: List[Dict] = []
        self.last_automatic_message_type = None

        # Thread locks para operaciones concurrentes
        self._calorie_lock = threading.Lock()
        self._message_lock = threading.Lock()

    def start(self):
        """Inicia la sesión de entrenamiento"""
        self.timer.start()
        self._log_message("Sesión iniciada", "info")

    def pause(self):
        """Pausa la sesión"""
        self.timer.pause()
        self._log_message("Sesión pausada", "info")

    def resume(self):
        """Reanuda la sesión"""
        self.timer.resume()
        self._log_message("Sesión reanudada", "info")

    def stop(self):
        """Detiene la sesión completamente y realiza predicción final"""
        self.timer.stop()

        # Hacer predicción final con los últimos datos
        if self.heart_rate_readings and self.temperature_readings:
            last_hr = self.heart_rate_readings[-1]
            last_temp = self.temperature_readings[-1]
            self._update_calorie_prediction(last_hr, last_temp)

        self._log_message("Sesión detenida - Predicción final completada", "info")

    def update_metrics(self, heart_rate: int = None, use_auto_sensors: bool = False) -> Dict:
        """
        Actualiza métricas en tiempo real con sensor biométrico automático

        Args:
            heart_rate: Frecuencia cardíaca (opcional si use_auto_sensors=True)
            use_auto_sensors: Si True, usa sensores biométricos automáticos

        Returns:
            Diccionario con métricas actualizadas
        """
        if not self.timer.is_running:
            return self.get_current_state()

        elapsed_minutes = self.timer.get_elapsed_minutes()
        current_time = time.time()

        # Obtener FC - manual, automática o basada en perfil de entrenamiento
        if use_auto_sensors:
            heart_rate = self.biometric_sensor.read_heart_rate(elapsed_minutes)
        elif heart_rate is None:
            # Usar perfil de entrenamiento para calcular BPM recomendado
            from services.workout_profiles import get_recommended_heart_rate
            heart_rate = get_recommended_heart_rate(
                self.workout_profile,
                elapsed_minutes,
                self.target_duration_minutes,
                self.user_data['edad']
            )

        if heart_rate is None:
            return self.get_current_state()

        # Leer temperatura del sensor biométrico
        temperature = self.biometric_sensor.read_temperature(
            heart_rate=heart_rate,
            elapsed_minutes=elapsed_minutes,
            user_age=self.user_data['edad'],
            user_weight=self.user_data['peso']
        )

        # Registrar lecturas
        self.heart_rate_readings.append(heart_rate)
        if temperature is not None:
            self.temperature_readings.append(temperature)
        self.timestamps.append(elapsed_minutes)

        # Predecir calorías cada 30 segundos (en thread separado para no bloquear)
        prediction_interval = TRAINING_CONFIG['prediction_interval']
        if current_time - self.last_prediction_time >= prediction_interval:
            # Ejecutar predicción en thread separado
            import threading
            thread = threading.Thread(
                target=self._update_calorie_prediction,
                args=(heart_rate, temperature or 37.0)
            )
            thread.daemon = True
            thread.start()
            self.last_prediction_time = current_time

        # Generar mensaje automático del coach cada 30 segundos (en thread separado)
        coach_interval = TRAINING_CONFIG['coach_message_interval']
        if current_time - self.last_coach_message_time >= coach_interval:
            # Ejecutar generación de mensaje en thread separado
            import threading
            thread = threading.Thread(target=self._generate_automatic_coach_message)
            thread.daemon = True
            thread.start()
            self.last_coach_message_time = current_time

        return self.get_current_state()

    def _update_calorie_prediction(self, heart_rate: int, temperature: float):
        """
        Actualiza predicción de calorías de forma acumulativa

        Args:
            heart_rate: Frecuencia cardíaca actual
            temperature: Temperatura actual
        """
        try:
            elapsed_minutes = self.timer.get_elapsed_minutes()

            # Predecir calorías para el tiempo total transcurrido
            # El modelo ya predice acumulativo basado en duration total
            calories, method = self.prediction_service.predict(
                model_name=self.model_name,
                sex=self.user_data['sexo'],
                age=self.user_data['edad'],
                height=self.user_data['estatura'],
                weight=self.user_data['peso'],
                duration=elapsed_minutes,
                heart_rate=heart_rate,
                body_temp=temperature,
                use_fallback=True
            )

            # Las calorías son acumulativas porque el modelo predice
            # para el tiempo TOTAL transcurrido (elapsed_minutes)
            with self._calorie_lock:
                self.current_calories = calories
                self.calorie_readings.append(calories)

        except Exception as e:
            print(f"Error en predicción: {e}")

    def get_current_state(self) -> Dict:
        """
        Obtiene estado actual de la sesión

        Returns:
            Diccionario con estado completo
        """
        progress = self.timer.get_progress_info(self.target_duration_minutes)

        # Temperatura actual (última lectura o None)
        current_temp = self.temperature_readings[-1] if self.temperature_readings else None

        # Frecuencia cardíaca actual (última lectura o None)
        current_hr = self.heart_rate_readings[-1] if self.heart_rate_readings else None

        # Progreso de calorías
        calorie_progress = 0.0
        if self.target_calories > 0:
            calorie_progress = (self.current_calories / self.target_calories) * 100

        return {
            'session_id': self.session_id,
            'timer': {
                'elapsed_seconds': progress['elapsed_seconds'],
                'elapsed_minutes': progress['elapsed_minutes'],
                'formatted_time': progress['formatted_time'],
                'progress_percent': progress['progress_percent'],
                'remaining_minutes': progress['remaining_minutes'],
                'is_complete': progress['is_complete'],
                'status': self.timer.get_status()
            },
            'metrics': {
                'current_calories': round(self.current_calories, 1),
                'target_calories': round(self.target_calories, 1),
                'calorie_progress_percent': round(calorie_progress, 1),
                'current_heart_rate': current_hr,
                'current_temperature': current_temp,
                'avg_heart_rate': self._calculate_avg_hr(),
                'avg_temperature': self._calculate_avg_temp()
            },
            'user': self.user_data,
            'readings_count': len(self.timestamps)
        }

    def get_coach_message(self, message_type: str = "motivation") -> str:
        """
        Obtiene mensaje del coach IA

        Args:
            message_type: Tipo de mensaje (motivation, progress, nutrition, wellness, encouragement)

        Returns:
            Mensaje del coach
        """
        user_name = self.user_data.get('nombre', 'atleta')

        if message_type == "motivation":
            message = self.ai_coach.generate_motivation(
                calories_burned=self.current_calories,
                elapsed_minutes=self.timer.get_elapsed_minutes(),
                target_calories=self.target_calories,
                user_name=user_name
            )
        elif message_type == "progress":
            message = self.ai_coach.generate_progress_update(
                calories_burned=self.current_calories,
                target_calories=self.target_calories,
                user_name=user_name
            )
        elif message_type == "nutrition":
            message = self.ai_coach.generate_nutrition_tip(
                calories_burned=self.current_calories,
                user_name=user_name
            )
        elif message_type == "wellness":
            message = self.ai_coach.generate_wellness_tip(user_name=user_name)
        elif message_type == "encouragement":
            progress = self.timer.get_progress_info(self.target_duration_minutes)
            stopped_early = not progress['is_complete']
            message = self.ai_coach.generate_encouragement(
                stopped_early=stopped_early,
                completed_percent=progress['progress_percent'],
                user_name=user_name
            )
        elif message_type == "food_comparison":
            message = self.ai_coach.generate_food_comparison(
                calories_burned=self.current_calories,
                user_name=user_name
            )
        else:
            message = f"¡Sigue adelante, {user_name}! 💪"

        # Registrar mensaje (thread-safe)
        with self._message_lock:
            self._log_message(message, "coach", message_type)

        # Reproducir con TTS si está habilitado (ya es no-bloqueante por sí mismo)
        if self.tts_service and self.enable_tts:
            # Reproducir de forma no bloqueante
            self.tts_service.speak(message, blocking=False)

        return message

    def _generate_automatic_coach_message(self) -> str:
        """
        Genera mensaje automático del coach de forma rotativa

        Returns:
            Mensaje generado y tipo de mensaje
        """
        # Tipos de mensajes según el contexto
        message_types = TRAINING_CONFIG['coach']['message_types']

        # Filtrar mensajes que requieren predicción de calorías
        calorie_dependent = ['motivation', 'progress', 'food_comparison']
        general_advice = ['nutrition', 'wellness']

        # Seleccionar tipo de mensaje de forma inteligente
        # 60% mensajes relacionados con calorías, 40% consejos generales
        if random.random() < 0.6 and self.current_calories > 0:
            # Mensajes que requieren calorías actualizadas
            message_type = random.choice(calorie_dependent)
        else:
            # Consejos generales
            message_type = random.choice(general_advice)

        # Evitar repetir el mismo tipo consecutivamente
        if message_type == self.last_automatic_message_type:
            available = [t for t in message_types if t != message_type]
            message_type = random.choice(available)

        self.last_automatic_message_type = message_type

        # Generar el mensaje
        return self.get_coach_message(message_type)

    def get_last_coach_message(self) -> Optional[Dict]:
        """
        Obtiene el último mensaje del coach

        Returns:
            Último mensaje o None
        """
        if self.coach_messages:
            return self.coach_messages[-1]
        return None

    def get_session_summary(self) -> Dict:
        """
        Obtiene resumen completo de la sesión

        Returns:
            Diccionario con resumen
        """
        progress = self.timer.get_progress_info(self.target_duration_minutes)

        return {
            'session_id': self.session_id,
            'user_data': self.user_data,
            'target_duration_minutes': self.target_duration_minutes,
            'completed_minutes': progress['elapsed_minutes'],
            'completion_percent': progress['progress_percent'],
            'calories_burned': round(self.current_calories, 1),
            'target_calories': round(self.target_calories, 1),
            'calorie_goal_achieved': self.current_calories >= self.target_calories,
            'avg_heart_rate': self._calculate_avg_hr(),
            'max_heart_rate': max(self.heart_rate_readings) if self.heart_rate_readings else 0,
            'min_heart_rate': min(self.heart_rate_readings) if self.heart_rate_readings else 0,
            'avg_temperature': self._calculate_avg_temp(),
            'max_temperature': max(self.temperature_readings) if self.temperature_readings else 0,
            'total_readings': len(self.timestamps),
            'coach_messages': self.coach_messages
        }

    def _estimate_target_calories(self) -> float:
        """
        Estima calorías objetivo basado en duración y perfil del usuario

        Returns:
            Calorías objetivo estimadas
        """
        # Estimación simple: ~10 calorías por minuto para ejercicio moderado
        # Ajustar por peso
        weight = self.user_data.get('peso', 70)
        base_rate = 10.0  # kcal/min base
        weight_factor = weight / 70.0  # Factor por peso

        estimated = base_rate * weight_factor * self.target_duration_minutes

        return estimated

    def _calculate_avg_hr(self) -> Optional[float]:
        """Calcula frecuencia cardíaca promedio"""
        if not self.heart_rate_readings:
            return None
        return round(sum(self.heart_rate_readings) / len(self.heart_rate_readings), 1)

    def _calculate_avg_temp(self) -> Optional[float]:
        """Calcula temperatura promedio"""
        if not self.temperature_readings:
            return None
        return round(sum(self.temperature_readings) / len(self.temperature_readings), 1)

    def _log_message(self, message: str, message_category: str, message_type: str = ""):
        """
        Registra mensaje en el historial

        Args:
            message: Texto del mensaje
            message_category: Categoría (info, coach, error)
            message_type: Tipo específico de mensaje
        """
        self.coach_messages.append({
            'timestamp': datetime.now().isoformat(),
            'elapsed_minutes': self.timer.get_elapsed_minutes(),
            'category': message_category,
            'type': message_type,
            'message': message
        })

    def export_session_data(self) -> Dict:
        """
        Exporta todos los datos de la sesión para análisis

        Returns:
            Diccionario completo con todos los datos
        """
        return {
            'summary': self.get_session_summary(),
            'time_series': {
                'timestamps': self.timestamps,
                'heart_rates': self.heart_rate_readings,
                'temperatures': self.temperature_readings,
                'calories': self.calorie_readings
            },
            'model_used': self.model_name
        }
