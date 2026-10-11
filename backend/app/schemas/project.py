from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None
    status: str = "active"


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int

    model_config = {"from_attributes": True}
