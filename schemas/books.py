from pydantic import BaseModel, ConfigDict, Field


class SBookBase(BaseModel):
    title: str
    author: str
    year: int
    pages: int = Field(gt=10)
    is_read: bool = False


class SBookAdd(SBookBase):
    pass


class SBook(SBookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SBookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    pages: int | None = Field(default=None, gt=10)
    is_read: bool | None = None
