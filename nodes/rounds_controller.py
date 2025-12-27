from state import DebateState
from utils.logger import log_event

MAX_TURNS = 8

def rounds_controller_node(state: DebateState) -> dict:
    """
    Controls debate rounds where each round is assigned to a single speaker.
    Alternates between A and B each round.
    """
    # --- STOP CONDITION ---
    if state.turn_count >= MAX_TURNS:
        log_event(
            "RoundsControllerNode",
            {"action": "END", "round": state.round},
            state.log_path,
        )
        return {"current_speaker": "JUDGE"}

    # --- INITIALIZATION (after UserInputNode) ---
    if state.current_speaker == "USER":
        log_event(
            "RoundsControllerNode",
            {"action": "INIT", "round": 1, "speaker": "A"},
            state.log_path,
        )
        return {
            "round": 1,            # First round = 1
            "turn_count": 1,       # First turn counts as turn 1
            "current_speaker": "A" # Scientist starts
        }

    # --- ALTERNATE SPEAKER EACH ROUND ---
    next_speaker = "B" if state.current_speaker == "A" else "A"
    next_turn = state.turn_count + 1

    log_event(
        "RoundsControllerNode",
        {
            "action": "ADVANCE",
            "next_round": next_turn,
            "next_speaker": next_speaker,
        },
        state.log_path,
    )

    return {
        "round": next_turn,         
        "turn_count": next_turn,
        "current_speaker": next_speaker,
    }
