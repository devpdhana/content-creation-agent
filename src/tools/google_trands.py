from pytrends.request import TrendReq
from src.dtos.trand import GoogleTrandsResult


class GoogleTrendsTool:
    def __init__(self):
        self.client = TrendReq(hl="en-IN", tz=330, timeout=(10, 30))

    def search(
        self, keyword: str, timeframe: str = "today 3-m", region: str = "IN"
    ) -> dict:

        try:
            self.client.build_payload(
                kw_list=[keyword], timeframe=timeframe, geo=region
            )

            interest = self.client.interest_over_time()

            regions = self.client.interest_by_region(resolution="REGION")

            related = self.client.related_queries()

            query_data = related.get(keyword, {})

            return GoogleTrandsResult(
                source="google_trends",
                keyword=keyword,
                top_queries=(
                    query_data["top"].to_dict("records")
                    if query_data.get("top") is not None
                    else []
                ),
            )

        except Exception as error:
            print(f"Google Trends error: {error}")

            return {"source": "google_trends", "keyword": keyword, "error": str(error)}
