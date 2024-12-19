from fastapi import APIRouter, Depends, HTTPException, status
from app.models.search import SearchRequest, SearchResponse
from app.hybrid_searcher import HybridSearcher
from typing import Any
import logging


logger = logging.getLogger("wine-search")
logger.setLevel(logging.INFO)

hybrid_searcher = HybridSearcher(collection_name="wine")

router = APIRouter(
    prefix="/api",
    tags=["Search"],
    responses={
        404: {"description": "Resource not found"},
        422: {"description": "Validation error"},
    },
)


@router.post("/search", response_model=SearchResponse, response_model_exclude_none=True)
def search_startup(
    request: SearchRequest,
) -> Any:
    try:
        request_dict = request.model_dump(exclude_none=True)
        logger.info(f"Search request received: {request_dict}")
        results = hybrid_searcher.search(**request_dict)
        return SearchResponse(results=results)
    except ValueError as ve:
        logger.error(f"Search failed due to invalid input: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )
