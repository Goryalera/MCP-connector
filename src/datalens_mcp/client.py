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

        auth_scheme = self.settings.datalens_auth_scheme.strip() or "Bearer"
        return {
            "Authorization": f"{auth_scheme} {self.settings.datalens_token}",
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

    async def healthcheck(self) -> dict[str, Any]:
        path = self.settings.health_path
        return await self.request("GET", path)

    async def list_entries(
        self,
        *,
        workbook_id: str = "",
        collection_id: str = "",
        limit: int = 50,
    ) -> Any:
        params: dict[str, Any] = {"limit": limit}
        if workbook_id:
            params["workbookId"] = workbook_id
        if collection_id:
            params["collectionId"] = collection_id
        return await self.request("GET", self.settings.entries_path, params=params)

    async def get_entry(self, entry_id: str) -> Any:
        return await self.request("GET", f"{self.settings.entries_path.rstrip('/')}/{entry_id}")

    async def create_dashboard(self, payload: dict[str, Any]) -> Any:
        return await self.request("POST", self.settings.dashboards_path, json_body=payload)
