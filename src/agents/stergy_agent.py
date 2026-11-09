from langchain_core.output_parsers import PydanticOutputParser
from langchain_nvidia import ChatNVIDIA
from src.configs.config import settings
from src.dtos.stergy import StergyResult
from langchain_core.prompts import ChatPromptTemplate
from src.dtos.brand import BrandProfile
from src.dtos.trand import TrandsAnalysisResult


class StergyAgent:
    def __init__(self):
        self.llm = ChatNVIDIA(
            model=settings.NVIDIA_CHAT_MODEL,
            nvidia_api_key=settings.NVIDIA_CHAT_MODEL_KEY,
            temperature=0,
            max_tokens=8192,
        )
        self.parser = PydanticOutputParser(pydantic_object=StergyResult)

        self.system_prompt = """
        You need to generate the content creation stergy for the provided brand and also current tranding for that domain you can 
        use those information and use that to generate the Stergy
        """
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "human",
                    """
                    Analyze the following business brand information and trandings information then create the content creation stergy for that business it need to 
                    meet their business uniquess and also meet the tone
                    {brand_information}
        
                    {tranding_information}
                    {format_instructions}
                    """,
                ),
            ]
        )
        self.chain = self.prompt | self.llm | self.parser

    async def run(
        self, brand_information: BrandProfile, trends: TrandsAnalysisResult
    ) -> StergyResult:
        result = await self.chain.ainvoke(
            {
                "brand_information": brand_information,
                "tranding_information": trends,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        return result
