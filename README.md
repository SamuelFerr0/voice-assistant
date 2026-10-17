# Jarvis: assistente pessoal por voz em Python

Assistente de voz que roda no computador, em português do Brasil. Você diz "Jarvis", fala um comando e ele abre programas e sites, toca músicas, dita texto, gera código e responde perguntas usando IA (Claude e Gemini).

## O que ele faz

- Ativa pela palavra **"Jarvis"**
- **Entende frases naturais**: a IA interpreta o que você fala e escolhe o comando certo, sem precisar decorar palavras exatas
- Abre o navegador (Brave) e sites favoritos
- Abre IDEs: Visual Studio Code, PyCharm e IntelliJ
- Procura músicas e filmes no YouTube
- Controla volume, pausa e tela cheia
- Diz a hora e a data
- **Dita** o que você fala onde o cursor estiver
- **Cria código por voz**: você descreve a função e a IA escreve no editor
- Responde perguntas com **Claude** ou **Gemini** (troca por voz) e lembra as últimas mensagens
- Reconhecimento de voz com o Google e **reserva offline** (Vosk) quando estiver sem internet
- **Janela animada** que mostra o que ele está fazendo: esperando, ouvindo, pensando ou falando

## Tecnologias

Python, tkinter, SpeechRecognition, pyttsx3, PyAutoGUI, Vosk, API do Claude (Anthropic), API do Gemini (Google), python-dotenv.

## Como instalar

Pensado para Windows.

```
git clone https://github.com/SamuelFerr0/jarvis-assistente.git
cd jarvis-assistente
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Se o `pyaudio` falhar na instalação: `pip install pipwin` e depois `pipwin install pyaudio`.

## Configuração

Copie o arquivo de exemplo e preencha com os seus dados:

```
copy .env.example .env
```

| Variável | Para que serve |
|---|---|
| `GEMINI_API_KEY` | Chave do Gemini (gratuita em aistudio.google.com/apikey) |
| `ANTHROPIC_API_KEY` | Chave do Claude (paga por uso, em console.anthropic.com) |
| `BRAVE_PATH` | Caminho do `brave.exe` |
| `VSCODE_PATH`, `PYCHARM_PATH`, `INTELLIJ_PATH` | Caminhos dos executáveis das IDEs |
| `VOSK_MODEL_PATH` | (opcional) Pasta do modelo de voz offline |

O arquivo `.env` fica só no seu computador e está no `.gitignore`. Nenhum caminho pessoal ou chave vai para o repositório.

## Como usar

```
python jarvis.py
```

Diga "Jarvis", espere o "Pois não?" e fale o comando.

| Comando | O que faz |
|---|---|
| abrir navegador / github / linkedin / gmail / netflix / spotify / shopify | Abre o site |
| abrir vs code / pycharm / intellij | Abre a IDE |
| tocar música (nome) / filme (nome) | Procura no YouTube |
| pausar, continuar, aumentar volume, diminuir volume, silenciar, tela cheia | Controla a mídia |
| que horas são / que dia é hoje | Fala a hora ou a data |
| ditar | Escreve o que você falar (diga "parar" para terminar) |
| criar código | Descreva a função e o código é colado no editor |
| usar claude / usar gemini | Troca a IA |
| esquecer conversa | Limpa a memória da IA |
| qualquer outra frase | Vira uma pergunta para a IA |
| sair | Encerra o Jarvis |

Os comandos ficam no arquivo `comandos.json`. Para adicionar um site novo, copie uma linha do tipo `"site"` e troque a `descricao` (é o que a IA lê para escolher o comando), as `palavras` (reserva sem internet) e o endereço.

## Como ele entende o que você fala

Os comandos da tabela acima são só exemplos. Com a IA ligada, você fala do seu jeito, e ela escolhe o comando certo na lista do `comandos.json`:

- "abre aquele editor de código da JetBrains para Python" abre o PyCharm
- "bota uma música do Legião Urbana" procura no YouTube
- "tá muito alto, abaixa o som" diminui o volume
- "o que é Spring Boot?" não é um comando, então ele responde falando

Cada frase vira uma chamada à API (poucos centavos por mil frases) e leva cerca de um segundo a mais. Sem internet ou sem chave, ele volta sozinho para as **palavras-chave** de cada comando. Para usar só as palavras-chave, troque `"interpretar_com_ia": true` por `false` no `comandos.json`.

## Janela e voz

Ao iniciar, abre uma janela com uma esfera que muda conforme o estado:

| Cor | Estado |
|---|---|
| Azul | Esperando você dizer "Jarvis" |
| Verde | Ouvindo |
| Amarelo (com arcos girando) | Pensando |
| Ciano (pulsando) | Falando |

Embaixo ficam o que você disse e o que ele respondeu. Fechar a janela encerra o Jarvis. Para rodar sem janela, troque `"janela": true` por `false` no `comandos.json`. Se o tkinter não estiver instalado, ele roda sem janela sozinho.

O Jarvis responde falando. Ele escolhe automaticamente uma voz em português do Windows (por exemplo, a Maria). Se não houver nenhuma instalada, instale uma em *Configurações → Hora e idioma → Fala*.

## Voz offline (opcional)

1. Baixe um modelo em português em alphacephei.com/vosk/models e descompacte numa pasta (por exemplo `modelo-vosk`).
2. Coloque o caminho em `VOSK_MODEL_PATH` no `.env`.

Com internet ele usa o Google. Sem internet, troca sozinho para o Vosk. As perguntas para a IA continuam precisando de internet.

## Iniciar com o Windows

1. Copie `iniciar_jarvis.bat.example` para `iniciar_jarvis.bat` e troque o caminho pelo da sua pasta.
2. Crie um atalho do `.bat`.
3. Aperte `Win + R`, digite `shell:startup` e coloque o atalho nessa pasta.

## Estrutura

```
jarvis.py      loop principal: escuta, interpreta e executa
voz.py         falar e ouvir (Google + Vosk offline)
apps.py        abrir sites, programas e YouTube
ia.py          Claude e Gemini, com memória da conversa
ditar.py       ditado por voz
codigo.py      geração de código por voz
interface.py   janela animada (tkinter)
utilidades.py  hora e data
comandos.json  lista de comandos de voz
```
