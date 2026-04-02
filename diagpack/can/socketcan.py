
"""
 @file socketcan.py
 @brief Outils pour interagir avec les interfaces SocketCAN sous Linux
 @copyright
 © 2025 SYLORIA — MIT License — BAQUEY Lucas (contact@syloria.fr)
"""

import socket
import struct

CAN_MAX_DLEN = 8
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

def send_frame(can_socket: socket.socket, can_id: int, can_dlc: int, data: bytes) -> None :
    if can_socket is None :
        raise RuntimeError(
            f"Socket CAN interface is not initialized"
        )
    
    if not (0 <= can_dlc <= CAN_MAX_DLEN):
        raise ValueError(f"CAN DLC must be in range 0 to {CAN_MAX_DLEN}")
    
    if len(data) != can_dlc:
        raise ValueError(
            f"Data length {len(data)} does not match DLC {can_dlc}"
        )

    # Pack l'ID and data in CAN format
    pad_data = data.ljust(8, b"\x00") # Pad data to 8 bytes if necessary
    frame = struct.pack(CAN_FRAME_FORMAT, can_id, can_dlc, pad_data)

    # Send frame
    try :
        can_socket.send(frame)
    except OSError as exc:
        raise RuntimeError(
            f"Failed to send CAN frame: ID={can_id}, DLC={can_dlc}, Data={data.hex()}"
        ) from exc



    


