from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any, List


class DBConnectionInput(BaseModel):
    api_version: str = "1"
    trace_id: Optional[str] = None
    db_url: str = Field(..., description="SQLAlchemy connection string, e.g. sqlite:///mydb.db")


class DBQueryInput(BaseModel):
    api_version: str = "1"
    trace_id: Optional[str] = None
    db_url: str
    query: str = Field(..., description="SQL query to execute (SELECT, INSERT, UPDATE, DELETE)")
    return_results: bool = Field(default=True, description="If True, returns fetched data for SELECT queries")


class DBQueryOutput(BaseModel):
    success: bool
    rows: Optional[List[Dict[str, Any]]] = None
    affected_rows: Optional[int] = None
    error: Optional[str] = None
    api_version: str = "1"
    trace_id: Optional[str] = None


class DBStatusOutput(BaseModel):
    connected: bool
    dialect: str
    driver: str
    api_version: str = "1"
    trace_id: Optional[str] = None
