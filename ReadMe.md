# **Hybrid Search and Summarization API**

This project provides an API to perform hybrid search and summarization of reviews using **FastAPI** and **Qdrant**. It combines dense and sparse vector embeddings for powerful hybrid search capabilities and offers an intuitive interface for querying review data.

---

## **Features**

- **Hybrid Search**: Combines sparse (BM25) and dense (transformers) vector embeddings for accurate and efficient search results.
- **Filtering**: Supports filtering results based on metadata (e.g., `rating`, `variety`).
- **Summarization**: Summarizes review texts for quick insights.
- **Flexible Deployment**: Supports local and containerized (Docker) setups.
- **Scalable Vector Search**: Uses [Qdrant](https://qdrant.tech/) as the vector database.

---

## **Prerequisites**

Before starting, ensure the following are installed:

- [Python 3.12](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/) (optional, for containerized deployment)
- A running [Qdrant instance](https://qdrant.tech/documentation/) (default URL: `http://localhost:6333`)

---

## **Installation**

### **Local Development**

1. Clone the repository:

   ```bash
   git clone https://github.com/gabrielmongalo/wine-tracker.git
   cd wine-tracker
   ```

2. Set up the Python environment:

   ```bash
   bash setup_env.sh
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

4. Start the FastAPI server:

   ```bash
   make run
   ```

5. Load the dataset into Qdrant:

   ```bash
   make load-data
   ```

6. Access the API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### **Docker Deployment**

1. Build the Docker image:

   ```bash
   make docker-build
   ```

2. Run the Docker container:

   ```bash
   make docker-run
   ```

3. Access the API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## **Usage**

### **Endpoints**

- `POST /api/search`: Perform a hybrid search with optional filters.
  - **Request Body**:
    ```json
    {
      "query": "Red wine",
      "limit": 10,
      "include": {
        "variety": "Red Wine",
        "rating": {
          "gte": 80
        }
      }
    }
    ```
  - **Response**:
    ```json
    {
      "results": [
        {
          "score": 0.85,
          "metadata": {
            "name": "Wine A",
            "rating": 90,
            "variety": "Red",
            "notes": "A full-bodied red wine."
          }
        }
      ]
    }
    ```

### **Accessing the API**

1. **Local Environment**:
   - `http://localhost:8000/api/search`
2. **Docker Container**:
   - Replace `localhost` with the container's IP or hostname.

---

## **Qdrant Integration**

- [Qdrant](https://qdrant.tech/) is a vector database for high-performance vector search and similarity matching.
- The project uses Qdrant's REST API for vector management and hybrid search.

**Key Features of Qdrant**:

- Scalable vector search for dense and sparse embeddings.
- Hybrid search support out of the box.
- Easy-to-integrate Python client.

Learn more: [Qdrant Documentation](https://qdrant.tech/documentation/)

---

## **Testing**

Run unit tests to ensure everything works as expected:

```bash
make test
```

---

## **Project Structure**

```plaintext
hybrid-search-app/
├── app/                    # Application logic
│   ├── models/             # Pydantic models
│   ├── routes/             # API endpoints
│   ├── hybrid_searcher.py  # Core search functionality
│   ├── main.py             # FastAPI entry point
├── tests/                  # Unit tests
├── vectorstore/            # Qdrant client and dataset loader
├── requirements.txt        # Python dependencies
├── setup_env.sh            # Setup script for local development
├── Dockerfile              # Docker configuration
├── makefile                # Common project commands
└── ReadMe.md               # Project documentation
```

---

## **References**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Transformers by Hugging Face](https://huggingface.co/docs/transformers/)
- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)

---

Feel free to customize this as needed. Let me know if there are additional features or sections you'd like to include! 🚀
