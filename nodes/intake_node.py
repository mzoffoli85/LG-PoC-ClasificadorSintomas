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


def intake_node(state: SymptomState) -> SymptomState:
    prompt_template = (Path(__file__).parent.parent / "prompts" / "intake.txt").read_text(encoding="utf-8")
    prompt = prompt_template.format(input=state["input"])

    response = _get_llm().invoke(prompt)

    lines = response.content.strip().split("\n")
    sintomas = [line.lstrip("- ").strip() for line in lines if line.strip()]

    return {**state, "sintomas": sintomas}
