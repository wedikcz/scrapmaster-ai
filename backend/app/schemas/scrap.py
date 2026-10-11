from pydantic import BaseModel, Field


class ScrapItemBase(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = "misc"
    source: str = "unknown"
    condition: str = "unknown"
    estimated_value: float = 0.0
    notes: str | None = None
    project_id: int | None = None


class ScrapItemCreate(ScrapItemBase):
    pass


class ScrapItemOut(ScrapItemBase):
    id: int

    model_config = {"from_attributes": True}
