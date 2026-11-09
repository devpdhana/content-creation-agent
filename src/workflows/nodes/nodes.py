from src.agents.brand_agent import BrandAgent
from src.agents.content_agent import ContentAgent
from src.agents.evaluation_agent import EvaluationAgent
from src.agents.stergy_agent import StergyAgent
from src.agents.trand_agent import TrandAgent
from src.agents.supervisor_agent import SupervisorAgent
from src.workflows.state.content_workflow_state import ContentWorkflowState

brand_agent = BrandAgent()
trend_agent = TrandAgent()
strategy_agent = StergyAgent()
content_agent = ContentAgent()
evaluation_agent = EvaluationAgent()
supervisor_agent = SupervisorAgent()


async def supervisor_node(state: ContentWorkflowState):
    decision = await supervisor_agent.decide(dict(state))
    return {
        "supervisor_decision": decision,
        "next_agent": decision.next_agent,
        "task": decision.task,
        "current_agent": "supervisor",
    }


async def brand_node(state: ContentWorkflowState):
    result = await brand_agent.run(state["business_input"])
    return {
        "brand_profile": result,
        "current_agent": "brand",
    }


async def trend_node(state: ContentWorkflowState):
    result = await trend_agent.run(state["brand_profile"])
    return {
        "trend_report": result,
        "current_agent": "trend",
    }


async def strategy_node(state: ContentWorkflowState):
    result = await strategy_agent.run(
        brand_information=state["brand_profile"], trends=state["trend_report"]
    )
    return {"content_strategy": result, "current_agent": "strategy"}


async def content_node(
    state: ContentWorkflowState,
):

    result = await content_agent.run(
        state["brand_profile"],
        state["content_strategy"],
    )

    return {
        "generated_content": result,
        "current_agent": "content",
        "generation_attempts": (state.get("generation_attempts", 0) + 1),
    }


async def evaluation_node(
    state: ContentWorkflowState,
):

    result = await evaluation_agent.evaluate(
        content=state["generated_content"],
        brand_profile=state["brand_profile"],
        trend_report=state["trend_report"],
        content_strategy=state["content_strategy"],
    )

    return {
        "evaluation": result,
        "current_agent": "evaluation",
    }
