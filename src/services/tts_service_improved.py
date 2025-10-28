"""
Servicio de Text-to-Speech mejorado con gTTS
Usa Google Text-to-Speech (gratis, sincrónico, sin problemas de event loop)
"""
import os
import tempfile
import threading
import hashlib
import time as time_module
import re
from typing import Optional
import pygame

# Importar gTTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("Advertencia: gTTS no está instalado. Instala con: pip install gtts")


class ImprovedTTSService:
    """Servicio TTS mejorado con gTTS (Google Text-to-Speech)"""

    def __init__(self, language: str = "Español", voice_gender: str = "Femenina"):
        """
        Inicializa el servicio TTS mejorado

        Args:
            language: Idioma (Español, English, Français)
            voice_gender: Género de voz (Femenina, Masculina) - solo informativo para gTTS
        """
        self.language = language
        self.voice_gender = voice_gender
        self.is_initialized = False
        self.last_text = None  # Para detectar textos nuevos

        # Mapeo de idiomas
        self.lang_codes = {
            'Español': 'es',
            'English': 'en',
            'Français': 'fr',
            'Deutsch': 'de',
            'Italiano': 'it',
            'Português': 'pt'
        }

        # Inicializar pygame mixer para reproducción
        try:
            pygame.mixer.init()
            self.pygame_available = True
        except Exception as e:
            print(f"Error inicializando pygame: {e}")
            self.pygame_available = False

        if GTTS_AVAILABLE and self.pygame_available:
            self.is_initialized = True
        else:
            print("Error: gTTS o pygame no disponibles")

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto para hacerlo más fluido
        Remueve/reemplaza puntuación que causa pausas largas
        """
        # Remover puntos suspensivos excesivos
        text = re.sub(r'\.{3,}', ',', text)

        # Reemplazar múltiples puntos/comas con uno solo
        text = re.sub(r'[\.]{2,}', '.', text)
        text = re.sub(r'[,]{2,}', ',', text)

        # Reemplazar punto y coma con coma (pausa más corta)
        text = text.replace(';', ',')

        # Remover paréntesis y corchetes (causan pausas)
        text = re.sub(r'[\(\)\[\]]', '', text)

        # Reducir múltiples espacios
        text = re.sub(r'\s+', ' ', text)

        # Limpiar espacios alrededor de puntuación
        text = re.sub(r'\s*([.,!?])\s*', r'\1 ', text)

        return text.strip()

    def speak(self, text: str, blocking: bool = False) -> bool:
        """
        Convierte texto a voz y lo reproduce

        Args:
            text: Texto a convertir en voz
            blocking: Si True, espera a que termine de hablar

        Returns:
            True si se reproduce correctamente, False si hay error
        """
        if not self.is_initialized or not text:
            return False

        # Verificar si es un texto nuevo (evitar duplicados)
        if text == self.last_text:
            print(f"TTS: Texto duplicado, ignorando...")
            return True

        # Actualizar último texto
        self.last_text = text

        # Preprocesar texto para lectura más fluida
        processed_text = self._preprocess_text(text)
        print(f"TTS: Generando audio para: {processed_text[:50]}...")

        try:
            if blocking:
                self._speak_gtts_blocking(processed_text)
            else:
                # Reproducir en thread separado
                thread = threading.Thread(target=self._speak_gtts_blocking, args=(processed_text,))
                thread.daemon = True
                thread.start()

            return True
        except Exception as e:
            print(f"Error al reproducir TTS: {e}")
            return False

    def _speak_gtts_blocking(self, text: str):
        """Reproduce texto con gTTS (bloqueante)"""
        temp_path = None
        try:
            # Crear archivo temporal único
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            timestamp = str(int(time_module.time() * 1000))
            temp_path = os.path.join(
                tempfile.gettempdir(),
                f"tts_{timestamp}_{text_hash}.mp3"
            )

            # Obtener código de idioma
            lang_code = self.lang_codes.get(self.language, 'es')

            # Generar audio con gTTS
            # slow=False hace la lectura más fluida y rápida
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(temp_path)

            # Detener cualquier audio previo
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.time.wait(100)  # Pequeña pausa

            # Reproducir con pygame
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()

            # Esperar a que termine
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Limpiar archivo temporal
            pygame.time.wait(100)  # Esperar antes de eliminar
            try:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)
            except:
                pass

        except Exception as e:
            print(f"Error reproduciendo gTTS: {e}")
            # Intentar limpiar en caso de error
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except:
                    pass

    def stop(self):
        """Detiene la reproducción actual"""
        try:
            if self.pygame_available:
                pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error al detener TTS: {e}")

    def change_voice(self, language: str, voice_gender: str):
        """
        Cambia el idioma y género de voz

        Args:
            language: Nuevo idioma
            voice_gender: Nuevo género (solo informativo para gTTS)
        """
        self.language = language
        self.voice_gender = voice_gender


# Función helper para crear instancia global
_improved_tts_instance: Optional[ImprovedTTSService] = None


def get_improved_tts_service(language: str = "Español", voice_gender: str = "Femenina") -> Optional[ImprovedTTSService]:
    """
    Obtiene o crea instancia del servicio TTS mejorado

    Args:
        language: Idioma
        voice_gender: Género de voz

    Returns:
        Instancia de ImprovedTTSService o None si hay error
    """
    global _improved_tts_instance

    if _improved_tts_instance is None:
        _improved_tts_instance = ImprovedTTSService(language, voice_gender)
    else:
        # Actualizar configuración si cambió
        if _improved_tts_instance.language != language or _improved_tts_instance.voice_gender != voice_gender:
            _improved_tts_instance.change_voice(language, voice_gender)

    return _improved_tts_instance if _improved_tts_instance.is_initialized else None
