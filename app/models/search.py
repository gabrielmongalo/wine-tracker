from pydantic import BaseModel, Field
from typing import List, Dict, Any


class Rangefilter(BaseModel):
    gte: int | float | None = Field(
        default=None, gte=1, lte=100, description="Rating must be between 1 and 100"
    )
    lte: int | float | None = Field(
        default=None, gte=1, lte=100, description="Rating must be between 1 and 100"
    )


class Filters(BaseModel):
    variety: str | None = Field(default=None, description="Variety of wine")
    rating: Rangefilter = Field(
        default_factory=Rangefilter, description="Rating of wine"
    )


class SearchRequest(BaseModel):
    query: str | None = Field(default=None, description="Search query")
    limit: int = Field(default=25, description="Number of results to return")
    include: Filters | None = Field(
        default=None, description="Filters for `variety` or `rating`"
    )


class SearchResult(BaseModel):
    score: float = Field(description="Score of the search result")
    metadata: Dict[str, Any] = Field(description="Metadata of the search result")


class SearchResponse(BaseModel):
    results: List[SearchResult] = Field(..., description="List of search results")
