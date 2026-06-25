from __future__ import annotations

from secrets import token_hex
from typing import Any, Literal

from pydantic import BaseModel, Field


class DashboardItemDraft(BaseModel):
    item: dict[str, Any] = Field(description="Native DataLens dashboard tab item")
    x: int = 0
    y: int = 0
    w: int = 12
    h: int = 8
    parent: str = ""


class DashboardDraft(BaseModel):
    name: str
    workbook_id: str
    key: str = ""
    description: str = ""
    mode: Literal["save", "publish"] = "save"
    tab_title: str = "Main"
    items: list[DashboardItemDraft] = Field(default_factory=list)
    meta: dict[str, Any] | None = None
    support_description: str = ""
    access_description: str = ""


def build_dashboard_spec(draft: DashboardDraft) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    layout: list[dict[str, Any]] = []

    for index, draft_item in enumerate(draft.items, start=1):
        item = dict(draft_item.item)
        item.setdefault("id", f"item-{index}")
        items.append(item)

        layout_item: dict[str, Any] = {
            "i": item["id"],
            "x": draft_item.x,
            "y": draft_item.y,
            "w": draft_item.w,
            "h": draft_item.h,
        }
        if draft_item.parent:
            layout_item["parent"] = draft_item.parent
        layout.append(layout_item)

    entry: dict[str, Any] = {
        "key": draft.key,
        "workbookId": draft.workbook_id,
        "name": draft.name,
        "meta": draft.meta,
        "annotation": {"description": draft.description},
        "data": {
            "counter": 0,
            "salt": token_hex(8),
            "schemeVersion": 8,
            "tabs": [
                {
                    "id": "tab-1",
                    "title": draft.tab_title,
                    "items": items,
                    "layout": layout,
                    "connections": [],
                    "aliases": {"default": []},
                }
            ],
            "settings": {
                "silentLoading": False,
                "dependentSelectors": True,
                "globalParams": {},
                "hideTabs": True,
                "expandTOC": False,
            },
            "supportDescription": draft.support_description,
            "accessDescription": draft.access_description,
        },
    }

    return {"entry": entry, "mode": draft.mode}
