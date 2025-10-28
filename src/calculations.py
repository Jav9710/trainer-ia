"""
Lógica de cálculos y predicciones de calorías
"""
from typing import Dict
import numpy as np

from config import FORMULA_CONSTANTS, FOOD_EQUIVALENTS


class CalorieCalculator:
    """Calcula calorías usando fórmulas cuando no hay modelos disponibles"""

    @staticmethod
    def calculate_by_heart_rate(
            sex: str,
            age: int,
            weight: float,
            heart_rate: int,
            duration: int
    ) -> float:
        """
        Calcula calorías basado en frecuencia cardíaca

        Args:
            sex: 'Masculino' o 'Femenino'
            age: Edad en años
            weight: Peso en kg
            heart_rate: Frecuencia cardíaca en ppm
            duration: Duración en minutos

        Returns:
            Calorías calculadas
        """
        if sex == 'Masculino':
            constants = FORMULA_CONSTANTS['male']
        else:
            constants = FORMULA_CONSTANTS['female']

        calories = (
                           (
                                   constants['base'] +
                                   (constants['hr_coef'] * heart_rate) +
                                   (constants['weight_coef'] * weight) +
                                   (constants['age_coef'] * age)
                           ) / constants['divisor']
                   ) * duration

        return calories

    @staticmethod
    def calculate_by_met(
            weight: float,
            duration: int,
            met: float = None
    ) -> float:
        """
        Calcula calorías usando MET (Metabolic Equivalent of Task)

        Args:
            weight: Peso en kg
            duration: Duración en minutos
            met: Valor MET (si no se proporciona, usa default)

        Returns:
            Calorías calculadas
        """
        if met is None:
            met = FORMULA_CONSTANTS['met_default']

        calories = ((met * weight * 3.5) / 200) * duration

        return calories

    @staticmethod
    def adjust_by_temperature(
            calories: float,
            body_temp: float
    ) -> float:
        """
        Ajusta calorías basado en temperatura corporal

        Args:
            calories: Calorías base
            body_temp: Temperatura corporal en °C

        Returns:
            Calorías ajustadas
        """
        temp_baseline = FORMULA_CONSTANTS['temp_baseline']
        temp_factor = FORMULA_CONSTANTS['temp_factor']

        adjustment = 1 + ((body_temp - temp_baseline) * temp_factor)

        return calories * adjustment

    @staticmethod
    def calculate_total(
            sex: str,
            age: int,
            weight: float,
            height: float,
            duration: int,
            heart_rate: int,
            body_temp: float
    ) -> float:
        """
        Calcula calorías totales usando múltiples métodos y promediando

        Args:
            sex: Género
            age: Edad
            weight: Peso
            height: Altura (no usado en cálculo actual pero disponible)
            duration: Duración
            heart_rate: Frecuencia cardíaca
            body_temp: Temperatura corporal

        Returns:
            Calorías totales calculadas
        """
        # Método 1: Por frecuencia cardíaca
        calories_hr = CalorieCalculator.calculate_by_heart_rate(
            sex, age, weight, heart_rate, duration
        )

        # Ajustar por temperatura
        calories_hr = CalorieCalculator.adjust_by_temperature(
            calories_hr, body_temp
        )

        # Método 2: Por MET
        calories_met = CalorieCalculator.calculate_by_met(
            weight, duration
        )

        # Promedio de ambos métodos
        final_calories = (calories_hr + calories_met) / 2

        return max(0, final_calories)


class FoodEquivalentCalculator:
    """Calcula equivalentes alimenticios"""

    @staticmethod
    def calculate_equivalents(calories: float) -> Dict[str, int]:
        """
        Calcula cuántas unidades de cada alimento equivalen a las calorías

        Args:
            calories: Calorías quemadas

        Returns:
            Diccionario con equivalentes {alimento: cantidad}
        """
        equivalents = {}

        for food, cal_per_unit in FOOD_EQUIVALENTS.items():
            equivalents[food] = round(calories / cal_per_unit)

        return equivalents

    @staticmethod
    def get_top_equivalents(calories: float, n: int = 3) -> Dict[str, int]:
        """
        Obtiene los top N equivalentes más relevantes

        Args:
            calories: Calorías quemadas
            n: Número de equivalentes a retornar

        Returns:
            Diccionario con top N equivalentes
        """
        all_equivalents = FoodEquivalentCalculator.calculate_equivalents(calories)

        # Ordenar por cantidad y tomar los top N
        sorted_equivalents = dict(
            sorted(
                all_equivalents.items(),
                key=lambda x: x[1],
                reverse=True
            )[:n]
        )

        return sorted_equivalents


class CaloriePredictionService:
    """Servicio principal para predicción de calorías"""

    def __init__(self, model_manager, feature_preparator, model_predictor):
        """
        Inicializa el servicio de predicción

        Args:
            model_manager: Gestor de modelos
            feature_preparator: Preparador de características
            model_predictor: Predictor de modelos
        """
        self.model_manager = model_manager
        self.feature_preparator = feature_preparator
        self.model_predictor = model_predictor
        self.calculator = CalorieCalculator()

    def predict_with_model(
            self,
            model_name: str,
            sex: str,
            age: int,
            height: float,
            weight: float,
            duration: int,
            heart_rate: int,
            body_temp: float
    ) -> float:
        """
        Predice calorías usando un modelo específico

        Args:
            model_name: Nombre del modelo a usar
            sex: Género
            age: Edad
            height: Altura
            weight: Peso
            duration: Duración
            heart_rate: Frecuencia cardíaca
            body_temp: Temperatura corporal

        Returns:
            Calorías predichas

        Raises:
            ValueError: Si el modelo no existe
            Exception: Si hay error en la predicción
        """
        # Obtener modelo
        model = self.model_manager.get_model(model_name)

        if model is None:
            raise ValueError(f"Modelo {model_name} no disponible")

        # Preparar características
        features = self.feature_preparator.prepare_features(
            sex=sex,
            age=age,
            height=height,
            weight=weight,
            duration=duration,
            heart_rate=heart_rate,
            body_temp=body_temp
        )

        # Predecir
        calories = self.model_predictor.predict(model, features)

        return calories

    def predict_with_formula(
            self,
            sex: str,
            age: int,
            height: float,
            weight: float,
            duration: int,
            heart_rate: int,
            body_temp: float
    ) -> float:
        """
        Predice calorías usando fórmulas (fallback)

        Args:
            sex: Género
            age: Edad
            height: Altura
            weight: Peso
            duration: Duración
            heart_rate: Frecuencia cardíaca
            body_temp: Temperatura corporal

        Returns:
            Calorías calculadas
        """
        return self.calculator.calculate_total(
            sex=sex,
            age=age,
            weight=weight,
            height=height,
            duration=duration,
            heart_rate=heart_rate,
            body_temp=body_temp
        )

    def predict(
            self,
            model_name: str,
            sex: str,
            age: int,
            height: float,
            weight: float,
            duration: int,
            heart_rate: int,
            body_temp: float,
            use_fallback: bool = True
    ) -> tuple[float, str]:
        """
        Predice calorías usando modelo o fórmula como fallback

        Args:
            model_name: Nombre del modelo
            ... (resto de parámetros)
            use_fallback: Si usar fórmula en caso de error

        Returns:
            Tuple (calorías, método_usado)
        """
        try:
            calories = self.predict_with_model(
                model_name, sex, age, height, weight,
                duration, heart_rate, body_temp
            )
            return calories, f"Modelo: {model_name}"

        except Exception as e:
            if use_fallback:
                calories = self.predict_with_formula(
                    sex, age, height, weight,
                    duration, heart_rate, body_temp
                )
                return calories, "Fórmula (fallback)"
            else:
                raise e