from pydantic import BaseModel


class ContentResult(BaseModel):
    platform: str
    content: str


class ContantsResult(BaseModel):
    contents: list[ContentResult]
