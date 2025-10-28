# 📑 Índice Rápido de la Aplicación

## 🎯 Buscar por Funcionalidad

### Quiero hacer una predicción de calorías
- **Archivo**: `app.py`
- **Clases clave**:
  - `CaloriePredictionService` en [calculations.py](./src/calculations.py)
  - `ModelPredictor` en [models.py](./src/models.py)

### Quiero gestionar modelos ML
- **Archivo**: [src/models.py](./src/models.py)
- **Clases**: `ModelManager`, `FeaturePreparator`, `ModelPredictor`

### Quiero validar datos de usuario
- **Archivo**: [src/utils.py](./src/utils.py)
- **Clase**: `DataValidator`

### Quiero crear gráficos
- **Archivo**: [src/utils.py](./src/utils.py)
- **Clase**: `ChartGenerator`

### Quiero generar reportes
- **Archivo**: [src/utils.py](./src/utils.py)
- **Clase**: `ReportGenerator`

### Quiero personalizar la interfaz
- **Archivos**:
  - Componentes: [src/ui/components.py](./src/ui/components.py)
  - Estilos: [src/ui/styles.py](./src/ui/styles.py)

### Quiero crear un entrenamiento en vivo
- **Archivo**: [src/services/training_session.py](./src/services/training_session.py)
- **Clase**: `TrainingSession`

### Quiero agregar mensajes del coach
- **Archivos**:
  - Coach: [src/services/ai_coach.py](./src/services/ai_coach.py)
  - Traducciones: [src/services/coach_translations.py](./src/services/coach_translations.py)

### Quiero implementar text-to-speech
- **Archivos**:
  - Básico: [src/services/tts_service.py](./src/services/tts_service.py)
  - Mejorado: [src/services/tts_service_improved.py](./src/services/tts_service_improved.py)

### Quiero simular sensores biométricos
- **Archivos**:
  - FC: [src/services/heart_rate_simulator.py](./src/services/heart_rate_simulator.py)
  - Temperatura: [src/services/temperature_simulator.py](./src/services/temperature_simulator.py)

### Quiero crear perfiles de ejercicio
- **Archivo**: [src/services/workout_profiles.py](./src/services/workout_profiles.py)

### Quiero configurar la aplicación
- **Archivo**: [src/config.py](./src/config.py)
- **Contiene**: Constantes, rangos, configuraciones

---

## 📦 Estructura por Capas

### Capa de Presentación (UI)
```
src/ui/
├── components.py       → Componentes de formularios y resultados
├── styles.py          → CSS y HTML personalizado
├── training_components.py → Componentes de entrenamiento
└── workout_selector.py    → Selector de perfiles
```

### Capa de Lógica de Negocio
```
src/
├── calculations.py    → Cálculos de calorías
├── models.py          → Gestión de modelos ML
└── utils.py          → Utilidades (validación, gráficos, reportes)
```

### Capa de Servicios
```
src/services/
├── training_session.py       → Orquestador de entrenamiento
├── ai_coach.py              → Coach motivacional
├── timer_service.py         → Cronómetro
├── heart_rate_simulator.py  → Sensor de FC
├── temperature_simulator.py → Sensor de temperatura
├── tts_service.py          → Text-to-Speech
└── workout_profiles.py     → Perfiles de ejercicio
```

### Capa de Configuración
```
src/
├── config.py         → Configuración central
└── .env             → Variables de entorno
```

---

## 🔍 Buscar por Tipo de Código

### Modelos de Machine Learning
| Archivo | Clases | Función |
|---------|--------|---------|
| [models.py](./src/models.py) | ModelManager | Cargar/gestionar modelos |
| [models.py](./src/models.py) | FeaturePreparator | Preparar datos |
| [models.py](./src/models.py) | ModelPredictor | Hacer predicciones |

### Cálculos y Fórmulas
| Archivo | Clases | Función |
|---------|--------|---------|
| [calculations.py](./src/calculations.py) | CalorieCalculator | Fórmulas matemáticas |
| [calculations.py](./src/calculations.py) | FoodEquivalentCalculator | Equivalentes alimenticios |
| [calculations.py](./src/calculations.py) | CaloriePredictionService | Orquestador de predicciones |

### Visualización
| Archivo | Clases | Función |
|---------|--------|---------|
| [utils.py](./src/utils.py) | ChartGenerator | Crear gráficos Plotly |
| [styles.py](./src/ui/styles.py) | (funciones) | CSS y HTML |

### Componentes de UI
| Archivo | Clases | Función |
|---------|--------|---------|
| [components.py](./src/ui/components.py) | FormComponents | Formularios |
| [components.py](./src/ui/components.py) | SidebarComponents | Barra lateral |
| [components.py](./src/ui/components.py) | ResultComponents | Resultados |
| [training_components.py](./src/ui/training_components.py) | TrainingUI | UI de entrenamiento |

### Servicios de Tiempo Real
| Archivo | Clases | Función |
|---------|--------|---------|
| [training_session.py](./src/services/training_session.py) | TrainingSession | Gestión de sesión |
| [timer_service.py](./src/services/timer_service.py) | TimerService | Cronómetro |
| [heart_rate_simulator.py](./src/services/heart_rate_simulator.py) | BiometricSensor | Sensores |

### Inteligencia Artificial
| Archivo | Clases | Función |
|---------|--------|---------|
| [ai_coach.py](./src/services/ai_coach.py) | AICoachService | Coach motivacional |
| [tts_service.py](./src/services/tts_service.py) | (funciones) | Voz básica |
| [tts_service_improved.py](./src/services/tts_service_improved.py) | (funciones) | Voz mejorada |

---

## 🚀 Casos de Uso Comunes

### Caso 1: Agregar un nuevo campo al formulario
1. Agregar rango en [config.py](./src/config.py) → `INPUT_RANGES`
2. Agregar campo en [components.py](./src/ui/components.py) → `FormComponents`
3. Actualizar validación en [utils.py](./src/utils.py) → `DataValidator`

### Caso 2: Crear un nuevo tipo de gráfico
1. Agregar método en [utils.py](./src/utils.py) → `ChartGenerator`
2. Llamar desde [components.py](./src/ui/components.py) → `ResultComponents`

### Caso 3: Agregar un nuevo perfil de entrenamiento
1. Editar [workout_profiles.py](./src/services/workout_profiles.py)
2. Agregar en función `get_recommended_heart_rate()`

### Caso 4: Personalizar mensajes del coach
1. Editar [coach_translations.py](./src/services/coach_translations.py)
2. Agregar nuevas frases en cada idioma

### Caso 5: Cambiar estilos visuales
1. Editar [styles.py](./src/ui/styles.py) → `get_custom_css()`

---

## 📚 Documentación Completa

Para ver la documentación detallada de cada clase:
- **[DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md)**

Para entender la estructura general:
- **[README.md](./README.md)**

---

## 🆘 Resolución Rápida de Problemas

### Problema: El modelo no carga
- **Solución**: Verificar que existe `models/MLPRegressor.joblib`
- **Archivo**: [models.py](./src/models.py) → `ModelManager._load_mlp()`

### Problema: Error en validación de datos
- **Solución**: Revisar rangos en [config.py](./src/config.py) → `INPUT_RANGES`
- **Archivo**: [utils.py](./src/utils.py) → `DataValidator`

### Problema: TTS no funciona
- **Solución**: Instalar edge-tts: `pip install edge-tts`
- **Archivo**: [tts_service_improved.py](./src/services/tts_service_improved.py)

### Problema: Coach no genera mensajes
- **Solución**: Verificar API key en `.env` o usar fallback
- **Archivo**: [ai_coach.py](./src/services/ai_coach.py)

### Problema: Gráficos no se muestran
- **Solución**: Instalar plotly: `pip install plotly`
- **Archivo**: [utils.py](./src/utils.py) → `ChartGenerator`

---

## 🔗 Enlaces Rápidos

| Necesito... | Ir a... |
|-------------|---------|
| Ver todas las clases | [DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md) |
| Entender la estructura | [README.md](./README.md) |
| Configurar la app | [config.py](./src/config.py) |
| Modificar la UI | [components.py](./src/ui/components.py) |
| Cambiar estilos | [styles.py](./src/ui/styles.py) |
| Agregar perfiles | [workout_profiles.py](./src/services/workout_profiles.py) |
| Personalizar coach | [coach_translations.py](./src/services/coach_translations.py) |
| Ejecutar la app | `streamlit run app.py` |
