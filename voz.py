import json
import os

import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

from interface import definir_estado, registrar

load_dotenv()

_voz = pyttsx3.init()
_rec = sr.Recognizer()
_rec.operation_timeout = 5  # se a internet estiver muito lenta, desiste do Google em 5s


def _escolher_voz_portugues():
    """Usa uma voz em português do Windows, se tiver alguma instalada."""
    try:
        for v in _voz.getProperty("voices"):
            texto = (v.id + " " + (v.name or "")).lower().replace("-", "").replace("_", "")
            if any(p in texto for p in ("ptbr", "portuguese", "brazil", "brasil")):
                _voz.setProperty("voice", v.id)
                print("Voz do Jarvis:", v.name)
                return
        print("Nenhuma voz em português encontrada: usando a voz padrão do Windows")
    except Exception as erro:
        print("Não consegui escolher a voz:", erro)


_escolher_voz_portugues()

# Voz offline (Vosk): reserva para quando estiver sem internet.
# Só liga se VOSK_MODEL_PATH (no .env) apontar para uma pasta de modelo.
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
    registrar("Jarvis", texto)
    definir_estado("falando")
    _voz.say(texto)
    _voz.runAndWait()
    definir_estado("esperando")


def _reconhecer_offline(audio):
    from vosk import KaldiRecognizer

    reconhecedor = KaldiRecognizer(_modelo, 16000)
    # Reaproveita o mesmo áudio que o microfone já capturou
    dados = audio.get_raw_data(convert_rate=16000, convert_width=2)
    reconhecedor.AcceptWaveform(dados)
    return json.loads(reconhecedor.FinalResult()).get("text", "")


def ouvir(estado="ouvindo"):
    """Escuta o microfone e devolve o texto. Use estado="esperando" para a palavra de ativação."""
    global _avisou_offline

    esperando = estado == "esperando"
    definir_estado(estado)

    with sr.Microphone() as mic:
        _rec.adjust_for_ambient_noise(mic, duration=0.5)
        try:
            audio = _rec.listen(mic, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""

    if not esperando:
        definir_estado("pensando")

    try:
        texto = _rec.recognize_google(audio, language="pt-BR")
        _avisou_offline = False
    except sr.UnknownValueError:
        return ""  # o Google respondeu, mas não entendeu a fala
    except (sr.RequestError, OSError):
        # Sem internet (ou internet lenta demais): tenta o modo offline
        if not _modelo:
            return ""
        if not _avisou_offline:
            print("Sem internet: usando a voz offline")
            _avisou_offline = True
        texto = _reconhecer_offline(audio)

    texto = texto.lower()
    if texto:
        print("Você:", texto)
        if not esperando:
            registrar("Você", texto)
    return texto
