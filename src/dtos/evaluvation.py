from pydantic import BaseModel, Field


class EvaluationCriterion(BaseModel):
    name: str = Field(description="Evaluation criterion")
    score: int = Field(ge=0, le=100)
    weight: int = Field(ge=0, le=100)
    feedback: str


class ContentEvaluation(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    passed: bool

    criteria: list[EvaluationCriterion]

    brand_violations: list[str] = Field(default_factory=list)
    factual_issues: list[str] = Field(default_factory=list)

    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    revision_instructions: list[str] = Field(default_factory=list)
    feedback_summary: str = ""


class HumanDecision(BaseModel):
    decision: str = Field(description="One of: approve, revise, reject")
    feedback: str = ""
    feedback_scope: str = Field(default="content", description="content or brand")
