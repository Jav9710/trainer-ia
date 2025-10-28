"""
Componentes reutilizables de la interfaz de usuario
"""
from typing import Dict, Optional

import streamlit as st

from config import INPUT_RANGES, GENDERS


class FormComponents:
    """Componentes para formularios"""

    @staticmethod
    def render_personal_info_section() -> Dict:
        """
        Renderiza sección de información personal

        Returns:
            Diccionario con datos personales
        """
        st.subheader("👤 Información Personal")
        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input(
                "Nombre",
                placeholder="Ingresa tu nombre",
                help="Tu nombre de pila"
            )

            edad_config = INPUT_RANGES['age']
            edad = st.number_input(
                "Edad (años)",
                min_value=edad_config['min'],
                max_value=edad_config['max'],
                value=edad_config['default'],
                step=1,
                help="Tu edad actual"
            )

            sexo = st.selectbox(
                "Género",
                [GENDERS['MALE'], GENDERS['FEMALE']],
                help="Selecciona tu género (M=1, F=0 en el modelo)"
            )

        with col2:
            apellidos = st.text_input(
                "Apellidos",
                placeholder="Ingresa tus apellidos",
                help="Tus apellidos"
            )

            peso_config = INPUT_RANGES['weight']
            peso = st.number_input(
                "Peso (kg)",
                min_value=peso_config['min'],
                max_value=peso_config['max'],
                value=peso_config['default'],
                step=peso_config['step'],
                help="Tu peso actual en kilogramos"
            )

            estatura_config = INPUT_RANGES['height']
            estatura = st.number_input(
                "Estatura (cm)",
                min_value=estatura_config['min'],
                max_value=estatura_config['max'],
                value=estatura_config['default'],
                step=estatura_config['step'],
                help="Tu altura en centímetros"
            )

        return {
            'nombre': nombre,
            'apellidos': apellidos,
            'edad': edad,
            'sexo': sexo,
            'peso': peso,
            'estatura': estatura
        }

    @staticmethod
    def render_exercise_info_section() -> Dict:
        """
        Renderiza sección de información del ejercicio

        Returns:
            Diccionario con datos del ejercicio
        """
        st.subheader("🏋️ Información del Ejercicio")
        col1, col2, col3 = st.columns(3)

        with col1:
            duracion_config = INPUT_RANGES['duration']
            duracion = st.number_input(
                "Duración (minutos)",
                min_value=duracion_config['min'],
                max_value=duracion_config['max'],
                value=duracion_config['default'],
                step=1,
                help="Duración de tu ejercicio en minutos"
            )

        with col2:
            hr_config = INPUT_RANGES['heart_rate']
            pulsaciones = st.number_input(
                "Frecuencia Cardíaca (ppm)",
                min_value=hr_config['min'],
                max_value=hr_config['max'],
                value=hr_config['default'],
                step=1,
                help="Tu frecuencia cardíaca durante el ejercicio"
            )

        with col3:
            temp_config = INPUT_RANGES['body_temp']
            temperatura = st.number_input(
                "Temperatura Corporal (°C)",
                min_value=temp_config['min'],
                max_value=temp_config['max'],
                value=temp_config['default'],
                step=temp_config['step'],
                help="Tu temperatura corporal durante el ejercicio"
            )

        return {
            'duracion': duracion,
            'pulsaciones': pulsaciones,
            'temperatura': temperatura
        }

    @staticmethod
    def render_data_preview(data: Dict, selected_model: str):
        """
        Renderiza vista previa de datos para el modelo

        Args:
            data: Diccionario con datos del usuario
            selected_model: Modelo seleccionado
        """
        with st.expander("👁️ Vista previa de datos para el modelo"):
            sex_preview = 1 if data['sexo'] == "Masculino" else 0

            # Calcular features derivadas
            height_m = data['estatura'] / 100.0
            bmi = data['peso'] / (height_m ** 2)
            hr_per_min = data['pulsaciones'] / (data['duracion'] / 60.0) if data['duracion'] > 0 else 0.0
            hr_x_duration = data['pulsaciones'] * data['duracion']

            st.code(f"""
Datos para el modelo {selected_model}:
================================================

FEATURES ORIGINALES:
--------------------
Sex:        {sex_preview} ({data['sexo']})
Age:        {data['edad']} años
Height:     {data['estatura']} cm
Weight:     {data['peso']} kg
Duration:   {data['duracion']} minutos
Heart_Rate: {data['pulsaciones']} ppm
Body_Temp:  {data['temperatura']} °C

FEATURES DERIVADAS (Feature Engineering):
------------------------------------------
Height_m:      {height_m:.2f} m
BMI:           {bmi:.2f} kg/m²
HR_per_min:    {hr_per_min:.2f} ppm/min
HRxDuration:   {hr_x_duration:.0f}

TOTAL: 11 características
            """)

            # Alerta sobre BMI
            if bmi < 18.5:
                st.info("ℹ️ BMI indica peso bajo")
            elif bmi > 30:
                st.info("ℹ️ BMI indica obesidad")


class SidebarComponents:
    """Componentes para el sidebar"""

    @staticmethod
    def render_model_selector(available_models: list) -> Optional[str]:
        """
        Renderiza selector de modelos

        Args:
            available_models: Lista de modelos disponibles

        Returns:
            Nombre del modelo seleccionado o None
        """
        st.subheader("🤖 Modelo de Predicción")

        if not available_models:
            st.error("❌ No se encontró el modelo MLP entrenado")
            st.info("""
            **Instrucciones:**

            1. Entrena el modelo MLP con scikit-learn
            2. Guarda el modelo como `MLPRegressor.joblib`
            3. Colócalo en la carpeta `models/`
            """)
            return None

        st.success(f"✅ Modelo MLP Regressor cargado correctamente")

        # Como solo hay un modelo, lo devolvemos directamente
        selected_model = available_models[0]

        st.info(f"**Modelo activo:** {selected_model}")

        return selected_model

    @staticmethod
    def render_model_info(model_info: Dict, model_details: Dict):
        """
        Renderiza información del modelo

        Args:
            model_info: Información básica del modelo
            model_details: Detalles técnicos del modelo
        """
        st.markdown("---")
        st.markdown("### 📋 Información del Modelo")

        st.markdown(f"""
        <div class='model-info'>
            <p><strong>🏷️ Nombre:</strong> {model_details.get('name', 'N/A')}</p>
            <p><strong>🔧 Tipo:</strong> {model_info.get('type', 'N/A')}</p>
            <p><strong>📚 Librería:</strong> {model_info.get('library', 'N/A')}</p>
            <p><strong>📊 Estado:</strong> {model_info.get('status', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Detalles técnicos expandibles
        with st.expander("🔍 Ver detalles técnicos"):
            for key, value in model_details.items():
                if key != 'name':
                    st.write(f"**{key}:** {value}")

    @staticmethod
    def render_info_section():
        """Renderiza sección informativa"""
        st.markdown("---")
        st.subheader("ℹ️ Información")
        st.info("""
        **Variables de entrada:**
        - Sex (codificado: M=1, F=0)
        - Age (años)
        - Height (cm)
        - Weight (kg)
        - Duration (minutos)
        - Heart_Rate (ppm)
        - Body_Temp (°C)
        
        **Salida:** Calories (kcal)
        """)

    @staticmethod
    def render_guide():
        """Renderiza guía de uso"""
        with st.expander("📖 Guía de Uso"):
            st.markdown("""
            1. Selecciona el modelo ML
            2. Completa todos los campos del formulario
            3. Revisa la vista previa de datos
            4. Haz clic en 'Predecir'
            5. Analiza los resultados
            6. Descarga el reporte si lo deseas
            """)


class ResultComponents:
    """Componentes para mostrar resultados"""

    @staticmethod
    def render_main_result(calories: float, model_used: str):
        """
        Renderiza resultado principal

        Args:
            calories: Calorías quemadas
            model_used: Modelo usado
        """
        from .styles import get_result_header_html, get_calories_card_html

        st.markdown(get_result_header_html(model_used), unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown(get_calories_card_html(calories), unsafe_allow_html=True)

    @staticmethod
    def render_user_info(user_data: Dict):
        """
        Renderiza información del usuario

        Args:
            user_data: Datos del usuario
        """
        from .styles import get_info_card_html

        content = {
            "Nombre": f"{user_data['nombre']} {user_data['apellidos']}",
            "Edad": f"{user_data['edad']} años",
            "Género": user_data['sexo'],
            "Peso": f"{user_data['peso']} kg",
            "Estatura": f"{user_data['estatura']} cm"
        }

        st.markdown(
            get_info_card_html("👤 Información del Usuario", content),
            unsafe_allow_html=True
        )

    @staticmethod
    def render_exercise_info(user_data: Dict):
        """
        Renderiza información del ejercicio

        Args:
            user_data: Datos del ejercicio
        """
        from .styles import get_info_card_html

        content = {
            "Duración": f"{user_data['duracion']} minutos",
            "Frecuencia Cardíaca": f"{user_data['pulsaciones']} ppm",
            "Temperatura": f"{user_data['temperatura']} °C"
        }

        st.markdown(
            get_info_card_html("🏋️ Detalles del Ejercicio", content),
            unsafe_allow_html=True
        )

    @staticmethod
    def render_food_equivalents(equivalents: Dict):
        """
        Renderiza equivalentes alimenticios

        Args:
            equivalents: Diccionario de equivalentes
        """
        st.markdown("### 🍽️ Equivalente en Alimentos")

        for food, quantity in equivalents.items():
            st.metric(
                label=food,
                value=f"{quantity}",
                delta="unidades"
            )

    @staticmethod
    def render_action_buttons(
        user_data: Dict,
        calories: float,
        equivalents: Dict,
        model_used: str
    ):
        """
        Renderiza botones de acción

        Args:
            user_data: Datos del usuario
            calories: Calorías
            equivalents: Equivalentes
            model_used: Modelo usado
        """
        from utils import ReportGenerator

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("🔄 Nueva Predicción", use_container_width=True):
                st.session_state.prediction_made = False
                st.session_state.last_prediction = None
                st.rerun()

        with col2:
            report_text = ReportGenerator.generate_text_report(
                user_data, calories, equivalents, model_used
            )

            st.download_button(
                label="📥 Descargar TXT",
                data=report_text,
                file_name=f"prediccion_{user_data['nombre']}_{user_data['apellidos']}.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col3:
            report_csv = ReportGenerator.generate_csv_report(
                user_data, calories, model_used
            )

            st.download_button(
                label="📊 Descargar CSV",
                data=report_csv,
                file_name=f"prediccion_{user_data['nombre']}_{user_data['apellidos']}.csv",
                mime="text/csv",
                use_container_width=True
            )