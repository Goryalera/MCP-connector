from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChartDraft(BaseModel):
    title: str
    chart_id: str = Field(description="Existing DataLens chart/entry id")
    x: int = 0
    y: int = 0
    width: int = 12
    height: int = 8


class TextDraft(BaseModel):
    text: str
    x: int = 0
    y: int = 0
    width: int = 12
    height: int = 3


class DashboardDraft(BaseModel):
    title: str
    workbook_id: str | None = None
    collection_id: str | None = None
    description: str = ""
    charts: list[ChartDraft] = Field(default_factory=list)
    texts: list[TextDraft] = Field(default_factory=list)
    layout_type: Literal["grid"] = "grid"


def build_dashboard_spec(draft: DashboardDraft) -> dict[str, Any]:
    widgets: list[dict[str, Any]] = []

    for chart in draft.charts:
        widgets.append(
            {
                "type": "chart",
                "title": chart.title,
                "source": {"entryId": chart.chart_id},
                "layout": {
                    "x": chart.x,
                    "y": chart.y,
                    "width": chart.width,
                    "height": chart.height,
                },
            }
        )

    for text in draft.texts:
        widgets.append(
            {
                "type": "text",
                "content": text.text,
                "layout": {
                    "x": text.x,
                    "y": text.y,
                    "width": text.width,
                    "height": text.height,
                },
            }
        )

    payload: dict[str, Any] = {
        "title": draft.title,
        "description": draft.description,
        "layoutType": draft.layout_type,
        "widgets": widgets,
    }

    if draft.workbook_id:
        payload["workbookId"] = draft.workbook_id
    if draft.collection_id:
        payload["collectionId"] = draft.collection_id

    return payload
