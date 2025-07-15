# 🤖 Daily Tech News Bot

Um bot automatizado que coleta diariamente notícias do mundo da tecnologia, filtra por relevância (foco em dados, IA, arquitetura de software e política/negócios relacionados), resume com LLM e envia os resumos direto para o seu Telegram.

---

## ⚙️ Funcionalidades

- 🔎 Coleta notícias de fontes confiáveis via RSS.
- 🧠 Filtra títulos usando inteligência artificial.
- ✍️ Resume conteúdos com o modelo GPT-4o da OpenAI.
- 📬 Envia mensagens formatadas no Telegram com resumo e link para leitura completa.
- 🌐 API REST para acionar o pipeline remotamente.

---

## 📦 Estrutura do projeto

```
daily-tech-news-bot/
├── agents/
│   └── summarizer.py          # Pipeline principal com LangGraph
├── api/
│   └── routers.py             # Rotas da API REST (FastAPI)
├── app.py                     # Inicialização da aplicação FastAPI
├── services/
│   ├── fetch_news.py          # Coleta de notícias via RSS
│   └── telegram.py            # Envio de mensagens via Telegram
├── .env.example               # Variáveis de ambiente (modelo)
├── requirements.txt           # Dependências do projeto
├── Dockerfile                 # Dockerfile para build da API
├── docker-compose.yml         # Orquestração com Docker Compose
```

A pasta `api/` contém as rotas da API REST, permitindo acionar o agente de notícias remotamente. O arquivo `app.py` inicializa a aplicação FastAPI e inclui as rotas.

---

## ✅ Pré-requisitos

- Python 3.10+
- Conta na [OpenAI](https://platform.openai.com/)
- Bot do Telegram criado com [@BotFather](https://t.me/BotFather)
- (Opcional) Docker e Docker Compose

---

## 🛠️ Instalação e uso

### Modo manual

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/daily-tech-news-bot.git
   cd daily-tech-news-bot
   ```

2. Crie o ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure seu `.env` baseado no `.env.example`:
   ```env
   OPENAI_API_KEY=sk-...
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_CHAT_ID=...
   ```

4. Execute manualmente:
   ```bash
   python -m agents.summarizer
   ```

### Executando a API

Você pode rodar a API localmente com FastAPI/Uvicorn:

```bash
uvicorn app:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

#### Endpoint disponível

- **POST** `/api/execute_agent`  
  Aciona o pipeline de notícias em background.
  - **Resposta:**  
    ```json
    {
      "status": "em processamento",
      "detail": "O agente foi iniciado em segundo plano. Aguarde ~1 minuto."
    }
    ```

---

## 🚀 Docker

Para rodar tudo em container:

1. Build e execute com Docker Compose:
   ```bash
   docker compose up --build
   ```

2. Acesse a API em [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💡 Exemplo de mensagem enviada

```
📰 [Título da notícia](https://link-da-noticia.com)
Resumo gerado por IA sobre o conteúdo da notícia.
```

---

## 🙋‍♂️ Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

