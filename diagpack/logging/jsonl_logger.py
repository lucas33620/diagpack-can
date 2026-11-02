# Copyright (c) 2026 Baquey Lucas. All rights reserved.
# Licensed under the DiagPack CAN Source-Available Internal-Use License.
# See LICENSE at the repository root for terms and permitted internal use.

import json
from typing import Any, TextIO


def write_event(event: dict[str, Any], file: TextIO) -> None:
    json_line = json.dumps(event)
    file.write(json_line)
    file.write("\n")