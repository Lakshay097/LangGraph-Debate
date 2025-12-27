from typing import List
from state import DebateState, Turn
from utils.logger import log_event, now_iso

def build_agent_view(turns : List[Turn], next_agent: str, max_turns: int = 4) -> List[Turn]:
    # Only last few turns plus all of next_agent's own previous turns
    last = turns[-max_turns:]
    own = [t for t in turns if t.agent == next_agent]
    # dedupe by round
    combined = {t.round: t for t in last + own}
    return sorted(combined.values(), key=lambda t: t.round)

def update_summary(turns : List[Turn]) -> str:
    # Minimal non-LLM summary: join last few turns into a compact narrative
    return " | ".join(
        f"R{t.round}-{t.agent}: {t.text}"
        for t in turns[-6:]
    )

def memory_node(state: "DebateState") -> dict:
    # state already has last agent output in meta
    turns = state.turns.copy()
    summary = update_summary(turns)
    if state.current_speaker == "A":
        next_agent = "Philosopher"
    elif state.current_speaker == "B":
        next_agent = "Scientist"
    else:
        next_agent = "Scientist"
    agent_view = build_agent_view(turns, next_agent)

    log_event("MemoryNode", {
        "turns_count": len(turns),
        "summary": summary,
        "next_agent": next_agent,
        "agent_view": [t.model_dump() for t in agent_view],
        "timestamp": now_iso()
    }, state.log_path
    )

    new_meta = dict(state.meta)
    new_meta["agent_view"] = [t.model_dump() for t in agent_view]

    return {
        "summary": summary,
        # Provide view in meta; actual agent nodes will slice from here
        "meta": new_meta
    }
