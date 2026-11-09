from pathlib import Path

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia import ChatNVIDIA

from src.configs.config import settings
from src.dtos.supervisor import SupervisorDecision


class SupervisorAgent:
    def __init__(self):
        self.llm = ChatNVIDIA(
            model=settings.NVIDIA_CHAT_MODEL,
            nvidia_api_key=settings.NVIDIA_CHAT_MODEL_KEY,
            temperature=0,
            max_tokens=8192,
        )

        self.parser = PydanticOutputParser(pydantic_object=SupervisorDecision)

        prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "supervisor.md"
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "human",
                    """
            Current Workflow State:

                {workflow_state}

                Based on the current state, decide which
                agent should execute next.

                {format_instructions}
            """,
                ),
            ]
        )
        self.chain = self.prompt | self.llm | self.parser

    async def decide(self, workflow_state: dict) -> SupervisorDecision:
        return await self.chain.ainvoke(
            {
                "workflow_state": str(workflow_state),
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
