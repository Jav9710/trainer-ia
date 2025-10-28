"""
Servicio de Coach IA - Asistente Motivacional
Conecta con OpenRouter para generar mensajes motivacionales
"""
import requests
from typing import Dict, Optional, List
import random
from .coach_translations import TRANSLATIONS


class AICoachService:
    """Servicio de coach virtual con IA para motivación durante entrenamiento"""

    def __init__(self, api_key: Optional[str] = None, language: str = "Español"):
        """
        Inicializa el servicio de coach IA

        Args:
            api_key: API key de OpenRouter (opcional, usa fallback si no se proporciona)
            language: Idioma para los mensajes (Español, English, Français)
        """
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "mistralai/mistral-7b-instruct"  # Modelo gratuito y rápido
        self.use_fallback = api_key is None or api_key == ""
        self.language = language
        self._load_translations()

    def _load_translations(self):
        """Carga traducciones para los mensajes fallback"""
        self.lang_messages = TRANSLATIONS.get(self.language, TRANSLATIONS['Español'])

    def generate_motivation(
        self,
        calories_burned: float,
        elapsed_minutes: float,
        target_calories: float,
        user_name: str = "atleta"
    ) -> str:
        """
        Genera mensaje motivacional personalizado

        Args:
            calories_burned: Calorías quemadas hasta ahora
            elapsed_minutes: Minutos transcurridos
            target_calories: Objetivo de calorías
            user_name: Nombre del usuario

        Returns:
            Mensaje motivacional
        """
        if self.use_fallback:
            return self._generate_fallback_motivation(
                calories_burned,
                elapsed_minutes,
                target_calories,
                user_name
            )

        prompt = self._build_motivation_prompt(
            calories_burned,
            elapsed_minutes,
            target_calories,
            user_name
        )

        try:
            return self._call_openrouter(prompt)
        except Exception as e:
            print(f"Error con OpenRouter: {e}")
            return self._generate_fallback_motivation(
                calories_burned,
                elapsed_minutes,
                target_calories,
                user_name
            )

    def generate_progress_update(
        self,
        calories_burned: float,
        target_calories: float,
        user_name: str = "atleta"
    ) -> str:
        """
        Genera actualización de progreso

        Args:
            calories_burned: Calorías quemadas
            target_calories: Objetivo de calorías
            user_name: Nombre del usuario

        Returns:
            Mensaje de progreso
        """
        progress_percent = (calories_burned / target_calories) * 100

        if self.use_fallback:
            return self._generate_fallback_progress(
                calories_burned,
                progress_percent,
                user_name
            )

        prompt = f"""Eres un coach personal motivador. El usuario {user_name} ha quemado {calories_burned:.0f} calorías,
lo que representa el {progress_percent:.1f}% de su objetivo.

Genera un mensaje ULTRA CORTO (máximo 1 línea de 10 palabras) sobre su progreso.

IMPORTANTE: NO uses emojis. Usa solo palabras. Sé profesional y motivador."""

        try:
            return self._call_openrouter(prompt)
        except Exception:
            return self._generate_fallback_progress(
                calories_burned,
                progress_percent,
                user_name
            )

    def generate_nutrition_tip(
        self,
        calories_burned: float,
        user_name: str = "atleta"
    ) -> str:
        """
        Genera consejo nutricional

        Args:
            calories_burned: Calorías quemadas
            user_name: Nombre del usuario

        Returns:
            Consejo nutricional
        """
        if self.use_fallback:
            return self._generate_fallback_nutrition_tip(calories_burned)

        prompt = f"""Eres un nutricionista deportivo. El usuario {user_name} acaba de quemar {calories_burned:.0f} calorías.

Da un consejo nutricional ULTRA CORTO (máximo 1 línea de 10 palabras) para recuperación post-ejercicio.

IMPORTANTE: NO uses emojis. Usa solo palabras. Sé profesional y claro."""

        try:
            return self._call_openrouter(prompt)
        except Exception:
            return self._generate_fallback_nutrition_tip(calories_burned)

    def generate_food_comparison(
        self,
        calories_burned: float,
        user_name: str = "atleta"
    ) -> str:
        """
        Compara calorías con comida chatarra

        Args:
            calories_burned: Calorías quemadas
            user_name: Nombre del usuario

        Returns:
            Mensaje de comparación
        """
        comparisons = {
            "una Hamburguesa Big Mac": 563,
            "una Pizza completa": 2000,
            "Papas fritas grandes": 510,
            "un Refresco de 1 litro": 420,
            "una Dona glaseada": 250,
            "una Barra de chocolate": 235,
            "3 Tacos": 450,
            "un Helado sundae": 340
        }

        # Encontrar comparación más cercana
        best_match = None
        min_diff = float('inf')

        for food, cals in comparisons.items():
            diff = abs(cals - calories_burned)
            if diff < min_diff:
                min_diff = diff
                best_match = (food, cals)

        if best_match:
            food_name, food_cals = best_match
            if calories_burned >= food_cals:
                msg = self.lang_messages['food_comparison_exceeded']
                return msg.format(name=user_name, food=food_name, food_cals=food_cals)
            else:
                percent = (calories_burned / food_cals) * 100
                msg = self.lang_messages['food_comparison_progress']
                return msg.format(percent=percent, food=food_name, name=user_name)

        msg = self.lang_messages['food_comparison_default']
        return msg.format(name=user_name)

    def generate_encouragement(
        self,
        stopped_early: bool = False,
        completed_percent: float = 0,
        user_name: str = "atleta"
    ) -> str:
        """
        Genera mensaje de ánimo

        Args:
            stopped_early: Si el usuario detuvo antes de terminar
            completed_percent: Porcentaje completado
            user_name: Nombre del usuario

        Returns:
            Mensaje de ánimo
        """
        if stopped_early:
            if self.use_fallback:
                return self._generate_fallback_encouragement(completed_percent, user_name)

            prompt = f"""Eres un coach empático y motivador. El usuario {user_name} detuvo su entrenamiento
habiendo completado el {completed_percent:.0f}% de su objetivo.

Genera un mensaje ULTRA CORTO y POSITIVO (máximo 1 línea de 10 palabras) que lo motive.

IMPORTANTE: NO uses emojis. Usa solo palabras. Sé empático y profesional."""

            try:
                return self._call_openrouter(prompt)
            except Exception:
                return self._generate_fallback_encouragement(completed_percent, user_name)
        else:
            msg = self.lang_messages['congratulations']
            return msg.format(name=user_name)

    def generate_wellness_tip(self, user_name: str = "atleta") -> str:
        """
        Genera consejo de bienestar general

        Args:
            user_name: Nombre del usuario

        Returns:
            Consejo de bienestar
        """
        if self.use_fallback:
            return self._generate_fallback_wellness_tip(user_name)

        prompt = """Eres un coach de vida y bienestar.
Genera un consejo ULTRA CORTO (máximo 1 línea de 10 palabras) sobre cómo vivir feliz y saludable.

IMPORTANTE: NO uses emojis. Usa solo palabras. Sé profesional y motivador."""

        try:
            return self._call_openrouter(prompt)
        except Exception:
            return self._generate_fallback_wellness_tip(user_name)

    def _call_openrouter(self, prompt: str) -> str:
        """
        Llama a OpenRouter API

        Args:
            prompt: Prompt para la IA

        Returns:
            Respuesta generada
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 50,
            "temperature": 0.7
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()

            # Limpiar todos los tags del modelo
            content = content.replace('[B_INST]', '').replace('[/B_INST]', '')
            content = content.replace('[INST]', '').replace('[/INST]', '')
            content = content.replace('[OUT]', '').replace('[/OUT]', '')
            content = content.replace('<s>', '').replace('</s>', '')
            content = content.replace('<<SYS>>', '').replace('<</SYS>>', '')

            # Limpiar espacios múltiples y saltos de línea extra
            import re
            content = re.sub(r'\s+', ' ', content)
            content = content.strip()

            return content
        else:
            raise Exception(f"OpenRouter error: {response.status_code}")

    def _build_motivation_prompt(
        self,
        calories_burned: float,
        elapsed_minutes: float,
        target_calories: float,
        user_name: str
    ) -> str:
        """Construye prompt para mensaje motivacional"""
        progress_percent = (calories_burned / target_calories) * 100

        # Mapeo de idiomas
        lang_map = {
            'Español': 'Spanish',
            'English': 'English',
            'Français': 'French'
        }
        lang_code = lang_map.get(self.language, 'Spanish')

        return f"""You are an energetic and motivating personal coach. Respond ONLY in {lang_code}. The user {user_name} is training:
- Has burned {calories_burned:.0f} calories in {elapsed_minutes:.0f} minutes
- Target is {target_calories:.0f} calories
- Progress: {progress_percent:.1f}%

IMPORTANT: Generate an ULTRA SHORT energetic message (maximum 1 line, 10 words) in {lang_code} to encourage them.
DO NOT use emojis. Use only words. Be professional and motivating."""

    # ========================================================================
    # MÉTODOS FALLBACK (cuando no hay API key)
    # ========================================================================

    def _generate_fallback_motivation(
        self,
        calories_burned: float,
        elapsed_minutes: float,
        target_calories: float,
        user_name: str
    ) -> str:
        """Genera motivación usando mensajes predefinidos multiidioma"""
        progress_percent = (calories_burned / target_calories) * 100

        if progress_percent < 25:
            messages = self.lang_messages['motivation_low']
        elif progress_percent < 50:
            messages = self.lang_messages['motivation_mid']
        elif progress_percent < 75:
            messages = self.lang_messages['motivation_high']
        else:
            messages = self.lang_messages['motivation_veryhigh']

        # Formatear mensaje con variables
        msg = random.choice(messages)
        return msg.format(
            name=user_name,
            percent=progress_percent,
            calories=calories_burned,
            remaining=target_calories - calories_burned
        )

    def _generate_fallback_progress(
        self,
        calories_burned: float,
        progress_percent: float,
        user_name: str
    ) -> str:
        """Genera actualización de progreso fallback multiidioma"""
        messages = self.lang_messages['progress']
        msg = random.choice(messages)
        return msg.format(name=user_name, calories=calories_burned, percent=progress_percent)

    def _generate_fallback_nutrition_tip(self, calories_burned: float) -> str:
        """Genera consejo nutricional fallback multiidioma"""
        tips = self.lang_messages['nutrition']
        return random.choice(tips)

    def _generate_fallback_encouragement(
        self,
        completed_percent: float,
        user_name: str
    ) -> str:
        """Genera mensaje de ánimo fallback sin emojis"""
        if completed_percent > 80:
            messages = [
                f"¡{user_name}! Completaste {completed_percent:.0f}%. ¡Eso es increíble! Mañana será aún mejor.",
                f"¡{completed_percent:.0f}% es EXCELENTE, {user_name}! Tu cuerpo te agradece. Descansa bien.",
                f"¡Qué gran esfuerzo, {user_name}! {completed_percent:.0f}% logrado. Estás construyendo disciplina."
            ]
        elif completed_percent > 50:
            messages = [
                f"{user_name}, {completed_percent:.0f}% es un logro real. Cada sesión cuenta. ¡Regresa pronto!",
                f"¡{completed_percent:.0f}% completado, {user_name}! Eso es progreso. Mañana es otro día.",
                f"¡Bien hecho, {user_name}! {completed_percent:.0f}% es mejor que cero. La constancia es clave."
            ]
        else:
            messages = [
                f"{user_name}, lo importante es que lo intentaste. Escucha a tu cuerpo. Vuelve cuando estés listo.",
                f"¡Hey {user_name}! Incluso {completed_percent:.0f}% es un paso adelante. No te presiones. Regresa fuerte.",
                f"¡{user_name}! Tu bienestar es primero. {completed_percent:.0f}% es mejor que nada. ¡Vuelve pronto!"
            ]
        return random.choice(messages)

    def _generate_fallback_wellness_tip(self, user_name: str) -> str:
        """Genera consejo de bienestar fallback multiidioma"""
        tips = self.lang_messages['wellness']
        msg = random.choice(tips)
        return msg.format(name=user_name)
