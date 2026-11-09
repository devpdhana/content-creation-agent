import asyncio

import json

from agents.brand_agent import BrandAgent

from dtos.brand import BrandInput
from dtos.evaluvation import HumanDecision
from src.workflows.content_creation_workflow import ContentCreationWorkFlow
from src.workflows.supervisor_workflow import build_supervisor_workflow
from datetime import datetime
from langgraph.types import Command


async def main():
    business = BrandInput(
        business_name="GreenBite",
        business_description=(
            "GreenBite is a healthy food brand that provides "
            "nutritious meals for busy professionals."
        ),
        products_services=[
            "Healthy meal subscriptions",
            "Organic salads",
            "High-protein meals",
        ],
        target_audience=[
            "Working professionals",
            "Fitness enthusiasts",
            "Health-conscious people",
        ],
        business_values=[
            "Healthy living",
            "Sustainability",
            "Fresh ingredients",
        ],
        preferred_tone=[
            "Friendly",
            "Professional",
            "Motivational",
        ],
        marketing_objectives=[
            "Increase brand awareness",
            "Generate more subscriptions",
        ],
        restrictions=[
            "Do not make unverified health claims",
            "Avoid promoting unhealthy eating habits",
        ],
    )
    workflow = build_supervisor_workflow()
    config = {
        "configurable": {
            "thread_id": f"content-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        }
    }
    initial_state = {
        "business_input": business,
        "generation_attempts": 0,
        "max_retries": 3,
        "workflow_status": "running",
        "is_approved": False,
        "is_rejected": False,
        "brand_profile_history": [],
    }
    result = await workflow.ainvoke(initial_state, config=config)

    # print(json.dumps(result.model_dump(), indent=4, ensure_ascii=False))
    while result.get("__interrupt__"):
        for interruption in result["__interrupt__"]:
            review_data = interruption.value

            print("\n========================================")
            print("          HUMAN CONTENT REVIEW")
            print("========================================\n")

            print(json.dumps(review_data, indent=4, default=str))

            while True:
                choice = (
                    input("\nEnter your decision (approve/reject): ").strip().lower()
                )

                if choice in {"approve", "reject"}:
                    break

                print(
                    "For now, choose approve or reject. "
                    "Revision support will be connected with the Feedback Agent."
                )

            decision = HumanDecision(
                decision=choice,
                feedback=input("Feedback (optional): ").strip(),
                feedback_scope="content",
            )

            print(f"\nSubmitting human decision: {choice}\n")

            result = await workflow.ainvoke(
                Command(resume=decision.model_dump()),
                config=config,
            )

    print("\n========================================")
    print("           WORKFLOW RESULT")
    print("========================================\n")

    print("Status:", result.get("workflow_status"))
    print("Generation attempts:", result.get("generation_attempts", 0))

    if result.get("output_file"):
        print("Approved Markdown:", result["output_file"])

    elif result.get("is_rejected"):
        print("Content was rejected by the human reviewer.")

    else:
        print("Workflow ended without producing approved Markdown.")

    print("\nWorkflow execution finished.")


if __name__ == "__main__":
    asyncio.run(main())
