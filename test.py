import asyncio
from src.agents.supervisor_agent import SupervisorAgent


async def main():

    supervisor = SupervisorAgent()

    workflow_state = {
        "brand_profile": None,
        "trend_report": None,
        "content_strategy": None,
        "generated_content": None,
        "evaluation": None,
        "generation_attempts": 0,
        "human_approval": False,
    }

    decision = await supervisor.decide(workflow_state)

    print("\nSUPERVISOR DECISION")
    print("-------------------")
    print(decision.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
