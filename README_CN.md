# Minecraft Wiki MCP Server

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![中文](https://img.shields.io/badge/lang-中文-red.svg)](README_CN.md)

## 项目简介

一个基于 **MCP** 的 **Minecraft Wiki** 服务器，提供对中文 Minecraft Wiki 内容的便捷访问。在同一项目中同时支持 **stdio**、**SSE**、**streamable-http** 三种传输方式，可通过 **uvx** 一键部署。

注意：本项目仅提供 MCP 层，后端仍依赖 Minecraft wiki API。如需本地搭建 API，请前往 [minecraft-wiki-fetch-api](https://github.com/rice-awa/minecraft-wiki-fetch-api)。

### 功能特性

- 🔍 **Wiki 搜索**: 支持中文关键词搜索，内置「少而精」的搜索提示
- 📄 **页面获取**: 默认 wikitext（省 token、保留模板语义），可选 html
- ✅ **页面存在性检查**: 快速检查页面是否存在（含重定向信息）
- 📚 **命名空间列表**: 获取命名空间 ID → 名称映射，配合搜索使用
- 🏥 **健康检查**: 监控后端 Wiki API 状态
- 🔌 **多传输协议**: `stdio`（Claude Desktop 等本地客户端）、`streamable-http`（远程/服务器）、`sse`（兼容旧客户端）
- 🚀 **一键部署**: 支持 `uvx`，无需本地安装
- ⚙️ **环境变量 + CLI**: 灵活配置

## 快速开始

### 🚀 推荐：使用 uvx

```bash
# stdio（默认）—— Claude Desktop / 本地 MCP 客户端
uvx mc-wiki-fetch-mcp

# streamable-http —— 远程 / 服务器部署
uvx mc-wiki-fetch-mcp --transport streamable-http --host 0.0.0.0 --port 3001

# 自定义 Wiki API 地址
uvx mc-wiki-fetch-mcp --api-url http://localhost:3000

# 或使用环境变量
MC_WIKI_API_BASE_URL=http://localhost:3000 \
MC_WIKI_MCP_TRANSPORT=streamable-http \
uvx mc-wiki-fetch-mcp

# 查看帮助
uvx mc-wiki-fetch-mcp --help
```

### 💻 与 Claude Desktop / Cherry Studio 集成（stdio）

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

Windows 若 `uvx` 无法直接启动，可尝试：

```json
{
  "mcpServers": {
    "minecraft-wiki": {
      "command": "cmd",
      "args": ["/c", "uvx", "mc-wiki-fetch-mcp"],
      "env": {
        "MC_WIKI_API_BASE_URL": "https://mcwiki.rice-awa.top"
      }
    }
  }
}
```

### 🌐 远程 / HTTP 客户端（streamable-http）

```bash
uvx mc-wiki-fetch-mcp -t streamable-http --host 0.0.0.0 --port 3001
```

MCP 客户端连接到 `http://<host>:3001/mcp`（MCP Python SDK 默认 streamable-http 路径）。

## 配置选项

### 环境变量

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `MC_WIKI_API_BASE_URL` / `API_BASE_URL` | Wiki API 基础 URL | `https://mcwiki.rice-awa.top` |
| `MC_WIKI_API_TIMEOUT` | API 请求超时（秒） | `60` |
| `MC_WIKI_MCP_TRANSPORT` | 传输协议：`stdio` / `sse` / `streamable-http` | `stdio` |
| `MC_WIKI_MCP_HOST` | HTTP/SSE 绑定地址 | `0.0.0.0` |
| `MC_WIKI_MCP_PORT` | HTTP/SSE 绑定端口 | `3001` |
| `MC_WIKI_MCP_NAME` | MCP 服务器显示名称 | `Minecraft Wiki` |
| `MC_WIKI_LOG_LEVEL` | 日志级别 | `INFO` |

### 命令行参数

| 参数 | 说明 |
|------|------|
| `--transport`, `-t` | `stdio` / `sse` / `streamable-http` |
| `--host` | HTTP/SSE 绑定地址 |
| `--port`, `-p` | HTTP/SSE 绑定端口 |
| `--api-url` | Wiki API 基础 URL |
| `--timeout` | API 请求超时（秒） |
| `--log-level` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `--name` | MCP 服务器显示名称 |
| `--version` | 显示版本 |
| `--help` | 显示帮助 |

优先级：**命令行参数 > 环境变量 > 默认值**。

## 可用工具

| 工具 | 功能 | 主要参数 |
|------|------|----------|
| `search_wiki` | 搜索中文 Minecraft Wiki | `q`, `limit`, `namespaces` |
| `get_page` | 获取页面内容（wikitext/html） | `pageName`, `format`, `useCache`, `includeMetadata` |
| `check_page_exists` | 检查页面是否存在 | `pageName` |
| `check_health` | 检查 Wiki API 健康状态 | — |
| `list_namespaces` | 列出命名空间 ID → 名称映射 | — |

### Agent 使用提示

- `search_wiki` 请用 **1–3 个游戏名词**；堆砌关键词会**缩小**结果范围。
- `get_page` 默认 **wikitext**（推荐）。仅在模板无法理解时改用 `html`。
- wikitext 里遇到不认识的 `{{Template}}` → 用 `search_wiki` 并传 `namespaces=[10]` 查模板文档。

## 传统安装（开发者）

```bash
git clone <repository-url>
cd mc-wiki-mcp-pypi

pip install -e .
# 或: uv pip install -e .

# stdio
mc-wiki-fetch-mcp

# streamable-http
mc-wiki-fetch-mcp -t streamable-http -p 3001
```

## 故障排除

### uvx 命令不存在

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或
pip install uv
```

### 无法连接 Wiki API

```bash
echo $MC_WIKI_API_BASE_URL
curl http://your-api-url/health
MC_WIKI_LOG_LEVEL=DEBUG uvx mc-wiki-fetch-mcp
```

### 客户端中看不到工具

1. 确认 `uvx mc-wiki-fetch-mcp --version` 可用
2. 查看客户端日志
3. 重启客户端

## 相关文档

- [API 文档](docs/API_DOCUMENTATION.md) — 详细接口说明
- [修改总结](docs/MODIFICATION_SUMMARY.md) — 近期打包与重构说明

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License — 详见 [LICENSE](./LICENSE)。

## 获取帮助

1. 查看上方故障排除
2. 浏览 [docs/](docs/)
3. 提交 Issue 并附上日志

---

**快速提示**
- 🚀 **本地客户端**: `uvx mc-wiki-fetch-mcp`（stdio）
- 🌐 **服务器模式**: `uvx mc-wiki-fetch-mcp -t streamable-http -p 3001`
- ⚙️ **配置**: 环境变量或 CLI 参数
- 🔧 **开发**: `pip install -e .`
