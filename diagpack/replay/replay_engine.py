"""
 @file replay_engine.py
 @brief Fournir une logique de lecture d'événements à partir d'un fichier JSONL et de les rejouer sur une interface SocketCAN
 @copyright
 © 2025 SYLORIA — MIT License — BAQUEY Lucas (contact@syloria.fr)
"""

import socket
from typing import Any
from diagpack.can.socketcan import send_frame

def event_to_frame_fields(event: dict[str, Any]) -> tuple[int, int, bytes]:
    can_id = event["id"]
    can_dlc = event["dlc"]
    data = bytes.fromhex(event["data"])
    return can_id, can_dlc, data


def replay_event(can_socket: socket.socket, event: dict[str, Any]) -> None:
    can_id, can_dlc, data = event_to_frame_fields(event)
    send_frame(can_socket, can_id, can_dlc, data)