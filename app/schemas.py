from typing import Literal
from pydantic import BaseModel, Field

class ContainerCreate(BaseModel):
    container_id: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$", description="ISO 6346 style eg: MSKU1234567")
    size: Literal["20", "40"] 
    weight_kg: float = Field(..., gt=0, le=350000)
    destination: str = Field(..., min_length=2, max_length=50)


class ContainerOut(ContainerCreate):
    status: str

class DwellRequest(BaseModel):
    weight_kg: float = Field(..., gt=0, le=350000)
    is_40ft: int = Field(..., gt=0,le=1)
    arrival_hour: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., ge=0, le=6)
    