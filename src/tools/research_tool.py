from src.tools.web_search import WebSearchTool
from src.tools.google_trands import GoogleTrendsTool
from src.dtos.trand import TrandSearch, TrandsAnalysisResult


class ResearchTool:
    def __init__(self):
        self.web_search = WebSearchTool()
        self.google_trands = GoogleTrendsTool()

    async def search(self, queries: TrandSearch) -> TrandsAnalysisResult:
        web_result = self.web_search.search(queries.web_search)
        google_trands_result = self.google_trands.search(
            keyword=queries.google_trends
        )
        return TrandsAnalysisResult(
            web_search_result=web_result, google_trands_result=google_trands_result
        )
