from pydantic import Field, BaseModel


class BrandProfile(BaseModel):
    brand_identity: str = Field(
        description="A concise explanation of the brand identity"
    )
    target_audience: list[str]
    brand_voice: list[str]
    communication_guidelines: list[str]
    content_pillers: list[str]
    unique_seeling_points: list[str]


class BrandInput(BaseModel):
    business_name: str = Field(description="Name of the business")
    business_description: str = Field(description="What the business does")
    products_services: list[str] = Field(default_factory=list)

    target_audience: list[str] = Field(default_factory=list)

    business_values: list[str] = Field(default_factory=list)

    preferred_tone: list[str] = Field(default_factory=list)

    marketing_objectives: list[str] = Field(default_factory=list)

    restrictions: list[str] = Field(default_factory=list)

    additional_information: str | None = None
