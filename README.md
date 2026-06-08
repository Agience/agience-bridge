# agience-bridge

The SDK for building **MCP servers that integrate with Agience** — delegation
auth, a typed core HTTP client, and a server scaffold. It's the bridge between
any MCP server and an Agience deployment.

**Apache-2.0 — permissive on purpose.** `agience-core` is AGPL-3.0, but the
*integration boundary* is permissive so **any** server can build on it:
first-party personas, premium add-ons (e.g. Beacon), and third-party servers
alike — without copyleft reaching their code. This package is integration glue
only; it contains **no platform IP** and depends on nothing from `agience-core`.

## Install

```bash
pip install agience-bridge      # mcp[cli] + httpx
```

## Quickstart

```python
from agience_bridge import create_server

mcp, bridge = create_server("agience-server-foo", instructions="What this server does.")

@mcp.tool(description="Search the caller's authorized artifacts via Agience.")
async def search(query: str, size: int = 10) -> str:
    import json
    return json.dumps(await bridge.client().search_query(query_text=query, candidate_budget=size * 5))

app = bridge.create_app(mcp)     # ASGI app; captures the inbound delegation token
```

Run it like any ASGI app (`uvicorn module:app`). See [`examples/`](examples/).

## What's in it

| Module | Purpose |
|--------|---------|
| `agience_bridge.Bridge` | Captures the inbound **delegation token** per request and forwards it on outbound calls (so Agience authorizes as the **user**); falls back to an API key for user-less calls. `create_app()` wraps a FastMCP app with capture middleware. |
| `agience_bridge.client.AgienceClient` | Typed HTTP helpers to core (`get`/`post`, `search_query`, `invoke`, `get_artifact`), authed via the Bridge. |
| `agience_bridge.create_server()` | Scaffold: returns `(FastMCP, Bridge)` wired together. |

## How auth works

A server **never holds standing user credentials**. Agience issues a delegation
token *for* the server on each user-driven call; the Bridge captures it
(`create_app` middleware) and forwards it (`bridge.user_headers()`), so the
server can only act within that user's authorization. Tokens are decoded
unverified only to surface a user id for logging — **Agience is the verifier**.
For server-to-server calls with no user context, configure an `api_key`
(`$AGIENCE_API_KEY`).

## Positioning

- `agience-core` (AGPL) — the platform.
- **`agience-bridge` (Apache-2.0) — this SDK**, the public integration layer.
- `agience-beacon` (proprietary) — a premium add-on that builds on the bridge.

Env: `AGIENCE_API_URI` (core base URL), `AGIENCE_API_KEY` (optional).
