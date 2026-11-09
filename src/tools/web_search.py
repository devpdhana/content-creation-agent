from ddgs import DDGS
from src.dtos.trand import WebSearhResult


class WebSearchTool:
    def search(self, search_query: str) -> list[WebSearhResult]:
        try:
            results = DDGS().text(search_query, max_result=10)
            return [
                WebSearhResult(
                    source="web",
                    title=item.get("title"),
                    url=item.get("href"),
                    snippet=item.get("body"),
                )
                for item in results
            ]
        except Exception as error:
            print(error)
            return []
