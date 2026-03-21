"""
 @file app_cli.py
 @brief Fournir une interface CLI (terminale)
 @copyright
 © 2025 SYLORIA — MIT License — BAQUEY Lucas (contact@syloria.fr)
"""

import argparse
from diagpack.can.socketcan import open_can_socket
from diagpack.capture.capture_loop import run_capture_loop

# Create command-line interfaces with multiple subcommands
def build_parfser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="diagpack",
        description = "DiagPack CAN - Linux/SocketCAN diagnostic toolbox"
    )

    subparsers = parser.add_subparsers(dest="command", required = True)

    capture_parser = subparsers.add_parser(
        "capture",   # Allows to capture CAN frame
        help = "Capture CAN frames from a SocketCAN interface"
    )

    capture_parser.add_argument(
        "--iface",
        required = True,
        help = "SocketCAN interface name as 'vcan0'"
    )

    capture_parser.add_argument(
        "--output",
        required = True,
        help = "Output JSON line"
    )

    return parser

def run_capture_command(args) -> None:
    can_socket = open_can_socket(args.iface)

    try:
        with open(args.output, "w", encoding="utf-8") as file:
            print(
                f"Starting CAN capture on interface '{args.iface}'. "
                f"Writing to '{args.output}'. Press Ctrl+C to stop."
            )
            run_capture_loop(can_socket, file)
    except KeyboardInterrupt:
        print("\n Capture stopped by user")
    finally:
        can_socket.close()

def main() -> None :
    parser = build_parfser()
    args = parser.parse_args()

    if args.command == "capture":
        run_capture_command(args)
