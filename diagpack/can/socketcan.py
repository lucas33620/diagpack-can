
"""
 @file socketcan.py
 @brief Ouvrir une interface socket
 @copyright
 © 2025 SYLORIA — MIT License — BAQUEY Lucas (contact@syloria.fr)
"""

import socket


def open_can_socket(interface: str) -> socket.socket:
    try:
        can_socket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        can_socket.bind((interface,))
    except OSError as exc:
        raise RuntimeError(
            f"Failed to open SocketCAN interface '{interface}': {exc}"
        ) from exc

    return can_socket