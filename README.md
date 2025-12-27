LangGraph Debate Assignment
A modular LangGraph application where a Scientist and a Philosopher debate a user-provided topic, and a Judge LLM chooses the winner and logs the full debate with memory and coherence checks.
​

Installation
Clone and enter the repo

bash
git clone https://github.com/Lakshay097/LangGraph-Debate.git
cd LangGraph-Debate
Create and activate a virtual environment (optional but recommended)

bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
# source .venv/bin/activate # macOS / Linux
Install dependencies

bash
pip install -r requirements.txt
Set API key

Create a .env file in the project root:

text
OPENROUTER_API_KEY=your_key_here
The LLM client in llm.py reads this variable.
​

How to run
Run the CLI:

bash
python run_debate.py --seed 42
Optional flags:

--seed – integer seed passed to the LLM for reproducibility.
​

--log-path – full path of the JSONL log file (e.g. logs/debate_test.jsonl). If omitted, a timestamped file is created under logs/.
​

The program will:

Prompt: Enter topic for debate:.
​

Run a fixed-length debate between Scientist and Philosopher.
​
​

Print the judge’s summary, winner, and justification.
​

Node roles and DAG
Nodes (in nodes/):
​
​

UserInputNode (user_input.py): reads and sanitizes the topic, validates length, initializes the debate state, and writes the first log entry.
​

RoundsControllerNode (rounds_controller_node.py): alternates speakers A/B and stops after a maximum number of turns, then routes to the Judge.
​

AgentA / AgentB (agents.py): LLM agents with Scientist / Philosopher personas, using prompts from personas/scientist.txt and personas/philosopher.txt. They log each turn and add coherence flags like repetition and topic drift.
​
​

TurnLogger (logger_node.py + utils/logger.py): appends structured JSON entries (node, round, agent, text, flags, timestamps) to the log file.
​
​

MemoryNode (memory.py): maintains a running summary and a per-agent memory view stored in state.meta, which is fed back to agents as context.
​
​

JudgeNode (judge.py): calls an LLM with the full transcript and coherence issues; expects JSON with summary, winner, and justification, prints them, and logs the verdict.
​
​

FinalLogger (logger_node.py): records the final verdict and finishes the DAG.
​
​

DAG wiring is defined in graph.py using StateGraph[DebateState] and conditional edges based on current_speaker.
​

DAG diagram
generate_diag.py compiles the LangGraph and exports both a Mermaid source (debate_dag.mmd) and a PNG diagram (debate_dag.png).
​
​

Generate/update the diagram:

bash
python generate_diag.py
Logs and sample run
Each run writes a JSONL file to the logs/ directory, e.g. logs/debate_YYYYMMDD_HHMMSS.jsonl.
​

Every line corresponds to a node event with fields such as node name, round, speaker, message text, memory snapshot, coherence flags, and timestamps; the final entry includes the judge’s summary and winner.
​
​

To reproduce a sample:

bash
python run_debate.py --seed 42