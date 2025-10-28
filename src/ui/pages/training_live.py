"""
Módulo de Entrenamiento en Tiempo Real
Contiene toda la lógica para la página de entrenamiento en vivo
"""
import streamlit as st
import sys
from pathlib import Path
import time
from datetime import datetime

# Asegurar que src esté en el path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import APP_VERSION, OPENROUTER_API_KEY
from services import TrainingSession
from ui.training_components import (
    TrainingTimerDisplay,
    TrainingMetricsDisplay,
    CoachMessageDisplay,
    TrainingSetupForm
)
from ui.styles import get_custom_css


# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

def initialize_page():
    """Inicializa configuración de la página"""
    st.set_page_config(
        page_title="Entrenamiento en Vivo - Predict Calorie Expenditure",
        page_icon="🏃",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(get_custom_css(), unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa variables de session state"""
    if 'training_session' not in st.session_state:
        st.session_state.training_session = None

    if 'session_started' not in st.session_state:
        st.session_state.session_started = False

    if 'current_hr' not in st.session_state:
        st.session_state.current_hr = 80

    if 'last_coach_message' not in st.session_state:
        st.session_state.last_coach_message = ""

    if 'last_message_type' not in st.session_state:
        st.session_state.last_message_type = ""

    if 'user_config' not in st.session_state:
        st.session_state.user_config = None


# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def render_header():
    """Renderiza encabezado de la página"""
    st.title("🏃 Entrenamiento en Tiempo Real")
    st.markdown("""
    ### Monitorea tu entrenamiento en vivo con predicción de calorías en tiempo real

    📊 **Características:**
    - ⏱️ Cronómetro con inicio, pausa y detención
    - 🔥 Predicción de calorías en tiempo real
    - 🌡️ Simulador de temperatura corporal
    - 🤖 Asistente virtual motivacional con IA
    - 📈 Gráficos de métricas en vivo
    """)
    st.markdown("---")


def render_sidebar():
    """Renderiza sidebar con información"""
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3171/3171927.png", width=100)
        st.title("🏃 Entrenamiento")

        st.markdown("### 📖 Guía Rápida")
        st.markdown("""
        **1. Controles:**
        - ▶️ Iniciar/Reanudar
        - ⏸️ Pausar
        - ⏹️ Detener

        **Durante el entrenamiento:**
        - BPM y temperatura se simulan automáticamente
        - Observa métricas en tiempo real
        - Recibe motivación del coach
        """)

        st.markdown("---")
        st.markdown(f"**Versión:** {APP_VERSION}")
        st.markdown("**Modelo:** MLP Regressor")


def render_training_setup():
    """Renderiza formulario de configuración inicial"""
    # Formulario de usuario
    if st.session_state.user_config is None:
        config = TrainingSetupForm.render_setup_form()

        if config:
            # Validar datos
            if not config['nombre'] or not config['apellidos']:
                st.error("❌ Por favor completa nombre y apellidos")
                return

            # Guardar config y crear sesión directamente
            st.session_state.user_config = config

            # Crear sesión de entrenamiento con perfil 'trote' por defecto
            session = TrainingSession(
                user_data={
                    'nombre': config['nombre'],
                    'apellidos': config['apellidos'],
                    'sexo': config['sexo'],
                    'edad': config['edad'],
                    'peso': config['peso'],
                    'estatura': config['estatura']
                },
                target_duration_minutes=config['duracion'],
                model_name="MLP",
                ai_coach_api_key=OPENROUTER_API_KEY,
                language=config['idioma'],
                enable_tts=config['enable_tts'],
                tts_voice_gender=config['voz'],
                workout_profile='trote'  # Siempre usar trote como perfil base
            )

            # Guardar en session state
            st.session_state.training_session = session
            st.session_state.session_started = True
            st.session_state.current_hr = config['pulsaciones']

            # Mostrar mensaje de éxito
            st.success(f"✅ Sesión configurada para {config['nombre']}. ¡Listo para comenzar!")
            st.rerun()
        return


def render_training_interface():
    """Renderiza interfaz principal de entrenamiento"""
    session: TrainingSession = st.session_state.training_session

    # Obtener estado actual
    state = session.get_current_state()

    # Sección de Cronómetro
    st.header("⏱️ Cronómetro de Entrenamiento")

    # Display del timer
    TrainingTimerDisplay.render_timer(
        formatted_time=state['timer']['formatted_time'],
        status=state['timer']['status'],
        progress_percent=state['timer']['progress_percent']
    )

    # Botones de control
    buttons = TrainingTimerDisplay.render_control_buttons(state['timer']['status'])

    # Manejar acciones de botones (sin rerun - se actualiza automáticamente)
    if buttons['start']:
        session.start()

    if buttons['pause']:
        session.pause()

    if buttons['resume']:
        session.resume()

    if buttons['stop']:
        session.stop()
        # Mostrar mensaje de ánimo
        encouragement = session.get_coach_message("encouragement")
        st.session_state.last_coach_message = encouragement
        st.session_state.last_message_type = "encouragement"

    st.markdown("---")

    # Modo automático siempre activo - sin control manual
    if session.timer.is_running and not session.timer.is_paused:
        # Actualización silenciosa en background con simuladores
        state = session.update_metrics(use_auto_sensors=True)

    # Mensaje informativo
    st.info("🤖 Los sensores de BPM y temperatura se simulan automáticamente durante el entrenamiento")

    st.markdown("---")

    # Métricas principales
    st.header("📊 Métricas en Tiempo Real")

    TrainingMetricsDisplay.render_metric_cards(
        calories=state['metrics']['current_calories'],
        target_calories=state['metrics']['target_calories'],
        heart_rate=state['metrics']['current_heart_rate'],
        temperature=state['metrics']['current_temperature']
    )

    # Gauge de calorías
    col_gauge = st.columns([1, 2, 1])
    with col_gauge[1]:
        TrainingMetricsDisplay.render_calorie_gauge(
            calories=state['metrics']['current_calories'],
            target_calories=state['metrics']['target_calories']
        )

    st.markdown("---")

    # Coach Virtual
    st.header("🤖 Asistente Virtual Motivacional")

    # Mostrar último mensaje automático del coach (se actualiza cada 30s)
    last_auto_message = session.get_last_coach_message()
    if last_auto_message and last_auto_message.get('category') == 'coach':
        CoachMessageDisplay.render_coach_message(
            message=last_auto_message['message'],
            message_type=last_auto_message.get('type', 'motivation')
        )
        # Guardar en session state para mantener consistencia
        st.session_state.last_coach_message = last_auto_message['message']
        st.session_state.last_message_type = last_auto_message.get('type', 'motivation')

    st.markdown("##### 💬 Solicita mensaje personalizado:")

    # Botones para mensajes manuales
    coach_msg_type = CoachMessageDisplay.render_coach_buttons()

    if coach_msg_type:
        # Generar mensaje sin rerun
        message = session.get_coach_message(coach_msg_type)
        st.session_state.last_coach_message = message
        st.session_state.last_message_type = coach_msg_type
        # El mensaje se mostrará en el próximo ciclo automático

    st.markdown("---")

    # Gráficos en tiempo real
    st.header("📈 Evolución de Métricas")

    # Obtener datos de la sesión
    session_data = session.export_session_data()
    time_series = session_data['time_series']

    TrainingMetricsDisplay.render_realtime_chart(
        timestamps=time_series['timestamps'],
        heart_rates=time_series['heart_rates'],
        temperatures=time_series['temperatures'],
        calories=time_series['calories']
    )

    st.markdown("---")

    # Resumen de la sesión (si está detenida)
    if session.timer.is_stopped:
        render_session_summary(session)


def render_session_summary(session: TrainingSession):
    """
    Renderiza resumen de la sesión al finalizar

    Args:
        session: Sesión de entrenamiento
    """
    st.header("🏆 Resumen de la Sesión")

    summary = session.get_session_summary()

    # Información general
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⏱️ Tiempo Total",
            f"{summary['completed_minutes']:.1f} min",
            f"{summary['completion_percent']:.0f}% del objetivo"
        )

    with col2:
        st.metric(
            "🔥 Calorías Quemadas",
            f"{summary['calories_burned']} kcal",
            f"Objetivo: {summary['target_calories']:.0f} kcal"
        )

    with col3:
        goal_status = "✅ ¡Objetivo logrado!" if summary['calorie_goal_achieved'] else "📊 Progreso parcial"
        st.metric(
            "🎯 Estado del Objetivo",
            goal_status
        )

    st.markdown("---")

    # Estadísticas detalladas
    st.subheader("📊 Estadísticas Detalladas")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("**❤️ Frecuencia Cardíaca**")
        st.write(f"- Promedio: {summary['avg_heart_rate']:.0f} ppm")
        st.write(f"- Máxima: {summary['max_heart_rate']} ppm")
        st.write(f"- Mínima: {summary['min_heart_rate']} ppm")

    with col5:
        st.markdown("**🌡️ Temperatura**")
        st.write(f"- Promedio: {summary['avg_temperature']:.1f} °C")
        st.write(f"- Máxima: {summary['max_temperature']:.1f} °C")

    with col6:
        st.markdown("**📈 Lecturas**")
        st.write(f"- Total: {summary['total_readings']}")
        st.write(f"- Modelo: MLP Regressor")

    st.markdown("---")

    # Botón para nueva sesión
    if st.button("🔄 Iniciar Nueva Sesión", use_container_width=True, type="primary"):
        # Limpiar sesión
        st.session_state.training_session = None
        st.session_state.session_started = False
        st.session_state.last_coach_message = ""
        st.session_state.last_message_type = ""
        st.session_state.user_config = None
        # Este rerun es necesario para volver al formulario inicial
        st.rerun()


# ============================================================================
# AUTO-REFRESH (para actualizar cronómetro)
# ============================================================================

def enable_auto_refresh():
    """
    Habilita auto-refresh cada 1 segundo para que el cronómetro avance
    """
    if st.session_state.training_session:
        session = st.session_state.training_session
        if session.timer.is_running and not session.timer.is_paused:
            # Hacer rerun cada 1 segundo para que el cronómetro avance
            time.sleep(1)
            st.rerun()


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def run():
    """Función principal para ejecutar la página"""
    initialize_page()
    initialize_session_state()

    # Renderizar header
    render_header()

    # Renderizar sidebar
    render_sidebar()

    # Lógica principal
    if not st.session_state.session_started:
        # Mostrar formulario de configuración
        render_training_setup()
    else:
        # Mostrar interfaz de entrenamiento
        render_training_interface()

        # Habilitar auto-refresh si está corriendo
        enable_auto_refresh()
