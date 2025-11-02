import json
import time
import os
from pathlib import Path

# Define log directory and file
LOG_DIR = "logs"
LOGFILE = os.path.join(LOG_DIR, "fs_events.jsonl")

def set_log_dir(new_dir):
    """Change log directory and ensure it exists. Returns new logfile path."""
    global LOG_DIR, LOGFILE
    LOG_DIR = new_dir
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    LOGFILE = os.path.join(LOG_DIR, "fs_events.jsonl")
    return LOGFILE

def get_log_file():
    """Return current logfile path."""
    return LOGFILE

def log_event(event_type, path, details=None):
    try:
        # Create logs directory if it doesn't exist
        Path(LOG_DIR).mkdir(exist_ok=True)
        
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "event": event_type,
            "path": path
        }
        
        if details is not None:
            # keep details reasonably sized in file
            event["details"] = details if len(details) <= 100000 else details[:100000] + "\n...truncated..."
        
        # Ensure directory exists and file is writable
        with open(LOGFILE, "a", encoding="utf-8") as f:
            json_str = json.dumps(event, ensure_ascii=False)
            f.write(json_str + "\n")
            f.flush()  # Force write to disk
            
    except Exception as e:
        print(f"Error logging event: {str(e)}")