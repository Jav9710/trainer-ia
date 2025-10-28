# 📖 LÉEME PRIMERO - Aplicación de Predicción de Calorías

Bienvenido a la aplicación de predicción de calorías. Esta carpeta `app/` contiene toda la aplicación Python organizada y documentada.

---

## 🎯 ¿Qué encontrarás aquí?

Esta es una **aplicación completa de Machine Learning** que:

- ✅ Predice calorías quemadas durante el ejercicio
- ✅ Usa modelos ML (MLP Regressor) o fórmulas matemáticas
- ✅ Tiene entrenamiento en tiempo real con cronómetro
- ✅ Coach motivacional con IA (OpenRouter) o mensajes predefinidos
- ✅ Text-to-Speech en 3 idiomas
- ✅ Sensores biométricos simulados
- ✅ Interfaz web con Streamlit
- ✅ Gráficos interactivos con Plotly
- ✅ Exportación de datos y reportes

---

## 📚 Índice de Documentación

Toda la documentación está organizada en archivos específicos. **Empieza aquí**:

### 1️⃣ Para empezar AHORA MISMO
**→ [INICIO_RAPIDO.md](./INICIO_RAPIDO.md)**
- Instalación rápida
- Cómo ejecutar la app
- Ejemplos de uso
- Solución de problemas comunes

**Tiempo estimado**: 5 minutos

---

### 2️⃣ Para entender la estructura
**→ [README.md](./README.md)**
- Estructura completa de carpetas
- Funcionalidades principales
- Flujo de trabajo
- Personalización básica

**Tiempo estimado**: 10 minutos

---

### 3️⃣ Para buscar algo específico
**→ [INDICE_RAPIDO.md](./INDICE_RAPIDO.md)**
- Buscar por funcionalidad
- Buscar por tipo de código
- Casos de uso comunes
- Enlaces rápidos a archivos

**Tiempo estimado**: 2 minutos (es un índice de búsqueda)

---

### 4️⃣ Para ver un resumen visual de las clases
**→ [RESUMEN_CLASES.txt](./RESUMEN_CLASES.txt)**
- 14 clases principales resumidas
- Argumentos y retornos de cada clase
- Flujo de datos visual
- Archivos de configuración

**Tiempo estimado**: 15 minutos

---

### 5️⃣ Para documentación completa de TODAS las clases
**→ [DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md)**
- Documentación detallada de cada clase
- Todos los métodos explicados
- Argumentos completos
- Flujos de datos

**Tiempo estimado**: 30-45 minutos (referencia completa)

---

## 🚦 ¿Por dónde empiezo?

### Si quieres USAR la aplicación:
1. **[INICIO_RAPIDO.md](./INICIO_RAPIDO.md)** ← Empieza aquí
2. Ejecuta `streamlit run app.py`
3. ¡Listo!

### Si quieres ENTENDER cómo funciona:
1. **[README.md](./README.md)** ← Estructura general
2. **[RESUMEN_CLASES.txt](./RESUMEN_CLASES.txt)** ← Clases principales
3. **[DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md)** ← Referencia completa

### Si quieres MODIFICAR o PERSONALIZAR:
1. **[INDICE_RAPIDO.md](./INDICE_RAPIDO.md)** ← Busca lo que necesitas
2. **[DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md)** ← Ve a la clase específica
3. Modifica el archivo correspondiente en `src/`

### Si quieres INTEGRAR en tu proyecto:
1. **[RESUMEN_CLASES.txt](./RESUMEN_CLASES.txt)** ← Ve las clases disponibles
2. **[DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md)** ← Aprende a usarlas
3. Importa las clases que necesites

---

## 📁 Archivos en esta carpeta

```
app/
│
├── 📖 LEEME_PRIMERO.md              ← Estás aquí - Índice general
├── 🚀 INICIO_RAPIDO.md              ← Guía de inicio rápido
├── 📘 README.md                     ← Estructura y visión general
├── 🔍 INDICE_RAPIDO.md              ← Búsqueda por funcionalidad
├── 📊 RESUMEN_CLASES.txt            ← Resumen visual de clases
├── 📚 DOCUMENTACION_CLASES.md       ← Documentación completa
│
├── 🐍 app.py                        ← Aplicación principal
├── 🔐 .env                          ← Variables de entorno (API keys)
│
├── 📂 src/                          ← Código fuente
│   ├── config.py                    ← Configuración
│   ├── models.py                    ← Modelos ML
│   ├── calculations.py              ← Cálculos de calorías
│   ├── utils.py                     ← Utilidades
│   ├── ui/                          ← Interfaz de usuario
│   └── services/                    ← Servicios (timer, coach, TTS, etc.)
│
└── 📂 pages/                        ← Páginas adicionales de Streamlit
    └── 1_🏃_Entrenamiento_En_Vivo.py
```

---

## 🎓 Niveles de Documentación

### Nivel 1: Usuario Básico
**Solo quiero usar la app**
- [INICIO_RAPIDO.md](./INICIO_RAPIDO.md)
- Tiempo: 5 minutos

### Nivel 2: Usuario Avanzado
**Quiero personalizar algunas cosas**
- [INICIO_RAPIDO.md](./INICIO_RAPIDO.md) → Sección "Personalización Rápida"
- [README.md](./README.md) → Sección "Personalización"
- Tiempo: 15 minutos

### Nivel 3: Desarrollador
**Quiero entender todo el código**
- [README.md](./README.md)
- [RESUMEN_CLASES.txt](./RESUMEN_CLASES.txt)
- [DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md)
- Tiempo: 1 hora

### Nivel 4: Integrador
**Quiero usar estas clases en mi proyecto**
- [INDICE_RAPIDO.md](./INDICE_RAPIDO.md) → Busca la funcionalidad
- [DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md) → Lee la clase
- Importa y usa
- Tiempo: Variable según necesidad

---

## 💡 Consejos

1. **No leas todo de una vez**: Usa esta guía para navegar según lo que necesites
2. **Empieza con INICIO_RAPIDO.md**: Es el camino más corto para empezar
3. **Usa INDICE_RAPIDO.md**: Cuando busques algo específico
4. **Consulta DOCUMENTACION_CLASES.md**: Como referencia cuando necesites detalles

---

## 🌟 Características Destacadas

### 🔥 Predicción de Calorías
- Modelo ML (MLP Regressor) entrenado
- Fallback a fórmulas matemáticas
- Gráficos interactivos
- Exportación de reportes

### ⏱️ Entrenamiento en Tiempo Real
- Cronómetro con pausa/reanudar
- Sensores biométricos simulados
- Predicción continua cada 30s
- Perfiles de entrenamiento personalizados

### 🤖 Coach con IA
- Mensajes motivacionales
- Consejos nutricionales
- Comparaciones con comida
- 3 idiomas: Español, English, Français

### 🔊 Text-to-Speech
- Voz en tiempo real
- Voces masculinas y femeninas
- Multiidioma
- No bloqueante (sigue entrenando mientras habla)

---

## 📊 Tecnologías Utilizadas

- **Python 3.8+**
- **Streamlit**: Interfaz web
- **Scikit-Learn**: Machine Learning
- **Plotly**: Gráficos interactivos
- **OpenRouter API**: Coach con IA (opcional)
- **Edge-TTS**: Text-to-Speech (opcional)

---

## 🎯 Casos de Uso

### ✅ Si eres...

**Deportista**: Usa la app para trackear tus calorías durante el ejercicio

**Nutricionista**: Usa la predicción para planificar dietas con tus pacientes

**Desarrollador**: Estudia el código para aprender arquitectura limpia en Python

**Data Scientist**: Analiza los datos exportados de las sesiones

**Estudiante**: Aprende ML, Streamlit, y diseño de software

**Profesor**: Usa como ejemplo de aplicación completa de ML

---

## 🆘 Ayuda Rápida

| Problema | Solución |
|----------|----------|
| No sé cómo empezar | [INICIO_RAPIDO.md](./INICIO_RAPIDO.md) |
| No encuentro una función | [INDICE_RAPIDO.md](./INDICE_RAPIDO.md) |
| Quiero entender una clase | [DOCUMENTACION_CLASES.md](./DOCUMENTACION_CLASES.md) |
| Error al ejecutar | [INICIO_RAPIDO.md](./INICIO_RAPIDO.md) → "Solución de Problemas" |
| Quiero personalizar | [README.md](./README.md) → "Personalización" |

---

## ✨ Próximos Pasos

1. **Empieza**: Lee [INICIO_RAPIDO.md](./INICIO_RAPIDO.md)
2. **Ejecuta**: `streamlit run app.py`
3. **Explora**: Prueba la predicción y el entrenamiento en vivo
4. **Profundiza**: Lee el resto de la documentación según necesites

---

## 📞 Estructura de la Documentación

```
LEEME_PRIMERO.md (estás aquí)
    ↓
    ├─→ INICIO_RAPIDO.md (para usuarios)
    │
    ├─→ README.md (visión general)
    │
    ├─→ INDICE_RAPIDO.md (búsqueda rápida)
    │
    ├─→ RESUMEN_CLASES.txt (resumen visual)
    │
    └─→ DOCUMENTACION_CLASES.md (referencia completa)
```

---

**¡Disfruta explorando la aplicación! 🚀**

*Documentación creada con ❤️ para facilitar el uso y comprensión del código*
