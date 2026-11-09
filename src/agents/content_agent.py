from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia import ChatNVIDIA

from src.configs.config import settings
from src.dtos.brand import BrandProfile
from src.dtos.content import ContantsResult
from src.dtos.stergy import StergyResult


class ContentAgent:
    def __init__(self):
        self.llm = ChatNVIDIA(
            model=settings.NVIDIA_CHAT_MODEL,
            nvidia_api_key=settings.NVIDIA_CHAT_MODEL_KEY,
            temperature=0,
            max_tokens=8192,
        )
        self.system_prompt = """"
        You are senior content creation you have an brand information and also 
        you have an content creation stergy use those content then you need to 
        generate the content for the given social media platforms
        """
        self.parser = PydanticOutputParser(pydantic_object=ContantsResult)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "human",
                    """"
            You need to generate the conent for that following bussiness domain for the given platforms
            and make sure to conside the branding information and also content creation stergy to create
            the contents
            {brand_profile}
            {stergy}
            {format_instructions}
            """,
                ),
            ]
        )
        self.chain = self.prompt | self.llm | self.parser

    async def run(self, brand_profile: BrandProfile, stergies: StergyResult):
        results = await self.chain.ainvoke(
            {
                "brand_profile": brand_profile,
                "stergy": stergies,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        return results
