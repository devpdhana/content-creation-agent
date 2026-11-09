from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia import ChatNVIDIA

from src.dtos.brand import BrandProfile
from src.configs.config import settings
from src.dtos.trand import TrandsAnalysisResult, TrandSearch
from src.tools.research_tool import ResearchTool


class TrandAgent:
    def __init__(self):
        self.llm = ChatNVIDIA(
            model=settings.NVIDIA_CHAT_MODEL,
            nvidia_api_key=settings.NVIDIA_CHAT_MODEL_KEY,
            temperature=0,
            max_tokens=8192,
        )
        self.research_tool = ResearchTool()
        self.parser = PydanticOutputParser(pydantic_object=TrandSearch)

        self.system_prompt = """
You are an search statergist you have brand profile information you need to generate the 
search query for the that brand to get the current trandings for that brand and domain
"""
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "human",
                    """
            Analyze the following business brand information and create the search query to get the trandings topics for that brand domain
            {brand_information}

            {format_instructions}
            """,
                ),
            ]
        )
        self.chain = self.prompt | self.llm | self.parser

    async def run(self, brand_profile: BrandProfile) -> TrandsAnalysisResult:
        result = await self.chain.ainvoke(
            {
                "brand_information": brand_profile.model_dump_json(indent=2),
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        research_result = await self.research_tool.search(result)
        return research_result
