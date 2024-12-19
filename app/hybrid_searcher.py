from vectorstore.client import get_client
from qdrant_client.http.models import Filter, FieldCondition, Range, MatchValue
from app.models.search import SearchResult


class HybridSearcher:
    """
    A class to perform hybrid search using Qdrant.
    """

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.qdrant_client = get_client()

    def search(
        self, query: str, limit: int = 25, include: dict | None = None
    ) -> list[SearchResult]:
        query_filter = self._construct_filter(include)
        search_result = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=query,
            query_filter=query_filter,
            limit=limit,
        )

        return [
            SearchResult(score=hit.score, metadata=hit.metadata)
            for hit in search_result
        ]

    @staticmethod
    def _construct_filter(include: dict) -> Filter | None:
        if not include:
            return None

        # NOTE: handle ability to filter on multiple values
        filter_map = {
            "variety": lambda value: FieldCondition(
                key="variety",
                match=MatchValue(value=value),
            ),
            "rating": lambda value: FieldCondition(
                key="rating",
                range=Range(gte=value.get("gte", 1), lte=value.get("lte", 100)),
            ),
        }

        conditions = []

        for key, value in include.items():
            if key in filter_map and value is not None:
                conditions.append(filter_map[key](value))

        return Filter(must=conditions) if conditions else None
