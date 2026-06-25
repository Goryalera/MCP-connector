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
    """Check whether DataLens Public API accepts the configured IAM token and org id."""
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
async def datalens_rpc(method_name: str, body: dict[str, Any] | None = None) -> Any:
    """Call a DataLens Public API RPC method, for example getEntriesRelations."""
    return await _client().rpc(method_name, body)


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_get_entries(
    page: int = 0,
    page_size: int = 50,
    name: str = "",
    include_data: bool = False,
    include_links: bool = False,
    include_permissions_info: bool = False,
    ignore_workbook_entries: bool = False,
    order_field: Literal["createdAt", "name"] = "name",
    order_direction: Literal["asc", "desc"] = "asc",
) -> Any:
    """Search DataLens entries with the official getEntries RPC method."""
    return await _client().get_entries(
        page=page,
        page_size=page_size,
        name=name,
        include_data=include_data,
        include_links=include_links,
        include_permissions_info=include_permissions_info,
        ignore_workbook_entries=ignore_workbook_entries,
        order_field=order_field,
        order_direction=order_direction,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_get_workbook_entries(
    workbook_id: str = "",
    page: int = 0,
    page_size: int = 50,
    scope: str = "",
    name: str = "",
    include_permissions_info: bool = False,
    order_field: Literal["createdAt", "name"] = "name",
    order_direction: Literal["asc", "desc"] = "asc",
) -> Any:
    """List entries inside a DataLens workbook."""
    settings = get_settings()
    resolved_workbook_id = workbook_id or settings.default_workbook_id
    return await _client().get_workbook_entries(
        workbook_id=resolved_workbook_id,
        page=page,
        page_size=page_size,
        scope=scope,
        name=name,
        include_permissions_info=include_permissions_info,
        order_field=order_field,
        order_direction=order_direction,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_get_entries_relations(
    entry_ids: list[str],
    link_direction: Literal["from", "to"] | None = None,
    scope: str = "",
    limit: int = 50,
    page_token: str = "",
    include_permissions_info: bool = False,
) -> Any:
    """Get related DataLens entries for one or more entry IDs."""
    return await _client().get_entries_relations(
        entry_ids=entry_ids,
        link_direction=link_direction,
        scope=scope,
        limit=limit,
        page_token=page_token,
        include_permissions_info=include_permissions_info,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_get_collection_content(
    collection_id: str | None = None,
    page: str | None = None,
    page_size: int = 50,
    filter_string: str = "",
    mode: Literal["all", "onlyCollections", "onlyWorkbooks"] = "all",
    order_field: Literal["title", "createdAt", "updatedAt"] = "title",
    order_direction: Literal["asc", "desc"] = "asc",
    only_my: bool = False,
    include_permissions_info: bool = False,
) -> Any:
    """List collections and workbooks in a DataLens collection."""
    settings = get_settings()
    resolved_collection_id = collection_id or settings.default_collection_id or None
    return await _client().get_collection_content(
        collection_id=resolved_collection_id,
        page=page,
        page_size=page_size,
        filter_string=filter_string,
        mode=mode,
        order_field=order_field,
        order_direction=order_direction,
        only_my=only_my,
        include_permissions_info=include_permissions_info,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_get_workbooks_list(
    collection_id: str | None = None,
    page: int = 0,
    page_size: int = 50,
    filter_string: str = "",
    order_field: Literal["title", "createdAt", "updatedAt"] = "title",
    order_direction: Literal["asc", "desc"] = "asc",
    only_my: bool = False,
    include_permissions_info: bool = False,
) -> Any:
    """List DataLens workbooks."""
    settings = get_settings()
    resolved_collection_id = collection_id or settings.default_collection_id or None
    return await _client().get_workbooks_list(
        collection_id=resolved_collection_id,
        page=page,
        page_size=page_size,
        filter_string=filter_string,
        order_field=order_field,
        order_direction=order_direction,
        only_my=only_my,
        include_permissions_info=include_permissions_info,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_get_workbook(
    workbook_id: str = "",
    include_permissions_info: bool = False,
) -> Any:
    """Get a DataLens workbook by ID."""
    settings = get_settings()
    return await _client().get_workbook(
        workbook_id or settings.default_workbook_id,
        include_permissions_info=include_permissions_info,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_create_workbook(
    title: str,
    description: str = "",
    collection_id: str | None = None,
) -> Any:
    """Create a DataLens workbook."""
    settings = get_settings()
    resolved_collection_id = collection_id or settings.default_collection_id or None
    return await _client().create_workbook(
        title=title,
        description=description,
        collection_id=resolved_collection_id,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_get_dashboard(
    dashboard_id: str,
    workbook_id: str = "",
    rev_id: str = "",
    branch: Literal["published", "saved"] | None = None,
    include_permissions: bool = False,
    include_links: bool = False,
    include_favorite: bool = False,
) -> Any:
    """Get a DataLens dashboard by ID."""
    settings = get_settings()
    return await _client().get_dashboard(
        dashboard_id,
        workbook_id=workbook_id or settings.default_workbook_id,
        rev_id=rev_id,
        branch=branch,
        include_permissions=include_permissions,
        include_links=include_links,
        include_favorite=include_favorite,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_build_dashboard_spec(draft: dict[str, Any]) -> dict[str, Any]:
    """
    Build a createDashboard payload skeleton from native DataLens dashboard items.

    This does not call DataLens. The returned `entry` can be passed to
    datalens_create_dashboard after checking the native item payloads.
    """
    return build_dashboard_spec(DashboardDraft.model_validate(draft))


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_create_dashboard(
    entry: dict[str, Any],
    mode: Literal["save", "publish"] = "save",
) -> Any:
    """Create a DataLens dashboard from a DataLens-compatible entry payload."""
    return await _client().create_dashboard(entry, mode=mode)


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def datalens_update_dashboard(
    entry: dict[str, Any],
    mode: Literal["save", "publish"] = "save",
) -> Any:
    """Update a DataLens dashboard from a DataLens-compatible entry payload."""
    return await _client().update_dashboard(entry, mode=mode)


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": True,
    }
)
async def datalens_delete_dashboard(dashboard_id: str, lock_token: str = "") -> Any:
    """Delete a DataLens dashboard by ID."""
    return await _client().delete_dashboard(dashboard_id, lock_token=lock_token)


def main() -> None:
    settings = get_settings()
    mcp.run(
        transport="streamable-http",
        host=settings.mcp_host,
        port=settings.mcp_port,
    )


if __name__ == "__main__":
    main()
