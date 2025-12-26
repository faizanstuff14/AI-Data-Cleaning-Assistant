from langgraph.graph import StateGraph
from app.cleaning.clean_any import clean_any_dataset


def build_graph():
    graph = StateGraph(dict)

    graph.add_node("clean_any", clean_any_dataset)

    graph.set_entry_point("clean_any")
    graph.set_finish_point("clean_any")

    return graph.compile()
