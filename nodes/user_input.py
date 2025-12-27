from state import DebateState
import re
from utils.logger import log_event

MIN_LEN = 5
MAX_LEN = 200

def sanitize_topic(raw: str) -> str:
    cleaned = re.sub(r"\s+", " ", raw).strip()
    return cleaned

def validate_topic(topic: str) -> None:
    if len(topic) < MIN_LEN or len(topic) > MAX_LEN:
        raise ValueError(f"Topic length must be between {MIN_LEN} and {MAX_LEN} characters")

def user_input_node(state: "DebateState") -> dict:
    topic = input("Enter topic for debate: ")
    topic = sanitize_topic(topic)
    validate_topic(topic)
    print(f"Starting debate between Scientist and Philosopher on: {topic}")
    log_event("UserInputNode", {"topic": topic}, state.log_path)
    return {
        "topic": topic,
        "round": 1,
        "current_speaker": "USER",
        "turn_count": 1,   
    }

