from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None


class ProjectResponse(ProjectBase):
    id: int
    created_by: int

    model_config = ConfigDict(from_attributes=True)
