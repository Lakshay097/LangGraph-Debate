import argparse
from datetime import datetime, timezone
from pathlib import Path
from state import DebateState
from graph import build_graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--log-path", type=str, default=None)
    args = parser.parse_args()

    if args.log_path:
        log_path = args.log_path
    else:
        log_path = f"logs/debate_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.jsonl"
    Path(log_path).parent.mkdir(exist_ok=True)

    initial_state = DebateState(
        topic="",
        round=0,
        turn_count=0,
        current_speaker="USER",
        seed=args.seed,
        log_path=log_path,
    )

    app = build_graph().compile()

    for _ in app.stream(initial_state, {"recursion_limit": 80}):
        pass

    print(f"\nDebate finished. Log saved to {log_path}")

if __name__ == "__main__":
    main()
