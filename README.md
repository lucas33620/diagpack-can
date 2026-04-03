# DiagPack CAN

DiagPack CAN is a lightweight Linux / SocketCAN toolbox built to make CAN-based prototypes easier to observe, replay, and stress.

It is made for a simple goal: expose what the firmware does not say yet.

What it can do:
- capture CAN traffic into JSONL logs
- replay a recorded log with timing
- filter replay by CAN ID or time window
- send a simple burst to stress a target
- run a reproducible demo on `vcan0` (may be modify)

## Why use it

A prototype can work in demo conditions and still fail in the field.

DiagPack CAN helps make issues easier to reproduce and inspect, such as:
- silent errors
- weak diagnostics
- missing counters or fault codes
- inconsistent behavior under load
- poor observability during debug

## Scope

Current MVP:
- Linux only
- SocketCAN only
- PC-side only
- CLI-first workflow

Not a full CAN analyzer.  
Not a GUI tool.  
Not a cybersecurity suite.

## Install

```bash
git clone https://github.com/lucas33620/diagpack-can.git
cd diagpack-can
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Prepare `vcan0`:

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

## Quick start

Capture:
```bash
python -m diagpack capture --iface vcan0 --output capture.jsonl
```

Replay:
```bash
python -m diagpack replay --iface vcan0 --file capture.jsonl
```

Replay with filters:
```bash
python -m diagpack replay --iface vcan0 --file capture.jsonl --id 123 291
python -m diagpack replay --iface vcan0 --file capture.jsonl --start 2.0 --end 6.0
```

Stress:
```bash
python -m diagpack stress --iface vcan0 --id 0x123 --data 11223344 --count 50
```

## Demo

Watch traffic:

```bash
candump -t d vcan0
```

Run the demo:

```bash
python demo/diagpack_vcan0_demo.py
```

The demo:
1. replays a sample log
2. sends a simple burst

Sample log:
```text
demo/logs/sample_log.jsonl
```

## Log format

One JSON object per line:

```json
{"ts": 1.0, "id": 123, "dlc": 4, "data": "11223344"}
{"ts": 2.0, "id": 291, "dlc": 2, "data": "AABB"}
```

## License

MIT
