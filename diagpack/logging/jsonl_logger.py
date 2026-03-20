import json
from typing import Any, TextIO


def write_event(event: dict[str, Any], file: TextIO) -> None:
    json_line = json.dumps(event)
    file.write(json_line)
    file.write("\n")