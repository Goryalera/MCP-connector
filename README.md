# DataLens MCP connector

MCP server for Claude that exposes Yandex DataLens Public API operations as tools. It follows the FastMCP + Streamable HTTP deployment pattern: endpoint `/mcp`, tool annotations, TCP healthcheck, and nginx buffering disabled for streaming responses.

## What it can do

- Check DataLens Public API connectivity with `getWorkbooksList`.
- Call any DataLens RPC method through `datalens_rpc`.
- List entries, workbook entries, collection content, and workbooks.
- Create workbooks.
- Get, create, update, and delete dashboards.
- Build a dashboard `entry` payload skeleton that matches the official `createDashboard` envelope.

The connector intentionally keeps DataLens payloads transparent. DataLens dashboard/chart item schemas are partly documented as `unknown`, so Claude can generate or adjust native JSON payloads while the MCP server handles authentication, HTTP calls, validation, and deployment transport.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

Edit `.env`:

```env
DATALENS_TOKEN=your_iam_token
DATALENS_ORG_ID=your_org_id
DATALENS_API_BASE=https://api.datalens.tech
DATALENS_API_VERSION=1
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
- `datalens_rpc`
- `datalens_raw_request`
- `datalens_get_entries`
- `datalens_get_workbook_entries`
- `datalens_get_entries_relations`
- `datalens_get_collection_content`
- `datalens_get_workbooks_list`
- `datalens_get_workbook`
- `datalens_create_workbook`
- `datalens_get_dashboard`
- `datalens_build_dashboard_spec`
- `datalens_create_dashboard`
- `datalens_update_dashboard`
- `datalens_delete_dashboard`

## Notes

The implementation follows the official DataLens Public API docs: `POST https://api.datalens.tech/rpc/<method>`, `x-dl-api-version: 1`, `x-dl-org-id: <ORG_ID>`, and `Authorization: Bearer <IAM_TOKEN>`. If DataLens adds a method that is not wrapped yet, call it through `datalens_rpc`.
