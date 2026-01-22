# OpenRouter attribution headers

OpenRouter recommends sending app attribution headers:

- `HTTP-Referer`: your app URL (e.g., `http://localhost` during dev, `https://myapp.com` in production)
- `X-Title`: your app name (e.g., `tech-notes-rag-bot`)

These are useful for OpenRouter analytics and attribution. They help OpenRouter understand which apps are using their service and can be used for analytics, rate limiting, and support.

## Implementation
When using OpenAI-compatible clients, set these as custom headers:
```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://myapp.com",
    "X-Title": "my-app-name"
}
```

## OpenRouter API basics
- Base URL: `https://openrouter.ai/api/v1`
- OpenAI-compatible API: works with standard OpenAI client libraries.
- Model routing: OpenRouter routes requests to the best available model.
- Free models: some models are available for free (check their collections page).
- Rate limits: vary by model and account tier.

## Model selection
- Check available models: `https://openrouter.ai/models`
- Free models collection: `https://openrouter.ai/collections/free-models`
- Model format: `provider/model-name` (e.g., `anthropic/claude-3-haiku`, `openai/gpt-4`)
- Model parameters: temperature, max_tokens, top_p, etc. work as in OpenAI API.

## Best practices
- Always set attribution headers (required for some features).
- Use environment variables for API keys (never commit them).
- Handle rate limits gracefully (429 status code).
- Monitor usage and costs (check OpenRouter dashboard).
- Test with free models first before using paid models.
- Use appropriate model for task (don't use expensive models for simple tasks).

## Error handling
- 401 Unauthorized: invalid or missing API key.
- 429 Too Many Requests: rate limited, implement exponential backoff.
- 500/502/503: service issues, retry with backoff.
- Always log errors for debugging and monitoring.

