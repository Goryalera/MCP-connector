def test_server_imports() -> None:
    from datalens_mcp.server import mcp

    assert mcp.name == "datalens-mcp"
