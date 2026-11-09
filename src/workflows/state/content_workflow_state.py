from typing import Any, Optional, TypedDict


class ContentWorkflowState(TypedDict, total=False):
    # Initial business information
    business_input: Any

    # Agent outputs
    brand_profile: Any
    trend_report: Any
    content_strategy: Any
    generated_content: Any
    evaluation: Any

    # Supervisor decision
    supervisor_decision: Any
    current_agent: str
    next_agent: str
    task: str

    # Retry management
    generation_attempts: int
    max_retries: int

    # Human review
    human_decision: Optional[str]
    human_feedback: Optional[str]
    feedback_scope: Optional[str]

    # Workflow status
    workflow_status: str
    is_approved: bool
    is_rejected: bool

    # Error tracking
    last_error: Optional[str]

    # Brand profile update tracking
    brand_profile_updated: bool
    brand_profile_history: list
    output_file: Optional[str]
