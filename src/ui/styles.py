"""
Estilos CSS para la aplicación
"""

def get_custom_css() -> str:
    """
    Retorna CSS personalizado para la aplicación

    Returns:
        String con CSS
    """
    return """
    <style>
    /* Fondo principal con gradiente */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.05), rgba(0,0,0,0.05));
    }
    
    /* Métricas */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    /* Títulos */
    h1 {
        color: #667eea;
        text-align: center;
        padding: 1rem 0;
    }
    
    h2 {
        color: #764ba2;
    }
    
    /* Tarjetas de resultados */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        color: #333;
    }

    .result-card h4 {
        color: #333;
    }

    .result-card p {
        color: #333;
    }
    
    /* Caja de información */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Caja de modelo */
    .model-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Tarjeta de calorías destacada */
    .calories-card {
        text-align: center;
        background: linear-gradient(135deg, #ff9a56 0%, #ff6a00 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .calories-card h1 {
        font-size: 4rem;
        margin: 0;
        color: white;
    }
    
    .calories-card h3 {
        color: white;
        margin: 10px 0;
    }
    
    /* Botones */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Formularios */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Espaciado */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Animaciones */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-card {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """


def get_header_html(title: str, subtitle: str) -> str:
    """
    Genera HTML para el header principal

    Args:
        title: Título principal
        subtitle: Subtítulo

    Returns:
        String con HTML
    """
    return f"""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1>{title}</h1>
        <p style='font-size: 1.3rem; color: #764ba2;'>
            {subtitle}
        </p>
    </div>
    """


def get_result_header_html(model_used: str = None) -> str:
    """
    Genera HTML para el header de resultados

    Args:
        model_used: Nombre del modelo usado (opcional)

    Returns:
        String con HTML
    """
    html = "<div style='text-align: center; padding: 1rem 0;'><h2 style='color: #764ba2;'>🎯 Resultados de la Predicción</h2>"

    if model_used:
        html += f"<p style='font-size: 1.2rem; color: #333;'><strong>{model_used}</strong></p>"

    html += "</div>"

    return html


def get_calories_card_html(calories: float) -> str:
    """
    Genera HTML para la tarjeta de calorías

    Args:
        calories: Calorías quemadas

    Returns:
        String con HTML
    """
    return f"""
    <div class='calories-card'>
        <h1>🔥 {calories:.0f}</h1>
        <h3>Calorías Quemadas</h3>
        <p style='opacity: 0.9;'>Predicción con Machine Learning</p>
    </div>
    """


def get_info_card_html(title: str, content: dict) -> str:
    """
    Genera HTML para tarjetas de información

    Args:
        title: Título de la tarjeta
        content: Diccionario con contenido {label: value}

    Returns:
        String con HTML
    """
    html = f"""
    <div class='result-card'>
        <h4>{title}</h4>
    """

    for label, value in content.items():
        html += f"<p><strong>{label}:</strong> {value}</p>\n"

    html += "</div>"

    return html


def get_footer_html(version: str = None) -> str:
    """
    Genera HTML para el footer

    Args:
        version: Versión de la aplicación (si no se proporciona, usa la del config)

    Returns:
        String con HTML
    """
    # Importar aquí para evitar problemas de import circular
    if version is None:
        try:
            from config import APP_VERSION
            version = APP_VERSION
        except ImportError:
            version = "2.0.0"  # Fallback

    return f"""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>💪 <strong>Predict Calorie Expenditure</strong> - Sistema ML con Scikit-Learn</p>
        <p>🤖 Random Forest Regressor | MLP Regressor</p>
        <p>Versión {version} | Powered by Streamlit & Scikit-Learn</p>
    </div>
    """