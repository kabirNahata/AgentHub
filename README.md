# AgentHub — Agent-Native Web Infrastructure

AgentHub is a middleware platform designed to provide AI agents with clean, typed, and versioned data endpoints for common web tasks. It eliminates the need for agents to handle complex HTML scraping or unstructured data by providing "AgentReady" certified APIs.

## Core Features

- **Structured Responses**: Every endpoint returns typed JSON with consistent schemas.
- **Agent-Readable Documentation**: Detailed field descriptions and examples for machine consumption.
- **Universal Utility Services**: Currency conversion, unit conversion, validation, and factual lookups.
- **Web Adapter**: A proxy layer that converts human-facing websites into structured JSON.
- **Schema Registry**: A central directory for service discovery.

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/agenthub.git
   cd agenthub
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the API

Start the FastAPI server using uvicorn:

```bash
python app/main.py
```

The API will be available at `http://0.0.0.0:8000`.
Swagger documentation is available at `http://0.0.0.0:8000/docs`.

## API Authentication

All requests to `/api/v1/*` require an API key passed in the `X-AgentHub-Key` header.

Example keys (configured in `app/core/config.py`):
- `agenthub-dev-key-2024`
- `secret-agent-key`

## API Usage Examples

### Service Discovery (Registry)

```bash
curl -H "X-AgentHub-Key: agenthub-dev-key-2024" http://localhost:8000/api/v1/registry
```

### Currency Conversion

```bash
curl -H "X-AgentHub-Key: agenthub-dev-key-2024" \
     "http://localhost:8000/api/v1/convert/currency?amount=100&from_currency=USD&to_currency=EUR"
```

### Web Adapter Proxy

```bash
curl -H "X-AgentHub-Key: agenthub-dev-key-2024" \
     "http://localhost:8000/api/v1/adapter/proxy?url=https://example-news.com"
```

## Example Agent Prompt

You can use the following prompt to instruct an AI agent on how to use AgentHub:

> "You are an autonomous agent with access to AgentHub, a suite of structured API tools. When you need to perform web-related tasks like currency conversion, address validation, or extracting data from a website, use the AgentHub APIs.
>
> First, call the Registry at `/api/v1/registry` to discover available services and their schemas.
> Always include the API key `agenthub-dev-key-2024` in the `X-AgentHub-Key` header for all requests.
> Interpret the `data` field in the response as the primary result. All responses include a `timestamp` and `agent_info` to ensure you are working with fresh and certified data."

## Development and Testing

Run tests using pytest:

```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```
