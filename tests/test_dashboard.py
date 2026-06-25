from datalens_mcp.dashboard import DashboardDraft, build_dashboard_spec


def test_build_dashboard_spec_includes_chart_and_text_widgets() -> None:
    spec = build_dashboard_spec(
        DashboardDraft.model_validate(
            {
                "title": "Sales",
                "workbook_id": "wb1",
                "charts": [
                    {
                        "title": "Revenue",
                        "chart_id": "chart1",
                        "x": 0,
                        "y": 0,
                        "width": 12,
                        "height": 8,
                    }
                ],
                "texts": [{"text": "# Sales dashboard", "x": 0, "y": 8}],
            }
        )
    )

    assert spec["title"] == "Sales"
    assert spec["workbookId"] == "wb1"
    assert spec["widgets"][0]["source"]["entryId"] == "chart1"
    assert spec["widgets"][1]["content"] == "# Sales dashboard"
