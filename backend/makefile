.PHONY: dev start test lint install

# Define environment variables if necessary
ENV_FILE=.env

dev:
	@echo "Running the development server..."
	@source $(ENV_FILE) && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

start:
	@echo "Starting the server..."
	@source $(ENV_FILE) && uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	@echo "Running tests..."
	@source $(ENV_FILE) && pytest --cov=.

lint:
	@echo "Linting code..."
	@source $(ENV_FILE) && flake8 .

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt