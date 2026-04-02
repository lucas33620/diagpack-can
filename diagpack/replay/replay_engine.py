"""
 @file replay_engine.py
 @brief Fournir une logique de lecture d'événements à partir d'un fichier JSONL et de les rejouer sur une interface SocketCAN
 @copyright
 © 2025 SYLORIA — MIT License — BAQUEY Lucas (contact@syloria.fr)
"""

import socket
import time
from typing import Any
from diagpack.replay.replay_timing import compute_delay
from diagpack.can.socketcan import send_frame
from diagpack.logging.jsonl_logger import read_events

def event_to_frame_fields(event: dict[str, Any]) -> tuple[int, int, bytes]:
    can_id = event["id"]
    can_dlc = event["dlc"]
    data = bytes.fromhex(event["data"])
    return can_id, can_dlc, data


def replay_event(can_socket: socket.socket, event: dict[str, Any]) -> None:
    can_id, can_dlc, data = event_to_frame_fields(event)
    send_frame(can_socket, can_id, can_dlc, data)


def event_matches_filters(event: dict[str, Any], id_filter: list[int], ts_start: float, ts_end: float):
    match_st = True

    if id_filter is not None and event["id"] not in id_filter:
        match_st = False
    if ts_start is not None and event["ts"] < ts_start:
        match_st = False
    if ts_end is not None and event["ts"] > ts_end:
        match_st = False
    
    return match_st

def replay_log(can_socket, id_filter: list[int], ts_start: float, ts_end: float, file, speed: float = 1.0) -> None:
    previous_ts = None

    for event in read_events(file):
        current_ts = event["ts"]  
        
        # Verify that event is present in the filter
        if event_matches_filters(event, id_filter, ts_start, ts_end) != True :
            continue

        if previous_ts is not None :
            delay = compute_delay(current_ts, previous_ts, speed)
            time.sleep(delay)

        replay_event(can_socket, event)
        previous_ts = current_ts
    

