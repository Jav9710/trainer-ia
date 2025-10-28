"""
🔥 App - Predict Calorie Expenditure
Arquitectura limpia con separación de responsabilidades
"""
import streamlit as st
import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import APP_CONFIG
from config import APP_VERSION
from models import model_manager, FeaturePreparator, ModelPredictor
from calculations import CaloriePredictionService, FoodEquivalentCalculator
from utils import ChartGenerator, DataValidator
from ui.styles import get_custom_css, get_header_html, get_footer_html
from ui.components import (
    FormComponents,
    SidebarComponents,
    ResultComponents
)


# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

def initialize_app():
    """Inicializa configuración de la aplicación"""
    st.set_page_config(**APP_CONFIG)
    st.markdown(get_custom_css(), unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa session state"""
    if 'prediction_made' not in st.session_state:
        st.session_state.prediction_made = False
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None


# ============================================================================
# SERVICIOS Y DEPENDENCIAS
# ============================================================================

def setup_services():
    """Configura servicios de la aplicación"""
    # Cargar modelos
    models, model_info = model_manager.load_models()

    # Configurar servicio de predicción
    prediction_service = CaloriePredictionService(
        model_manager=model_manager,
        feature_preparator=FeaturePreparator,
        model_predictor=ModelPredictor
    )

    return models, model_info, prediction_service


# ============================================================================
# INTERFAZ DE USUARIO
# ============================================================================

def render_header():
    """Renderiza header principal"""
    st.markdown(
        get_header_html(
            "🔥 Predict Calorie Expenditure 🔥",
            "Sistema ML para predicción de calorías quemadas"
        ),
        unsafe_allow_html=True
    )

    # Badges informativos
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🤖 Machine Learning")
    with col2:
        st.markdown("### 📊 Scikit-Learn")
    with col3:
        st.markdown("### 🎯 Predicción Precisa")

    st.markdown("---")


def render_sidebar(models, model_info):
    """
    Renderiza sidebar

    Args:
        models: Diccionario de modelos
        model_info: Información de modelos

    Returns:
        Modelo seleccionado o None
    """
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2936/2936886.png", width=100)
        st.title("⚙️ Configuración")

        # Selector de modelo (solo MLP disponible)
        available_models = list(models.keys())
        selected_model = SidebarComponents.render_model_selector(available_models)

        if selected_model is None:
            return None

        # Información del modelo MLP
        if selected_model in model_info:
            model_details = model_manager.get_model_details(selected_model)
            SidebarComponents.render_model_info(
                model_info[selected_model],
                model_details
            )

        # Información general
        SidebarComponents.render_info_section()

        # Guía de uso
        SidebarComponents.render_guide()

        return selected_model


def render_form(selected_model):
    """
    Renderiza formulario principal

    Args:
        selected_model: Modelo seleccionado

    Returns:
        Tuple (submitted, user_data) o None
    """
    st.header("📝 Información del Usuario")

    with st.form("calorie_form"):
        # Sección de información personal
        personal_data = FormComponents.render_personal_info_section()

        st.markdown("---")

        # Sección de información del ejercicio
        exercise_data = FormComponents.render_exercise_info_section()

        # Combinar datos
        user_data = {**personal_data, **exercise_data}

        # Vista previa de datos
        FormComponents.render_data_preview(user_data, selected_model)

        # Botón de envío
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🔥 Predecir Calorías",
            use_container_width=True,
            type="primary"
        )

        if submitted:
            return submitted, user_data

    return None, None


def process_prediction(user_data, selected_model, prediction_service):
    """
    Procesa la predicción

    Args:
        user_data: Datos del usuario
        selected_model: Modelo seleccionado
        prediction_service: Servicio de predicción

    Returns:
        Tuple (success, calories, method_used)
    """
    # Validar datos
    is_valid, errors = DataValidator.validate_user_data(
        nombre=user_data['nombre'],
        apellidos=user_data['apellidos'],
        edad=user_data['edad'],
        peso=user_data['peso'],
        estatura=user_data['estatura'],
        duracion=user_data['duracion'],
        pulsaciones=user_data['pulsaciones'],
        temperatura=user_data['temperatura']
    )

    if not is_valid:
        error_msg = DataValidator.format_validation_errors(errors)
        st.error(error_msg)
        return False, None, None

    # Realizar predicción
    with st.spinner(f"🤖 Realizando predicción con {selected_model}..."):
        try:
            calories, method_used = prediction_service.predict(
                model_name=selected_model,
                sex=user_data['sexo'],
                age=user_data['edad'],
                height=user_data['estatura'],
                weight=user_data['peso'],
                duration=user_data['duracion'],
                heart_rate=user_data['pulsaciones'],
                body_temp=user_data['temperatura'],
                use_fallback=True
            )

            st.success(f"✅ Predicción completada con {method_used}")
            return True, calories, method_used

        except Exception as e:
            st.error(f"❌ Error en la predicción: {str(e)}")
            return False, None, None


def render_results(user_data, calories, model_used):
    """
    Renderiza resultados

    Args:
        user_data: Datos del usuario
        calories: Calorías predichas
        model_used: Modelo usado
    """
    st.markdown("---")

    # Resultado principal
    ResultComponents.render_main_result(calories, model_used)

    # Gráfico de gauge - Visualización mejorada
    st.markdown("### 🎯 Medidor de Calorías")
    fig_gauge = ChartGenerator.create_calorie_gauge(calories)
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Detalles del entrenamiento
    st.markdown("### 📊 Detalles del Análisis")

    col1, col2 = st.columns(2)

    with col1:
        ResultComponents.render_user_info(user_data)
        ResultComponents.render_exercise_info(user_data)

    with col2:
        # Equivalentes alimenticios
        equivalents = FoodEquivalentCalculator.calculate_equivalents(calories)
        ResultComponents.render_food_equivalents(equivalents)

    # Gráfico de comparación
    st.markdown("### 📈 Comparación de Actividades")
    fig_comparison = ChartGenerator.create_comparison_chart(
        user_calories=calories,
        user_label="Tu Entrenamiento"
    )
    st.plotly_chart(fig_comparison, use_container_width=True)

    # Botones de acción
    st.markdown("---")
    ResultComponents.render_action_buttons(
        user_data=user_data,
        calories=calories,
        equivalents=equivalents,
        model_used=model_used
    )


def render_footer():
    """Renderiza footer"""
    st.markdown("---")
    st.markdown(get_footer_html(), unsafe_allow_html=True)


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal de la aplicación"""
    # Inicialización
    initialize_app()
    initialize_session_state()

    # Configurar servicios
    models, model_info, prediction_service = setup_services()

    # Renderizar header
    render_header()

    # Renderizar sidebar y obtener modelo seleccionado
    selected_model = render_sidebar(models, model_info)

    if selected_model is None:
        st.stop()

    # Renderizar formulario
    form_result = render_form(selected_model)

    # Procesar predicción si se envió el formulario
    if form_result[0]:  # Si submitted es True
        user_data = form_result[1]

        success, calories, method_used = process_prediction(
            user_data,
            selected_model,
            prediction_service
        )

        if success:
            # Guardar en session state
            st.session_state.prediction_made = True
            st.session_state.last_prediction = {
                **user_data,
                'calories': round(calories, 2),
                'model_used': method_used
            }

    # Mostrar resultados si hay predicción
    if st.session_state.prediction_made and st.session_state.last_prediction:
        pred = st.session_state.last_prediction
        render_results(
            user_data=pred,
            calories=pred['calories'],
            model_used=pred['model_used']
        )

    # Footer
    render_footer()


if __name__ == "__main__":
    main()