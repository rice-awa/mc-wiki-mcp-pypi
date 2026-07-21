# Minecraft Wiki MCP Server

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![中文](https://img.shields.io/badge/lang-中文-red.svg)](README_CN.md)

## Project Overview

A **MCP**-based **Minecraft Wiki** server that provides convenient access to Chinese Minecraft Wiki content. Supports **stdio**, **SSE** and **http** transports in a single package, and can be deployed quickly via **uvx**.

Note: This project only provides the MCP layer on top of a Minecraft wiki API. For local API deployment, please visit [minecraft-wiki-fetch-api](https://github.com/rice-awa/minecraft-wiki-fetch-api).

### Features

- 🔍 **Wiki Search**: Search Chinese Minecraft Wiki pages with concise keyword guidance
- 📄 **Page Retrieval**: Get full page content in wikitext (default, token-efficient) or html
- ✅ **Page Existence Check**: Quick check if a page exists (including redirects)
- 📚 **Namespace Listing**: List available wiki namespaces for targeted search
- 🏥 **Health Monitoring**: Monitor backend Wiki API service status
- 🔌 **Multi Transport**: `stdio` (Claude Desktop / local clients), `http` (remote/server), `sse` (legacy)
- 🚀 **One-Click Deployment**: Run via `uvx` without local install
- ⚙️ **Env + CLI Config**: Flexible configuration via environment variables and CLI flags

## Quick Start

### 🚀 Recommended: Using uvx

```bash
# stdio (default) — for Claude Desktop / local MCP clients
uvx mc-wiki-fetch-mcp

# http — for remote / server deployment
uvx mc-wiki-fetch-mcp --transport http --host 0.0.0.0 --port 3001

# Custom Wiki API URL
uvx mc-wiki-fetch-mcp --api-url http://localhost:3000

# Or via environment variables
MC_WIKI_API_BASE_URL=http://localhost:3000 \
MC_WIKI_MCP_TRANSPORT=http \
uvx mc-wiki-fetch-mcp

# Help
uvx mc-wiki-fetch-mcp --help
```

### 💻 Integration with Claude Desktop (stdio)

1. **Config file locations:**
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

2. **Edit configuration:**
   ```json
   {
     "mcpServers": {
       "minecraft-wiki": {
         "command": "uvx",
         "args": ["mc-wiki-fetch-mcp"],
         "env": {
           "MC_WIKI_API_BASE_URL": "https://mcwiki.rice-awa.top"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**

### 🌐 Remote / HTTP clients (http)

```bash
uvx mc-wiki-fetch-mcp -t http --host 0.0.0.0 --port 3001
```

Then point your MCP client to `http://<host>:3001/mcp` (default /mcp path of the MCP Python SDK).

## Configuration Options

### Environment Variables

| Environment Variable | Description | Default |
|----------------------|-------------|---------|
| `MC_WIKI_API_BASE_URL` / `API_BASE_URL` | Wiki API base URL | `https://mcwiki.rice-awa.top` |
| `MC_WIKI_API_TIMEOUT` | API request timeout (seconds) | `60` |
| `MC_WIKI_MCP_TRANSPORT` | Transport: `stdio` / `sse` / `http` | `stdio` |
| `MC_WIKI_MCP_HOST` | Bind host (HTTP/SSE) | `0.0.0.0` |
| `MC_WIKI_MCP_PORT` | Bind port (HTTP/SSE) | `3001` |
| `MC_WIKI_MCP_NAME` | MCP server display name | `Minecraft Wiki` |
| `MC_WIKI_LOG_LEVEL` | Log level | `INFO` |

### Command Line Arguments

| Parameter | Description |
|-----------|-------------|
| `--transport`, `-t` | `stdio` / `sse` / `http` |
| `--host` | Bind host for HTTP/SSE |
| `--port`, `-p` | Bind port for HTTP/SSE |
| `--api-url` | Wiki API base URL |
| `--timeout` | API request timeout (seconds) |
| `--log-level` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `--name` | MCP server display name |
| `--version` | Show version |
| `--help` | Show help |

Priority: **CLI args > environment variables > defaults**.

## Available Tools

| Tool | Description | Main Parameters |
|------|-------------|-----------------|
| `search_wiki` | Search Chinese Minecraft Wiki | `q`, `limit`, `namespaces` |
| `get_page` | Get page content (wikitext/html) | `pageName`, `format`, `useCache`, `includeMetadata` |
| `check_page_exists` | Check whether a page exists | `pageName` |
| `check_health` | Check Wiki API health | — |
| `list_namespaces` | List wiki namespace ID → name map | — |

### Tips for Agents

- Prefer **1–3 game terms** in `search_wiki`; extra keywords **narrow** results.
- Prefer **wikitext** for `get_page` (default). Use `html` only when a template is unreadable.
- Unknown `{{Template}}` in wikitext → call `search_wiki` with `namespaces=[10]`.

## Traditional Installation (Developers)

```bash
git clone <repository-url>
cd mc-wiki-mcp-pypi

pip install -e .
# or: uv pip install -e .

# stdio
mc-wiki-fetch-mcp

# http
mc-wiki-fetch-mcp -t http -p 3001
```

## Troubleshooting

### uvx not found

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

### Cannot connect to Wiki API

```bash
echo $MC_WIKI_API_BASE_URL
curl http://your-api-url/health
MC_WIKI_LOG_LEVEL=DEBUG uvx mc-wiki-fetch-mcp
```

### Tools not visible in Claude Desktop

1. Confirm `uvx mc-wiki-fetch-mcp --version` works
2. Check Claude Desktop logs
3. Restart Claude Desktop

## Related Documentation

- [API Documentation](docs/API_DOCUMENTATION.md) — Detailed API interface documentation
- [Modification Summary](docs/MODIFICATION_SUMMARY.md) — Recent packaging changes

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License — see [LICENSE](./LICENSE).

## Getting Help

1. Check the troubleshooting section above
2. Browse [docs/](docs/)
3. Open an Issue with logs

---

**Quick tips**
- 🚀 **Local client**: `uvx mc-wiki-fetch-mcp` (stdio)
- 🌐 **Server mode**: `uvx mc-wiki-fetch-mcp -t http -p 3001`
- ⚙️ **Configure**: env vars or CLI flags
- 🔧 **Develop**: `pip install -e .`
