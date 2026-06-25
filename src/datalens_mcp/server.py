from __future__ import annotations

from typing import Any, Literal

from fastmcp import FastMCP

from datalens_mcp.client import DataLensClient
from datalens_mcp.config import get_settings
from datalens_mcp.dashboard import DashboardDraft, build_dashboard_spec

mcp = FastMCP("datalens-mcp")


def _client() -> DataLensClient:
    return DataLensClient(get_settings())


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_healthcheck() -> dict[str, Any]:
    """Check whether the configured DataLens API endpoint accepts the token."""
    return await _client().healthcheck()


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": True,
    }
)
async def datalens_raw_request(
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
    path: str,
    json_body: dict[str, Any] | list[Any] | None = None,
    params: dict[str, Any] | None = None,
) -> Any:
    """
    Call a DataLens Public API path with the configured bearer token.

    Use this for endpoints not yet wrapped by a dedicated MCP tool.
    """
    return await _client().request(method, path, json_body=json_body, params=params)


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_list_entries(
    workbook_id: str = "",
    collection_id: str = "",
    limit: int = 50,
) -> Any:
    """List DataLens entries in a workbook or collection."""
    settings = get_settings()
    return await _client().list_entries(
        workbook_id=workbook_id or settings.default_workbook_id,
        collection_id=collection_id or settings.default_collection_id,
        limit=limit,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_get_entry(entry_id: str) -> Any:
    """Get a DataLens entry by id."""
    return await _client().get_entry(entry_id)


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_build_dashboard_spec(draft: dict[str, Any]) -> dict[str, Any]:
    """
    Build a dashboard JSON payload from a compact draft.

    This does not call DataLens. Pass the returned payload to
    datalens_create_dashboard after checking it.
    """
    return build_dashboard_spec(DashboardDraft.model_validate(draft))


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_create_dashboard(payload: dict[str, Any]) -> Any:
    """Create a DataLens dashboard from a DataLens-compatible JSON payload."""
    return await _client().create_dashboard(payload)


def main() -> None:
    settings = get_settings()
    mcp.run(
        transport="streamable-http",
        host=settings.mcp_host,
        port=settings.mcp_port,
    )


if __name__ == "__main__":
    main()
