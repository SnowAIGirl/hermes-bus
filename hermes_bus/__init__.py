"""Hermes MessageBus — Unix Domain Socket message bus transport layer.

Long-lived (CLI/Gateway): use BusClient to register an endpoint.
Short-lived (external agent): use send_message() to fire one message and disconnect.
"""
from hermes_bus.client import BusClient, send_message, ensure_bus_running
from hermes_bus.server import BusServer, run_server
