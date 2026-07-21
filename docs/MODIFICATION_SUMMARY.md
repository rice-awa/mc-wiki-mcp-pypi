# v0.5.0 修改总结：stdio + HTTP 统一包

## 目标

把原先仅 stdio 的 PyPI 包，与独立 HTTP 版工具设计合并为同一项目：

- 一套工具定义
- 三种传输：`stdio` / `sse` / `http`
- 仍可通过 `uvx mc-wiki-fetch-mcp` 一键运行

## 主要变更

### 1. 包结构

```
src/mc_wiki_fetch_mcp/
  __init__.py   # CLI 入口 main()、日志、参数解析
  __main__.py   # python -m mc_wiki_fetch_mcp
  config.py     # 环境变量配置
  server.py     # FastMCP 工具注册
```

统一入口：`mc-wiki-fetch-mcp` / `python -m mc_wiki_fetch_mcp`。

### 2. 工具

| 工具 | 返回类型 | 说明 |
|------|----------|------|
| `search_wiki` | `str` | 参数 `q` / `limit` / `namespaces: list[int]`，精简搜索提示 |
| `get_page` | `str` | 替代旧 `get_wiki_page`；仅 `wikitext` / `html` |
| `check_page_exists` | `str` | 参数 `pageName` |
| `check_health` | `str` | 替代旧 `check_wiki_api_health` |
| `list_namespaces` | `str` | 新增 |

已移除：`get_wiki_pages_batch`、MCP resources、旧 JSON dict 返回格式。

HTTP 客户端由 `aiohttp` 改为 **`httpx`**。

### 3. 多传输启动

```bash
# 默认 stdio（兼容 Claude Desktop / uvx 旧用法）
mc-wiki-fetch-mcp

# 服务器模式
mc-wiki-fetch-mcp -t http --host 0.0.0.0 --port 3001

# 兼容旧 SSE
mc-wiki-fetch-mcp -t sse --port 3001
```

环境变量：`MC_WIKI_MCP_TRANSPORT` / `MC_WIKI_MCP_HOST` / `MC_WIKI_MCP_PORT`。

### 4. 配置

| 来源 | 说明 |
|------|------|
| 环境变量 | `MC_WIKI_*`，并兼容 `API_BASE_URL` |
| CLI | `--transport` `--host` `--port` `--api-url` 等，覆盖环境变量 |

### 5. 版本

`0.4.0` → **`0.5.0`**（工具 API 有破坏性变更：名称与返回类型均改变）。

## 兼容性说明

- **传输默认仍是 stdio**：现有 Claude Desktop / Cherry Studio 配置无需改传输参数。
- **工具名与参数有 breaking change**：若客户端侧有硬编码旧工具名（如 `get_wiki_page`），需改为 `get_page` 等。
