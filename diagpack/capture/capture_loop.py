import time
import socket
from typing import TextIO

from diagpack.can.socketcan import read_frame
from diagpack.logging.jsonl_logger import write_event

def run_capture_loop(can_socket: socket.socket, file: TextIO) -> None:
    while True:
        can_id, dlc, data = read_frame(can_socket)
        timestamp = time.time()

        event = {
            "ts" : timestamp,
            "id" : can_id,
            "dlc" : dlc,
            "data" : data.hex(),
        }

        write_event(event, file)
        file.flush() # Allow to watch the file fill up immediately while it's processing
        