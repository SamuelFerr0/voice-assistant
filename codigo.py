import pyautogui
import pyperclip

from ia import gerar_codigo
from voz import falar, ouvir


def criar_codigo():
    falar("Descreva o que você quer criar")
    pedido = ouvir()
    if not pedido:
        falar("Não ouvi nada")
        return
    falar("Gerando o código. Clique onde quer colar.")
    codigo = gerar_codigo(pedido)
    if not codigo:
        falar("Não consegui gerar")
        return
    pyperclip.copy(codigo)
    pyautogui.sleep(3)
    pyautogui.hotkey("ctrl", "v")
    falar("Código colado")
