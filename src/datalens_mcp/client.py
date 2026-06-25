from __future__ import annotations

from typing import Any, Literal
from urllib.parse import urljoin

import httpx

from datalens_mcp.config import Settings

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


class DataLensError(RuntimeError):
    """Raised when DataLens returns an unsuccessful response."""


class DataLensClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = str(settings.datalens_api_base).rstrip("/") + "/"

    def _headers(self) -> dict[str, str]:
        if not self.settings.datalens_token:
            raise DataLensError("DATALENS_TOKEN is not configured")
        if not self.settings.datalens_org_id:
            raise DataLensError("DATALENS_ORG_ID is not configured")

        auth_scheme = self.settings.datalens_auth_scheme.strip() or "Bearer"
        return {
            "Authorization": f"{auth_scheme} {self.settings.datalens_token}",
            "x-dl-api-version": self.settings.datalens_api_version,
            "x-dl-org-id": self.settings.datalens_org_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _url(self, path: str) -> str:
        clean_path = path.lstrip("/")
        return urljoin(self.base_url, clean_path)

    async def request(
        self,
        method: HttpMethod,
        path: str,
        *,
        json_body: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.request(
                method,
                self._url(path),
                headers=self._headers(),
                json=json_body,
                params=params,
            )

        if response.status_code >= 400:
            raise DataLensError(
                f"DataLens API returned HTTP {response.status_code}: {response.text[:2000]}"
            )

        if not response.content:
            return {"status_code": response.status_code, "ok": True}

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        return {"status_code": response.status_code, "body": response.text}

    async def rpc(self, method_name: str, body: dict[str, Any] | None = None) -> Any:
        return await self.request("POST", f"rpc/{method_name}", json_body=body or {})

    async def healthcheck(self) -> Any:
        return await self.get_workbooks_list(page_size=1)

    async def get_entries(
        self,
        *,
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
        body: dict[str, Any] = {
            "includeData": include_data,
            "includeLinks": include_links,
            "page": page,
            "pageSize": page_size,
            "includePermissionsInfo": include_permissions_info,
            "ignoreWorkbookEntries": ignore_workbook_entries,
            "orderBy": {"field": order_field, "direction": order_direction},
        }
        if name:
            body["filters"] = {"name": name}
        return await self.rpc("getEntries", body)

    async def get_workbook_entries(
        self,
        *,
        workbook_id: str,
        page: int = 0,
        page_size: int = 50,
        scope: str = "",
        name: str = "",
        include_permissions_info: bool = False,
        order_field: Literal["createdAt", "name"] = "name",
        order_direction: Literal["asc", "desc"] = "asc",
    ) -> Any:
        body: dict[str, Any] = {
            "workbookId": workbook_id,
            "includePermissionsInfo": include_permissions_info,
            "page": page,
            "pageSize": page_size,
            "orderBy": {"field": order_field, "direction": order_direction},
        }
        if scope:
            body["scope"] = scope
        if name:
            body["filters"] = {"name": name}
        return await self.rpc("getWorkbookEntries", body)

    async def get_entries_relations(
        self,
        *,
        entry_ids: list[str],
        link_direction: Literal["from", "to"] | None = None,
        scope: str = "",
        limit: int = 50,
        page_token: str = "",
        include_permissions_info: bool = False,
    ) -> Any:
        body: dict[str, Any] = {
            "entryIds": entry_ids,
            "limit": limit,
            "includePermissionsInfo": include_permissions_info,
        }
        if link_direction:
            body["linkDirection"] = link_direction
        if scope:
            body["scope"] = scope
        if page_token:
            body["pageToken"] = page_token
        return await self.rpc("getEntriesRelations", body)

    async def get_collection_content(
        self,
        *,
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
        body: dict[str, Any] = {
            "collectionId": collection_id,
            "page": page,
            "filterString": filter_string,
            "orderField": order_field,
            "orderDirection": order_direction,
            "onlyMy": only_my,
            "mode": mode,
            "pageSize": page_size,
            "includePermissionsInfo": include_permissions_info,
        }
        return await self.rpc("getCollectionContent", body)

    async def get_workbooks_list(
        self,
        *,
        collection_id: str | None = None,
        page: int = 0,
        page_size: int = 50,
        filter_string: str = "",
        order_field: Literal["title", "createdAt", "updatedAt"] = "title",
        order_direction: Literal["asc", "desc"] = "asc",
        only_my: bool = False,
        include_permissions_info: bool = False,
    ) -> Any:
        return await self.rpc(
            "getWorkbooksList",
            {
                "collectionId": collection_id,
                "includePermissionsInfo": include_permissions_info,
                "filterString": filter_string,
                "page": page,
                "pageSize": page_size,
                "orderField": order_field,
                "orderDirection": order_direction,
                "onlyMy": only_my,
            },
        )

    async def get_workbook(self, workbook_id: str, *, include_permissions_info: bool = False) -> Any:
        return await self.rpc(
            "getWorkbook",
            {"workbookId": workbook_id, "includePermissionsInfo": include_permissions_info},
        )

    async def create_workbook(
        self,
        *,
        title: str,
        description: str = "",
        collection_id: str | None = None,
    ) -> Any:
        return await self.rpc(
            "createWorkbook",
            {"collectionId": collection_id, "title": title, "description": description},
        )

    async def get_dashboard(
        self,
        dashboard_id: str,
        *,
        workbook_id: str = "",
        rev_id: str = "",
        branch: Literal["published", "saved"] | None = None,
        include_permissions: bool = False,
        include_links: bool = False,
        include_favorite: bool = False,
    ) -> Any:
        body: dict[str, Any] = {
            "dashboardId": dashboard_id,
            "includePermissions": include_permissions,
            "includeLinks": include_links,
            "includeFavorite": include_favorite,
        }
        if workbook_id:
            body["workbookId"] = workbook_id
        if rev_id:
            body["revId"] = rev_id
        if branch:
            body["branch"] = branch
        return await self.rpc("getDashboard", body)

    async def create_dashboard(
        self,
        entry: dict[str, Any],
        *,
        mode: Literal["save", "publish"] = "save",
    ) -> Any:
        return await self.rpc("createDashboard", {"entry": entry, "mode": mode})

    async def update_dashboard(
        self,
        entry: dict[str, Any],
        *,
        mode: Literal["save", "publish"] = "save",
    ) -> Any:
        return await self.rpc("updateDashboard", {"entry": entry, "mode": mode})

    async def delete_dashboard(self, dashboard_id: str, *, lock_token: str = "") -> Any:
        body = {"dashboardId": dashboard_id}
        if lock_token:
            body["lockToken"] = lock_token
        return await self.rpc("deleteDashboard", body)
