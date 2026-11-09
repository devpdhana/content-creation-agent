from pydantic import BaseModel, Field


class TrandSearch(BaseModel):
    web_search: str = Field(description="search query for website")
    google_trends: str = Field(description="search query for Google Trends")


class TrandResult(BaseModel):
    youtube_content: str = Field(description="Content for the youtube platform")


class SearchResult(BaseModel):
    source: str = Field(description="Source of the results")


class WebSearhResult(SearchResult):
    title: str = Field(description="Title of the result")
    snippet: str = Field(description="snippet of the result")
    url: str = Field(description="URL of the result")


class GoogleTrandsResult(SearchResult):
    keyword: str = Field(description="Keyword of the result")
    top_queries: list[dict] = Field(
        default_factory=list, description="Top queries of the result"
    )


class TrandsAnalysisResult(BaseModel):
    web_search_result: list[WebSearhResult] = Field(description="web search results")
    google_trands_result: GoogleTrandsResult = Field(description="google search result")
