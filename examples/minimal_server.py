"""Minimal Agience MCP server built on agience-bridge.

Run:
    pip install agience-bridge uvicorn
    AGIENCE_API_URI=http://localhost:8081 python examples/minimal_server.py
"""

import json

from agience_bridge import create_server

mcp, bridge = create_server(
    "agience-server-example",
    instructions="Example server demonstrating agience-bridge.",
)


@mcp.tool(description="Echo a message back, with the calling user's id.")
async def echo(message: str) -> str:
    return json.dumps({"echo": message, "user": bridge.get_user_id()})


@mcp.tool(description="Search the caller's authorized artifacts via Agience.")
async def search(query: str, size: int = 10) -> str:
    result = await bridge.client().search_query(query_text=query, candidate_budget=size * 5)
    return json.dumps(result)


app = bridge.create_app(mcp)


if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(app, host=os.getenv("MCP_HOST", "0.0.0.0"), port=int(os.getenv("MCP_PORT", "8099")))
