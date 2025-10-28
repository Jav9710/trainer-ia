"""
Utilidades y funciones auxiliares
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List

from config import CHART_CONFIG, ACTIVITY_CALORIES


class ChartGenerator:
    """Genera gráficos y visualizaciones"""

    @staticmethod
    def create_calorie_gauge(
            calories: float,
            max_calories: int = None
    ) -> go.Figure:
        """
        Crea un gráfico de medidor para calorías

        Args:
            calories: Calorías quemadas
            max_calories: Máximo para el gauge (si no se especifica, usa config)

        Returns:
            Figura de Plotly
        """
        if max_calories is None:
            max_calories = CHART_CONFIG['gauge']['max_calories']

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=calories,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': "🔥 Calorías Quemadas 🔥",
                'font': {'size': 32, 'color': '#FF6347', 'family': "Arial Black"}
            },
            number={
                'font': {'size': 60, 'color': '#FF6347', 'family': "Arial Black"},
                'suffix': ' kcal'
            },
            delta={
                'reference': max_calories / 2,
                'increasing': {'color': "#00C851"},
                'decreasing': {'color': "#FFB900"},
                'font': {'size': 24, 'color': '#FFFFFF'}
            },
            gauge={
                'axis': {
                    'range': [None, max_calories],
                    'tickwidth': 2,
                    'tickcolor': "#CCCCCC",
                    'tickfont': {'size': 16, 'color': '#CCCCCC', 'family': "Arial"}
                },
                'bar': {
                    'color': "#FF6347",
                    'thickness': 0.85
                },
                'bgcolor': "rgba(50, 50, 50, 0.3)",
                'borderwidth': 3,
                'bordercolor': "#666666",
                'steps': [
                    {'range': [0, max_calories / 3], 'color': 'rgba(100, 150, 100, 0.4)', 'name': 'Bajo'},
                    {'range': [max_calories / 3, 2 * max_calories / 3], 'color': 'rgba(150, 150, 70, 0.5)', 'name': 'Medio'},
                    {'range': [2 * max_calories / 3, max_calories], 'color': 'rgba(200, 100, 80, 0.5)', 'name': 'Alto'}
                ],
                'threshold': {
                    'line': {'color': "#D32F2F", 'width': 6},
                    'thickness': 0.85,
                    'value': max_calories * 0.9
                }
            }
        ))

        fig.update_layout(
            height=CHART_CONFIG['gauge']['height'],
            margin=dict(l=30, r=30, t=80, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#FFFFFF", 'family': "Arial", 'size': 14}
        )

        return fig

    @staticmethod
    def create_comparison_chart(
            user_calories: float,
            user_label: str = "Tu Entrenamiento"
    ) -> go.Figure:
        """
        Crea gráfico de comparación con otras actividades

        Args:
            user_calories: Calorías del usuario
            user_label: Etiqueta para el entrenamiento del usuario

        Returns:
            Figura de Plotly
        """
        # Combinar actividades predefinidas con el del usuario
        activities = list(ACTIVITY_CALORIES.keys()) + [user_label]
        calories = list(ACTIVITY_CALORIES.values()) + [user_calories]

        # Colores
        colors = CHART_CONFIG['comparison']['colors']

        fig = px.bar(
            x=activities,
            y=calories,
            labels={'x': 'Actividad', 'y': 'Calorías (kcal)'},
            title='Comparación de Calorías Quemadas (30 min)',
            color=activities,
            color_discrete_sequence=colors
        )

        fig.update_layout(
            showlegend=False,
            height=CHART_CONFIG['comparison']['height'],
            xaxis_title="Tipo de Actividad",
            yaxis_title="Calorías Quemadas"
        )

        return fig

    @staticmethod
    def create_food_equivalents_chart(equivalents: Dict[str, int]) -> go.Figure:
        """
        Crea gráfico de equivalentes alimenticios

        Args:
            equivalents: Diccionario de equivalentes

        Returns:
            Figura de Plotly
        """
        foods = list(equivalents.keys())
        quantities = list(equivalents.values())

        fig = px.bar(
            x=quantities,
            y=foods,
            orientation='h',
            labels={'x': 'Cantidad', 'y': 'Alimento'},
            title='Equivalentes en Alimentos'
        )

        fig.update_layout(
            showlegend=False,
            height=300,
            xaxis_title="Cantidad de Unidades",
            yaxis_title=""
        )

        return fig


class ReportGenerator:
    """Genera reportes de resultados"""

    @staticmethod
    def generate_text_report(
            user_data: Dict,
            calories: float,
            equivalents: Dict[str, int],
            model_used: str
    ) -> str:
        """
        Genera reporte en texto plano

        Args:
            user_data: Datos del usuario
            calories: Calorías quemadas
            equivalents: Equivalentes alimenticios
            model_used: Modelo usado para predicción

        Returns:
            String con el reporte
        """
        report = f"""
            REPORTE DE PREDICCIÓN DE CALORÍAS
            ={'=' * 50}
            
            INFORMACIÓN DEL USUARIO
            {'-' * 50}
            Nombre: {user_data.get('nombre', 'N/A')} {user_data.get('apellidos', 'N/A')}
            Género: {user_data.get('sexo', 'N/A')}
            Edad: {user_data.get('edad', 'N/A')} años
            Peso: {user_data.get('peso', 'N/A')} kg
            Estatura: {user_data.get('estatura', 'N/A')} cm
            
            DATOS DEL EJERCICIO
            {'-' * 50}
            Duración: {user_data.get('duracion', 'N/A')} minutos
            Frecuencia Cardíaca: {user_data.get('pulsaciones', 'N/A')} ppm
            Temperatura Corporal: {user_data.get('temperatura', 'N/A')} °C
            
            RESULTADO DE LA PREDICCIÓN
            {'-' * 50}
            CALORÍAS QUEMADAS: {calories:.2f} kcal
            Método de predicción: {model_used}
            
            EQUIVALENTES EN ALIMENTOS
            {'-' * 50}
            """
        for food, quantity in equivalents.items():
            report += f"{food}: {quantity} unidades\n"

        report += f"\n{'=' * 50}\n"
        report += "Generado por: Predict Calorie Expenditure System\n"

        return report

    @staticmethod
    def generate_csv_report(
            user_data: Dict,
            calories: float,
            model_used: str
    ) -> str:
        """
        Genera reporte en formato CSV

        Args:
            user_data: Datos del usuario
            calories: Calorías quemadas
            model_used: Modelo usado

        Returns:
            String en formato CSV
        """
        csv = "Campo,Valor\n"
        csv += f"Nombre,{user_data.get('nombre', '')} {user_data.get('apellidos', '')}\n"
        csv += f"Género,{user_data.get('sexo', '')}\n"
        csv += f"Edad,{user_data.get('edad', '')}\n"
        csv += f"Peso,{user_data.get('peso', '')}\n"
        csv += f"Estatura,{user_data.get('estatura', '')}\n"
        csv += f"Duración,{user_data.get('duracion', '')}\n"
        csv += f"Frecuencia Cardíaca,{user_data.get('pulsaciones', '')}\n"
        csv += f"Temperatura,{user_data.get('temperatura', '')}\n"
        csv += f"Calorías Quemadas,{calories:.2f}\n"
        csv += f"Modelo Usado,{model_used}\n"

        return csv


class DataValidator:
    """Valida datos de entrada"""

    @staticmethod
    def validate_user_data(
            nombre: str,
            apellidos: str,
            edad: int,
            peso: float,
            estatura: float,
            duracion: int,
            pulsaciones: int,
            temperatura: float
    ) -> tuple[bool, List[str]]:
        """
        Valida todos los datos del usuario

        Args:
            nombre: Nombre
            apellidos: Apellidos
            edad: Edad
            peso: Peso
            estatura: Estatura
            duracion: Duración
            pulsaciones: Pulsaciones
            temperatura: Temperatura

        Returns:
            Tuple (es_válido, lista_de_errores)
        """
        errors = []
        #Esto es para el Agente Claude, stos campos de validacion deben ser validados con config.py que es donde estan
        #los valores minimos y maximos para cada input del usuario, modifica esta clase para que cargue de confyg.py
        #dichos valores y los use aqui para validar.
        # Validar campos de texto
        if not nombre or not nombre.strip():
            errors.append("El nombre es requerido")

        if not apellidos or not apellidos.strip():
            errors.append("Los apellidos son requeridos")

        # Validar rangos numéricos
        if edad < 10 or edad > 100:
            errors.append("La edad debe estar entre 10 y 100 años")

        if peso < 30 or peso > 300:
            errors.append("El peso debe estar entre 30 y 300 kg")

        if estatura < 100 or estatura > 250:
            errors.append("La estatura debe estar entre 100 y 250 cm")

        if duracion < 1 or duracion > 300:
            errors.append("La duración debe estar entre 1 y 300 minutos")

        if pulsaciones < 60 or pulsaciones > 220:
            errors.append("Las pulsaciones deben estar entre 60 y 220 ppm")

        if temperatura < 35 or temperatura > 42:
            errors.append("La temperatura debe estar entre 35 y 42 °C")

        is_valid = len(errors) == 0

        return is_valid, errors

    @staticmethod
    def format_validation_errors(errors: List[str]) -> str:
        """
        Formatea errores de validación para mostrar

        Args:
            errors: Lista de errores

        Returns:
            String formateado con los errores
        """
        if not errors:
            return ""

        error_text = "Se encontraron los siguientes errores:\n\n"
        for i, error in enumerate(errors, 1):
            error_text += f"{i}. {error}\n"

        return error_text