import pytest
from unittest.mock import MagicMock
from app.hybrid_searcher import HybridSearcher
from app.models.search import SearchResult


@pytest.fixture
def mock_qdrant_client():
    """
    Mock Qdrant client with predefined query results.
    """
    mock_client = MagicMock()
    mock_client.query.return_value = [
        {
            "score": 0.85,
            "metadata": {
                "name": "Wine A",
                "rating": 90,
                "variety": "Red",
                "notes": "This is a red wine",
            },
        },
        {
            "score": 0.80,
            "metadata": {
                "name": "Wine B",
                "rating": 85,
                "variety": "Red",
                "notes": "This is a white wine",
            },
        },
    ]
    return mock_client


@pytest.fixture
def hybrid_searcher(mock_qdrant_client):
    """
    Initialize HybridSearcher with a mocked Qdrant client.
    """
    searcher = HybridSearcher(collection_name="wine")
    searcher.qdrant_client = mock_qdrant_client
    return searcher


def test_search_no_filters(hybrid_searcher):
    """
    Test search without any filters applied.
    """
    results = hybrid_searcher.search(query="red wine", limit=2)

    # Assertions
    assert len(results) == 2

    # Validate score and metadata
    assert isinstance(results[0], SearchResult)
    assert results[0].score == 0.85
    assert results[0].metadata["name"] == "Wine A"
    assert results[0].metadata["notes"] == "This is a red wine"

    assert results[1].score == 0.80
    assert results[1].metadata["name"] == "Wine B"
    assert results[1].metadata["notes"] == "This is a white wine"


def test_search_with_filters(hybrid_searcher):
    """
    Test search with filters applied.
    """
    filters = {"variety": "Red", "rating": {"gte": 80}}
    results = hybrid_searcher.search(query="red wine", limit=2, include=filters)

    # Assertions
    assert len(results) == 2

    # Validate score, variety, and rating
    assert results[0].score == 0.85
    assert results[1].score == 0.80
    assert all(result.metadata["variety"] == "Red" for result in results)
    assert all(result.metadata["rating"] >= 80 for result in results)

    # Validate specific fields
    assert results[0].metadata["name"] == "Wine A"
    assert results[0].metadata["notes"] == "This is a red wine"


def test_construct_filter(hybrid_searcher):
    """
    Test that the filter construction produces the correct conditions.
    """
    include_filters = {"variety": "Red", "rating": {"gte": 85, "lte": 90}}
    query_filter = hybrid_searcher._construct_filter(include=include_filters)

    # Assertions
    assert query_filter is not None
    assert len(query_filter.must) == 2  # Two conditions: variety and rating

    # Validate filter structure
    variety_condition = next(
        cond for cond in query_filter.must if cond.key == "variety"
    )
    assert variety_condition.match.value == "Red"

    rating_condition = next(cond for cond in query_filter.must if cond.key == "rating")
    assert rating_condition.range.gte == 85
    assert rating_condition.range.lte == 90
