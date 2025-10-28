"""
Componentes UI para Entrenamiento en Tiempo Real
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional


class TrainingTimerDisplay:
    """Componentes de visualización del cronómetro"""

    @staticmethod
    def render_timer(
        formatted_time: str,
        status: str,
        progress_percent: float
    ):
        """
        Renderiza el cronómetro principal

        Args:
            formatted_time: Tiempo formateado (HH:MM:SS)
            status: Estado del timer (running, paused, stopped)
            progress_percent: Porcentaje de progreso
        """
        # Color según estado
        if status == "running":
            color = "#00C851"
            status_emoji = "▶️"
            status_text = "EN MARCHA"
        elif status == "paused":
            color = "#FFB900"
            status_emoji = "⏸️"
            status_text = "PAUSADO"
        else:
            color = "#D32F2F"
            status_emoji = "⏹️"
            status_text = "DETENIDO"

        # HTML personalizado para el cronómetro
        timer_html = f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {color}20, {color}40);
                    border-radius: 20px; border: 4px solid {color}; margin: 10px 0;">
            <div style="font-size: 18px; color: {color}; font-weight: bold; margin-bottom: 10px;">
                {status_emoji} {status_text}
            </div>
            <div style="font-size: 72px; font-weight: bold; color: {color}; font-family: 'Courier New', monospace;">
                {formatted_time}
            </div>
            <div style="margin-top: 15px;">
                <div style="background-color: #E0E0E0; height: 20px; border-radius: 10px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {color}, {color}AA);
                                height: 100%; width: {progress_percent}%; transition: width 0.3s ease;">
                    </div>
                </div>
                <div style="font-size: 16px; color: {color}; margin-top: 5px; font-weight: bold;">
                    {progress_percent:.1f}% Completado
                </div>
            </div>
        </div>
        """
        st.markdown(timer_html, unsafe_allow_html=True)

    @staticmethod
    def render_control_buttons(status: str) -> Dict[str, bool]:
        """
        Renderiza botones de control del cronómetro

        Args:
            status: Estado actual del timer

        Returns:
            Diccionario con botones presionados
        """
        col1, col2, col3 = st.columns(3)

        buttons = {
            'start': False,
            'pause': False,
            'resume': False,
            'stop': False
        }

        with col1:
            if status == "stopped":
                buttons['start'] = st.button(
                    "▶️ INICIAR",
                    use_container_width=True,
                    type="primary",
                    key="btn_start"
                )
            elif status == "paused":
                buttons['resume'] = st.button(
                    "▶️ REANUDAR",
                    use_container_width=True,
                    type="primary",
                    key="btn_resume"
                )

        with col2:
            if status == "running":
                buttons['pause'] = st.button(
                    "⏸️ PAUSAR",
                    use_container_width=True,
                    key="btn_pause"
                )

        with col3:
            if status in ["running", "paused"]:
                buttons['stop'] = st.button(
                    "⏹️ DETENER",
                    use_container_width=True,
                    type="secondary",
                    key="btn_stop"
                )

        return buttons


class TrainingMetricsDisplay:
    """Componentes de visualización de métricas"""

    @staticmethod
    def render_metric_cards(
        calories: float,
        target_calories: float,
        heart_rate: Optional[int],
        temperature: Optional[float]
    ):
        """
        Renderiza tarjetas con métricas principales

        Args:
            calories: Calorías quemadas
            target_calories: Calorías objetivo
            heart_rate: Frecuencia cardíaca
            temperature: Temperatura corporal
        """
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="🔥 Calorías Quemadas",
                value=f"{calories:.1f} kcal",
                delta=f"{target_calories - calories:.0f} hasta meta"
            )

        with col2:
            if heart_rate is not None:
                # Determinar zona de FC
                if heart_rate < 100:
                    zone = "Baja"
                    zone_color = "🟢"
                elif heart_rate < 140:
                    zone = "Media"
                    zone_color = "🟡"
                elif heart_rate < 170:
                    zone = "Alta"
                    zone_color = "🟠"
                else:
                    zone = "Máxima"
                    zone_color = "🔴"

                st.metric(
                    label=f"❤️ Frecuencia Cardíaca",
                    value=f"{heart_rate} ppm",
                    delta=f"{zone_color} {zone}"
                )
            else:
                st.metric(
                    label="❤️ Frecuencia Cardíaca",
                    value="-- ppm"
                )

        with col3:
            if temperature is not None:
                # Determinar estado de temperatura
                if temperature < 37.0:
                    temp_status = "Normal"
                elif temperature < 38.0:
                    temp_status = "Elevada"
                else:
                    temp_status = "Alta"

                st.metric(
                    label="🌡️ Temperatura",
                    value=f"{temperature:.1f} °C",
                    delta=temp_status
                )
            else:
                st.metric(
                    label="🌡️ Temperatura",
                    value="-- °C"
                )

        with col4:
            calorie_progress = (calories / target_calories * 100) if target_calories > 0 else 0
            st.metric(
                label="🎯 Progreso Calorías",
                value=f"{calorie_progress:.0f}%",
                delta=f"{min(calorie_progress, 100):.0f}% del objetivo"
            )

    @staticmethod
    def render_calorie_gauge(calories: float, target_calories: float):
        """
        Renderiza gauge de calorías en tiempo real

        Args:
            calories: Calorías actuales
            target_calories: Calorías objetivo
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=calories,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': "🔥 Calorías en Tiempo Real 🔥",
                'font': {'size': 28, 'color': '#FF6347', 'family': "Arial Black"}
            },
            number={
                'font': {'size': 50, 'color': '#FF6347', 'family': "Arial Black"},
                'suffix': ' kcal'
            },
            delta={
                'reference': target_calories,
                'increasing': {'color': "#00C851"},
                'decreasing': {'color': "#FFA500"},
                'font': {'size': 20, 'color': '#FFFFFF'}
            },
            gauge={
                'axis': {
                    'range': [None, target_calories * 1.2],
                    'tickwidth': 2,
                    'tickcolor': "#CCCCCC",
                    'tickfont': {'size': 14, 'color': '#CCCCCC'}
                },
                'bar': {
                    'color': "#FF6347",
                    'thickness': 0.8
                },
                'bgcolor': "rgba(50, 50, 50, 0.3)",
                'borderwidth': 3,
                'bordercolor': "#666666",
                'steps': [
                    {'range': [0, target_calories * 0.5], 'color': 'rgba(100, 50, 50, 0.4)'},
                    {'range': [target_calories * 0.5, target_calories], 'color': 'rgba(150, 70, 70, 0.5)'},
                    {'range': [target_calories, target_calories * 1.2], 'color': 'rgba(0, 200, 81, 0.4)'}
                ],
                'threshold': {
                    'line': {'color': "#00C851", 'width': 5},
                    'thickness': 0.8,
                    'value': target_calories
                }
            }
        ))

        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#FFFFFF"}
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def render_realtime_chart(
        timestamps: List[float],
        heart_rates: List[int],
        temperatures: List[float],
        calories: List[float]
    ):
        """
        Renderiza gráficos de métricas en tiempo real

        Args:
            timestamps: Marcas de tiempo
            heart_rates: Lecturas de frecuencia cardíaca
            temperatures: Lecturas de temperatura
            calories: Lecturas de calorías
        """
        if not timestamps:
            st.info("📊 Los gráficos aparecerán cuando comience el entrenamiento")
            return

        # Crear subplots
        from plotly.subplots import make_subplots

        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('❤️ Frecuencia Cardíaca', '🌡️ Temperatura Corporal', '🔥 Calorías Acumuladas'),
            vertical_spacing=0.1
        )

        # Gráfico de FC
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=heart_rates,
                mode='lines+markers',
                name='FC (ppm)',
                line=dict(color='#FF6347', width=3),
                marker=dict(size=6)
            ),
            row=1, col=1
        )

        # Gráfico de Temperatura
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=temperatures,
                mode='lines+markers',
                name='Temp (°C)',
                line=dict(color='#FF8C00', width=3),
                marker=dict(size=6)
            ),
            row=2, col=1
        )

        # Gráfico de Calorías
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=calories,
                mode='lines+markers',
                name='Calorías (kcal)',
                line=dict(color='#00C851', width=3),
                fill='tozeroy',
                marker=dict(size=6)
            ),
            row=3, col=1
        )

        # Actualizar ejes
        fig.update_xaxes(title_text="Tiempo (minutos)", row=3, col=1)
        fig.update_yaxes(title_text="ppm", row=1, col=1)
        fig.update_yaxes(title_text="°C", row=2, col=1)
        fig.update_yaxes(title_text="kcal", row=3, col=1)

        fig.update_layout(
            height=700,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)


class CoachMessageDisplay:
    """Componentes para mensajes del coach IA"""

    @staticmethod
    def render_coach_message(message: str, message_type: str = "motivation"):
        """
        Renderiza mensaje del coach con estilo

        Args:
            message: Texto del mensaje
            message_type: Tipo de mensaje
        """
        # Colores según tipo
        type_config = {
            'motivation': {'color': '#00C851', 'emoji': '💪', 'title': 'Motivación'},
            'progress': {'color': '#1E88E5', 'emoji': '📊', 'title': 'Progreso'},
            'nutrition': {'color': '#FF8C00', 'emoji': '🥗', 'title': 'Nutrición'},
            'wellness': {'color': '#9C27B0', 'emoji': '😊', 'title': 'Bienestar'},
            'encouragement': {'color': '#FFB900', 'emoji': '🌟', 'title': 'Ánimo'},
            'food_comparison': {'color': '#FF6347', 'emoji': '🍔', 'title': 'Comparación'}
        }

        config = type_config.get(message_type, type_config['motivation'])

        message_html = f"""
        <div style="background: linear-gradient(135deg, {config['color']}40, {config['color']}60);
                    border-left: 6px solid {config['color']};
                    padding: 20px;
                    border-radius: 10px;
                    margin: 15px 0;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
            <div style="font-size: 16px; color: #FFFFFF; font-weight: bold; margin-bottom: 10px;">
                {config['emoji']} {config['title']}
            </div>
            <div style="font-size: 18px; color: #FFFFFF; line-height: 1.6; font-weight: 500;">
                {message}
            </div>
        </div>
        """
        st.markdown(message_html, unsafe_allow_html=True)

    @staticmethod
    def render_coach_buttons() -> str:
        """
        Renderiza botones para solicitar diferentes tipos de mensajes

        Returns:
            Tipo de mensaje solicitado o cadena vacía
        """
        st.markdown("### 🤖 Asistente Virtual")

        col1, col2, col3 = st.columns(3)

        message_type = ""

        with col1:
            if st.button("💪 Motivación", use_container_width=True, key="coach_motivation"):
                message_type = "motivation"
            if st.button("🥗 Nutrición", use_container_width=True, key="coach_nutrition"):
                message_type = "nutrition"

        with col2:
            if st.button("📊 Progreso", use_container_width=True, key="coach_progress"):
                message_type = "progress"
            if st.button("😊 Bienestar", use_container_width=True, key="coach_wellness"):
                message_type = "wellness"

        with col3:
            if st.button("🍔 Comparar Comida", use_container_width=True, key="coach_food"):
                message_type = "food_comparison"

        return message_type


class TrainingSetupForm:
    """Formulario de configuración de entrenamiento"""

    @staticmethod
    def render_setup_form() -> Optional[Dict]:
        """
        Renderiza formulario de configuración

        Returns:
            Diccionario con datos de configuración o None
        """
        st.header("⚙️ Configuración de Entrenamiento")

        with st.form("training_setup_form"):
            # Información personal
            st.subheader("👤 Información Personal")
            col1, col2 = st.columns(2)

            with col1:
                nombre = st.text_input("Nombre", placeholder="Ej: Juan")
                edad = st.number_input("Edad", min_value=10, max_value=100, value=25)
                peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.5)

            with col2:
                apellidos = st.text_input("Apellidos", placeholder="Ej: Pérez")
                sexo = st.selectbox("Género", options=["Masculino", "Femenino"])
                estatura = st.number_input("Estatura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.5)

            st.markdown("---")

            # Configuración del entrenamiento
            st.subheader("🏃 Configuración del Entrenamiento")
            col3, col4 = st.columns(2)

            with col3:
                duration = st.number_input(
                    "Duración Objetivo (minutos)",
                    min_value=5,
                    max_value=180,
                    value=30,
                    help="¿Cuántos minutos planeas entrenar?"
                )

            with col4:
                heart_rate = st.number_input(
                    "Frecuencia Cardíaca Inicial (ppm)",
                    min_value=60,
                    max_value=220,
                    value=80,
                    help="Tu FC en reposo o al comenzar"
                )

            st.markdown("---")

            # Configuración del asistente IA
            st.subheader("🤖 Configuración del Asistente IA")
            col5, col6 = st.columns(2)

            with col5:
                idioma = st.selectbox(
                    "🌍 Idioma del Asistente",
                    options=["Español", "English", "Français"],
                    help="Selecciona el idioma para los mensajes del coach"
                )

                enable_tts = st.checkbox(
                    "🔊 Activar voz del asistente (Text-to-Speech)",
                    value=False,
                    help="El asistente leerá los mensajes en voz alta"
                )

            with col6:
                voz = st.selectbox(
                    "🎤 Tipo de Voz",
                    options=["Femenina", "Masculina"],
                    help="Selecciona el tipo de voz para el asistente"
                )

                if not enable_tts:
                    st.caption("⚠️ Activa TTS para usar esta opción")

            st.info("🤖 El asistente IA está configurado automáticamente desde las variables de entorno")

            submitted = st.form_submit_button(
                "🚀 Iniciar Sesión de Entrenamiento",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                return {
                    'nombre': nombre,
                    'apellidos': apellidos,
                    'sexo': sexo,
                    'edad': edad,
                    'peso': peso,
                    'estatura': estatura,
                    'duracion': duration,
                    'pulsaciones': heart_rate,
                    'idioma': idioma,
                    'enable_tts': enable_tts,
                    'voz': voz
                }

        return None
