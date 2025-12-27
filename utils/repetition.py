import hashlib

def argument_signature(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()


def check_repetition(text: str, signatures: list[str]) -> None:
    sig = argument_signature(text)
    if sig in signatures:
        raise RuntimeError("Repeated argument detected")


def add_signature(text: str, signatures: list[str]) -> list[str]:
    return signatures + [argument_signature(text)]

def detect_topic_drift(text: str, topic: str) -> bool:
    topic_tokens = [t.lower() for t in topic.split() if len(t) > 3]
    text_lower = text.lower()

    return not any(tok in text_lower for tok in topic_tokens)
