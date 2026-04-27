from langgraph.graph import StateGraph, END

from state import SymptomState
from nodes.intake_node import intake_node
from nodes.classifier_node import classifier_node
from nodes.leve_node import leve_node
from nodes.moderado_node import moderado_node
from nodes.grave_node import grave_node
from nodes.formatter_node import formatter_node


def route_by_severity(state: SymptomState) -> str:
    gravedad = state["gravedad"]
    if gravedad == "leve":
        return "leve"
    elif gravedad == "moderado":
        return "moderado"
    else:
        return "grave"


def build_graph():
    graph = StateGraph(SymptomState)

    graph.add_node("intake", intake_node)
    graph.add_node("classifier", classifier_node)
    graph.add_node("node_leve", leve_node)
    graph.add_node("node_moderado", moderado_node)
    graph.add_node("node_grave", grave_node)
    graph.add_node("formatter", formatter_node)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "classifier")

    graph.add_conditional_edges(
        "classifier",
        route_by_severity,
        {
            "leve":     "node_leve",
            "moderado": "node_moderado",
            "grave":    "node_grave",
        }
    )

    graph.add_edge("node_leve", "formatter")
    graph.add_edge("node_moderado", "formatter")
    graph.add_edge("node_grave", "formatter")
    graph.add_edge("formatter", END)

    return graph.compile()
