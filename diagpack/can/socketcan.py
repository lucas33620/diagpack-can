# Copyright (c) 2026 Baquey Lucas. All rights reserved.
# Licensed under the DiagPack CAN Source-Available Internal-Use License.
# See LICENSE at the repository root for terms and permitted internal use.


"""
 @file socketcan.py
 @brief Ouvrir une interface socket
 @copyright
 Copyright (c) 2026 Baquey Lucas — see LICENSE
"""

import socket
import struct

CAN_FRAME_FORMAT = "=IB3x8s" # 4 + 1 + 3 + 8 = 16 octets
CAN_FRAME_SIZE = struct.calcsize(CAN_FRAME_FORMAT)

def open_can_socket(interface: str) -> socket.socket:
    try:
        can_socket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        can_socket.bind((interface,))
    except OSError as exc:
        raise RuntimeError(
            f"Failed to open SocketCAN interface '{interface}': {exc}"
        ) from exc

    return can_socket

def read_frame(can_socket: socket.socket) -> tuple [int, int, bytes]:
    if can_socket is None :
        raise RuntimeError(
            f"Socket CAN interface is not initialized"
        )

    frame = can_socket.recv(CAN_FRAME_SIZE)

    if CAN_FRAME_SIZE != len(frame):
        raise RuntimeError(
            f"Incomplete CAN frame received: expected {CAN_FRAME_SIZE} bytes, got {len(frame)}"
        )
    
    can_id, dlc, data = struct.unpack(CAN_FRAME_FORMAT, frame)

    return can_id, dlc, data[:dlc]
