import os
from pathlib import Path

from langchain_openai import ChatOpenAI

from state import SymptomState


def _get_llm():
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        temperature=0.3,
    )


def grave_node(state: SymptomState) -> SymptomState:
    prompt_template = (Path(__file__).parent.parent / "prompts" / "grave.txt").read_text(encoding="utf-8")
    sintomas_str = "\n".join(f"- {s}" for s in state["sintomas"])
    prompt = prompt_template.format(sintomas=sintomas_str)

    response = _get_llm().invoke(prompt)

    return {**state, "ruta": "node_grave", "respuesta": response.content.strip()}
