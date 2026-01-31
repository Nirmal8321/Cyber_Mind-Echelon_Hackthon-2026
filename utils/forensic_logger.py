import json
import datetime
import os

def log_forensic_step(agent_name, input_data, output_score, reasoning):
    """
    Records a specific forensic action into a permanent, queryable log.
    """
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "forensic_audit.jsonl")

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "agent": agent_name,
        "input_hash": hash(str(input_data)), 
        "verdict_score": output_score,
        "internal_thought": reasoning
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")