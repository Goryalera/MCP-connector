import asyncio
from typing import Any

from datalens_mcp.client import DataLensClient
from datalens_mcp.config import Settings


class RecordingClient(DataLensClient):
    def __init__(self) -> None:
        super().__init__(
            Settings(
                datalens_token="token",
                datalens_org_id="org",
            )
        )
        self.calls: list[tuple[str, dict[str, Any] | None]] = []

    async def rpc(self, method_name: str, body: dict[str, Any] | None = None) -> Any:
        self.calls.append((method_name, body))
        return {"ok": True}


def test_headers_include_datalens_public_api_requirements() -> None:
    client = RecordingClient()

    headers = client._headers()

    assert headers["Authorization"] == "Bearer token"
    assert headers["x-dl-api-version"] == "1"
    assert headers["x-dl-org-id"] == "org"


def test_get_workbook_entries_uses_rpc_body() -> None:
    client = RecordingClient()

    asyncio.run(
        client.get_workbook_entries(
            workbook_id="wb1",
            page_size=25,
            scope="dash",
            name="Sales",
        )
    )

    assert client.calls == [
        (
            "getWorkbookEntries",
            {
                "workbookId": "wb1",
                "includePermissionsInfo": False,
                "page": 0,
                "pageSize": 25,
                "orderBy": {"field": "name", "direction": "asc"},
                "scope": "dash",
                "filters": {"name": "Sales"},
            },
        )
    ]


def test_create_dashboard_uses_official_rpc_envelope() -> None:
    client = RecordingClient()

    asyncio.run(client.create_dashboard({"name": "Sales"}, mode="publish"))

    assert client.calls == [
        ("createDashboard", {"entry": {"name": "Sales"}, "mode": "publish"})
    ]
