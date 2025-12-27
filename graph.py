from langgraph.graph import StateGraph, START, END
from state import DebateState
from nodes.user_input import user_input_node
from nodes.agents import agent_a_node, agent_b_node
from nodes.memory import memory_node
from nodes.logger_node import logger_node
from nodes.rounds_controller import rounds_controller_node
from nodes.judge import judge_node


def build_graph():
    graph = StateGraph(DebateState)

    graph.add_node("UserInputNode", user_input_node)
    graph.add_node("RoundsControllerNode", rounds_controller_node)

    graph.add_node("AgentA", agent_a_node)
    graph.add_node("AgentB", agent_b_node)

    graph.add_node("TurnLogger", logger_node)
    graph.add_node("MemoryNode", memory_node)

    graph.add_node("JudgeNode", judge_node)
    graph.add_node("FinalLogger", logger_node)

    # ALWAYS start with UserInputNode
    graph.add_edge(START, "UserInputNode")

    graph.add_edge("UserInputNode", "RoundsControllerNode")

    def route_from_controller(state: DebateState):
        if state.current_speaker == "A":
            return "AgentA"
        if state.current_speaker == "B":
            return "AgentB"
        return "JudgeNode"

    graph.add_conditional_edges(
        "RoundsControllerNode", route_from_controller,{"AgentA": "AgentA", 
                                                       "AgentB": "AgentB",
                                                       "JudgeNode": "JudgeNode",},
    )

    graph.add_edge("AgentA", "TurnLogger")
    graph.add_edge("AgentB", "TurnLogger")

    graph.add_edge("TurnLogger", "MemoryNode")
    graph.add_edge("MemoryNode", "RoundsControllerNode")

    graph.add_edge("JudgeNode", "FinalLogger")
    graph.add_edge("FinalLogger", END)

    return graph
