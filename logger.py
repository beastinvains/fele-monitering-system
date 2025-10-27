import json
import time

LOGFILE = "fs_events.jsonl"

def log_event(event_type, path):
    event = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "path": path
    }
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

