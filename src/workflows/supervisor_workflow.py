from datetime import datetime
from pathlib import Path

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.types import interrupt

from src.dtos.evaluvation import HumanDecision
from src.workflows.state.content_workflow_state import ContentWorkflowState
from src.workflows.nodes.nodes import (
    supervisor_node,
    brand_node,
    trend_node,
    strategy_node,
    content_node,
    evaluation_node,
)
from src.workflows.routing.routing import route_from_supervisor


# --------------------------------------------------
# Human Review Node
# --------------------------------------------------


def human_review_node(state: ContentWorkflowState):
    """
    Pause execution and request a human decision.
    Execution resumes using Command(resume=...).
    """

    review_payload = {
        "generated_content": [
            item.model_dump() if hasattr(item, "model_dump") else item
            for item in state.get("generated_content", [])
        ],
        "evaluation": (
            state["evaluation"].model_dump()
            if hasattr(state.get("evaluation"), "model_dump")
            else state.get("evaluation")
        ),
        "generation_attempts": state.get("generation_attempts", 0),
        "message": "Review the generated content and provide your decision.",
    }

    human_response = interrupt(review_payload)

    decision = HumanDecision.model_validate(human_response)

    return {
        "human_decision": decision.decision,
        "human_feedback": decision.feedback,
        "feedback_scope": decision.feedback_scope,
        "is_approved": decision.decision == "approve",
        "is_rejected": decision.decision == "reject",
        "workflow_status": (
            "approved"
            if decision.decision == "approve"
            else "rejected"
            if decision.decision == "reject"
            else "running"
        ),
        "current_agent": "human_review",
    }


# --------------------------------------------------
# Markdown Writer Node
# --------------------------------------------------


def markdown_writer_node(state: ContentWorkflowState):
    """
    Save content only after explicit human approval.
    """

    if not state.get("is_approved", False):
        raise ValueError("Markdown output blocked: human approval is required.")

    output_dir = Path("generated_content/approved")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"approved_content_{timestamp}.md"

    lines = [
        "# Approved Social Media Content",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
    ]

    for index, item in enumerate(state.get("generated_content", []), start=1):
        platform = (
            item.platform
            if hasattr(item, "platform")
            else item.get("platform", "Unknown")
        )

        content = item.content if hasattr(item, "content") else item.get("content", "")

        lines.extend(
            [
                f"## Content {index} — {platform}",
                "",
                content,
                "",
                "---",
                "",
            ]
        )

    output_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return {
        "workflow_status": "completed",
        "current_agent": "markdown_writer",
        "output_file": str(output_file),
    }


# --------------------------------------------------
# Supervisor-Controlled LangGraph
# --------------------------------------------------


def build_supervisor_workflow():
    workflow = StateGraph(ContentWorkflowState)

    # Register Supervisor and specialist workers.
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("brand", brand_node)
    workflow.add_node("trend", trend_node)
    workflow.add_node("strategy", strategy_node)
    workflow.add_node("content", content_node)
    workflow.add_node("evaluation", evaluation_node)

    # Register human and deterministic output nodes.
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("markdown_writer", markdown_writer_node)

    # Workflow starts with the Supervisor.
    workflow.set_entry_point("supervisor")

    # Supervisor chooses the next worker dynamically.
    workflow.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "brand": "brand",
            "trend": "trend",
            "strategy": "strategy",
            "content": "content",
            "evaluation": "evaluation",
            "human_review": "human_review",
            "markdown_writer": "markdown_writer",
            END: END,
        },
    )

    # Every specialist returns control to the Supervisor.
    workflow.add_edge("brand", "supervisor")
    workflow.add_edge("trend", "supervisor")
    workflow.add_edge("strategy", "supervisor")
    workflow.add_edge("content", "supervisor")
    workflow.add_edge("evaluation", "supervisor")

    # Human decision also returns to the Supervisor.
    workflow.add_edge("human_review", "supervisor")

    # Only the Markdown Writer finishes the approved workflow.
    workflow.add_edge("markdown_writer", END)

    # In-memory checkpointing for initial development/testing.
    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)
