"""Server scaffold — spin up an Agience-integrated MCP server in a few lines.

    from agience_bridge import create_server

    mcp, bridge = create_server("agience-server-example", instructions="…")

    @mcp.tool(description="…")
    async def my_tool(...): ...

    app = bridge.create_app(mcp)   # ASGI app with delegation-token capture
"""

from __future__ import annotations

import os
from typing import Optional, Tuple

from .auth import Bridge


def create_server(
    name: str,
    *,
    instructions: str = "",
    api_uri: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Tuple[object, Bridge]:
    """Build a FastMCP server + an Agience :class:`Bridge` wired for delegation auth.

    ``api_uri`` defaults to ``$AGIENCE_API_URI`` (or localhost:8081); ``api_key``
    to ``$AGIENCE_API_KEY``. Returns ``(mcp, bridge)`` — define tools on ``mcp``,
    then serve ``bridge.create_app(mcp)``.
    """
    from mcp.server.fastmcp import FastMCP  # lazy: importing this package needs no mcp

    bridge = Bridge(
        name,
        api_uri or os.getenv("AGIENCE_API_URI", "http://localhost:8081"),
        api_key=api_key or os.getenv("AGIENCE_API_KEY"),
    )
    mcp = FastMCP(name, instructions=instructions)
    return mcp, bridge
