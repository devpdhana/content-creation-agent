from src.agents.brand_agent import BrandAgent
from src.agents.trand_agent import TrandAgent
from src.agents.stergy_agent import StergyAgent
from src.dtos.brand import BrandInput
from src.dtos.trand import TrandsAnalysisResult


class ContentCreationWorkFlow:
    def __init__(self):
        self.brand_agent = BrandAgent()
        self.trand_agent = TrandAgent()
        self.stergy_agent = StergyAgent()

    async def run(self, brand_info: BrandInput):
        brand_profile = await self.brand_agent.run(brand_input=brand_info)
        print(f"brand {brand_profile}")
        trand_analysis = await self.trand_agent.run(brand_profile=brand_profile)
        stergy_result = await self.stergy_agent.run(
            trends=trand_analysis, brand_information=brand_profile
        )
        print(f"stergy_result {stergy_result}")
        return stergy_result
