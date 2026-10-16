import json
import os
import traceback

import pyautogui

import ia
from apps import abrir_app, abrir_site, buscar_youtube
from codigo import criar_codigo
from ditar import ditar
from utilidades import data_atual, hora_atual
from voz import falar, ouvir

PASTA = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(PASTA, "comandos.json"), encoding="utf-8") as arquivo:
    CONFIG = json.load(arquivo)
ATIVACAO = CONFIG["ativacao"]
COMANDOS = CONFIG["comandos"]


def musica(comando):
    termo = comando
    for palavra in ["tocar", "música", "musica", "filme"]:
        termo = termo.replace(palavra, "")
    termo = termo.strip()
    if not termo:
        falar("O que você quer assistir ou ouvir?")
        termo = ouvir()
    if termo:
        falar("Procurando " + termo)
        buscar_youtube(termo)



FUNCOES = {
    "hora": lambda c: falar(hora_atual()),
    "data": lambda c: falar(data_atual()),
    "ditar": lambda c: ditar(),
    "criar_codigo": lambda c: criar_codigo(),
    "claude": lambda c: ia.trocar_agente("claude"),
    "gemini": lambda c: ia.trocar_agente("gemini"),
    "esquecer": lambda c: ia.esquecer(),
    "musica": musica,
}


def rodar(cmd, comando):
    tipo = cmd["tipo"]
    valor = cmd["valor"]

    if cmd.get("fala"):
        falar(cmd["fala"])

    if tipo == "site":
        abrir_site(valor)
    elif tipo == "app":
        if not abrir_app(valor):
            falar("Não achei o caminho desse aplicativo no arquivo ponto env")
    elif tipo == "tecla":
        pyautogui.press(valor, presses=cmd.get("repetir", 1))
    elif tipo == "funcao":
        if valor == "sair":
            return False
        FUNCOES[valor](comando)
    return True


def executar(comando):
    for cmd in COMANDOS:
        if any(palavra in comando for palavra in cmd["palavras"]):
            return rodar(cmd, comando)


    if comando:
        falar(ia.perguntar(comando))
    return True


def principal():
    falar("Jarvis iniciado")
    rodando = True
    while rodando:
        fala = ouvir()
        if any(nome in fala for nome in ATIVACAO):
            falar("Pois não?")
            rodando = executar(ouvir())


if __name__ == "__main__":
    try:
        principal()
    except Exception:
        with open(os.path.join(PASTA, "erro.log"), "w", encoding="utf-8") as arquivo:
            arquivo.write(traceback.format_exc())
