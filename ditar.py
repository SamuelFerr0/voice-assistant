import pyautogui
import pyperclip

from voz import falar, ouvir

SIMBOLOS = {
    "abre parênteses": "(",
    "fecha parênteses": ")",
    "abre chaves": "{",
    "fecha chaves": "}",
    "abre colchetes": "[",
    "fecha colchetes": "]",
    "ponto e vírgula": ";",
    "dois pontos": ":",
    "nova linha": "\n",
}


def ditar():
    falar("Clique onde quer escrever. Diga parar para terminar.")
    while True:
        texto = ouvir()
        if not texto:
            continue
        if "parar" in texto:
            falar("Ditado encerrado")
            return
        for fala, simbolo in SIMBOLOS.items():
            texto = texto.replace(fala, simbolo)
        pyperclip.copy(texto + " ")
        pyautogui.hotkey("ctrl", "v")
