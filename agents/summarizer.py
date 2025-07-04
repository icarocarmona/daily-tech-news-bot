from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

from services.fetch_news import fetch_latest_news
from services.telegram import send_message
from typing import TypedDict, List

load_dotenv()


class AppState(TypedDict):
    noticias: List[dict]
    resumos: List[dict]
    status: str


llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um assistente que resume notícias técnicas da área de dados, Tech, ChatGPT ,IA ou arquitetura de software.",
        ),
        (
            "human",
            "Resuma a seguinte notícia em no máximo 5 linhas, com foco no ponto principal e linguagem técnica direta: {noticia}",
        ),
    ]
)


def filter_news_by_title(state):
    chain = (
        ChatPromptTemplate.from_messages(
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
        | llm
    )

    filtradas = []
    for noticia in state["noticias"]:
        resposta = chain.invoke({"titulo": noticia["title"]})
        if isinstance(resposta.content, str) and "SIM" == resposta.content:
            filtradas.append(noticia)
    return {"noticias": filtradas, "resumos": [], "status": "filtrado"}


def summarize_news(state):
    summaries = []
    for noticia in state["noticias"]:
        chain = prompt | llm
        res = chain.invoke({"noticia": noticia["content"]})
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
workflow = StateGraph[AppState](state_schema=AppState)
workflow.add_node("filtrar", filter_news_by_title)
workflow.add_node("resumir", summarize_news)
workflow.add_node("enviar", format_and_send)
workflow.set_entry_point("filtrar")
workflow.add_edge("filtrar", "resumir")
workflow.add_edge("resumir", "enviar")
workflow.set_finish_point("enviar")


def run():
    noticias = fetch_latest_news()
    graph = workflow.compile()
    graph.invoke({"noticias": noticias, "resumos": [], "status": ""})


if __name__ == "__main__":
    run()
