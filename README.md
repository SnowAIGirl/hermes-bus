# hermes-bus

[English](./README.md) | [中文](./README.zh.md)

A generic message bus for Unix Socket IPC — message routing, session management, heartbeat.

Transport-only. Notification logic is injected via configurable hooks — the bus itself knows nothing about audio, display, or LLM context.

## Install

```bash
pip install hermes-bus
```

Or from source:

```bash
git clone https://github.com/mlinquan/hermes-bus.git
cd hermes-bus && pip install -e .
```

## CLI

```bash
# Daemon management
hermes-busd start       # Start the bus daemon
hermes-busd stop        # Stop the daemon
hermes-busd status      # Check daemon + connected endpoints
hermes-busd restart     # Restart the daemon

# Foreground server (for debugging)
hermes-bus-server
```

## Python API

```python
from hermes_bus.client import BusClient, send_message

# Long-lived: register as an endpoint and receive messages
client = BusClient("my-service")
client.connect()
for msg in client.poll():
    print(msg)

# Short-lived: fire-and-forget
send_message("target-service", {"text": "hello", "type": "ack"})
```

## Architecture

```
client.py ──── Unix Socket ──── server.py
  (BusClient)                    (BusServer)
   - Register endpoint           - Session management
   - Heartbeat (60s)             - Message routing
   - Auto-reconnect              - Hook triggers
   - Thread-safe message queue
   
busd.py — Daemon manager: start / stop / status / restart
```

## Protocol

4-byte big-endian length prefix + JSON body. Max payload: 10 MB.

Long-lived connections register an endpoint name and can send/receive. Short-lived connections send one message and disconnect — no registration, no endpoint_map pollution.

## Hooks

After each message is routed, hook scripts are triggered asynchronously. Resolution priority:

1. `HERMES_BUS_HOOKS` env var (comma-separated or JSON array of script paths)
2. `hooks.yaml` config file
3. Default: none (routing handled by hermes-bus-plugin)

Each hook receives the full message JSON on stdin. Hook execution is non-blocking — the bus continues routing.

## Messages

```json
{
  "type": "message",
  "to": "target-endpoint",
  "from": "sender-endpoint",
  "text": "hello",
  "body": { }
}
```

Special message types: `register` (endpoint registration), `ping`/`pong` (heartbeat), `list_endpoints` (admin query).
