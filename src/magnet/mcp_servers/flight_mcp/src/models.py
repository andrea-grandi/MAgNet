from typing import Optional, List
from pydantic import BaseModel, Field


class FlightInfoInput(BaseModel):
    api_version: str = "1"
    city: str
    date: str
    time: Optional[str] = None
    include_details: bool = Field(default=True)


class FlightInfoOutput(BaseModel):
    api_version: str = "1"
    flight_id: str
    status: str
    departure: str
    arrival: str
    duration: str
    details: Optional[str] = None
