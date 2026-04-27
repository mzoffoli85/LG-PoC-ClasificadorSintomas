import os
from pathlib import Path

from langchain_openai import ChatOpenAI

from state import SymptomState

DISCLAIMER = (
    "Este reporte es generado por una IA con fines educativos. "
    "No reemplaza una consulta médica profesional."
)


def _get_llm():
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        temperature=0.1,
    )


def classifier_node(state: SymptomState) -> SymptomState:
    prompt_template = (Path(__file__).parent.parent / "prompts" / "classifier.txt").read_text(encoding="utf-8")
    sintomas_str = "\n".join(f"- {s}" for s in state["sintomas"])
    prompt = prompt_template.format(sintomas=sintomas_str)

    response = _get_llm().invoke(prompt)
    content = response.content.strip().lower()

    if "grave" in content:
        gravedad = "grave"
    elif "moderado" in content:
        gravedad = "moderado"
    else:
        gravedad = "leve"

    return {**state, "gravedad": gravedad, "disclaimer": DISCLAIMER}
