"""
services/voice_service.py
Speech recognition helpers for voice interview mode.
"""

import speech_recognition as sr


def recognize_speech(timeout: int = 10, phrase_time_limit: int = 30) -> tuple[bool, str]:
    """
    Listen via microphone and return (success, text).
    Returns (False, error_message) on failure.
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )
        text = recognizer.recognize_google(audio)
        return True, text
    except sr.WaitTimeoutError:
        return False, "No speech detected. Please speak within the time limit."
    except sr.UnknownValueError:
        return False, "Could not understand audio. Please speak clearly."
    except sr.RequestError as e:
        return False, f"Speech recognition service error: {e}"
    except OSError:
        return False, "No microphone found. Please connect a microphone and try again."


def list_microphones() -> list[str]:
    """Return available microphone names."""
    try:
        return sr.Microphone.list_microphone_names()
    except Exception:
        return []
