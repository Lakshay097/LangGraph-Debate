from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class Turn(BaseModel):
    round: int
    agent: Literal["Scientist", "Philosopher"]
    text: str
    meta: dict = Field(default_factory=dict)

class DebateState(BaseModel):
    topic: str
    round: int = 0
    turn_count: int = 0
    current_speaker: Literal["A", "B", "JUDGE", "USER"] = "USER"
    turns: List[Turn] = Field(default_factory=list)
    summary: Optional[str] = None
    coherence_flags: List[str] = Field(default_factory=list)
    argument_signatures: List[str] = Field(default_factory=list)
    seed: Optional[int] = None
    log_path: Optional[str] = None
    meta: dict = Field(default_factory=dict)
