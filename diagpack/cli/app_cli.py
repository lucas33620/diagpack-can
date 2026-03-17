"""
 @file app_cli.py
 @brief Fournir une interface CLI (terminale)
 @copyright
 © 2025 SYLORIA — MIT License — BAQUEY Lucas (contact@syloria.fr)
"""

import argparse

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

def main() -> None :
    parser = build_parfser()
    args = parser.parse_args()

    if args.command == "capture":
        print(
            f"[diapack] capture command selected"
            f"(iface={args.iface}, output={args.output})"
        )



