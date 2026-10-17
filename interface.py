"""Janela animada do Jarvis.

A esfera muda de cor e de movimento conforme o que ele está fazendo:
esperando (azul), ouvindo (verde), pensando (amarelo) e falando (ciano).
Embaixo aparece o que você disse e o que ele respondeu.

O resto do código só chama definir_estado() e registrar(). Se a janela não
estiver aberta, essas funções não fazem nada.
"""

import math
import queue
import random
import threading
import time

FUNDO = "#0b0f1a"
CORES = {
    "esperando": "#3b82f6",
    "ouvindo": "#22c55e",
    "pensando": "#eab308",
    "falando": "#06b6d4",
}
LEGENDAS = {
    "esperando": 'Diga "Jarvis"',
    "ouvindo": "Ouvindo...",
    "pensando": "Pensando...",
    "falando": "Falando...",
}

_fila = queue.Queue()
_ativa = False


# Estas três funções podem ser chamadas de qualquer thread.
def definir_estado(nome):
    if _ativa:
        _fila.put(("estado", nome))


def registrar(quem, texto):
    if _ativa:
        _fila.put(("log", (quem, texto)))


def fechar():
    if _ativa:
        _fila.put(("fechar", None))


def misturar(a, b, f):
    """Mistura duas cores em hexadecimal: f=0 devolve a, f=1 devolve b."""
    ra, ga, ba = int(a[1:3], 16), int(a[3:5], 16), int(a[5:7], 16)
    rb, gb, bb = int(b[1:3], 16), int(b[3:5], 16), int(b[5:7], 16)
    r = round(ra + (rb - ra) * f)
    g = round(ga + (gb - ga) * f)
    bl = round(ba + (bb - ba) * f)
    return f"#{r:02x}{g:02x}{bl:02x}"


def nivel_alvo(estado, t):
    """Quanto a esfera deve 'inchar' (de 0 a 1) em cada estado."""
    if estado == "ouvindo":
        return 0.45 + 0.35 * math.sin(t * 5)
    if estado == "pensando":
        return 0.25 + 0.05 * math.sin(t * 3)
    if estado == "falando":
        voz = abs(math.sin(t * 7.3)) * (0.5 + 0.5 * abs(math.sin(t * 3.1 + 1)))
        return 0.2 + 0.6 * voz + random.uniform(0, 0.2)
    return 0.15 + 0.15 * math.sin(t * 1.6)  # esperando: respiração lenta


class Janela:
    def __init__(self):
        import tkinter as tk

        self.raiz = tk.Tk()
        self.raiz.title("Jarvis")
        self.raiz.configure(bg=FUNDO)
        self.raiz.geometry("440x620")
        self.raiz.minsize(360, 520)

        self.canvas = tk.Canvas(self.raiz, width=440, height=380, bg=FUNDO, highlightthickness=0)
        self.canvas.pack(fill="x")

        self.legenda = tk.Label(
            self.raiz, text=LEGENDAS["esperando"], bg=FUNDO,
            fg=CORES["esperando"], font=("Segoe UI", 14, "bold"),
        )
        self.legenda.pack(pady=(0, 8))

        self.texto = tk.Text(
            self.raiz, height=8, bg="#111827", fg="#e5e7eb", relief="flat",
            wrap="word", font=("Consolas", 10), padx=10, pady=8, state="disabled",
            highlightthickness=0,
        )
        self.texto.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.texto.tag_configure("voce", foreground="#9ca3af")
        self.texto.tag_configure("jarvis", foreground="#67e8f9")

        self.estado = "esperando"
        self.nivel = 0.0
        self.inicio = time.time()
        self.fechando = False
        self.raiz.protocol("WM_DELETE_WINDOW", self._fechar)
        self.raiz.after(33, self._tick)

    def _fechar(self):
        self.fechando = True
        self.raiz.destroy()

    def _tick(self):
        if self.fechando:
            return
        self._processar_fila()
        if self.fechando:
            return
        self._desenhar(time.time() - self.inicio)
        self.raiz.after(33, self._tick)  # cerca de 30 quadros por segundo

    def _processar_fila(self):
        while True:
            try:
                tipo, dado = _fila.get_nowait()
            except queue.Empty:
                return
            if tipo == "estado":
                self.estado = dado
                cor = CORES.get(dado, CORES["esperando"])
                self.legenda.configure(text=LEGENDAS.get(dado, ""), fg=cor)
            elif tipo == "log":
                self._escrever(*dado)
            elif tipo == "fechar":
                self._fechar()
                return

    def _escrever(self, quem, texto):
        self.texto.configure(state="normal")
        etiqueta = "jarvis" if quem == "Jarvis" else "voce"
        self.texto.insert("end", f"{quem}: {texto}\n", etiqueta)
        linhas = int(self.texto.index("end-1c").split(".")[0])
        if linhas > 200:
            self.texto.delete("1.0", f"{linhas - 200}.0")
        self.texto.see("end")
        self.texto.configure(state="disabled")

    def _desenhar(self, t):
        c = self.canvas
        c.delete("all")
        largura, altura = c.winfo_width(), c.winfo_height()
        cx, cy = largura / 2, altura / 2
        base = min(largura, altura) * 0.17
        cor = CORES.get(self.estado, CORES["esperando"])

        # Suaviza o movimento para a esfera não "tremer"
        self.nivel += (nivel_alvo(self.estado, t) - self.nivel) * 0.25

        # Anéis de brilho, do maior para o menor
        for i in range(4, 0, -1):
            raio = base + i * 15 + self.nivel * 12 * i
            c.create_oval(
                cx - raio, cy - raio, cx + raio, cy + raio,
                fill=misturar(FUNDO, cor, 0.10 * (5 - i)), outline="",
            )

        # Esfera central e um reflexo para dar volume
        nucleo = base + self.nivel * 10
        c.create_oval(cx - nucleo, cy - nucleo, cx + nucleo, cy + nucleo, fill=cor, outline="")
        rx, ry, rr = cx - nucleo * 0.3, cy - nucleo * 0.3, nucleo * 0.4
        c.create_oval(rx - rr, ry - rr, rx + rr, ry + rr,
                      fill=misturar(cor, "#ffffff", 0.45), outline="")

        # Pensando: dois arcos girando em volta
        if self.estado == "pensando":
            r = base + 40
            angulo = (t * 240) % 360
            for deslocamento in (0, 180):
                c.create_arc(
                    cx - r, cy - r, cx + r, cy + r,
                    start=angulo + deslocamento, extent=80,
                    style="arc", outline=cor, width=5,
                )


def iniciar(funcao):
    """Abre a janela e roda `funcao` (o Jarvis) numa thread.

    A janela fecha quando a função termina. Fechar a janela encerra o Jarvis.
    Levanta ImportError se o tkinter não estiver instalado.
    """
    global _ativa
    janela = Janela()
    _ativa = True

    def rodar():
        try:
            funcao()
        finally:
            fechar()

    threading.Thread(target=rodar, daemon=True).start()
    janela.raiz.mainloop()
    _ativa = False
