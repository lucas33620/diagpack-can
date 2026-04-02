"""
@file app_cli.py
@brief Fournit une interface CLI terminale pour DiagPack CAN
@copyright
© 2025 SYLORIA — MIT License — BAQUEY Lucas (contact@syloria.fr)
"""

import argparse

from diagpack.can.socketcan import open_can_socket
from diagpack.capture.capture_loop import run_capture_loop
from diagpack.replay.replay_engine import replay_log


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="diagpack",
        description="DiagPack CAN - Linux/SocketCAN diagnostic toolbox",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Capture command
    capture_parser = subparsers.add_parser(
        "capture",
        help="Capture CAN frames from a SocketCAN interface",
    )

    capture_parser.add_argument(
        "--iface",
        required=True,
        help="SocketCAN interface name, for example vcan0",
    )

    capture_parser.add_argument(
        "--output",
        required=True,
        help="Output JSONL file path",
    )

    # Replay command
    replay_parser = subparsers.add_parser(
        "replay",
        help="Replay CAN frame events from a JSONL file",
    )

    replay_parser.add_argument(
        "--iface",
        required=True,
        help="SocketCAN interface name. For example : vcan0",
    )

    replay_parser.add_argument(
        "--file",
        required=True,
        help="Input JSONL log file path",
    )

    replay_parser.add_argument(
        "--id",
        dest="id_filter",
        type=int,
        nargs="*",
        default=None,
        help="Optional CAN ID filter (one or more IDs)",
    )

    replay_parser.add_argument(
        "--start",
        type=float,
        default=None,
        help="Optional replay start timestamp",
    )

    replay_parser.add_argument(
        "--end",
        type=float,
        default=None,
        help="Optional replay end timestamp",
    )

    replay_parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Replay speed factor (default: 1.0)",
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
        print("\nCapture stopped by user.")
    finally:
        can_socket.close()


def run_replay_command(args) -> None:
    can_socket = open_can_socket(args.iface)

    try:
        print(
            f"Starting CAN replay on interface '{args.iface}' "
            f"from '{args.file}'. Press Ctrl+C to stop."
        )

        with open(args.file, "r", encoding="utf-8") as file:
            replay_log(
                can_socket=can_socket,
                file=file,
                id_filter=args.id_filter,
                ts_start=args.start,
                ts_end=args.end,
                speed=args.speed,
            )

    except KeyboardInterrupt:
        print("\nReplay stopped by user.")
    finally:
        can_socket.close()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "capture":
        run_capture_command(args)
    elif args.command == "replay":
        run_replay_command(args)