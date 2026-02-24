# Pydantic AI API Reference

## Agent Class

```python
from pydantic_ai import Agent

agent = Agent(
    model='openai:gpt-4o',
    *,
    instructions: str | None = None,
    deps_type: type = None,
    output_type: type[BaseModel] | None = None,
    model_settings: ModelSettings | None = None,
    instrument: bool | InstrumentationSettings | None = None,
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | str or Model | LLM model identifier or Model instance |
| `instructions` | str | Static system instructions for the agent |
| `deps_type` | type | Type annotation for dependency injection |
| `output_type` | type[BaseModel] | Pydantic model for structured output |
| `model_settings` | ModelSettings | Default model configuration |
| `instrument` | bool | Enable instrumentation |

### Methods

#### `agent.run(message, *, deps=None, model=None, model_settings=None)`

Async execution. Returns `RunResult`.

```python
result = await agent.run('Hello, world!', deps=deps)
print(result.output)
print(result.messages)  # Message history
```

#### `agent.run_sync(message, *, deps=None, model=None, model_settings=None)`

Synchronous execution. Returns `RunResult`.

```python
result = agent.run_sync('Hello, world!')
```

#### `agent.run_stream(message, *, deps=None, model=None, ...)`

Stream text or structured output. Returns async context manager.

```python
async with agent.run_stream('Tell me a story') as response:
    async for chunk in response.stream_text():
        print(chunk, end='')
```

#### `agent.run_stream_events(message, *, deps=None, model=None, ...)`

Stream all events. Returns async iterable.

```python
async for event in agent.run_stream_events('Hello'):
    if isinstance(event, PartStartEvent):
        print(f"Part {event.index} started")
```

#### `agent.iter(message, *, deps=None, ...)`

Iterate over graph nodes. Returns context manager.

```python
async with agent.iter('Hello') as run:
    async for node in run:
        print(node)
```

## Decorators

### `@agent.tool`

Register a function tool.

```python
@agent.tool
async def my_tool(
    ctx: RunContext[Dependencies],
    param1: str,
    param2: int = 10,
) -> str:
    """Tool description shown to LLM."""
    return f"Result: {param1}, {param2}"
```

The first parameter can be `RunContext[Dependencies]` for dependency injection.
Other parameters form the tool schema sent to the LLM.

### `@agent.tool_plain`

Register a tool without automatic schema generation.

```python
@agent.tool_plain
async def my_tool_plain(ctx: RunContext[Dependencies]) -> ToolReturn:
    return ToolReturn(
        content="Result",
        tool_name="my_tool_plain",
    )
```

### `@agent.instructions`

Register dynamic instructions.

```python
@agent.instructions
async def dynamic_instructions(ctx: RunContext[Dependencies]) -> str:
    return f"Current user: {ctx.deps.user_id}"
```

### `@agent.result_validator`

Validate agent output before returning.

```python
@agent.result_validator
async def validate_output(ctx: RunContext[Dependencies], result: OutputType) -> OutputType:
    # Modify or validate result
    return result
```

## RunContext

Provides access to dependencies and agent context.

```python
@agent.tool
async def my_tool(ctx: RunContext[Dependencies], query: str) -> str:
    deps = ctx.deps  # Access dependencies
    # Implementation
```

## RunResult

Result of agent execution.

```python
result: RunResult = await agent.run('Hello')
print(result.output)  # Final output
print(result.messages)  # List of ModelMessages
print(result.usage)  # Token usage
```

## StreamedRunResult

Streaming result with methods to access streamed content.

```python
async with agent.run_stream('Hello') as response:
    async for chunk in response.stream_text():
        print(chunk)

    async for chunk in response.stream_structured():
        print(chunk)  # Structured output chunks

    final = await response.get()
```

## ModelSettings

Configuration for model requests.

```python
from pydantic_ai.settings import ModelSettings

settings = ModelSettings(
    temperature=0.7,
    max_tokens=1000,
    timeout_ms=30000,
    top_p=0.9,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)
```

## ToolReturn

Return value for `@agent.tool_plain`.

```python
from pydantic_ai.tools import ToolReturn

@agent.tool_plain
async def my_tool(ctx: RunContext[Dependencies]) -> ToolReturn:
    return ToolReturn(
        content="Tool result",
        tool_name="my_tool",
        tool_call_id="call_123",
    )
```

## Output Types

Use Pydantic models for structured outputs.

```python
from pydantic import BaseModel, Field

class MyOutput(BaseModel):
    name: str
    value: int = Field(ge=0)
    items: list[str]

agent = Agent('openai:gpt-4o', output_type=MyOutput)
result = await agent.run('Create something')
output: MyOutput = result.output  # Guaranteed to be MyOutput
```

## Dependency Injection

Use dataclasses or Pydantic models for dependencies.

```python
from dataclasses import dataclass

@dataclass
class MyDeps:
    db: Database
    config: Config

agent = Agent('openai:gpt-4o', deps_type=MyDeps)

@agent.tool
async def my_tool(ctx: RunContext[MyDeps], query: str) -> str:
    data = await ctx.deps.db.fetch(query)
    return data
```

## Toolsets

Group related tools into a toolset.

```python
from pydantic_ai import Agent, Tool

weather_tool = Tool(
    lambda location: f"Weather in {location}: 72°F",
    name="get_weather",
    description="Get weather for a location",
)

agent = Agent('openai:gpt-4o', tools=[weather_tool])
```

## Events

Event types for `run_stream_events`:

- `PartStartEvent` - A new part started
- `PartDeltaEvent` - Incremental update to a part
- `PartEndEvent` - A part completed
- `FunctionToolCallEvent` - Tool was called
- `FunctionToolResultEvent` - Tool returned result
- `FinalResultEvent` - Final result started
- `AgentRunResultEvent` - Run completed

```python
from pydantic_ai import (
    AgentStreamEvent,
    PartStartEvent,
    FunctionToolCallEvent,
)

async for event in agent.run_stream_events('Hello'):
    if isinstance(event, PartStartEvent):
        print(f"Part {event.index} started: {event.part}")
    elif isinstance(event, FunctionToolCallEvent):
        print(f"Tool called: {event.part.tool_name}")
```
