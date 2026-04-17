from engine.storage_helper import read_data, write_data
from datetime import datetime


def add_log(stage, status, message, payload=None):
    logs = read_data("logs.json")

    log_entry = {
        "time": datetime.now().isoformat(),
        "stage": stage,
        "status": status,
        "message": message,
        "payload": payload
    }

    logs.append(log_entry)
    write_data("logs.json", logs)