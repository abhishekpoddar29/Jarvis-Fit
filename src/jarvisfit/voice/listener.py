import time
import speech_recognition as sr
from typing import Optional


class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recognizer.pause_threshold = 1.0
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

    def listen_once(self, timeout: int = 5, phrase_limit: int = 10) -> Optional[str]:
        with self.microphone as source:
            print("[VoiceListener] Waiting for speech...")

            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )

                print("[VoiceListener] Audio captured")

                text = self.recognizer.recognize_google(audio)

                print(f"[VoiceListener] Recognized: {text}")

                return text.strip().lower()

            except sr.WaitTimeoutError:
                print("[VoiceListener] Timeout waiting for speech")
                return None

            except sr.UnknownValueError:
                print("[VoiceListener] Could not understand audio")
                return None

            except sr.RequestError as e:
                print(f"[VoiceListener] Google STT error: {e}")
                return None

    def listen_for_wake_word(
        self,
        wake_phrases: list,
        shutdown_phrases: list,
        on_wake,
        on_shutdown,
        stop_flag,
        session_active_flag=None,
    ):
        print("[VoiceListener] Listening for wake word...")
        while not stop_flag.is_set():
            # ── Pause wake detection during active session ──
            if session_active_flag and session_active_flag.is_set():
                time.sleep(0.3)
                continue

            utterance = self.listen_once(timeout=3, phrase_limit=5)
            if utterance is None:
                continue
            if any(phrase in utterance for phrase in wake_phrases):
                print(f"[VoiceListener] Wake word detected: {utterance}")
                on_wake()
            elif any(phrase in utterance for phrase in shutdown_phrases):
                print(f"[VoiceListener] Shutdown word detected: {utterance}")
                on_shutdown()