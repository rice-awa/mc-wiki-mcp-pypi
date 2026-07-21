"""Environment-variable based configuration for the MCP server."""

from __future__ import annotations

import os


def _env(key: str, default: str) -> str:
    return os.getenv(key, default)


def _env_int(key: str, default: int) -> int:
    raw = os.getenv(key)
    if raw is None or raw == "":
        return default
    return int(raw)


def _resolve_api_base() -> str:
    """Prefer MC_WIKI_API_BASE_URL, fall back to API_BASE_URL (server.py style)."""
    return (
        os.getenv("MC_WIKI_API_BASE_URL")
        or os.getenv("API_BASE_URL")
        or "https://mcwiki.rice-awa.top"
    )


# Wiki API
WIKI_API_BASE_URL = _resolve_api_base()
DEFAULT_TIMEOUT = _env_int("MC_WIKI_API_TIMEOUT", 60)

# MCP server
MCP_SERVER_NAME = _env("MC_WIKI_MCP_NAME", "Minecraft Wiki")
MCP_TRANSPORT = _env("MC_WIKI_MCP_TRANSPORT", "stdio")
MCP_HOST = _env("MC_WIKI_MCP_HOST", "0.0.0.0")
MCP_PORT = _env_int("MC_WIKI_MCP_PORT", 3001)

# Logging
LOG_LEVEL = _env("MC_WIKI_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Public CLI/env names. "http" maps to the SDK transport "streamable-http".
SUPPORTED_TRANSPORTS = ("stdio", "sse", "http")
TRANSPORT_ALIASES = {
    "streamable-http": "http",  # accept old name for compatibility
}
