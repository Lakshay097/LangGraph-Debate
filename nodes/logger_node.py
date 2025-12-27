from state import DebateState
from utils.logger import log_event


def logger_node(state: DebateState) -> DebateState:
    log_event("LoggerNode", state.model_dump(), state.log_path)
    return {}
