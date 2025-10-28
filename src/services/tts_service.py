"""
Servicio de Text-to-Speech usando Edge-TTS (Microsoft Edge)
Voces naturales de alta calidad, completamente gratis, con verdaderas voces masculinas/femeninas
"""
import os
import tempfile
import threading
import hashlib
import time
from typing import Optional
import queue
import re
import asyncio

# Importar Edge-TTS y pygame
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("ERROR: edge-tts no esta instalado. Ejecuta: pip install edge-tts pygame")

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("ERROR: pygame no esta instalado. Ejecuta: pip install edge-tts pygame")


class TTSService:
    """Servicio TTS con Edge-TTS (Microsoft) para voces naturales y efusivas"""

    def __init__(self, language: str = "Español", voice_gender: str = "Femenina"):
        """
        Inicializa el servicio TTS con Edge-TTS

        Args:
            language: Idioma (Español, English, Français)
            voice_gender: Género de voz (Femenina, Masculina)
        """
        self.language = language
        self.voice_gender = voice_gender
        self.is_initialized = False

        # Mapeo de voces Edge-TTS (VOCES REALES de Microsoft)
        self.voice_map = {
            ('Español', 'Femenina'): 'es-MX-DaliaNeural',      # Mexicana, muy expresiva
            ('Español', 'Masculina'): 'es-ES-AlvaroNeural',    # Español, voz grave y clara
            ('English', 'Femenina'): 'en-US-AriaNeural',       # Estadounidense, natural
            ('English', 'Masculina'): 'en-US-GuyNeural',       # Estadounidense, profesional
            ('Français', 'Femenina'): 'fr-FR-DeniseNeural',    # Francesa, elegante
            ('Français', 'Masculina'): 'fr-FR-HenriNeural',    # Francés, profundo
        }

        # Obtener voz seleccionada
        self.voice_name = self.voice_map.get((language, voice_gender), 'es-MX-DaliaNeural')

        # Cola de mensajes
        self.message_queue = queue.Queue()
        self.is_running = False
        self.worker_thread = None

        # Cache de archivos de audio
        self.cache_dir = os.path.join(tempfile.gettempdir(), 'tts_cache_edge')
        os.makedirs(self.cache_dir, exist_ok=True)

        # Inicializar pygame mixer
        if PYGAME_AVAILABLE:
            try:
                # Frecuencia estándar para buena calidad
                pygame.mixer.init(frequency=24000, size=-16, channels=2, buffer=512)
                pygame.mixer.music.set_volume(1.0)
            except Exception as e:
                print(f"Error inicializando pygame mixer: {e}")
                return

        if EDGE_TTS_AVAILABLE and PYGAME_AVAILABLE:
            self.is_initialized = True
            self._start_worker()
            print(f"[OK] TTS inicializado con Edge-TTS (Microsoft)")
            print(f"[VOZ] Voz seleccionada: {self.voice_name} ({voice_gender})")
        else:
            print("[ERROR] TTS no disponible - Instala: pip install edge-tts pygame")

    def _start_worker(self):
        """Inicia el thread worker que procesa la cola de TTS"""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def _worker_loop(self):
        """Loop principal que procesa mensajes de la cola"""
        while self.is_running:
            try:
                # Obtener mensaje de la cola (timeout de 0.5s)
                text = self.message_queue.get(timeout=0.5)

                if text and text.strip():
                    self._speak_edge_tts(text.strip())

                self.message_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error procesando TTS: {e}")

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto para hacerlo más natural

        Args:
            text: Texto original

        Returns:
            Texto procesado
        """
        # 1. Remover tags HTML/XML como <res>, <div>, etc.
        text = re.sub(r'<[^>]+>', '', text)

        # 2. Remover tags de modelos de IA: [/OST], [/INST], [B_INST], etc.
        # Esto cubre tags comunes de modelos LLM
        text = re.sub(r'\[/?[A-Z_]+\]', '', text)
        text = re.sub(r'\[/?[a-z]+\]', '', text)

        # 3. Remover TODOS los emojis usando rangos Unicode completos
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # símbolos y pictogramas
            "\U0001F680-\U0001F6FF"  # transporte y símbolos de mapa
            "\U0001F1E0-\U0001F1FF"  # banderas (iOS)
            "\U00002702-\U000027B0"  # dingbats
            "\U000024C2-\U0001F251"  # símbolos varios
            "\U0001F900-\U0001F9FF"  # símbolos suplementarios
            "\U0001FA00-\U0001FA6F"  # símbolos extendidos-A
            "\U00002600-\U000026FF"  # símbolos misceláneos
            "\U00002700-\U000027BF"  # dingbats
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub('', text)

        # 4. Remover texto entre paréntesis (incluyendo los paréntesis)
        text = re.sub(r'\([^)]*\)', '', text)

        # 5. Remover marcadores de formato como asteriscos dobles
        text = re.sub(r'\*\*', '', text)

        # 6. Limpiar múltiples espacios
        text = re.sub(r'\s+', ' ', text)

        # 7. Limpiar puntuación excesiva para mejor fluidez
        text = re.sub(r'\.{3,}', '.', text)
        text = re.sub(r'!{2,}', '!', text)
        text = re.sub(r'\?{2,}', '?', text)

        # 8. Limpiar espacios antes de puntuación
        text = re.sub(r'\s+([.,!?])', r'\1', text)

        return text.strip()

    def _get_cache_key(self, text: str) -> str:
        """Genera clave única para cachear audio"""
        cache_string = f"{text}_{self.voice_name}"
        return hashlib.md5(cache_string.encode()).hexdigest()

    def _speak_edge_tts(self, text: str):
        """
        Genera y reproduce audio con Edge-TTS

        Args:
            text: Texto a reproducir
        """
        audio_path = None
        try:
            # Preprocesar texto
            processed_text = self._preprocess_text(text)

            if not processed_text:
                return

            print(f"[TTS] Reproduciendo '{processed_text[:60]}...'")

            # Verificar cache
            cache_key = self._get_cache_key(processed_text)
            audio_path = os.path.join(self.cache_dir, f"{cache_key}.mp3")

            # Generar audio si no existe en cache
            if not os.path.exists(audio_path):
                print(f"[TTS] Generando audio con {self.voice_name}...")

                # Crear nuevo event loop para este thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                # Generar audio con Edge-TTS de forma asíncrona
                communicate = edge_tts.Communicate(processed_text, self.voice_name)
                loop.run_until_complete(communicate.save(audio_path))

                # Cerrar loop
                loop.close()

                print(f"[OK] Audio generado y guardado en cache")
            else:
                print(f"[CACHE] Audio cargado desde cache")

            # Detener cualquier reproducción previa
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                time.sleep(0.1)

            # Cargar y reproducir
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            # Esperar a que termine la reproducción
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            print(f"[OK] Reproduccion completada")

        except Exception as e:
            print(f"[ERROR] Error en TTS: {e}")
            import traceback
            traceback.print_exc()

    def speak(self, text: str, blocking: bool = False) -> bool:
        """
        Convierte texto a voz y lo reproduce

        Args:
            text: Texto a convertir en voz
            blocking: Si True, espera a que termine de hablar

        Returns:
            True si se encola correctamente, False si hay error
        """
        if not self.is_initialized:
            print("[WARN] TTS no inicializado")
            return False

        if not text or not text.strip():
            return False

        try:
            # Encolar mensaje
            self.message_queue.put(text.strip())
            print(f"[TTS] Mensaje encolado ({self.message_queue.qsize()} en cola)")

            # Si es bloqueante, esperar
            if blocking:
                self.message_queue.join()

            return True

        except Exception as e:
            print(f"[ERROR] Error al encolar TTS: {e}")
            return False

    def stop(self):
        """Detiene la reproducción actual y limpia la cola"""
        try:
            # Detener reproducción
            if PYGAME_AVAILABLE:
                pygame.mixer.music.stop()

            # Limpiar cola
            while not self.message_queue.empty():
                try:
                    self.message_queue.get_nowait()
                    self.message_queue.task_done()
                except queue.Empty:
                    break

            print("[STOP] TTS detenido y cola limpiada")

        except Exception as e:
            print(f"Error al detener TTS: {e}")

    def change_voice(self, language: str, voice_gender: str = "Femenina"):
        """
        Cambia el idioma y género de voz

        Args:
            language: Nuevo idioma
            voice_gender: Género de voz
        """
        # Actualizar configuración
        self.language = language
        self.voice_gender = voice_gender

        # Actualizar voz
        old_voice = self.voice_name
        self.voice_name = self.voice_map.get((language, voice_gender), 'es-MX-DaliaNeural')

        if old_voice != self.voice_name:
            # Limpiar cache para regenerar con nueva voz
            self.clear_cache()
            print(f"[CHANGE] Voz cambiada: {self.voice_name} ({voice_gender})")

    def clear_cache(self):
        """Limpia el cache de archivos de audio"""
        try:
            import shutil
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)
                os.makedirs(self.cache_dir, exist_ok=True)
            print("[CLEAN] Cache de audio limpiado")
        except Exception as e:
            print(f"Error limpiando cache: {e}")

    def shutdown(self):
        """Detiene el worker thread y cierra el servicio"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=2)
        if PYGAME_AVAILABLE:
            pygame.mixer.quit()
        print("[SHUTDOWN] TTS cerrado")


# Instancia global
_tts_instance: Optional[TTSService] = None


def get_tts_service(language: str = "Español", voice_gender: str = "Femenina") -> Optional[TTSService]:
    """
    Obtiene o crea instancia del servicio TTS

    Args:
        language: Idioma
        voice_gender: Género de voz

    Returns:
        Instancia de TTSService o None si hay error
    """
    global _tts_instance

    # Si no existe, crear nueva instancia
    if _tts_instance is None:
        _tts_instance = TTSService(language, voice_gender)
        time.sleep(0.3)
        return _tts_instance if _tts_instance.is_initialized else None

    # Si cambió el género o idioma, recrear instancia
    if _tts_instance.voice_gender != voice_gender or _tts_instance.language != language:
        print(f"[CHANGE] Recreando TTS para cambiar voz: {language} ({voice_gender})")
        # Cerrar instancia anterior
        _tts_instance.shutdown()
        # Crear nueva instancia
        _tts_instance = TTSService(language, voice_gender)
        time.sleep(0.3)

    return _tts_instance if _tts_instance.is_initialized else None
