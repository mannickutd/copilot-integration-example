# copilot-integration-example
Demonstrate an integration with github copilot

## Dependencies
UV is required to run


## Installation
Install python dependencies
```
uv sync
```

Start up the postgres database
```
uv run docker compose up -d
```

## Migration
Run alembic migrations
```
PYTHONPATH=. uv run alembic upgrade head
```

## Run tests
Run pytest
```
uv run pytest tests
```

## Usage
```
uv run uvicorn copilot_integration_example.api:app --host 0.0.0.0 --port 80
```
