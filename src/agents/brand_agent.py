from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia import ChatNVIDIA
from langchain_core.output_parsers import PydanticOutputParser

from src.configs.config import settings
from src.dtos.brand import BrandInput, BrandProfile


class BrandAgent:
    def __init__(self):
        self.llm = ChatNVIDIA(
            model=settings.NVIDIA_CHAT_MODEL,
            nvidia_api_key=settings.NVIDIA_CHAT_MODEL_KEY,
            temperature=0,
            max_tokens=8192,
        )
        # self.structred_output = self.llm.with_structured_output(BrandProfile)
        self.parser = PydanticOutputParser(pydantic_object=BrandProfile)
        prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "brand.md"
        system_prompt = prompt_path.read_text(encoding="utf-8")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "human",
                    """
Analyze the following business information
                    and create its brand profile.

                    Business information:
                    {business_information}
                    {format_instructions}
""",
                ),
            ]
        )
        self.chain = self.prompt | self.llm | self.parser

    async def run(self, brand_input: BrandInput) -> BrandProfile:
        result = await self.chain.ainvoke(
            {
                "business_information": brand_input.model_dump_json(indent=2),
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        return result
