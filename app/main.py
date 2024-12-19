from fastapi import FastAPI
from app.routes.search import router as search_router

# Initialize the FastAPI app
app = FastAPI(
    title="Wine Search API",
    description="An API for hybrid searching of wines using metadata and embeddings.",
    version="1.0.0",
)

# Include the search router
app.include_router(search_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
