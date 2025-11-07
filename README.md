# 🔥 Aplicación de Predicción de Calorías

Esta carpeta contiene toda la aplicación Python organizada de forma modular.

## 🎥 Demos en Video

**¡Mira la aplicación en acción!**

### 🏃 Demo: Entrenamiento en Vivo

Video demostrativo completo del módulo de **Entrenamiento en Tiempo Real** donde puedes ver:
- ✨ Cronómetro en tiempo real con controles (iniciar, pausar, reanudar, detener)
- 📊 Simulación realista de sensores biométricos (frecuencia cardíaca y temperatura)
- 🤖 Coach de IA con mensajes motivacionales contextuales
- 🔊 Text-to-Speech con voces naturales de Microsoft Edge
- 📈 Predicción automática de calorías cada 30 segundos
- 💪 Perfiles de entrenamiento personalizados (caminata, trote, carrera, HIIT, pirámide, resistencia)
- 📉 Gráficos en tiempo real de métricas biométricas
- 📋 Resumen final de la sesión con estadísticas completas

**👉 [VER DEMO ENTRENAMIENTO EN VIVO](https://drive.google.com/file/d/1SYbCiE7Tsko65evXIKU1WKlGBO5IQpz6/view?usp=sharing)**

### 📊 Demo: Predicción Simple de Calorías

*Próximamente: Video demostrativo del módulo de predicción simple*

---

## 📂 Estructura de la Aplicación

```
app/
├── app.py                          # Aplicación principal (entrada de Streamlit)
├── .env                            # Variables de entorno (API keys)
├── DOCUMENTACION_CLASES.md        # Documentación detallada de cada clase
├── README.md                       # Este archivo
│
├── src/                            # Código fuente
│   ├── __init__.py
│   ├── config.py                   # Configuración y constantes
│   ├── models.py                   # Gestión de modelos ML
│   ├── calculations.py             # Cálculos de calorías
│   ├── utils.py                    # Utilidades (gráficos, reportes, validación)
│   │
│   ├── ui/                         # Interfaz de usuario
│   │   ├── __init__.py
│   │   ├── components.py           # Componentes reutilizables (formularios, resultados)
│   │   ├── styles.py               # Estilos CSS y HTML
│   │   ├── training_components.py # Componentes de entrenamiento en vivo
│   │   ├── workout_selector.py    # Selector de perfiles de ejercicio
│   │   └── pages/                  # Páginas de la aplicación
│   │       ├── __init__.py
│   │       └── training_live.py   # Lógica de entrenamiento en vivo
│   │
│   └── services/                   # Servicios de la aplicación
│       ├── __init__.py
│       ├── timer_service.py        # Cronómetro
│       ├── temperature_simulator.py # Simulador de temperatura
│       ├── heart_rate_simulator.py  # Simulador de frecuencia cardíaca
│       ├── training_session.py      # Gestión de sesión de entrenamiento
│       ├── ai_coach.py              # Coach de IA con OpenRouter
│       ├── coach_translations.py    # Traducciones para el coach
│       ├── tts_service.py           # Text-to-Speech básico
│       ├── tts_service_improved.py  # Text-to-Speech mejorado (edge-tts)
│       └── workout_profiles.py      # Perfiles de entrenamiento
│
└── pages/                          # Páginas adicionales de Streamlit
    └── 1_🏃_Entrenamiento_En_Vivo.py  # Página de entrenamiento en tiempo real
```

## 🚀 Cómo Ejecutar la Aplicación

### 1. Página Principal (Predicción de Calorías)
```bash
cd app
streamlit run app.py
```

### 2. Entrenamiento en Vivo
```bash
cd app
streamlit run pages/1_🏃_Entrenamiento_En_Vivo.py
```

O acceder desde la interfaz de Streamlit usando el selector de páginas en el sidebar.

## 📋 Requisitos

### Dependencias principales:
- **streamlit**: Interfaz web
- **scikit-learn**: Modelo ML (MLP Regressor)
- **joblib**: Carga de modelos
- **plotly**: Gráficos interactivos
- **pandas**: Manipulación de datos
- **numpy**: Operaciones numéricas
- **requests**: Llamadas a APIs (OpenRouter)
- **python-dotenv**: Variables de entorno

### Dependencias opcionales:
- **edge-tts**: Text-to-Speech mejorado (para entrenamiento en vivo)

## 🔧 Configuración

### Variables de Entorno (.env)
```
OPEN_ROUTER_API_KEY=tu_api_key_aqui
```

**Nota**: El API key es opcional. Si no se proporciona, el coach IA usa mensajes predefinidos (fallback).

## 📖 Documentación

Para ver la documentación detallada de cada clase, consulta:
- **[DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md)**: Documentación completa de todas las clases

## 🎯 Funcionalidades Principales

### 1. Predicción de Calorías (app.py)
- Formulario para datos del usuario
- Predicción con modelo ML (MLP Regressor)
- Fallback a fórmulas matemáticas si falla el modelo
- Visualización de resultados con gráficos
- Equivalentes en alimentos
- Descarga de reportes (TXT, CSV)

### 2. Entrenamiento en Vivo (pages/1_🏃_Entrenamiento_En_Vivo.py)
- Cronómetro en tiempo real
- Sensores biométricos simulados (FC y temperatura)
- Predicción de calorías cada 30 segundos
- Coach de IA con mensajes motivacionales
- Text-to-Speech (voz) opcional
- Perfiles de entrenamiento personalizados
- Exportación de datos de la sesión

## 🧩 Módulos Principales

### config.py
Centraliza toda la configuración de la aplicación:
- Rutas de modelos
- Rangos de validación
- Constantes de cálculo
- Configuración de UI

### models.py
Gestiona modelos de Machine Learning:
- **ModelManager**: Carga y gestiona modelos
- **FeaturePreparator**: Prepara datos para el modelo
- **ModelPredictor**: Realiza predicciones

### calculations.py
Lógica de cálculo de calorías:
- **CalorieCalculator**: Fórmulas matemáticas
- **FoodEquivalentCalculator**: Equivalentes alimenticios
- **CaloriePredictionService**: Orquesta todo el proceso

### utils.py
Utilidades generales:
- **ChartGenerator**: Crea gráficos con Plotly
- **ReportGenerator**: Genera reportes descargables
- **DataValidator**: Valida datos de entrada

### ui/components.py
Componentes de interfaz:
- **FormComponents**: Formularios de entrada
- **SidebarComponents**: Barra lateral
- **ResultComponents**: Visualización de resultados

### services/training_session.py
Gestión de entrenamiento en tiempo real:
- **TrainingSession**: Coordina cronómetro, sensores, predicciones y coach

### services/ai_coach.py
Coach motivacional con IA:
- **AICoachService**: Genera mensajes con OpenRouter o fallback

## 🔄 Flujo de Trabajo

### Predicción Simple:
1. Usuario ingresa datos en formulario
2. `DataValidator` valida datos
3. `FeaturePreparator` prepara características
4. `ModelPredictor` hace predicción con modelo ML
5. Si falla, `CalorieCalculator` usa fórmulas
6. `ChartGenerator` crea visualizaciones
7. `ResultComponents` muestra resultados

### Entrenamiento en Vivo:
1. Usuario configura sesión (duración, perfil, etc.)
2. `TrainingSession` inicia cronómetro y sensores
3. Cada 30s: actualiza métricas y predice calorías
4. Cada 30s: `AICoachService` genera mensaje motivacional
5. Si TTS activo: reproduce mensaje con voz
6. Al finalizar: genera resumen y permite exportar datos

## 🎨 Personalización

### Agregar nuevos perfiles de entrenamiento:
Edita `src/services/workout_profiles.py`

### Cambiar voces TTS:
Edita `src/services/tts_service.py` o `tts_service_improved.py`

### Modificar mensajes del coach:
Edita `src/services/coach_translations.py`

### Personalizar estilos:
Edita `src/ui/styles.py`

## 📊 Modelos ML

La aplicación espera encontrar:
- **models/MLPRegressor.joblib**: Modelo MLP entrenado

Si no existe el modelo, la aplicación usa cálculos con fórmulas matemáticas como fallback.

## 🌐 Idiomas Soportados

- **Español** (por defecto)
- **English**
- **Français**

El coach IA y TTS funcionan en los 3 idiomas.

## 🤝 Contribuir

Para agregar nuevas funcionalidades:
1. Crea nuevos servicios en `src/services/`
2. Agrega componentes UI en `src/ui/`
3. Actualiza configuración en `src/config.py`
4. Documenta en `DOCUMENTACION_CLASES.md`

## 📝 Notas

- Toda la lógica de negocio está en `src/`
- Los componentes UI están separados de la lógica
- La configuración está centralizada
- Los servicios son independientes y reutilizables
- El código sigue arquitectura limpia con separación de responsabilidades
