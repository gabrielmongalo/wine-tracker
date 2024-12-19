# Install dependencies and set up the environment
env:
	bash setup_env.sh

# Run the FastAPI server locally
run:
	source .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	source .venv/bin/activate && pytest tests/

# Build the Docker image
docker-build:
	docker build -t hybrid-search-app .

# Run the Docker container
docker-run:
	docker run -p 8000:8000 hybrid-search-app

# Load the dataset into Qdrant
load-data:
	source .venv/bin/activate && python vectorstore/client.py