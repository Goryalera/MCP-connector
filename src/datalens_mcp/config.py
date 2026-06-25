from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic import BaseModel, Field, HttpUrl


class Settings(BaseModel):
    datalens_token: str = Field(default="", repr=False)
    datalens_org_id: str = ""
    datalens_api_base: HttpUrl = "https://api.datalens.tech"
    datalens_api_version: str = "1"
    datalens_auth_scheme: str = "Bearer"
    default_workbook_id: str = ""
    default_collection_id: str = ""
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8000
    request_timeout_seconds: float = 30.0


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        datalens_token=getenv("DATALENS_TOKEN", ""),
        datalens_org_id=getenv("DATALENS_ORG_ID", ""),
        datalens_api_base=getenv("DATALENS_API_BASE", "https://api.datalens.tech"),
        datalens_api_version=getenv("DATALENS_API_VERSION", "1"),
        datalens_auth_scheme=getenv("DATALENS_AUTH_SCHEME", "Bearer"),
        default_workbook_id=getenv("DATALENS_DEFAULT_WORKBOOK_ID", ""),
        default_collection_id=getenv("DATALENS_DEFAULT_COLLECTION_ID", ""),
        mcp_host=getenv("MCP_HOST", "0.0.0.0"),
        mcp_port=int(getenv("MCP_PORT", "8000")),
        request_timeout_seconds=float(getenv("DATALENS_TIMEOUT_SECONDS", "30")),
    )
