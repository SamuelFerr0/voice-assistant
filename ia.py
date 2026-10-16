import os

import anthropic
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODELO_CLAUDE = "claude-haiku-5-5"
MODELO_GEMINI = "gemini-2.5-flash"


MAX_MENSAGENS = 20

agente_atual = "claude"
historico = []
_clientes = {}


def _claude():
    if "claude" not in _clientes:
        _clientes["claude"] = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _clientes["claude"]


def _gemini():
    if "gemini" not in _clientes:
        _clientes["gemini"] = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _clientes["gemini"]


def trocar_agente(nome):
    global agente_atual
    agente_atual = nome


def esquecer():
    historico.clear()


def _chamar(instrucao, mensagens):
    if agente_atual == "claude":
        resposta = _claude().messages.create(
            model=MODELO_CLAUDE,
            max_tokens=1500,
            system=instrucao,
            messages=mensagens,
        )
        return resposta.content[0].text

    conteudo = [
        {
            "role": "model" if m["role"] == "assistant" else "user",
            "parts": [{"text": m["content"]}],
        }
        for m in mensagens
    ]
    resposta = _gemini().models.generate_content(
        model=MODELO_GEMINI,
        contents=conteudo,
        config={"system_instruction": instrucao},
    )
    return resposta.text


def perguntar(texto):
    mensagens = historico + [{"role": "user", "content": texto}]
    try:
        resposta = _chamar("Responda em português, em no máximo 3 frases.", mensagens)
    except Exception as erro:
        print("Erro IA:", erro)
        return "Não consegui falar com a IA."


    historico.append({"role": "user", "content": texto})
    historico.append({"role": "assistant", "content": resposta})
    del historico[:-MAX_MENSAGENS]
    return resposta


def gerar_codigo(pedido):
    try:
        codigo = _chamar(
            "Você escreve código. Responda SOMENTE com o código, "
            "sem explicação e sem markdown. Use comentários curtos em português.",
            [{"role": "user", "content": pedido}],
        )
        return limpar(codigo)
    except Exception as erro:
        print("Erro IA:", erro)
        return ""


def limpar(codigo):
    linhas = [l for l in codigo.strip().split("\n") if not l.strip().startswith("```")]
    return "\n".join(linhas)
