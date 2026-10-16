import os
import subprocess
import webbrowser
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

BRAVE = os.getenv("BRAVE_PATH")
APPS = {
    "vscode": os.getenv("VSCODE_PATH"),
    "pycharm": os.getenv("PYCHARM_PATH"),
    "intellij": os.getenv("INTELLIJ_PATH"),
}


def abrir_site(url):
    if BRAVE:
        subprocess.Popen([BRAVE, url])
    else:
        webbrowser.open(url)


def abrir_app(nome):
    caminho = APPS.get(nome)
    if caminho:
        subprocess.Popen([caminho])
        return True
    return False


def buscar_youtube(termo):
    abrir_site("https://www.youtube.com/results?search_query=" + quote_plus(termo))
