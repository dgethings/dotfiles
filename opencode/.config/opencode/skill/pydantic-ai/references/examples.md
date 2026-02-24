# Pydantic AI Examples

## Hello World

Simple agent with static instructions.

```python
from pydantic_ai import Agent

agent = Agent(
    'openai:gpt-4o',
    instructions='Be concise, reply with one sentence.',
)

result = agent.run_sync('Where does "hello world" come from?')
print(result.output)
# "The first known use of 'hello, world' was in a 1974 textbook about the C programming language."
```

## Bank Support Agent

Agent with tools, dependencies, and structured output.

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

@dataclass
class SupportDependencies:
    customer_id: int
    db: DatabaseConn

class SupportOutput(BaseModel):
    support_advice: str = Field(description='Advice returned to the customer')
    block_card: bool = Field(description="Whether to block the customer's card")
    risk: int = Field(description='Risk level of query', ge=0, le=10)

support_agent = Agent(
    'openai:gpt-4o',
    deps_type=SupportDependencies,
    output_type=SupportOutput,
    instructions='You are a bank support agent.',
)

@support_agent.tool
async def customer_balance(
    ctx: RunContext[SupportDependencies],
    include_pending: bool = False,
) -> float:
    """Returns the customer's current account balance."""
    return await ctx.deps.db.customer_balance(
        id=ctx.deps.customer_id,
        include_pending=include_pending,
    )

async def main():
    deps = SupportDependencies(customer_id=123, db=DatabaseConn())
    result = await support_agent.run('What is my balance?', deps=deps)
    print(result.output)
    # SupportOutput(support_advice='Your balance is $123.45', block_card=False, risk=1)
```

## Streaming Responses

Stream text as it's generated.

```python
agent = Agent('openai:gpt-4o', instructions='Tell a short story.')

async def main():
    async with agent.run_stream('Tell me about space exploration') as response:
        async for chunk in response.stream_text():
            print(chunk, end='', flush=True)
```

## Stream Structured Output

Stream structured data chunks.

```python
from pydantic import BaseModel
from typing import Literal

class StoryPart(BaseModel):
    content: str
    type: Literal['intro', 'action', 'conclusion']

agent = Agent('openai:gpt-4o', output_type=StoryPart)

async def main():
    async with agent.run_stream('Tell a story') as response:
        async for chunk in response.stream_structured(debounce_by=0.1):
            print(f"[{chunk.type}] {chunk.content}")
```

## Stream All Events

Access complete event stream for debugging.

```python
from pydantic_ai import (
    Agent,
    AgentStreamEvent,
    PartStartEvent,
    FunctionToolCallEvent,
)

agent = Agent('openai:gpt-4o')

@agent.tool
async def search(query: str) -> str:
    """Search the web."""
    return f"Results for {query}"

async def main():
    async for event in agent.run_stream_events('What is Python?'):
        if isinstance(event, PartStartEvent):
            print(f"Part {event.index} started")
        elif isinstance(event, FunctionToolCallEvent):
            print(f"Tool called: {event.part.tool_name}")
```

## Dynamic Instructions

Instructions that depend on runtime dependencies.

```python
from datetime import date

agent = Agent('openai:gpt-4o', deps_type=date)

@agent.instructions
async def add_context(ctx: RunContext[date]) -> str:
    return f"Today is {ctx.deps}. Provide context-appropriate responses."

result = await agent.run('What should I wear?', deps=date.today())
```

## Multi-Agent Workflow

Multiple agents working together.

```python
researcher = Agent('openai:gpt-4o', instructions='Research topics thoroughly.')
writer = Agent('openai:gpt-4o', instructions='Write engaging content.')

async def research_and_write(topic: str) -> str:
    # Research phase
    research = await researcher.run(f'Research: {topic}')
    research_data = research.output

    # Writing phase
    draft = await writer.run(f'Write an article based on: {research_data}')
    return draft.output
```

## Graph-Based Agent

Use pydantic_graph for complex workflows.

```python
from pydantic_graph import Graph, End, GraphRunContext

@dataclass
class State:
    topic: str
    research: str = ''
    article: str = ''

async def research_step(ctx: GraphRunContext[State, None]) -> State:
    agent = Agent('openai:gpt-4o', instructions='Research the topic.')
    result = await agent.run(f'Research: {ctx.state.topic}')
    ctx.state.research = result.output
    return ctx.state

async def write_step(ctx: GraphRunContext[State, None]) -> End:
    agent = Agent('openai:gpt-4o', instructions='Write based on research.')
    result = await agent.run(f'Write about: {ctx.state.research}')
    ctx.state.article = result.output
    return End(ctx.state)

graph = Graph(nodes=[research_step, write_step])

async def main():
    state = State(topic='Climate change')
    final_state = await graph.run(state)
    print(final_state.article)
```

## A2A Server

Expose agent as an A2A server.

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', instructions='Be helpful!')
app = agent.to_a2a()

# Run with: uvicorn a2a_server:app --host 0.0.0.0 --port 8000
```

## Tool with Multiple Parameters

Tools with complex parameter schemas.

```python
from pydantic import BaseModel

class SearchParams(BaseModel):
    query: str
    max_results: int = 10
    include_images: bool = False

@agent.tool
async def search_web(params: SearchParams) -> list[str]:
    """Search the web with parameters."""
    # Implementation
    return [f"Result 1 for {params.query}"]
```

## Retry Configuration

Configure retry behavior for model requests.

```python
from pydantic_ai import Agent
from pydantic_ai.retries import RetrySettings

agent = Agent(
    'openai:gpt-4o',
    retry_settings=RetrySettings(
        max_retries=3,
        initial_delay_ms=100,
        exponential_base=2,
    ),
)
```

## Tool Validation

Validate tool calls before execution.

```python
@agent.tool
async def sensitive_operation(ctx: RunContext[Dependencies], action: str) -> str:
    """Perform a sensitive operation requiring approval."""
    if not ctx.deps.is_approved(action):
        raise ValueError("Action not approved")
    return f"Executed: {action}"
```

## Multiple Output Tools

Agent can choose which output tool to call.

```python
from pydantic_ai import Agent, Tool
from pydantic import BaseModel

class SuccessOutput(BaseModel):
    result: str

class ErrorOutput(BaseModel):
    error: str
    code: int

agent = Agent(
    'openai:gpt-4o',
    output_tools=[
        Tool.validate_as_type(SuccessOutput),
        Tool.validate_as_type(ErrorOutput),
    ],
)

result = await agent.run('Process data')
if isinstance(result.output, SuccessOutput):
    print(result.output.result)
else:
    print(f"Error: {result.output.error}")
```

## Conversation History

Maintain conversation across multiple runs.

```python
messages = []

async def chat(user_input: str):
    global messages
    messages.append(ModelTextPart(user_input))

    agent = Agent('openai:gpt-4o')
    result = await agent.run(
        '',
        message_history=messages,
    )

    messages.extend(result.all_messages())
    return result.output
```

## Thinking Model

Use thinking-capable models.

```python
from pydantic_ai import Agent

agent = Agent('openai:o1', instructions='Think through problems carefully.')

async with agent.run_stream('Solve: 25 * 47') as response:
    async for chunk in response.stream_text():
        print(chunk, end='')
```

## Image Input

Process images with multimodal models.

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def analyze_image(image_path: str):
    result = await agent.run(
        'Describe this image',
        messages=[ModelImagePart.from_path(image_path)],
    )
    return result.output
```
