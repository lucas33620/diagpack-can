import json
from typing import Any, TextIO

def write_event(event: dict[str, Any], file: TextIO) -> None:
    json_line = json.dumps(event)
    file.write(json_line)
    file.write("\n")

def read_events(file: TextIO):
    for line in file:
        line = line.strip()
        if not line:
            continue

        yield json.loads(line) # Allow to optimize memory to give only evenement by evenements