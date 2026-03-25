"""Voice input/output module for Deepan AI."""
import pyttsx3
import speech_recognition as sr
import threading

_speak_lock = threading.Lock()


def speak(text):
    """Speak text using pyttsx3 in a background thread (non-blocking)."""
    clean_text = ''.join(c for c in text if c.isascii() or c.isspace())
    if not clean_text.strip():
        return

    def _run():
        with _speak_lock:
            try:
                eng = pyttsx3.init()
                eng.setProperty('rate', 170)
                voices = eng.getProperty('voices')
                if len(voices) > 1:
                    eng.setProperty('voice', voices[1].id)
                eng.say(clean_text)
                eng.runAndWait()
                eng.stop()
            except Exception as e:
                print(f"[TTS] Error: {e}")

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()


def listen():
    """Listen for voice input via microphone and return recognized text."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"[Voice] Speech API error: {e}")
        return ""
    except sr.WaitTimeoutError:
        return ""
    except Exception as e:
        print(f"[Voice] Error: {e}")
        return ""
