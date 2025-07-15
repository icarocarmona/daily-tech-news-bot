from fastapi import APIRouter, BackgroundTasks
from agents.summarizer import run_agent

router = APIRouter()


@router.post("/execute_agent")
def execute_agent(background_task: BackgroundTasks):
    background_task.add_task(run_agent)
    return {
        "status": "em processamento",
        "detail": "O agente foi iniciado em segundo plano. Aguarde ~1 minuto.",
    }
