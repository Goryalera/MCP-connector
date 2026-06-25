from datalens_mcp.dashboard import DashboardDraft, build_dashboard_spec


def test_build_dashboard_spec_includes_chart_and_text_widgets() -> None:
    spec = build_dashboard_spec(
        DashboardDraft.model_validate(
            {
                "name": "Sales",
                "workbook_id": "wb1",
                "items": [
                    {
                        "item": {
                            "id": "chart1",
                            "namespace": "default",
                            "type": "widget",
                            "widgetId": "chart-entry-id",
                        },
                        "x": 0,
                        "y": 0,
                        "w": 12,
                        "h": 8,
                    }
                ],
            }
        )
    )

    assert spec["mode"] == "save"
    assert spec["entry"]["name"] == "Sales"
    assert spec["entry"]["workbookId"] == "wb1"
    assert spec["entry"]["data"]["schemeVersion"] == 8
    assert spec["entry"]["data"]["tabs"][0]["items"][0]["widgetId"] == "chart-entry-id"
    assert spec["entry"]["data"]["tabs"][0]["layout"][0]["i"] == "chart1"
