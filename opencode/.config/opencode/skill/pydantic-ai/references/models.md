# Supported Models

Pydantic AI supports virtually every LLM provider through a unified API.

## Model Specification Syntax

Models are specified as `{provider}:{model}` or `{gateway}/{provider}:{model}`.

Examples:
- `openai:gpt-4o`
- `anthropic:claude-3-5-sonnet-20241022`
- `google:gemini-2.0-flash-exp`
- `gateway/openai:gpt-4o` (via Pydantic AI Gateway)

## Supported Providers

### OpenAI

```python
agent = Agent('openai:gpt-4o')
```

Models: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo, o1, o1-mini

API Key: `OPENAI_API_KEY` environment variable

### Anthropic

```python
agent = Agent('anthropic:claude-3-5-sonnet-20241022')
```

Models: claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus

API Key: `ANTHROPIC_API_KEY` environment variable

### Google

```python
agent = Agent('google:gemini-2.0-flash-exp')
```

Models: gemini-2.0-flash, gemini-2.5-pro, gemini-1.5-pro

API Key: `GOOGLE_API_KEY` environment variable

### Groq

```python
agent = Agent('groq:llama-3.3-70b-versatile')
```

Models: llama-3.3-70b, llama-3.1-70b, mixtral-8x7b

API Key: `GROQ_API_KEY` environment variable

### OpenRouter

```python
agent = Agent('openrouter:anthropic/claude-3.5-sonnet')
```

Models: Access to 100+ models from various providers

API Key: `OPENROUTER_API_KEY` environment variable

### Azure OpenAI

```python
from pydantic_ai.models.azure import AzureOpenAIModel
model = AzureOpenAIModel('gpt-4o', endpoint='https://...', api_key='...')
agent = Agent(model)
```

### AWS Bedrock

```python
from pydantic_ai.models.bedrock import BedrockModel
model = BedrockModel('anthropic.claude-3-5-sonnet-20241022-v2:0')
agent = Agent(model)
```

### Other Providers

- **Mistral**: `mistral:mistral-large-latest`
- **Cohere**: `cohere:command-r-plus`
- **Hugging Face**: `huggingface:{model_id}`
- **Cerebras**: `cerebras:llama3.1-70b`
- **DeepSeek**: `deepseek:deepseek-chat`
- **Perplexity**: `perplexity:sonar-medium-online`

## Gateway

The Pydantic AI Gateway provides unified access and routing:

```python
agent = Agent('gateway/openai:gpt-4o')
# or
agent = Agent('gateway/anthropic:claude-3-5-sonnet-20241022')
```

Gateway API Key: `PYDANTIC_AI_GATEWAY_API_KEY`

## Custom Models

Implement custom models by subclassing `KnownModel`:

```python
from pydantic_ai.models import KnownModel

class CustomModel(KnownModel):
    async def request(self, messages):
        # Implementation
        pass
```

## Model Configuration

Set model at runtime:

```python
agent = Agent()  # No default model
result = await agent.run('Hello', model='openai:gpt-4o')
```

Or configure model settings:

```python
from pydantic_ai.settings import ModelSettings

agent = Agent(
    'openai:gpt-4o',
    model_settings=ModelSettings(
        temperature=0.7,
        max_tokens=1000,
        timeout_ms=30000
    )
)
```

## Slim Installation

Install only required dependencies:

```bash
uv add "pydantic-ai-slim[openai,anthropic]"
```

Available extras: `openai`, `anthropic`, `google`, `groq`, `mistral`, `cohere`, `bedrock`, `huggingface`, `logfire`, `evals`, `mcp`, `a2a`, `ui`, etc.
