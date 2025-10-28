# 🚀 Guía de Inicio Rápido

Esta guía te ayudará a empezar a usar la aplicación en minutos.

---

## 📋 Requisitos Previos

1. **Python 3.8+** instalado
2. **pip** actualizado
3. **Modelo ML** en la carpeta `models/` (opcional, la app funciona con fórmulas si no existe)

---

## ⚡ Instalación Rápida

### Paso 1: Instalar dependencias

```bash
cd app
pip install streamlit scikit-learn joblib plotly pandas numpy requests python-dotenv
```

### Paso 2 (Opcional): Instalar Text-to-Speech mejorado

```bash
pip install edge-tts
```

---

## 🎯 Uso Básico

### Opción 1: Predicción Simple de Calorías

```bash
cd app
streamlit run app.py
```

**¿Qué hace?**
- Abre una interfaz web
- Te pide datos personales (edad, peso, altura, etc.)
- Te pide datos de ejercicio (duración, FC, temperatura)
- Predice calorías quemadas
- Muestra resultados con gráficos

**Pasos en la interfaz:**
1. Completa el formulario con tus datos
2. Haz clic en "🔥 Predecir Calorías"
3. Revisa los resultados
4. Descarga el reporte (TXT o CSV) si lo deseas

---

### Opción 2: Entrenamiento en Tiempo Real

```bash
cd app
streamlit run pages/1_🏃_Entrenamiento_En_Vivo.py
```

O acceder desde la barra lateral de la aplicación principal.

**¿Qué hace?**
- Cronómetro en tiempo real
- Simula sensores de FC y temperatura
- Predice calorías cada 30 segundos
- Coach motivacional con mensajes cada 30 segundos
- Text-to-Speech (voz) opcional

**Pasos en la interfaz:**
1. Completa datos personales
2. Selecciona duración del entrenamiento
3. Elige perfil de ejercicio (caminata, trote, carrera, etc.)
4. Configura idioma y voz (opcional)
5. Haz clic en "▶️ Iniciar Entrenamiento"
6. Usa los controles (Pausar, Reanudar, Detener)

---

## 🔑 Configuración Opcional

### API Key para Coach IA (OpenRouter)

Si quieres usar el coach con IA en lugar de mensajes predefinidos:

1. Obtén una API key en [OpenRouter](https://openrouter.ai/)
2. Edita el archivo `.env`:
   ```
   OPEN_ROUTER_API_KEY=tu_api_key_aqui
   ```
3. Reinicia la aplicación

**Sin API key**: La app funciona perfectamente con mensajes predefinidos en 3 idiomas.

---

## 📁 Estructura de Archivos que Necesitas

```
app/
├── app.py                    # ✅ Necesario
├── .env                      # ⚠️  Opcional (solo si quieres API key)
├── src/                      # ✅ Necesario (todo)
├── pages/                    # ✅ Necesario (para entrenamiento)
└── models/
    └── MLPRegressor.joblib   # ⚠️  Opcional (usa fórmulas si no existe)
```

---

## 🎨 Personalización Rápida

### Cambiar rangos de entrada

Edita [src/config.py](./src/config.py):

```python
INPUT_RANGES = {
    'age': {'min': 10, 'max': 100, 'default': 25},
    'weight': {'min': 30.0, 'max': 300.0, 'default': 70.0},
    # ... etc
}
```

### Agregar nuevos alimentos equivalentes

Edita [src/config.py](./src/config.py):

```python
FOOD_EQUIVALENTS = {
    '🍎 Manzanas': 52,
    '🍔 Hamburguesas': 250,
    '🆕 Tu Alimento': 150,  # ← Agregar aquí
}
```

### Cambiar colores y estilos

Edita [src/ui/styles.py](./src/ui/styles.py):

```python
def get_custom_css() -> str:
    return """
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    /* ... modificar CSS aquí */
    </style>
    """
```

### Agregar nuevos perfiles de entrenamiento

Edita [src/services/workout_profiles.py](./src/services/workout_profiles.py):

```python
WORKOUT_PROFILES = {
    'mi_perfil': {
        'name': 'Mi Perfil Personalizado',
        'description': 'Descripción',
        'zones': [...],
    }
}
```

---

## 🐛 Solución de Problemas

### Error: "Modelo MLP no encontrado"

**Solución**:
- Esto es normal si no tienes el modelo entrenado
- La app usará fórmulas matemáticas automáticamente
- Para entrenar el modelo, consulta la documentación de entrenamiento

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Solución**:
```bash
pip install streamlit
```

### Error en Text-to-Speech

**Solución**:
```bash
pip install edge-tts
```

Si sigue sin funcionar, desactiva TTS en la interfaz.

### Error: "API key inválida"

**Solución**:
- Verifica que el API key en `.env` sea correcto
- O simplemente deja vacío el archivo `.env` para usar mensajes predefinidos

### La aplicación se ve rara o sin estilos

**Solución**:
- Refresca la página (F5)
- Limpia caché de Streamlit: `streamlit cache clear`

---

## 📊 Ejemplo de Uso Completo

### Escenario: Quiero predecir calorías de una caminata

```bash
# 1. Ejecutar la app
cd app
streamlit run app.py

# 2. En la interfaz web:
- Nombre: Juan
- Apellidos: Pérez
- Género: Masculino
- Edad: 30 años
- Peso: 75 kg
- Estatura: 175 cm
- Duración: 30 minutos
- Frecuencia Cardíaca: 110 ppm
- Temperatura: 37.2 °C

# 3. Clic en "🔥 Predecir Calorías"

# 4. Ver resultados:
- Calorías: ~250 kcal
- Equivalentes: 5 manzanas, 1 hamburguesa, etc.
- Gráficos comparativos

# 5. Descargar reporte si lo deseas
```

---

## 🎓 Siguiente Nivel

Una vez que domines lo básico:

1. **Lee la documentación completa**: [DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md)
2. **Explora el código**: Usa [INDICE_RAPIDO.md](./INDICE_RAPIDO.md) para navegar
3. **Personaliza**: Modifica clases según tus necesidades
4. **Integra**: Usa las clases en tus propios proyectos

---

## 📚 Documentación Adicional

| Documento | ¿Para qué sirve? |
|-----------|------------------|
| [README.md](./README.md) | Visión general de la estructura |
| [DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md) | Documentación detallada de cada clase |
| [INDICE_RAPIDO.md](./INDICE_RAPIDO.md) | Navegación rápida por funcionalidad |
| [RESUMEN_CLASES.txt](./RESUMEN_CLASES.txt) | Resumen visual de las clases principales |

---

## ✅ Checklist de Inicio

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install ...`)
- [ ] Carpeta `app/` con todos los archivos
- [ ] Ejecutar `streamlit run app.py`
- [ ] La interfaz se abre en el navegador
- [ ] Puedes hacer predicciones

**¡Listo! Ya estás usando la aplicación.**

---

## 💡 Tips Útiles

1. **Modo auto-refresh**: Streamlit actualiza automáticamente cuando modificas archivos
2. **Modo oscuro**: Configura en Settings > Theme en la interfaz de Streamlit
3. **Panel lateral**: Usa la flechita para ocultar/mostrar el sidebar
4. **Teclas útiles**:
   - `R` = Rerun app
   - `C` = Clear cache
   - `H` = Help

---

## 🆘 Soporte

Si tienes problemas:

1. Revisa la sección "Solución de Problemas" arriba
2. Verifica que todas las dependencias estén instaladas
3. Consulta la documentación completa
4. Revisa los logs en la consola donde ejecutaste `streamlit run`

---

**¡Disfruta usando la aplicación de predicción de calorías! 🔥**
