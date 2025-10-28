"""
Página de Entrenamiento en Tiempo Real
Punto de entrada para Streamlit - La lógica está en src/ui/pages/training_live.py
"""
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ui.pages import run_training_live

if __name__ == "__main__":
    run_training_live()
