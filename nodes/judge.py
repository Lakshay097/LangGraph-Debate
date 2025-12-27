import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import build_llm
from state import DebateState
from utils.logger import log_event, now_iso

JUDGE_PROMPT = """You are a neutral Judge evaluating a formal debate.

STRICT RULES:
- Respond ONLY with valid JSON
- Do NOT use markdown
- Do NOT include explanations outside JSON

Return JSON with keys:
summary (string),
winner ("Scientist" or "Philosopher"),
justification (string)
"""

def judge_node(state: "DebateState") -> dict:
    llm = build_llm(state.seed)

    turns_txt = "\n".join(
        f"Round {t.round} {t.agent}: {t.text}" for t in state.turns
    )
    coherence = "; ".join(state.coherence_flags) or "None"

    sys_msg = SystemMessage(content=JUDGE_PROMPT)
    user_msg = HumanMessage(content=(
        f"Debate topic: {state.topic}\n"
        f"Transcript:\n{turns_txt}\n\n"
        f"Coherence issues flagged: {coherence}"
    ))

    resp = llm.invoke([sys_msg, user_msg])
    resp = resp.content
    
    try:
        verdict = json.loads(resp)
    except Exception :
        verdict = {
            "summary": resp,
            "winner": "Scientist",
            "justification": "Fallback due to parsing failure",
        }

    summary = verdict['summary']
    winner = verdict["winner"]
    justification = verdict["justification"]

    print("[Judge] Summary of debate:")
    print(summary)
    print(f"[Judge] Winner: {winner}")
    print(f"Reason: {justification}")

    log_event("JudgeNode", {
        "summary": summary,
        "winner": winner,
        "justification": justification,
        "timestamp": now_iso()
    }, state.log_path)

    return {
        "summary": summary,
        "meta": {
            "winner": winner,
            "justification": justification
        }
    }
