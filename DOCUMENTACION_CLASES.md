# Documentación de Clases - Aplicación de Predicción de Calorías

Esta documentación describe de forma sencilla cada clase de la aplicación.

---

## 📁 app.py - Aplicación Principal

### Funciones principales:
- **initialize_app()**: Configura Streamlit y carga estilos CSS
- **initialize_session_state()**: Inicializa variables de sesión
- **setup_services()**: Carga modelos ML y servicios de predicción
- **render_header()**: Muestra el encabezado de la aplicación
- **render_sidebar()**: Muestra la barra lateral con info del modelo
- **render_form()**: Muestra formulario para datos del usuario
- **process_prediction()**: Procesa los datos y hace la predicción
- **render_results()**: Muestra resultados y gráficos
- **main()**: Función principal que orquesta toda la aplicación

---

## 📁 src/config.py - Configuración

### Constantes:
- **APP_VERSION**: Versión de la aplicación
- **APP_CONFIG**: Configuración de Streamlit
- **MODELS_DIR**: Ruta donde están los modelos ML
- **INPUT_RANGES**: Rangos válidos para inputs del usuario
- **FOOD_EQUIVALENTS**: Calorías de cada alimento
- **FORMULA_CONSTANTS**: Constantes para cálculo de calorías
- **TRAINING_CONFIG**: Configuración del entrenamiento en vivo

---

## 📁 src/models.py - Gestión de Modelos ML

### Clase: ModelManager
**Propósito**: Carga y gestiona modelos de Machine Learning

**Métodos principales**:
- `load_models()`: Carga el modelo MLP desde disco
- `get_model(model_name)`: Obtiene un modelo específico
- `get_available_models()`: Lista modelos disponibles
- `get_model_details(model_name)`: Detalles técnicos del modelo

**Argumentos comunes**:
- `model_name`: Nombre del modelo (ej: "MLP Regressor")

---

### Clase: FeaturePreparator
**Propósito**: Prepara datos del usuario para el modelo ML

**Métodos principales**:
- `encode_gender(gender)`: Convierte género a número (M=1, F=0)
- `prepare_features(sex, age, height, weight, duration, heart_rate, body_temp)`: Prepara todas las características
- `validate_features(features)`: Valida que las características sean correctas

**Argumentos**:
- `sex`: "Masculino" o "Femenino"
- `age`: Edad en años
- `height`: Altura en cm
- `weight`: Peso en kg
- `duration`: Duración en minutos
- `heart_rate`: Frecuencia cardíaca en ppm
- `body_temp`: Temperatura corporal en °C

**Retorna**: DataFrame con 7 características preparadas

---

### Clase: ModelPredictor
**Propósito**: Hace predicciones con el modelo ML

**Métodos principales**:
- `predict(model, features)`: Realiza predicción de calorías

**Argumentos**:
- `model`: Modelo ML cargado
- `features`: DataFrame con características preparadas

**Retorna**: Calorías predichas (float)

---

## 📁 src/calculations.py - Cálculos de Calorías

### Clase: CalorieCalculator
**Propósito**: Calcula calorías con fórmulas matemáticas (cuando no hay modelo)

**Métodos principales**:
- `calculate_by_heart_rate(sex, age, weight, heart_rate, duration)`: Calcula por frecuencia cardíaca
- `calculate_by_met(weight, duration, met)`: Calcula por MET (equivalente metabólico)
- `adjust_by_temperature(calories, body_temp)`: Ajusta por temperatura corporal
- `calculate_total(...)`: Combina todos los métodos y promedia

**Argumentos**: Mismos que FeaturePreparator
**Retorna**: Calorías calculadas (float)

---

### Clase: FoodEquivalentCalculator
**Propósito**: Convierte calorías en equivalentes de comida

**Métodos principales**:
- `calculate_equivalents(calories)`: Calcula cuántas unidades de cada alimento
- `get_top_equivalents(calories, n)`: Obtiene top N equivalentes

**Argumentos**:
- `calories`: Calorías quemadas
- `n`: Número de equivalentes a retornar

**Retorna**: Diccionario {alimento: cantidad}

---

### Clase: CaloriePredictionService
**Propósito**: Servicio principal que coordina todo

**Métodos principales**:
- `predict_with_model(...)`: Predice usando modelo ML
- `predict_with_formula(...)`: Predice usando fórmulas
- `predict(..., use_fallback=True)`: Intenta modelo, si falla usa fórmulas

**Argumentos**: Datos del usuario (sex, age, height, weight, duration, heart_rate, body_temp)
**Retorna**: Tupla (calorías, método_usado)

---

## 📁 src/utils.py - Utilidades

### Clase: ChartGenerator
**Propósito**: Crea gráficos con Plotly

**Métodos principales**:
- `create_calorie_gauge(calories, max_calories)`: Crea medidor de calorías
- `create_comparison_chart(user_calories, user_label)`: Compara con otras actividades
- `create_food_equivalents_chart(equivalents)`: Gráfico de equivalentes

**Argumentos**:
- `calories`: Calorías a mostrar
- `max_calories`: Máximo del medidor
- `equivalents`: Diccionario de equivalentes

**Retorna**: Figura de Plotly

---

### Clase: ReportGenerator
**Propósito**: Genera reportes descargables

**Métodos principales**:
- `generate_text_report(user_data, calories, equivalents, model_used)`: Reporte TXT
- `generate_csv_report(user_data, calories, model_used)`: Reporte CSV

**Argumentos**:
- `user_data`: Diccionario con datos del usuario
- `calories`: Calorías quemadas
- `equivalents`: Equivalentes alimenticios
- `model_used`: Nombre del modelo

**Retorna**: String con el reporte

---

### Clase: DataValidator
**Propósito**: Valida datos de entrada del usuario

**Métodos principales**:
- `validate_user_data(nombre, apellidos, edad, peso, estatura, duracion, pulsaciones, temperatura)`: Valida todos los campos
- `format_validation_errors(errors)`: Formatea errores para mostrar

**Argumentos**: Todos los datos del usuario
**Retorna**: Tupla (es_válido: bool, lista_errores: list)

---

## 📁 src/ui/components.py - Componentes UI

### Clase: FormComponents
**Propósito**: Componentes de formularios

**Métodos principales**:
- `render_personal_info_section()`: Muestra campos de info personal
- `render_exercise_info_section()`: Muestra campos de ejercicio
- `render_data_preview(data, selected_model)`: Vista previa de datos

**Retorna**: Diccionario con datos capturados

---

### Clase: SidebarComponents
**Propósito**: Componentes de la barra lateral

**Métodos principales**:
- `render_model_selector(available_models)`: Selector de modelo
- `render_model_info(model_info, model_details)`: Info del modelo
- `render_info_section()`: Sección informativa
- `render_guide()`: Guía de uso

**Argumentos**:
- `available_models`: Lista de modelos disponibles
- `model_info`: Info básica del modelo
- `model_details`: Detalles técnicos

---

### Clase: ResultComponents
**Propósito**: Muestra resultados

**Métodos principales**:
- `render_main_result(calories, model_used)`: Resultado principal
- `render_user_info(user_data)`: Info del usuario
- `render_exercise_info(user_data)`: Info del ejercicio
- `render_food_equivalents(equivalents)`: Equivalentes alimenticios
- `render_action_buttons(user_data, calories, equivalents, model_used)`: Botones de descarga

---

## 📁 src/ui/styles.py - Estilos CSS

### Funciones:
- `get_custom_css()`: Retorna CSS personalizado
- `get_header_html(title, subtitle)`: HTML del encabezado
- `get_result_header_html(model_used)`: HTML de resultados
- `get_calories_card_html(calories)`: Tarjeta de calorías
- `get_info_card_html(title, content)`: Tarjetas informativas
- `get_footer_html(version)`: Pie de página

**Todas retornan**: String con HTML/CSS

---

## 📁 src/services/training_session.py - Sesión de Entrenamiento

### Clase: TrainingSession
**Propósito**: Gestiona entrenamiento en tiempo real

**Constructor**:
```python
TrainingSession(
    user_data,              # Datos del usuario
    target_duration_minutes, # Duración objetivo
    model_name,             # Modelo ML a usar
    ai_coach_api_key,       # API key (opcional)
    language,               # Idioma
    enable_tts,             # Activar voz
    tts_voice_gender,       # Género de voz
    workout_profile         # Perfil de ejercicio
)
```

**Métodos principales**:
- `start()`: Inicia cronómetro
- `pause()`: Pausa sesión
- `resume()`: Reanuda sesión
- `stop()`: Detiene y hace predicción final
- `update_metrics(heart_rate, use_auto_sensors)`: Actualiza métricas en tiempo real
- `get_current_state()`: Estado actual de la sesión
- `get_coach_message(message_type)`: Obtiene mensaje del coach
- `get_session_summary()`: Resumen completo
- `export_session_data()`: Exporta datos para análisis

**Argumentos comunes**:
- `heart_rate`: Frecuencia cardíaca manual (opcional)
- `use_auto_sensors`: Usar sensores automáticos
- `message_type`: Tipo de mensaje ("motivation", "progress", "nutrition", "wellness", "encouragement")

---

## 📁 src/services/ai_coach.py - Coach de IA

### Clase: AICoachService
**Propósito**: Genera mensajes motivacionales con IA

**Constructor**:
```python
AICoachService(
    api_key,    # API key de OpenRouter (opcional)
    language    # Idioma ("Español", "English", "Français")
)
```

**Métodos principales**:
- `generate_motivation(calories_burned, elapsed_minutes, target_calories, user_name)`: Mensaje motivacional
- `generate_progress_update(calories_burned, target_calories, user_name)`: Actualización de progreso
- `generate_nutrition_tip(calories_burned, user_name)`: Consejo nutricional
- `generate_food_comparison(calories_burned, user_name)`: Comparación con comida
- `generate_encouragement(stopped_early, completed_percent, user_name)`: Mensaje de ánimo
- `generate_wellness_tip(user_name)`: Consejo de bienestar

**Argumentos**:
- `calories_burned`: Calorías quemadas
- `elapsed_minutes`: Tiempo transcurrido
- `target_calories`: Objetivo de calorías
- `user_name`: Nombre del usuario
- `stopped_early`: Si detuvo antes de terminar
- `completed_percent`: Porcentaje completado

**Retorna**: String con mensaje generado

**Nota**: Si no hay API key, usa mensajes predefinidos (fallback)

---

## 📁 src/services/timer_service.py - Cronómetro

### Clase: TimerService
**Propósito**: Cronómetro para el entrenamiento

**Métodos principales**:
- `start()`: Inicia cronómetro
- `pause()`: Pausa
- `resume()`: Reanuda
- `stop()`: Detiene
- `reset()`: Reinicia
- `get_elapsed_seconds()`: Segundos transcurridos
- `get_elapsed_minutes()`: Minutos transcurridos
- `get_formatted_time()`: Tiempo formateado (HH:MM:SS)
- `get_progress_info(target_minutes)`: Info de progreso

**Argumentos**:
- `target_minutes`: Duración objetivo para calcular progreso

**Retorna**: float (segundos/minutos) o dict (info de progreso)

---

## 📁 src/services/temperature_simulator.py - Sensor de Temperatura

### Clase: TemperatureSensor
**Propósito**: Simula sensor de temperatura corporal

**Métodos principales**:
- `read_temperature(heart_rate, elapsed_minutes)`: Lee temperatura simulada

**Argumentos**:
- `heart_rate`: Frecuencia cardíaca actual
- `elapsed_minutes`: Tiempo transcurrido

**Retorna**: Temperatura corporal (float, °C)

---

## 📁 src/services/heart_rate_simulator.py - Sensor Biométrico

### Clase: BiometricSensor
**Propósito**: Simula sensores de frecuencia cardíaca y temperatura

**Métodos principales**:
- `calibrate(resting_hr, age, fitness_level)`: Calibra sensor
- `read_heart_rate(elapsed_minutes)`: Lee frecuencia cardíaca
- `read_temperature(heart_rate, elapsed_minutes, user_age, user_weight)`: Lee temperatura

**Argumentos**:
- `resting_hr`: FC en reposo
- `age`: Edad del usuario
- `fitness_level`: Nivel de fitness ("low", "medium", "high")
- `elapsed_minutes`: Tiempo transcurrido
- `user_age`: Edad
- `user_weight`: Peso

**Retorna**: int (heart_rate) o float (temperature)

---

## 📁 src/services/workout_profiles.py - Perfiles de Entrenamiento

### Funciones:
- `get_recommended_heart_rate(profile, elapsed_minutes, target_duration, user_age)`: Calcula FC recomendada según perfil

**Argumentos**:
- `profile`: Perfil ("caminata", "trote", "carrera", "hiit", "piramide", "resistencia")
- `elapsed_minutes`: Tiempo transcurrido
- `target_duration`: Duración objetivo
- `user_age`: Edad del usuario

**Retorna**: Frecuencia cardíaca recomendada (int)

---

## 📁 src/services/tts_service.py - Text-to-Speech

### Función: get_tts_service(language, voice_gender)
**Propósito**: Crea servicio de texto a voz

**Argumentos**:
- `language`: Idioma ("Español", "English", "Français")
- `voice_gender`: Género ("Masculina", "Femenina")

**Retorna**: Objeto con método `speak(text, blocking=False)`

---

## 📁 pages/1_🏃_Entrenamiento_En_Vivo.py - Página de Entrenamiento

**Propósito**: Punto de entrada para la página de entrenamiento en vivo de Streamlit

**Función**:
- `run_training_live()`: Ejecuta la interfaz de entrenamiento en tiempo real

**Nota**: La lógica está en `src/ui/pages/training_live.py`

---

## Resumen de Flujo de Datos

```
Usuario → Formulario (components.py)
       → DataValidator (utils.py)
       → FeaturePreparator (models.py)
       → ModelPredictor (models.py)
       → CaloriePredictionService (calculations.py)
       → Resultados (components.py + utils.py)
```

## Resumen de Entrenamiento en Vivo

```
Usuario → TrainingSession (training_session.py)
       → TimerService + BiometricSensor + TemperatureSensor
       → CaloriePredictionService (cada 30s)
       → AICoachService (mensajes cada 30s)
       → TTSService (voz si está habilitado)
       → UI actualizada en tiempo real
```
