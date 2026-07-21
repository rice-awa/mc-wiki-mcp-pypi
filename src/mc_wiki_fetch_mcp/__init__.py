"""Minecraft Wiki MCP Server — stdio / SSE / http unified entry."""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Optional

from . import config
from .server import create_mcp_server

__version__ = "0.5.0"
__all__ = ["main", "create_mcp_server", "__version__"]


class StderrHandler(logging.StreamHandler):
    """Logging handler that always writes to stderr.

    Required for stdio transport so protocol messages on stdout stay clean.
    """

    def __init__(self) -> None:
        super().__init__(sys.stderr)


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """Configure package-wide logging to stderr."""
    log_level_name = (level or config.LOG_LEVEL).upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    logging.basicConfig(
        level=log_level,
        format=config.LOG_FORMAT,
        handlers=[StderrHandler()],
        force=True,
    )
    return logging.getLogger("mc-wiki-mcp")


def normalize_transport(name: str) -> str:
    """Normalize public transport names (e.g. streamable-http -> http)."""
    return config.TRANSPORT_ALIASES.get(name, name)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments. Environment variables remain the base defaults."""
    parser = argparse.ArgumentParser(
        prog="mc-wiki-fetch-mcp",
        description=(
            "Minecraft Wiki MCP Server — supports stdio, SSE and "
            "http transports in a single package."
        ),
    )
    parser.add_argument(
        "--transport",
        "-t",
        choices=list(config.SUPPORTED_TRANSPORTS),
        default=None,
        help=(
            "MCP transport protocol: stdio / sse / http "
            f"(default: env MC_WIKI_MCP_TRANSPORT or '{config.MCP_TRANSPORT}')"
        ),
    )
    parser.add_argument(
        "--host",
        default=None,
        help=(
            "Bind host for HTTP/SSE transports "
            f"(default: env MC_WIKI_MCP_HOST or '{config.MCP_HOST}')"
        ),
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=None,
        help=(
            "Bind port for HTTP/SSE transports "
            f"(default: env MC_WIKI_MCP_PORT or {config.MCP_PORT})"
        ),
    )
    parser.add_argument(
        "--api-url",
        default=None,
        help=(
            "Wiki API base URL (default: env MC_WIKI_API_BASE_URL / "
            f"API_BASE_URL or '{config.WIKI_API_BASE_URL}')"
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="API request timeout in seconds",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=None,
        help="Log level (default: env MC_WIKI_LOG_LEVEL or INFO)",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="MCP server display name",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args(argv)


def apply_cli_overrides(args: argparse.Namespace) -> None:
    """Apply CLI arguments on top of environment/config defaults."""
    if args.api_url is not None:
        config.WIKI_API_BASE_URL = args.api_url
    if args.timeout is not None:
        config.DEFAULT_TIMEOUT = args.timeout
    if args.log_level is not None:
        config.LOG_LEVEL = args.log_level
    if args.name is not None:
        config.MCP_SERVER_NAME = args.name
    if args.transport is not None:
        config.MCP_TRANSPORT = normalize_transport(args.transport)
    if args.host is not None:
        config.MCP_HOST = args.host
    if args.port is not None:
        config.MCP_PORT = args.port


def main(argv: Optional[list[str]] = None) -> None:
    """CLI entry point for uvx / console_scripts."""
    args = parse_args(argv)
    apply_cli_overrides(args)

    logger = setup_logging(config.LOG_LEVEL)
    transport = normalize_transport(config.MCP_TRANSPORT)
    host = config.MCP_HOST
    port = config.MCP_PORT

    if transport not in config.SUPPORTED_TRANSPORTS:
        logger.error(
            "Unsupported transport %r. Choose from: %s",
            transport,
            ", ".join(config.SUPPORTED_TRANSPORTS),
        )
        sys.exit(2)

    logger.info("Starting Minecraft Wiki MCP Server v%s...", __version__)
    logger.info("Transport: %s", transport)
    logger.info("Server Name: %s", config.MCP_SERVER_NAME)
    logger.info("Wiki API Base URL: %s", config.WIKI_API_BASE_URL)
    logger.info("Log Level: %s", config.LOG_LEVEL)
    if transport != "stdio":
        logger.info("Listening on %s:%s", host, port)
    logger.info(
        "版权信息: 本工具获取的所有内容均来自中文Minecraft Wiki，"
        "遵循CC BY-NC-SA 3.0协议"
    )

    mcp_server = create_mcp_server(
        name=config.MCP_SERVER_NAME,
        host=host,
        port=port,
    )

    try:
        if transport == "stdio":
            mcp_server.run(transport="stdio")
        elif transport == "sse":
            logger.warning(
                "SSE transport is deprecated by the MCP spec; "
                "prefer http for production."
            )
            mcp_server.run(transport="sse")
        else:
            # Public name is "http"; SDK transport name is streamable-http.
            mcp_server.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error("服务器启动失败: %s", e)
        raise


if __name__ == "__main__":
    main()