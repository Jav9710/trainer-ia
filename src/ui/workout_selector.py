"""
Componente UI para seleccionar tipo de entrenamiento
"""
import streamlit as st
import plotly.graph_objects as go
from services.workout_profiles import list_workout_profiles, get_workout_profile


def render_workout_selector():
    """
    Renderiza el selector visual de tipos de entrenamiento

    Returns:
        Nombre del perfil seleccionado o 'manual' para modo manual
    """
    # Verificar si ya fue confirmado (modo manual o guiado)
    if st.session_state.get('workout_confirmed', False):
        if st.session_state.get('workout_mode') == 'manual':
            return 'manual'
        elif 'selected_workout' in st.session_state:
            return st.session_state['selected_workout']

    # Verificar si ya hay uno seleccionado pero no confirmado
    if 'selected_workout' in st.session_state and not st.session_state.get('workout_confirmed', False):
        selected_name = st.session_state['selected_workout']
        selected = get_workout_profile(selected_name)

        st.success(f"Entrenamiento seleccionado: {selected.name}")

        # Mostrar gráfico de intensidad
        st.subheader("Patron de Intensidad")

        times, intensities = selected.get_chart_data()

        fig = go.Figure()

        # Area de intensidad
        fig.add_trace(go.Scatter(
            x=times,
            y=intensities,
            fill='tozeroy',
            name='Intensidad',
            line=dict(color='#FF6B6B', width=3),
            fillcolor='rgba(255, 107, 107, 0.3)'
        ))

        # Lineas de referencia
        fig.add_hline(y=25, line_dash="dash", line_color="green", annotation_text="Bajo")
        fig.add_hline(y=50, line_dash="dash", line_color="yellow", annotation_text="Medio")
        fig.add_hline(y=75, line_dash="dash", line_color="orange", annotation_text="Alto")
        fig.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="Maximo")

        fig.update_layout(
            title="Progresion de Intensidad Durante el Entrenamiento",
            xaxis_title="Tiempo (%)",
            yaxis_title="Intensidad (%)",
            yaxis=dict(range=[0, 105]),
            height=400,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Informacion adicional
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dificultad", selected.difficulty)
        with col2:
            st.metric("Cal/30min", f"{selected.avg_calories_30min} kcal")
        with col3:
            avg_intensity = sum(intensities) / len(intensities)
            st.metric("Intensidad Promedio", f"{avg_intensity:.0f}%")

        st.markdown("---")

        # Boton para confirmar y continuar
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("Cambiar Entrenamiento", use_container_width=True):
                del st.session_state['selected_workout']
                st.rerun()
        with col_btn2:
            if st.button("Continuar con este Entrenamiento", type="primary", use_container_width=True):
                st.session_state['workout_confirmed'] = True
                st.rerun()

        # Mientras no confirme, retornar None
        return None

    # Mostrar selector si no hay ninguno seleccionado
    st.subheader("Selecciona tu Tipo de Entrenamiento")

    # Opción para modo manual
    st.markdown("### Opciones de Entrenamiento")
    col_manual, col_auto = st.columns(2)

    with col_manual:
        st.info("**Modo Manual**: Tu controlas el ritmo")
        if st.button("Ir a mi Propio Ritmo", use_container_width=True, type="secondary"):
            st.session_state['workout_mode'] = 'manual'
            st.session_state['workout_confirmed'] = True
            st.rerun()

    with col_auto:
        st.info("**Modo Guiado**: Sigue un plan de entrenamiento")
        st.caption("Selecciona uno de los planes abajo")

    st.markdown("---")
    st.subheader("Planes de Entrenamiento Guiados")

    # Obtener perfiles disponibles
    profiles = list_workout_profiles()

    # Crear columnas para mostrar tarjetas
    cols = st.columns(3)

    for idx, (name, profile) in enumerate(profiles):
        with cols[idx % 3]:
            # Crear tarjeta visual
            difficulty_colors = {
                'Facil': '#4CAF50',
                'Moderado': '#FFC107',
                'Intenso': '#FF9800',
                'Muy Intenso': '#F44336'
            }

            difficulty_color = difficulty_colors.get(profile.difficulty, '#9E9E9E')

            # Mostrar tarjeta
            card_html = f"""
            <div style="
                border: 2px solid {difficulty_color};
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 10px;
                background-color: rgba(255,255,255,0.05);
            ">
                <h3 style="margin:0; text-align:center;">{profile.name}</h3>
                <p style="
                    background-color: {difficulty_color};
                    color: white;
                    padding: 5px;
                    border-radius: 5px;
                    text-align: center;
                    font-weight: bold;
                ">{profile.difficulty}</p>
                <p style="font-size: 0.9em; color: #ccc;">{profile.description}</p>
                <p style="text-align: center; font-weight: bold;">~{profile.avg_calories_30min} kcal/30min</p>
            </div>
            """

            st.markdown(card_html, unsafe_allow_html=True)

            # Boton para seleccionar
            if st.button(f"Seleccionar", key=f"select_{name}", use_container_width=True):
                st.session_state['selected_workout'] = name
                st.session_state['workout_confirmed'] = False
                st.rerun()

    return None


def render_compact_workout_selector():
    """
    Versión compacta del selector para sidebar

    Returns:
        Nombre del perfil seleccionado
    """
    profiles = list_workout_profiles()

    # Crear opciones para selectbox
    options = {
        f"{profile.name} ({profile.difficulty})": name
        for name, profile in profiles
    }

    selected = st.selectbox(
        "Tipo de Entrenamiento",
        options=list(options.keys()),
        help="Selecciona el tipo de entrenamiento que vas a realizar"
    )

    selected_profile_name = options[selected]

    # Mostrar mini gráfico
    if st.checkbox("Ver patrón de intensidad", value=False):
        profile = get_workout_profile(selected_profile_name)
        times, intensities = profile.get_chart_data()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times,
            y=intensities,
            fill='tozeroy',
            line=dict(color='#FF6B6B', width=2),
            fillcolor='rgba(255, 107, 107, 0.2)'
        ))

        fig.update_layout(
            height=200,
            margin=dict(l=0, r=0, t=20, b=20),
            showlegend=False,
            xaxis_title="Tiempo %",
            yaxis_title="Intensidad %"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(f"~{profile.avg_calories_30min} kcal en 30 min")

    return selected_profile_name
