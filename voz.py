import json
import os

import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

_voz = pyttsx3.init()
_rec = sr.Recognizer()
_rec.operation_timeout = 5


_modelo = None
_caminho = os.getenv("VOSK_MODEL_PATH")
if _caminho and os.path.isdir(_caminho):
    try:
        from vosk import Model, SetLogLevel

        SetLogLevel(-1)
        _modelo = Model(_caminho)
        print("Voz offline (Vosk) carregada como reserva")
    except Exception as erro:
        print("Não consegui carregar o Vosk:", erro)

_avisou_offline = False


def falar(texto):
    print("Jarvis:", texto)
    _voz.say(texto)
    _voz.runAndWait()


def _reconhecer_offline(audio):
    from vosk import KaldiRecognizer

    reconhecedor = KaldiRecognizer(_modelo, 16000)

    dados = audio.get_raw_data(convert_rate=16000, convert_width=2)
    reconhecedor.AcceptWaveform(dados)
    return json.loads(reconhecedor.FinalResult()).get("text", "")


def ouvir():
    global _avisou_offline

    with sr.Microphone() as mic:
        _rec.adjust_for_ambient_noise(mic, duration=0.5)
        try:
            audio = _rec.listen(mic, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""

    try:
        texto = _rec.recognize_google(audio, language="pt-BR")
        _avisou_offline = False
    except sr.UnknownValueError:
        return ""
    except (sr.RequestError, OSError):

        if not _modelo:
            return ""
        if not _avisou_offline:
            print("Sem internet: usando a voz offline")
            _avisou_offline = True
        texto = _reconhecer_offline(audio)

    texto = texto.lower()
    if texto:
        print("Você:", texto)
    return texto
