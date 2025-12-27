import json
from datetime import datetime

def now_iso():
    return datetime.utcnow().isoformat()

def log_event(name: str, data: dict, log_path: str):
    if not log_path:
        return

    def serialize(obj):
        try:
            return obj.model_dump()
        except AttributeError:
            return str(obj)

    serializable_data = {k: serialize(v) for k, v in data.items()}

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "event": name,
            "timestamp": now_iso(),
            "data": serializable_data
        }, ensure_ascii=False) + "\n")
