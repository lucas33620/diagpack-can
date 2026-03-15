# DiagPack CAN - MVP specification

## Purpose
DiagPack CAN is a lightweight Linux toolbox designed to observe, replay and stress a CAN bus during the prototype phase.

It's goal is to quickly reveal firmware robustness and observability limitations by :
- capturing CAN traffic
- producing structured logs
- replaying traffic scenarios
- injecting perturbations

DiagPack CAN is not a CAN analysis suite or cybersecurity tool.  
It is a **diagnostic and observability tool for embedded firmware prototypes**.

# Scope of the MVP
The MVP focuses on **PC-side tooling only**, running on Linux with SocketCAN.
The first version will operate on a **virtual CAN interface (vcan)** for reproducibility.

Supported environment:
- OS: Linux (Ubuntu tested)
- CAN stack: SocketCAN
- interface: `vcan0`

No MCU firmware is included in this repository.

# Main Use Cases

## 1. Capture CAN traffic

Capture CAN frames from SocketCAN interface and log them in **JSON Lines format**.
Each frame is logged as one JSON event.
Example use case: `diagpack capture --iface vcan0 --output log.jsonl`

Expected behavior:

- read frames from SocketCAN
- timestamp frames
- store events as JSON lines
- allow interruption (CTRL+C)

## 2. Replay recorded traffic

Replay a previously recorded CAN log.
Example: `diagpack replay --input log.jsonl --iface vcan0`

Replay modes:

- real-time
- accelerated (x2, x5, x10)

Optional filters:

- CAN ID
- time window

Example: diagpack replay --input log.jsonl --iface vcan0 --speed 5

## 3. Basic stress testing

Inject perturbations to stress a prototype.

Stress modes (MVP):

- burst injection
- random CAN frames
- timing jitter

Example: `diagpack stress --iface vcan0 --mode burst`

Purpose:

- simulate traffic spikes
- reveal missing error handling
- expose fragile firmware behavior

# Logging Format

DiagPack uses **JSON Lines** (`.jsonl`).

Each event corresponds to one CAN frame.

Example: `{"ts": 1700000000.123, "id": 256, "dlc": 8, "data": "1122334455667788"}`

Fields:

| Field | Description |
|------|-------------|
| ts | timestamp (seconds, float) |
| id | CAN identifier |
| dlc | data length code |
| data | hex payload |

Optional fields (future):

- flags
- interface
- direction

# Command Line Interface

The tool is a **CLI application**.

Base command: diagpack <command>

Commands:
- capture
- replay
- stress

Examples:
- `diagpack capture --iface vcan0 --output log.jsonl`
- `diagpack replay --input log.jsonl --iface vcan0`
- `diagpack stress --iface vcan0`

# Architecture Goals

The project should remain simple but structured.

Recommended modules:
- diagpack/
- cli/
- capture/
- replay/
- stress/
- logging/
- can/

Responsibilities:

- `cli`: command parsing
- `capture`: frame capture
- `replay`: replay engine
- `stress`: traffic injection
- `logging`: JSON serialization
- `can`: SocketCAN abstraction

---

# Non-Goals (MVP)

The following features are **explicitly excluded from the MVP**:

- GUI
- DBC decoding
- protocol decoding (J1939, CANopen, UDS)
- cybersecurity features
- advanced statistical analysis
- multi-bus orchestration

These may be considered for future versions.

# Demonstration

The repository must include a **reproducible demo** using `vcan`.

## create vcan interface

sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

## start capture

diagpack capture --iface vcan0 --output demo.jsonl

## generate traffic

cansend vcan0 123#1122334455667788

## replay traffic

diagpack replay --input demo.jsonl --iface vcan0
