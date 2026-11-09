from typing import Literal, Optional

from pydantic import BaseModel, Field


class SupervisorDecision(BaseModel):
    next_agent: Literal[
        "brand",
        "trend",
        "strategy",
        "content",
        "evaluation",
        "feedback",
        "human_review",
        "markdown_writer",
        "finish",
    ]

    reason: str

    task: str = ""

    retry_generation: bool = False

    feedback_scope: Optional[Literal["content", "brand"]] = None


class SupervisorResult(BaseModel):
    status: Literal[
        "running",
        "waiting_for_human",
        "approved",
        "rejected",
        "completed",
        "failed",
    ]

    current_agent: str = ""

    generation_attempts: int = 0

    max_retries: int = 3

    last_error: Optional[str] = None
