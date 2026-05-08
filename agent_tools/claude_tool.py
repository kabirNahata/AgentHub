# Claude Tool Definition for AgentHub Web Adapter

CLAUDE_WEB_ADAPTER_TOOL = {
    "name": "agenthub_web_adapter",
    "description": "Converts a human-facing website into clean, agent-readable JSON. Useful for extracting structured data from any URL.",
    "input_schema": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The URL of the website to adapt."
            }
        },
        "required": ["url"]
    }
}

# Example usage with Anthropic Python SDK:
#
# response = client.messages.create(
#     model="claude-3-5-sonnet-20240620",
#     max_tokens=1024,
#     tools=[CLAUDE_WEB_ADAPTER_TOOL],
#     messages=[{"role": "user", "content": "What are the latest news on example.com?"}]
# )
