# DataLens MCP connector

MCP server for Claude that exposes Yandex DataLens operations as tools. It follows the FastMCP + Streamable HTTP deployment pattern from the Habr article: endpoint `/mcp`, tool annotations, TCP healthcheck, and nginx buffering disabled for streaming responses.

## What it can do

- Check DataLens API connectivity.
- Run controlled raw API requests for unsupported/new DataLens endpoints.
- List workbook or collection entries.
- Create a dashboard from a JSON payload.
- Build a simple dashboard draft spec from a compact chart/layout description.

The connector intentionally keeps DataLens payloads transparent. DataLens dashboard/chart schemas can change, so Claude can generate or adjust JSON payloads while the MCP server handles authentication, HTTP calls, validation, and deployment transport.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

Edit `.env`:

```env
DATALENS_TOKEN=your_token
DATALENS_API_BASE=https://datalens.yandex.cloud/api
DATALENS_AUTH_SCHEME=Bearer
```

Run locally:

```powershell
datalens-mcp
```

The MCP endpoint is:

```text
http://localhost:8000/mcp
```

## Claude

For a remote connector, deploy it behind HTTPS and add this URL in Claude:

```text
https://your-domain.example/mcp
```

In Claude: Settings -> Connectors -> Add custom connector.

## Docker

```powershell
docker compose up -d --build
```

The compose file binds the container to `127.0.0.1:8096`, so expose it through nginx with TLS. See `nginx.example.conf`.

## MCP tools

- `datalens_healthcheck`
- `datalens_raw_request`
- `datalens_list_entries`
- `datalens_get_entry`
- `datalens_create_dashboard`
- `datalens_build_dashboard_spec`

## Notes

The official DataLens documentation has a DataLens Public API section. If a concrete endpoint differs in your account/API version, update `DATALENS_API_BASE`, `DATALENS_ENTRIES_PATH`, `DATALENS_DASHBOARDS_PATH`, or call `datalens_raw_request` with the exact path.
