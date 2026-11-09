from typing import Any

from langgraph.graph import END


WORKER_ROUTES = {
    "brand",
    "trend",
    "strategy",
    "content",
    "evaluation",
    "human_review",
    "markdown_writer",
}


def get_value(data: Any, key: str, default=None):
    if isinstance(data, dict):
        return data.get(key, default)

    return getattr(data, key, default)


def route_from_supervisor(state: dict) -> str:

    decision = state.get("supervisor_decision")
    next_agent = get_value(decision, "next_agent")

    # 1. Rejection always stops the workflow.
    human_decision = state.get("human_decision")

    if human_decision == "reject" or state.get("is_rejected", False):
        return END

    # 2. Explicit human approval permits Markdown writing.
    if state.get("is_approved", False) or human_decision == "approve":
        return "markdown_writer"

    # 3. Never execute a worker without its prerequisites.
    if not state.get("brand_profile"):
        return "brand"

    if not state.get("trend_report"):
        return "trend"

    if not state.get("content_strategy"):
        return "strategy"

    if not state.get("generated_content"):
        return "content"

    # 4. Evaluate generated content before human review.
    evaluation = state.get("evaluation")

    if evaluation is None:
        return "evaluation"

    evaluation_passed = get_value(evaluation, "passed", None)

    # 5. Failed evaluation: enforce maximum three regenerations.
    if evaluation_passed is False:
        generation_attempts = state.get("generation_attempts", 0)
        max_retries = state.get("max_retries", 3)

        retries_used = max(0, generation_attempts - 1)

        if retries_used < max_retries:
            return "content"

        return "human_review"

    # 6. Passing evaluation always requires human approval.
    if evaluation_passed is True:
        return "human_review"

    # 7. Validate any remaining Supervisor decision.
    if next_agent == "markdown_writer":
        return "human_review"

    if next_agent in WORKER_ROUTES:
        return next_agent

    return END
