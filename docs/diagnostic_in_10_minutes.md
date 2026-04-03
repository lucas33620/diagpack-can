# Diagnostic in 10 Minutes

## When to Use It

Use DiagPack CAN when a CAN-based prototype works in demo conditions but starts to show reliability or observability issues in real use.

**Typical signs:**
- Intermittent faults
- Resets that are hard to explain
- Weak or missing diagnostics
- Behavior that is hard to reproduce
- Unclear reaction under burst or repeated traffic

## Mission Scenario

A realistic use case in mission is:

1. Capture a short CAN session from the prototype
2. Replay the same traffic to check whether the behavior is reproducible
3. Narrow the replay to one CAN ID or one time window
4. Inject a simple burst to expose weak spots faster
5. Observe what the firmware reports, and what it does not report

## What the Tool Reveals

DiagPack CAN helps reveal:

- Silent errors
- Lack of fault codes
- Missing counters
- Weak timeout visibility
- Inconsistent recovery behavior
- Watchdog reactions that are unclear or ineffective
- Firmware paths that are difficult to reproduce manually

## What This Opens on the Firmware Side

Once the issue is visible and reproducible, the next firmware improvements are usually clearer:

- Add or clean up fault codes
- Add counters for retries, drops, timeouts, resets
- Improve watchdog cause visibility
- Make error handling more deterministic
- Improve logs for field returns
- Separate nominal behavior from degraded behavior

## Recommended Order in Mission

**Recommended minimal sequence:**

1. Capture a short real session
2. Replay it as-is
3. Replay only the suspicious frames
4. Apply a small burst
5. Note what is visible and what is still invisible

This gives a quick first view of:
- Reproducibility
- Observability
- Robustness under simple stress

## Limits

**Current MVP limits:**

- Linux only
- SocketCAN only
- PC-side only
- No GUI
- No advanced CAN analysis
- No DBC decoding