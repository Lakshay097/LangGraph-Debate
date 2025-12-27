from langchain_core.messages import SystemMessage, HumanMessage
from utils.logger import log_event, now_iso
from utils.repetition import check_repetition, add_signature, detect_topic_drift
from llm import build_llm
from state import DebateState

def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

SCIENTIST_PROMPT = load_prompt("personas/scientist.txt")
PHILOSOPHER_PROMPT = load_prompt("personas/philosopher.txt")

def make_agent_node(agent_id: str):

    def node(state: DebateState) -> dict:
        llm = build_llm(state.seed)

        persona = "Scientist" if agent_id == "A" else "Philosopher"
        system_template = SCIENTIST_PROMPT if agent_id == "A" else PHILOSOPHER_PROMPT

        topic = state.topic
        summary = state.summary or "No summary yet"

        # Memory prepared by MemoryNode
        memory_view = state.meta.get("agent_view", [])
        memory_text = "\n".join(
            f"Round {t['round']} {t['agent']}: {t['text']}"
            for t in memory_view
        )

        sys_msg = SystemMessage(
            content=system_template.format(topic=topic)
        )

        user_msg = HumanMessage(
            content=(
                f"Debate topic: {topic}\n"
                f"Summary so far: {summary}\n\n"
                f"Relevant past turns:\n{memory_text}\n\n"
                f"Your role: {persona}. Provide your next argument."
            )
        )

        response = llm.invoke([sys_msg, user_msg])
        text = response.content.strip()


        check_repetition(text, state.argument_signatures)
        drift = detect_topic_drift(text, topic)

        flags = list(state.coherence_flags)
        if drift:
            flags.append(f"[{persona}] topic drift detected in round {state.round}")

        new_sigs = add_signature(text, state.argument_signatures)


        print(f"[Round {state.round}] {persona}: {text}\n")

        log_event(
            f"Agent{agent_id}",
            {
                "round": state.round,
                "agent": persona,
                "text": text,
                "topic_drift": drift,
                "timestamp": now_iso(),
            },
            state.log_path,
        )

        return {
            "meta": {
                **state.meta,
                "last_agent": agent_id,
                "last_persona": persona,
                "last_message": text,
            },
            "coherence_flags": flags,
            "argument_signatures": new_sigs,
        }

    return node

agent_a_node = make_agent_node("A")  # Scientist
agent_b_node = make_agent_node("B")  # Philosopher
