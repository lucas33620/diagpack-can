import socket
import time
from typing import Any

from diagpack.replay.replay_engine import replay_event

def send_burst(can_socket, can_id: int, data_hex: str, count: int, delay: float = 0.001) -> None:
    if count <= 0:
        raise ValueError("Count must be a positive integer.")
    if delay < 0:
        raise ValueError("Delay must be a non-negative float.")
    if len(data_hex) % 2 != 0:
        raise ValueError("Data hex string must have an even length.")
    
    try:
        data = bytes.fromhex(data_hex)
    except ValueError:
        raise ValueError("Data hex string is not valid.")

    event = {
        "id": can_id,
        "dlc": len(data),
        "data": data_hex,
        "ts": time.time()
    }

    for i in range(count):
        replay_event(can_socket, event)
        time.sleep(delay)  # Small delay between messages