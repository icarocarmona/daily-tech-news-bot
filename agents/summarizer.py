from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.fetch_news import fetch_latest_news
from services.telegram import send_message
from typing import TypedDict, List

load_dotenv()


class AppState(TypedDict):
    noticias: List[dict]
    resumos: List[dict]
    status: str


llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
resumo_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Você é um assistente conciso e direto que resume notícias técnicas em português sobre dados, Tech, ChatGPT, IA ou arquitetura de software. Apresente o resumo principal de imediato. 
            Evite iniciar o reumo com ['A notícia destaca', 'A notícia aborda']
            Inicie direto com o resumo sem enrolação.
            """,
        ),
        (
            "human",
            "Resuma a seguinte notícia em no máximo 5 linhas, focando no ponto principal e utilizando linguagem técnica direta, sem introduções: {noticia}",
        ),
    ]
)
filtro_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um filtro inteligente que analisa o título de uma notícia e decide se ela é relevante para alguém interessado em dados, IA, arquitetura de software ou política/negócios que impactam tecnologia.",
        ),
        (
            "human",
            "Título: {titulo}\nA notícia é relevante? Responda apenas com 'SIM' ou 'NAO'",
        ),
    ]
)


filtro_llm = filtro_prompt | llm

resumo_llm = resumo_prompt | llm


def filter_news_by_title(state):
    filtradas = []
    for noticia in state["noticias"]:
        resposta = filtro_llm.invoke({"titulo": noticia["title"]})
        if isinstance(resposta.content, str) and "SIM" == resposta.content:
            filtradas.append(noticia)
            print(f"Noticia:  \n{noticia}")

    return {"noticias": filtradas, "resumos": [], "status": "filtrado"}


def summarize_news(state):
    summaries = []
    for noticia in state["noticias"]:
        res = resumo_llm.invoke({"noticia": noticia["content"]})
        summaries.append(
            {"title": noticia["title"], "link": noticia["link"], "resumo": res.content}
        )
    return {"resumos": summaries}


def format_and_send(state):
    mensagens = []
    for item in state["resumos"]:
        msg = f"\u2728 *{item['title']}*\n{item['resumo']}\n[Leia mais]({item['link']})"
        mensagens.append(msg)
        send_message(msg)
    return {"status": "enviado"}


# Construindo o grafo
# workflow = StateGraph[AppState](state_schema=AppState)
# workflow.add_node("filtrar", filter_news_by_title)
# workflow.add_node("resumir", summarize_news)
# workflow.add_node("enviar", format_and_send)
# workflow.set_entry_point("filtrar")
# workflow.add_edge("filtrar", "resumir")
# workflow.add_edge("resumir", "enviar")
# workflow.set_finish_point("enviar")


def process_noticia(noticia: dict):
    resposta = filtro_llm.invoke({"titulo": noticia["title"]})
    if "SIM" not in resposta.content:
        return

    resposta_resumo = resumo_llm.invoke({"noticia": noticia["title"]})
    resumo = resposta_resumo.content

    msg = f"✨ *{noticia['title']}*\n{resumo}\n[Leia mais]({noticia['link']})"
    send_message(msg)


def run():
    noticias = fetch_latest_news()
    for noticia in noticias:
        process_noticia(noticia)
    # graph = workflow.compile()
    # graph.invoke({"noticias": noticias, "resumos": [], "status": ""})


if __name__ == "__main__":
    run()
