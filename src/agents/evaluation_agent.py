from pathlib import Path
from typing import Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from src.configs.config import settings
from src.dtos.evaluvation import ContentEvaluation, EvaluationCriterion


class EvaluationAgent:
    def __init__(self):
        self.llm = ChatNVIDIA(
            model=settings.NVIDIA_CHAT_MODEL,
            api_key=settings.NVIDIA_CHAT_MODEL_KEY,
            temperature=0,
            max_tokens=8192,
        )

        self.parser = PydanticOutputParser(pydantic_object=ContentEvaluation)

        prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "evaluation.md"

        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "human",
                    """
            Evaluate the following content.

                Content:
                {content}

                Brand Profile:
                {brand_profile}

                Trend Report:
                {trend_report}

                Content Strategy:
                {content_strategy}

                {format_instructions}
            """,
                ),
            ]
        )
        self.chain = self.prompt | self.llm | self.parser

    async def evaluate(
        self,
        content: Any,
        brand_profile: Any,
        trend_report: Any,
        content_strategy: Any,
    ) -> ContentEvaluation:

        result = await self.chain.ainvoke(
            {
                "content": str(content),
                "brand_profile": str(brand_profile),
                "trend_report": str(trend_report),
                "content_strategy": str(content_strategy),
                "format_instructions": self.parser.get_format_instructions(),
            }
        )

        return self._calculate_final_score(result)

    def _calculate_final_score(
        self,
        evaluation: ContentEvaluation,
    ) -> ContentEvaluation:

        total_weight = sum(item.weight for item in evaluation.criteria)

        if total_weight == 0:
            raise ValueError("Evaluation criteria must have a non-zero weight.")

        weighted_score = (
            sum(item.score * item.weight for item in evaluation.criteria) / total_weight
        )

        evaluation.overall_score = round(weighted_score)

        evaluation.passed = (
            evaluation.overall_score >= 85
            and not evaluation.brand_violations
            and not evaluation.factual_issues
        )

        return evaluation
