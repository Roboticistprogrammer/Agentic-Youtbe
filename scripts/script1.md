# Zenoh Protocol in PX4 1.17

Title alternatives:
- Zenoh + PX4 v1.17: Low-latency middleware for constrained drones
- PX4 v1.17: Enabling Zenoh (rmw_zenoh) for ROS2 workflows
- How to build and test Zenoh in PX4 v1.17 (FMU and SITL)

Hook — promise:
PX4 v1.17 ships a matured in-tree Zenoh middleware (rmw_zenoh) that finally makes low-latency, wire-efficient comms practical for constrained flight controllers — in this video I'll show you how to enable it, build firmware, and run a simple publisher/subscriber test so you can get a reliable demo running today.

Stakes (why you should care):
- Zenoh reduces network overhead and gives lower-latency pub/sub for edge devices — if you need reliable ROS2 messaging across unreliable links or on modest hardware, this changes what you can run onboard.

Segment 1 — Setup (what you'll need)
- Hardware/OS: a dev machine (Ubuntu 20.04/22.04 recommended), PX4 source, and either an FMU board (v6x family recommended for default Zenoh build) or SITL.
- Tools: `git`, `make`, `cmake`, the PX4 toolchain, and the Zenoh CLI/tools (install from https://zenoh.io/docs/getting-started/installation/).
- Versions: PX4 v1.17 firmware; Zenoh in-tree is matured to `rmw_zenoh` compatibility (CDRv1 serialization, ROS 2 graph liveliness, auto-generated config from `dds_topics.yaml`, Domain ID parameter).

Segment 2 — Build and enable Zenoh in PX4
1. Clone PX4 and checkout the v1.17 tag or branch:

```bash
git clone https://github.com/PX4/PX4-Autopilot.git
cd PX4-Autopilot
git checkout v1.17.0
```

2. Build for SITL with Zenoh (quick test):

```bash
make px4_sitl_zenoh
```

3. Build for FMU-v6x with Zenoh built into default firmware (for supported targets):

```bash
make px4_fmu-v6xrt_default
# or for a zenoh variant on FMU-v6x
make px4_fmu-v6x_zenoh
```

Notes and tips:
- The v1.17 release explicitly documents the Zenoh middleware improvements: Domain ID parameter, Zenoh CLI support, and rmw_zenoh compatibility. Use the Zenoh CLI to inspect network status and topics during testing.
- If building for hardware, confirm your board supports the FMU-v6xRT target or use the zenoh build variant that matches your FMU.

Segment 3 — Quick integration test (publisher/subscriber)
1. Start a Zenoh router or use the default local mode for a quick test. Follow Zenoh docs to install and run `zenohd` or use the CLI for ephemeral tests.

2. On the PX4 (SITL or device) enable the middleware and ensure `Domain ID` and configuration are set in the auto-generated config from `dds_topics.yaml`.

3. Run a simple publisher on your machine (example using zenoh CLI or a small Python script that publishes a topic), and on PX4 confirm the corresponding ROS2 topic or rmw_zenoh mapping is active.

What to demo on camera:
- Show the build command and a successful build artifact.
- Start `zenohd` or the chosen router and show `zenoh` CLI listing topics.
- Run the publisher and show PX4 logs or `ros2 topic echo` (or equivalent) receiving messages.
- If possible, show SITL telemetry streaming over the Zenoh-enabled middleware so viewers can see actual messages flowing.

Troubleshooting checklist (for viewers like Amir):
- Versions mismatch: ensure PX4 tag is v1.17 and Zenoh tools are recent.
- Build variant: verify you used the `_zenoh` build variant when your target requires it.
- Network: if using devices on different networks, check Domain ID and connectivity with `zenoh` CLI.

Closing / next steps
- If you'd like, I can add the exact `zenohd`/CLI commands and a minimal Python publisher to drop into your workstation for a live demo.
- End-screen CTA: (will draft after you provide the pushed-video target or transcript.)

S1 calibration — your action required:
Before we go further — please rewrite the hook or Segment 1 yourself and paste it here. I'll use it to redraft all remaining segments to match.

