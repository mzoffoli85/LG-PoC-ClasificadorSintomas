from datetime import date

from state import SymptomState


def formatter_node(state: SymptomState) -> SymptomState:
    sintomas_md = "\n".join(f"- {s}" for s in state["sintomas"])
    gravedad_display = state["gravedad"].capitalize()

    output_md = f"""# Reporte de Síntomas
**Fecha:** {date.today()}
**Gravedad detectada:** {gravedad_display}
**Ruta tomada:** {state["ruta"]}

## Síntomas identificados
{sintomas_md}

## Recomendación
{state["respuesta"]}

## ⚠️ Disclaimer
{state["disclaimer"]}
"""

    return {**state, "output_md": output_md}
