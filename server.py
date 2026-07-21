"""Local convenience entry for streamable-http (dev / docker).

Production / uvx users should prefer:

    uvx mc-wiki-fetch-mcp
    uvx mc-wiki-fetch-mcp --transport streamable-http --port 3001

This script keeps a simple `python server.py` path that defaults to
streamable-http, matching the previous standalone behaviour.
"""

from mc_wiki_fetch_mcp import main

if __name__ == "__main__":
    main(
        [
            "--transport",
            "streamable-http",
        ]
    )
