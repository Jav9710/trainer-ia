"""
Configuración y constantes de la aplicación
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Versión de la aplicación
APP_VERSION = "2.0.0"

# Configuración de la aplicación
APP_CONFIG = {
    'page_title': 'App - Predict Calorie Expenditure',
    'page_icon': '🏠',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Rutas de archivos
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / 'models'
MLP_PATH = MODELS_DIR / 'MLPRegressor.joblib'

# Nombres de modelos
MODEL_NAMES = {
    'MLP': 'MLP Regressor'
}

# Rangos de validación para inputs
INPUT_RANGES = {
    'age': {'min': 10, 'max': 100, 'default': 25},
    'weight': {'min': 30.0, 'max': 300.0, 'default': 70.0, 'step': 0.5},
    'height': {'min': 100.0, 'max': 250.0, 'default': 170.0, 'step': 0.5},
    'duration': {'min': 1, 'max': 300, 'default': 30},
    'heart_rate': {'min': 60, 'max': 220, 'default': 120},
    'body_temp': {'min': 35.0, 'max': 42.0, 'default': 37.0, 'step': 0.1}
}

# Géneros
GENDERS = {
    'MALE': 'Masculino',
    'FEMALE': 'Femenino'
}

# Equivalentes calóricos (calorías por unidad)
FOOD_EQUIVALENTS = {
    '🍎 Manzanas': 52,
    '🍔 Hamburguesas': 250,
    '🍪 Galletas': 50,
    '🥤 Refrescos': 140,
    '🍕 Rebanadas de pizza': 285,
    '🍫 Barras de chocolate': 235
}

# Calorías de actividades para comparación (30 min)
ACTIVITY_CALORIES = {
    'Caminar': 150,
    'Correr': 400,
    'Ciclismo': 350,
    'Natación': 300
}

# Orden de características para modelos ML
# IMPORTANTE: Este orden debe coincidir EXACTAMENTE con el entrenamiento
# FEATURES TOTALES: 11 (basado en 04_feature_engineering.ipynb)
FEATURE_ORDER = [
    'Sex_male',      # 0 = Femenino, 1 = Masculino (NO escalado)
    'Age',           # Escalado
    'Height',        # cm (Escalado)
    'Weight',        # kg (Escalado)
    'Duration',      # minutos (Escalado)
    'Heart_Rate',    # ppm (Escalado)
    'Body_Temp',     # °C (Escalado)
    'Height_m',      # Feature derivada: altura en metros (NO escalado)
    'BMI',           # Feature derivada: peso / altura² (Escalado)
    'HR_per_min',    # Feature derivada: HR / (Duration/60) (Escalado)
    'HRxDuration'    # Feature derivada: interacción HR * Duration (Escalado)
]

# Features numéricas que se escalaron durante el entrenamiento (9 features)
SCALED_FEATURES = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp', 'BMI', 'HR_per_min', 'HRxDuration']

# Features NO escaladas (2 features)
UNSCALED_FEATURES = ['Sex_male', 'Height_m']

# Constantes para cálculos
FORMULA_CONSTANTS = {
    'male': {
        'base': -55.0969,
        'hr_coef': 0.6309,
        'weight_coef': 0.1988,
        'age_coef': 0.2017,
        'divisor': 4.184
    },
    'female': {
        'base': -20.4022,
        'hr_coef': 0.4472,
        'weight_coef': 0.1263,
        'age_coef': 0.074,
        'divisor': 4.184
    },
    'met_default': 8.0,
    'temp_baseline': 37.0,
    'temp_factor': 0.05
}

# Configuración de gráficos
CHART_CONFIG = {
    'gauge': {
        'max_calories': 1000,
        'height': 450
    },
    'comparison': {
        'height': 400,
        'colors': ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'orange']
    }
}

# Configuración de Entrenamiento en Tiempo Real
TRAINING_CONFIG = {
    'auto_update_interval': 2,      # segundos entre auto-refresh de UI
    'prediction_interval': 30,      # segundos entre predicciones de calorías
    'coach_message_interval': 30,   # segundos entre mensajes del coach
    'temperature': {
        'base': 36.5,
        'min': 36.0,
        'max': 39.5
    },
    'heart_rate': {
        'min': 60,
        'max': 220,
        'resting': 70,
        'warmup_target': 110,
        'exercise_target': 150,
        'intense_target': 170,
        'zones': {
            'low': (60, 100),
            'medium': (100, 140),
            'high': (140, 170),
            'maximum': (170, 220)
        }
    },
    'coach': {
        'openrouter_model': 'mistralai/mistral-7b-instruct',
        'max_tokens': 150,
        'temperature': 0.7,
        'message_types': ['motivation', 'progress', 'nutrition', 'wellness', 'food_comparison']
    }
}

# API Keys desde .env
OPENROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY', '')