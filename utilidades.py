from datetime import datetime

DIAS = [
    "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sábado", "domingo",
]
MESES = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]


def hora_atual():
    agora = datetime.now()
    h, m = agora.hour, agora.minute
    verbo = "É" if h == 1 else "São"
    unidade = "hora" if h == 1 else "horas"
    texto = f"{verbo} {h} {unidade}"
    if m == 0:
        return texto + " em ponto"
    return texto + f" e {m} minuto" + ("" if m == 1 else "s")


def data_atual():
    agora = datetime.now()
    dia_semana = DIAS[agora.weekday()]
    mes = MESES[agora.month - 1]
    return f"Hoje é {dia_semana}, {agora.day} de {mes} de {agora.year}"
