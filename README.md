# 🤖 Daily Tech News Bot

Um bot automatizado que coleta diariamente notícias do mundo da tecnologia, filtra por relevância (foco em dados, IA, arquitetura de software e política/negócios relacionados), resume com LLM e envia os resumos direto para o seu Telegram.

---

## ⚙️ Funcionalidades

- 🔎 Coleta notícias de fontes confiáveis via RSS.
- 🧠 Filtra títulos usando inteligência artificial.
- ✍️ Resume conteúdos com o modelo GPT-4o da OpenAI.
- 📬 Envia mensagens formatadas no Telegram com resumo e link para leitura completa.

---

## 📦 Estrutura do projeto

```
daily-tech-news-bot/
├── agents/
│   └── summarizer.py          # Pipeline principal com LangGraph
├── services/
│   ├── fetch_news.py          # Coleta de notícias via RSS
│   └── telegram.py            # Envio de mensagens via Telegram
├── .env.example               # Variáveis de ambiente (modelo)
├── requirements.txt           # Dependências do projeto
```
---

## ✅ Pré-requisitos

- Python 3.10+
- Conta no [OpenAI](https://platform.openai.com/)
- Bot do Telegram criado com [@BotFather](https://t.me/BotFather)

---

## 🛠️ Instalação e uso

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/daily-tech-news-bot.git
cd daily-tech-news-bot
```
   
2.	Crie o ambiente e instale dependências:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3.	Configure seu .env baseado no .env.example:
```bash
OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

4.	Execute manualmente:
```sh
python -m agents.summarizer
```

