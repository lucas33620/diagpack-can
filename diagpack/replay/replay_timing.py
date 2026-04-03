

def compute_delay(current_ts: float, previous_ts:float, speed: float) -> float:
    if speed <= 0:
        raise ValueError("speed must be > 0")

    delta = current_ts - previous_ts

    if delta < 0:
        return 0.0

    return delta / speed