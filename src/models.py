"""
Gestión de modelos de Machine Learning
"""
from typing import Dict, Optional, Tuple, Any

import joblib
import numpy as np
import streamlit as st

from config import (
    MLP_PATH,
    MODEL_NAMES,
    FEATURE_ORDER
)


class ModelManager:
    """Gestiona la carga y uso de modelos de scikit-learn"""

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.model_info: Dict[str, Dict] = {}

    @st.cache_resource
    def load_models(_self) -> Tuple[Dict, Dict]:
        """
        Carga los modelos pre-entrenados de scikit-learn

        Returns:
            Tuple con diccionarios de modelos e información
        """
        _self._load_mlp()

        return _self.models, _self.model_info

    def _load_mlp(self):
        """Carga el modelo MLP"""
        try:
            if MLP_PATH.exists():
                self.models[MODEL_NAMES['MLP']] = joblib.load(MLP_PATH)
                self.model_info[MODEL_NAMES['MLP']] = {
                    'type': 'MLPRegressor',
                    'library': 'scikit-learn',
                    'status': '✅ Cargado',
                    'path': str(MLP_PATH)
                }
            else:
                st.warning(f"⚠️ Modelo MLP no encontrado en {MLP_PATH}")
        except Exception as e:
            st.error(f"❌ Error cargando MLP: {e}")

    def get_model(self, model_name: str) -> Optional[Any]:
        """
        Obtiene un modelo específico

        Args:
            model_name: Nombre del modelo

        Returns:
            Modelo de scikit-learn o None
        """
        return self.models.get(model_name)

    def get_available_models(self) -> list:
        """Retorna lista de modelos disponibles"""
        return list(self.models.keys())

    def has_models(self) -> bool:
        """Verifica si hay modelos cargados"""
        return len(self.models) > 0

    def get_model_details(self, model_name: str) -> Dict:
        """
        Obtiene detalles técnicos de un modelo

        Args:
            model_name: Nombre del modelo

        Returns:
            Diccionario con detalles del modelo
        """
        if model_name not in self.models:
            return {}

        model = self.models[model_name]
        details = {
            'name': model_name,
            'type': type(model).__name__,
        }

        # Agregar detalles específicos según tipo de modelo
        if hasattr(model, 'n_estimators'):
            details['n_estimators'] = model.n_estimators

        if hasattr(model, 'max_depth'):
            details['max_depth'] = model.max_depth

        if hasattr(model, 'hidden_layer_sizes'):
            details['hidden_layer_sizes'] = model.hidden_layer_sizes

        if hasattr(model, 'activation'):
            details['activation'] = model.activation

        return details


class FeaturePreparator:
    """Prepara características para los modelos"""

    @staticmethod
    def encode_gender(gender: str) -> int:
        """
        Codifica el género para el modelo

        Args:
            gender: 'Masculino' o 'Femenino'

        Returns:
            1 para Masculino, 0 para Femenino
        """
        return 1 if gender == 'Masculino' else 0

    @staticmethod
    def prepare_features(
        sex: str,
        age: int,
        height: float,
        weight: float,
        duration: int,
        heart_rate: int,
        body_temp: float
    ) -> np.ndarray:
        """
        Prepara las características en formato numpy para modelos de scikit-learn.
        Aplica el mismo feature engineering y scaling que en el entrenamiento.

        Args:
            sex: Género ('Masculino' o 'Femenino')
            age: Edad en años
            height: Altura en cm
            weight: Peso en kg
            duration: Duración del ejercicio en minutos
            heart_rate: Frecuencia cardíaca en ppm
            body_temp: Temperatura corporal en °C

        Returns:
            Array numpy con características en el orden correcto:
            [Sex_male, Age, Height, Weight, Duration, Heart_Rate, Body_Temp,
             Height_m, BMI, HR_per_min, HRxDuration]

            Total: 11 features
            - Sex_male: NO escalado (0 o 1)
            - Age, Height, Weight, Duration, Heart_Rate, Body_Temp, BMI, HR_per_min, HRxDuration: ESCALADOS
            - Height_m: NO escalado (no estaba en numeric_feats del notebook)
        """
        # 1. Codificación de género (Sex_male: 1=Masculino, 0=Femenino)
        sex_encoded = 1 if sex.lower() in ['masculino', 'male', 'm'] else 0

        # ============================================================
        # 2. FEATURE ENGINEERING (igual que en 04_feature_engineering.ipynb)
        # ============================================================

        # Height a metros
        height_m = height / 100.0

        # BMI (Body Mass Index)
        bmi = weight / (height_m ** 2)

        # HR por minuto normalizado por duración
        if duration > 0:
            hr_per_min = heart_rate / (duration / 60.0)
        else:
            hr_per_min = 0.0

        # Interacción HR * Duration
        hr_x_duration = heart_rate * duration

        # ============================================================
        # 3. APLICAR SCALING con el scaler entrenado
        # ============================================================
        # El scaler fue entrenado SOLO con estas 9 features numéricas:
        # ['Age','Height','Weight','Duration','Heart_Rate','Body_Temp','BMI','HR_per_min','HRxDuration']

        import joblib
        from pathlib import Path

        # ============================================================
        # 4. CONSTRUIR FEATURES EN EL ORDEN CORRECTO DEL DATASET
        # ============================================================
        # Dataset columnas: Gender, Age, Height, Weight, Duration, Heart_Rate, Body_Temp
        # El modelo regenerado espera exactamente estas columnas sin escalar

        import pandas as pd
        features = pd.DataFrame({
            'Gender': [sex_encoded],
            'Age': [age],
            'Height': [height],
            'Weight': [weight],
            'Duration': [duration],
            'Heart_Rate': [heart_rate],
            'Body_Temp': [body_temp]
        })

        return features

    @staticmethod
    def validate_features(features) -> bool:
        """
        Valida que las características sean correctas

        Args:
            features: Array numpy o DataFrame de características

        Returns:
            True si son válidas, False si no
        """
        import pandas as pd

        # Convertir a numpy si es DataFrame
        if isinstance(features, pd.DataFrame):
            features_array = features.values
        else:
            features_array = features

        # Verificar que haya al menos 7 features (las básicas del modelo regenerado)
        if features_array.shape[1] < 7:
            return False

        # Validar que no haya valores NaN o infinitos
        if np.isnan(features_array).any() or np.isinf(features_array).any():
            return False

        return True


class ModelPredictor:
    """Realiza predicciones con los modelos"""

    @staticmethod
    def predict(model: Any, features) -> float:
        """
        Realiza predicción usando modelo de scikit-learn

        Args:
            model: Modelo entrenado
            features: DataFrame o Array de características

        Returns:
            Predicción de calorías quemadas

        Raises:
            ValueError: Si las características no son válidas
            Exception: Si hay error en la predicción
        """
        # Validar características
        if not FeaturePreparator.validate_features(features):
            raise ValueError("Características inválidas para el modelo")

        try:
            # Realizar predicción (scikit-learn maneja tanto DataFrames como arrays)
            prediction = model.predict(features)[0]

            # Asegurar que sea positivo
            prediction = max(0, prediction)

            return float(prediction)

        except Exception as e:
            raise Exception(f"Error en la predicción: {str(e)}")


# Instancia global del gestor de modelos
model_manager = ModelManager()