import time

from diagpack.can.socketcan import open_can_socket
from diagpack.replay.replay_engine import replay_log
from diagpack.stress.burst_mode import send_burst


DEMO_LOG_PATH = "demo/logs/sample_log.jsonl"
DEMO_IFACE = "vcan0"


def main() -> None:
    print("--- DiagPack CAN demo start ---")

    can_socket = open_can_socket(DEMO_IFACE)
    print(f"CAN socket opened on {DEMO_IFACE}")

    try:
        print(f"\n[1/2] Replaying demo log from '{DEMO_LOG_PATH}' without filter")
        with open(DEMO_LOG_PATH, "r", encoding="utf-8") as file:
            replay_log(
                can_socket=can_socket,
                file=file,
                id_filter=None,
                ts_start=None,
                ts_end=None,
                speed=1.0,
            )
        print("Replay completed")

        time.sleep(1.0)

        print("\n[2/2] Sending stress burst")
        send_burst(
            can_socket=can_socket,
            can_id=0x123,
            data_hex="DEADBEEF",
            count=10,
            delay=0.01,
        )
        print("Stress burst completed")

    finally:
        can_socket.close()
        print(f"CAN socket on {DEMO_IFACE} closed")

    print("--- DiagPack CAN demo end ---")


if __name__ == "__main__":
    main()