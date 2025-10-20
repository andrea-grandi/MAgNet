from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class ArithmeticInput(BaseModel):
    api_version: str = "1"
    trace_id: Optional[str] = None
    operation: Literal["add", "subtract", "multiply", "divide"]
    numbers: List[float] = Field(min_length=2)


class ArithmeticOutput(BaseModel):
    api_version: str = "1"
    trace_id: Optional[str] = None
    result: float
    confidence: float = Field(ge=0, le=1)


class StatisticsInput(BaseModel):
    api_version: str = "1"
    trace_id: Optional[str] = None
    numbers: List[float] = Field(min_length=2)
    metric: Literal["mean", "median", "stdev", "variance"]


class StatisticsOutput(BaseModel):
    api_version: str = "1"
    trace_id: Optional[str] = None
    value: float
    confidence: float = Field(ge=0, le=1)
