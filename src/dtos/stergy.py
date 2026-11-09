from pydantic import BaseModel, Field


class StergyResult(BaseModel):
    topic: str = Field(description="Topic for the content stergy")
    objective: str = Field(description="Objective of the content")
    recommed_platform: str = Field(description="Platforms like youtube,linkedin")
    cta: str = Field(description="To gain the user attention")
