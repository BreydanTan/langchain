# 🧠 LangChain Cognitive Learning Engine - Complete Teaching Modules (English)

This document contains complete content for all 8 learning modules. Each module includes answers to the previous module's challenges for convenient self-paced study with spaced retrieval practice.

---

## 📚 Table of Contents

1. [Module 1: Architecture & Core Concepts](#module-1-architecture--core-concepts)
2. [Module 2: Message System](#module-2-message-system)
3. [Module 3: Prompt Engineering](#module-3-prompt-engineering)
4. [Module 4: Core Runnable Abstraction](#module-4-core-runnable-abstraction)
5. [Module 5: Chat Models](#module-5-chat-models)
6. [Module 6: Chain Composition (LCEL)](#module-6-chain-composition-lcel)
7. [Module 7: Tools & Agents](#module-7-tools--agents)
8. [Module 8: Advanced Features](#module-8-advanced-features)

---

# Module 1: Architecture & Core Concepts

## 1.1 Monorepo Structure

```
/home/user/langchain/libs/
├─ core/              ⭐ Core abstraction layer (most important)
├─ langchain_v1/      📦 Main package
├─ partners/          🔌 Official integrations
└─ text-splitters/    ✂️  Utility libraries
```

## 1.2 Three Design Principles

### Principle 1: Everything is Runnable
```python
class Runnable(ABC, Generic[Input, Output]):
    def invoke(self, input: Input) -> Output
    def batch(self, inputs: list[Input]) -> list[Output]
    def stream(self, input: Input) -> Iterator[Output]
    async def ainvoke(self, input: Input) -> Output
```

### Principle 2: Declarative Composition (Pipe `|`)
```python
chain = component1 | component2 | component3
chain.invoke(input)  # Automatically chains execution
```

### Principle 3: Plugin Architecture
```
langchain_core defines interfaces
    ↓
langchain_anthropic/openai implement interfaces
```

## 🧠 Knowledge Challenge

1. Which package is the "foundation"? Why?
2. What are the 4 core methods of Runnable?
3. What happens when `prompt | llm` executes?

---

# Module 2: Message System

## 📝 Module 1 Answers

1. **Foundation:** `libs/core/` - All packages depend on it, defines stable interfaces
2. **4 Methods:** `invoke()` (single), `batch()` (batch), `stream()` (streaming), `ainvoke()` (async)
3. **Execution Flow:**
   ```
   User input → prompt.invoke() → Prompt object
             → llm.invoke() → AIMessage
   ```

## 2.1 Message Type Hierarchy

```
BaseMessage
├─ HumanMessage (type="human")    # User input
├─ AIMessage (type="ai")          # AI response
├─ SystemMessage (type="system")  # System instructions
└─ ToolMessage (type="tool")      # Tool results
```

**File Locations:**
- `libs/core/langchain_core/messages/base.py:93`
- `libs/core/langchain_core/messages/human.py:9`
- `libs/core/langchain_core/messages/ai.py`

## 2.2 Core Usage

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Typical conversation structure
conversation = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is 2+2?"),
    AIMessage(content="2+2 equals 4."),
]

# Multimodal content
msg = HumanMessage(content=[
    {"type": "text", "text": "What's in this image?"},
    {"type": "image_url", "image_url": {"url": "..."}}
])

# AI message with tool calls
ai_msg = AIMessage(
    content="Let me check the weather.",
    tool_calls=[{"name": "get_weather", "args": {"city": "SF"}}]
)
```

## 🧠 Knowledge Challenge

1. What are the three core message types and their purposes?
2. How would you build prompts for a customer service chatbot? (pseudocode)
3. What is the purpose of the `tool_calls` field in AIMessage?

---

# Module 3: Prompt Engineering

## 📝 Module 2 Answers

1. **Three Types:**
   - `SystemMessage` - Sets AI behavior
   - `HumanMessage` - User input
   - `AIMessage` - AI response

2. **Customer Service Bot:**
```python
messages = [
    SystemMessage(content="You are a professional customer service rep. Rules: 1) Stay polite 2) Escalate to human if unsure"),
    HumanMessage(content="Where is my order?")
]
```

3. **tool_calls:** Enables AI to invoke external tools (search, calculator, etc.), breaking through LLM knowledge limitations

## 3.1 Prompt Template Types

```
BasePromptTemplate
├─ PromptTemplate        # String templates
└─ ChatPromptTemplate    # Chat templates
   └─ MessagesPlaceholder # History placeholder
```

**File Locations:**
- `libs/core/langchain_core/prompts/prompt.py:24`
- `libs/core/langchain_core/prompts/chat.py`

## 3.2 Core Usage

### PromptTemplate (Simple Strings)
```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {topic}."
)
prompt.format(adjective="funny", topic="cats")
# → "Tell me a funny joke about cats."

# As Runnable
prompt.invoke({"adjective": "funny", "topic": "cats"})
# → StringPromptValue(...)
```

### ChatPromptTemplate (Chat Templates)
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are {role}."),
    ("human", "{input}"),
])

prompt.invoke({"role": "chef", "input": "How to cook?"})
# → ChatPromptValue(messages=[
#     SystemMessage(content="You are chef."),
#     HumanMessage(content="How to cook?"),
# ])
```

### MessagesPlaceholder (Conversation History)
```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    MessagesPlaceholder("history"),  # Insert history
    ("human", "{question}"),
])

prompt.invoke({
    "history": [("human", "5+2?"), ("ai", "7")],
    "question": "multiply by 4"
})
# → Automatically expands history into full message list
```

## 3.3 Practical: Combining Prompt + Model

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a comedian."),
    ("human", "Joke about {topic}"),
])

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

chain = prompt | model  # LCEL composition

chain.invoke({"topic": "programming"})
# → AIMessage("Why do programmers prefer dark mode?...")
```

**Execution Flow:**
```
{"topic": "programming"}
    ↓ prompt.invoke()
ChatPromptValue([SystemMessage(...), HumanMessage(...)])
    ↓ model.invoke()
AIMessage("...")
```

## 🧠 Knowledge Challenge

1. Difference between `PromptTemplate` vs `ChatPromptTemplate`?
2. What problem does `MessagesPlaceholder` solve?
3. Predict output: `(prompt | model).invoke({"role": "chef", "input": "pasta?"})`

---

# Module 4: Core Runnable Abstraction

## 📝 Module 3 Answers

1. **Difference:**
   - `PromptTemplate` → Generates strings (StringPromptValue)
   - `ChatPromptTemplate` → Generates message lists (ChatPromptValue)

2. **MessagesPlaceholder:** Dynamically inserts conversation history, avoiding manual message list concatenation

3. **Predicted Output:**
```python
# Step 1: prompt.invoke() generates messages
# Step 2: model.invoke() calls Claude
# Final output: AIMessage(content="To make pasta, first boil water...")
```

## 4.1 Deep Dive into Runnable Protocol

**File Location:** `libs/core/langchain_core/runnables/base.py:124`

```python
class Runnable(ABC, Generic[Input, Output]):
    """A unit of work that can be invoked, batched, streamed, transformed and composed"""

    # 🔑 Core methods (must implement)
    @abstractmethod
    def invoke(self, input: Input, config: RunnableConfig | None = None) -> Output:
        """Single synchronous invocation"""

    # 🔑 Default implementations (optional to override for optimization)
    def batch(
        self,
        inputs: list[Input],
        config: RunnableConfig | None = None
    ) -> list[Output]:
        """Batch processing (defaults to parallel invoke calls)"""

    def stream(
        self,
        input: Input,
        config: RunnableConfig | None = None
    ) -> Iterator[Output]:
        """Streaming output (defaults to single return)"""

    async def ainvoke(
        self,
        input: Input,
        config: RunnableConfig | None = None
    ) -> Output:
        """Async invocation (defaults to invoke in thread pool)"""
```

## 4.2 Why is Runnable So Important?

### Reason 1: Unified Interface
All components implement Runnable → consistent calling pattern

```python
# These all have the same methods!
prompt.invoke(...)
model.invoke(...)
chain.invoke(...)
retriever.invoke(...)
```

### Reason 2: Automatic Composition
Chains created with `|` automatically inherit all Runnable methods

```python
chain = prompt | model | output_parser

# Automatically supports:
chain.invoke(input)
chain.batch([input1, input2])
chain.stream(input)
await chain.ainvoke(input)
```

### Reason 3: Config Propagation
`RunnableConfig` automatically propagates through chains (for callbacks, tags, metadata, etc.)

```python
chain.invoke(
    input,
    config={
        "tags": ["experiment"],
        "metadata": {"user_id": "123"}
    }
)
# config passes to every component in the chain
```

## 4.3 Runnable Composition Primitives

### RunnableSequence (Sequential Execution)
```python
from langchain_core.runnables import RunnableLambda

# Using | to create (recommended)
seq = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 2)
seq.invoke(5)  # (5+1)*2 = 12

# Equivalent to
from langchain_core.runnables import RunnableSequence
seq = RunnableSequence(steps=[...])
```

**Execution Flow:**
```
Input(5) → [step1: +1] → 6 → [step2: *2] → Output(12)
```

### RunnableParallel (Parallel Execution)
```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    add=RunnableLambda(lambda x: x + 1),
    mul=RunnableLambda(lambda x: x * 2),
)
parallel.invoke(5)
# {"add": 6, "mul": 10}

# Using in chains
chain = parallel | RunnableLambda(lambda d: d["add"] + d["mul"])
chain.invoke(5)  # 6 + 10 = 16
```

**Execution Flow:**
```
Input(5) ┬→ [add: +1] → 6  ┐
         └→ [mul: *2] → 10 ┘→ {"add": 6, "mul": 10}
```

### RunnableLambda (Custom Functions)
```python
from langchain_core.runnables import RunnableLambda

def my_function(input_dict):
    return input_dict["x"] * 2

runnable_fn = RunnableLambda(my_function)
runnable_fn.invoke({"x": 5})  # 10

# Or using decorator
@RunnableLambda
def my_function(x):
    return x * 2
```

## 4.4 Practical: Building Complex Chains

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_anthropic import ChatAnthropic

# Step 1: Create two parallel branches
branch_a = ChatPromptTemplate.from_template("Summarize: {text}") | model
branch_b = ChatPromptTemplate.from_template("Translate to French: {text}") | model

# Step 2: Execute in parallel
parallel_chain = RunnableParallel(summary=branch_a, translation=branch_b)

# Step 3: Merge results
def combine(results):
    return f"Summary: {results['summary'].content}\n\nFrench: {results['translation'].content}"

final_chain = parallel_chain | RunnableLambda(combine)

# Execute
final_chain.invoke({"text": "LangChain is awesome!"})
```

**Flow Diagram:**
```
{"text": "..."}
    ┌→ [Summarize prompt] → [Model] → summary ┐
    └→ [Translate prompt] → [Model] → translation ┘
                    ↓
              [Combine function]
                    ↓
        "Summary: ...\nFrench: ..."
```

## 🧠 Knowledge Challenge

1. Of Runnable's 4 core methods, which is abstract (must be implemented)?
2. Difference between `RunnableSequence` and `RunnableParallel`? Give examples
3. Predict output:
```python
chain = RunnableLambda(lambda x: x["a"] + x["b"]) | RunnableLambda(lambda x: x * 3)
chain.invoke({"a": 2, "b": 3})
```

---

# Module 5: Chat Models

## 📝 Module 4 Answers

1. **Abstract Method:** `invoke()` is the only abstract method, other methods have default implementations

2. **Difference:**
   - `RunnableSequence` - Sequential execution, output→input chaining
   - `RunnableParallel` - Parallel execution, all branches receive same input, returns dict

3. **Predicted Output:**
```python
# Step 1: lambda x: x["a"] + x["b"] → 2 + 3 = 5
# Step 2: lambda x: x * 3 → 5 * 3 = 15
# Output: 15
```

## 5.1 BaseChatModel Architecture

**File Location:** `libs/core/langchain_core/language_models/chat_models.py`

```python
class BaseChatModel(BaseLanguageModel[BaseMessage], ABC):
    """Abstract base class for chat models

    All chat model providers (OpenAI, Anthropic, etc.) inherit this class
    """

    @abstractmethod
    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Core generation method (subclasses must implement)"""

    # Advanced features
    def bind_tools(
        self,
        tools: Sequence[BaseTool | dict],
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        """Bind tools to support function calling"""

    def with_structured_output(
        self,
        schema: type[BaseModel] | dict,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseModel | dict]:
        """Force output to conform to specific structure"""
```

## 5.2 Using Chat Models

### Basic Invocation
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=1024,
)

# Method 1: Using message lists
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?"),
]
response = model.invoke(messages)
# → AIMessage(content="The capital of France is Paris.")

# Method 2: Using strings (automatically converts to HumanMessage)
response = model.invoke("What is 2+2?")
# → AIMessage(content="2+2 equals 4.")
```

### Streaming Output
```python
for chunk in model.stream("Tell me a long story"):
    print(chunk.content, end="", flush=True)
# Output: Once... upon... a... time...
```

### Batch Processing
```python
results = model.batch([
    "What is 1+1?",
    "What is 2+2?",
    "What is 3+3?",
])
# → [AIMessage("2"), AIMessage("4"), AIMessage("6")]
```

## 5.3 Tool Calling (Function Calling)

```python
from langchain_core.tools import tool

# Define tool
@tool
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny."

# Bind tool to model
model_with_tools = model.bind_tools([get_weather])

# AI will generate tool calls
response = model_with_tools.invoke("What's the weather in SF?")
print(response.tool_calls)
# → [{"name": "get_weather", "args": {"location": "SF"}, "id": "..."}]

# Execute tool and return result
from langchain_core.messages import ToolMessage

tool_call = response.tool_calls[0]
tool_result = get_weather.invoke(tool_call["args"])

messages = [
    HumanMessage(content="What's the weather in SF?"),
    response,  # AIMessage with tool_calls
    ToolMessage(content=tool_result, tool_call_id=tool_call["id"]),
]

final_response = model.invoke(messages)
# → AIMessage("The weather in San Francisco is sunny.")
```

**Tool Calling Flow:**
```
User question → AI generates tool_call → Execute tool → Return ToolMessage → AI generates final answer
```

## 5.4 Structured Output

```python
from pydantic import BaseModel, Field

class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")

structured_model = model.with_structured_output(Joke)

result = structured_model.invoke("Tell me a joke about cats")
# → Joke(
#     setup="Why don't cats play poker in the jungle?",
#     punchline="Too many cheetahs!"
# )

print(result.setup)      # Type-safe access
print(result.punchline)
```

## 🧠 Knowledge Challenge

1. What is the core abstract method of `BaseChatModel`?
2. Difference between `bind_tools()` and `with_structured_output()`?
3. What is the complete flow of tool calling? (describe with flow diagram)

---

# Module 6: Chain Composition (LCEL)

## 📝 Module 5 Answers

1. **Core Abstract Method:** `_generate()` - Subclasses must implement this method to generate responses

2. **Difference:**
   - `bind_tools()` - Enables AI to call external tools (AI decides whether to call)
   - `with_structured_output()` - Forces AI output to conform to specific structure (Pydantic model)

3. **Tool Calling Flow:**
```
User question
  → AI analyzes and generates tool_call
  → Your code executes tool function
  → Return result as ToolMessage
  → AI generates final answer based on tool result
```

## 6.1 What is LCEL?

**LCEL = LangChain Expression Language**

This is LangChain's "pipeline syntax" for composing components in a declarative way.

**Core Idea:** Use the `|` operator to connect Runnable objects

```python
# Traditional approach (imperative)
prompt_result = prompt.invoke(input)
model_result = model.invoke(prompt_result)
parser_result = parser.invoke(model_result)

# LCEL approach (declarative)
chain = prompt | model | parser
result = chain.invoke(input)
```

**Why is LCEL Better?**
- ✅ **Automatic support for all Runnable methods** (invoke, batch, stream, ainvoke)
- ✅ **Composable** - Chains can be components of other chains
- ✅ **Automatic error handling and retry**
- ✅ **Built-in tracing and debugging**

## 6.2 LCEL Core Operators

### 1️⃣ Pipe Operator `|` (Sequential Composition)

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
parser = StrOutputParser()  # Extracts AIMessage.content

chain = prompt | model | parser

result = chain.invoke({"topic": "cats"})
# → "Why did the cat sit on the computer? ..." (direct string)
```

**Data Flow:**
```
{"topic": "cats"}
  → prompt → ChatPromptValue([HumanMessage("Tell me a joke about cats")])
  → model  → AIMessage(content="Why did the cat...")
  → parser → "Why did the cat..." (str)
```

### 2️⃣ Dict Operator `{}` (Parallel Composition)

```python
from langchain_core.runnables import RunnablePassthrough

chain = {
    "context": retriever,  # Parallel branch 1
    "question": RunnablePassthrough()  # Parallel branch 2 (passes input through)
} | prompt | model

chain.invoke("What is LangChain?")
```

**Data Flow:**
```
"What is LangChain?"
    ┌→ retriever.invoke() → Retrieved documents ┐
    └→ RunnablePassthrough() → "What is LangChain?" ┘
              ↓
    {"context": "...", "question": "What is LangChain?"}
              ↓
          prompt | model
```

### 3️⃣ Conditional Branching `RunnableBranch`

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

def is_short(input):
    return len(input) < 10

branch = RunnableBranch(
    (is_short, RunnableLambda(lambda x: f"Short: {x}")),
    (lambda x: len(x) < 50, RunnableLambda(lambda x: f"Medium: {x}")),
    RunnableLambda(lambda x: f"Long: {x}")  # Default branch
)

branch.invoke("Hi")        # → "Short: Hi"
branch.invoke("Hello world!")  # → "Medium: Hello world!"
```

## 6.3 Practical: RAG Chain (Retrieval Augmented Generation)

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Assume you have a vector database retriever
# retriever = ...

prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context:

Context: {context}

Question: {question}
""")

# Build RAG chain
rag_chain = (
    {
        "context": lambda x: retriever.invoke(x["question"]),
        "question": lambda x: x["question"]
    }
    | prompt
    | model
    | StrOutputParser()
)

result = rag_chain.invoke({"question": "What is LangChain?"})
```

**Flow Diagram:**
```
{"question": "What is LangChain?"}
    ┌→ retriever → "LangChain is a framework..." (context) ┐
    └→ passthrough → "What is LangChain?" (question) ┘
                ↓
    {"context": "...", "question": "..."}
                ↓
            prompt → ChatPromptValue
                ↓
            model → AIMessage
                ↓
            parser → str
```

## 6.4 LCEL Advanced Features

### Fallbacks
```python
primary_model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
backup_model = ChatOpenAI(model="gpt-4")

chain = primary_model.with_fallbacks([backup_model])

# If primary_model fails, automatically use backup_model
result = chain.invoke("Hello")
```

### Retry
```python
chain = (prompt | model).with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)
```

### Configurable Alternatives
```python
from langchain_core.runnables import ConfigurableField

model = ChatAnthropic(model="claude-3-5-sonnet-20241022").configurable_fields(
    model=ConfigurableField(id="model_name")
)

chain = prompt | model

# Switch models at runtime
chain.invoke(
    {"topic": "cats"},
    config={"configurable": {"model_name": "claude-3-opus-20240229"}}
)
```

## 🧠 Knowledge Challenge

1. What do LCEL's `|` operator and Python dict `{}` represent in chains?
2. Why is `StrOutputParser` useful? What happens without it?
3. Design an LCEL chain that:
   - Takes user question as input
   - Executes in parallel: translate to French + generate answer
   - Merge and output results

---

# Module 7: Tools & Agents

## 📝 Module 6 Answers

1. **Operator Meanings:**
   - `|` - Sequential execution (pipe), output passed to next component
   - `{}` - Parallel execution, same input to multiple branches, outputs merged to dict

2. **StrOutputParser:**
   - Purpose: Extracts `AIMessage.content` to plain string
   - Without it: `invoke()` returns full `AIMessage` object

3. **Design Solution:**
```python
chain = (
    {
        "translation": translate_prompt | model,
        "answer": answer_prompt | model
    }
    | RunnableLambda(lambda d: f"Answer: {d['answer'].content}\nFrench: {d['translation'].content}")
)
```

## 7.1 What is a Tool?

**Tool = Python function callable by AI**

**File Location:** `libs/core/langchain_core/tools/base.py`

```python
from langchain_core.tools import BaseTool

class BaseTool(ABC, RunnableSerializable[str, Any]):
    """Abstract base class for tools

    Tools enable AI to perform external operations (search, calculate, API calls, etc.)
    """

    name: str
    """Unique name of the tool"""

    description: str
    """Tool functionality description (AI uses this to decide when to call)"""

    @abstractmethod
    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Tool execution logic"""
```

## 7.2 Three Ways to Create Tools

### Method 1: Using @tool Decorator (Recommended)

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number
    """
    return a * b

# Auto-generated properties
print(multiply.name)         # "multiply"
print(multiply.description)  # "Multiply two numbers..."
print(multiply.args_schema)  # Pydantic model (from type annotations)

# Invocation
result = multiply.invoke({"a": 3, "b": 4})  # 12
```

### Method 2: Using StructuredTool

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="The search query")
    num_results: int = Field(default=5, description="Number of results")

def search_function(query: str, num_results: int = 5) -> str:
    return f"Found {num_results} results for '{query}'"

search_tool = StructuredTool.from_function(
    func=search_function,
    name="web_search",
    description="Search the web for information",
    args_schema=SearchInput
)
```

### Method 3: Inheriting BaseTool

```python
from langchain_core.tools import BaseTool
from typing import Type

class CustomTool(BaseTool):
    name: str = "custom_calculator"
    description: str = "Performs advanced calculations"

    def _run(self, expression: str) -> str:
        try:
            return str(eval(expression))  # Note: Don't use eval in production!
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, expression: str) -> str:
        # Async version
        return self._run(expression)

tool = CustomTool()
tool.invoke({"expression": "2 + 2"})  # "4"
```

## 7.3 Agent Architecture

**Agent = Autonomous AI system that can use tools**

**Core Concepts:**
1. AI receives task
2. AI **decides** which tools to call
3. Execute tools
4. AI continues reasoning based on results
5. Loop until task complete

### Simple Agent Implementation (Using LCEL)

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic

# Define tools
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [get_word_length, multiply]

# Create model with tools
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
model_with_tools = model.bind_tools(tools)

# Agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when necessary."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),  # Tool call records
])

# Agent loop logic
from langchain_core.messages import AIMessage, ToolMessage

def run_agent(user_input: str, max_iterations: int = 5):
    messages = [("human", user_input)]

    for i in range(max_iterations):
        # AI generates response (may include tool calls)
        response = model_with_tools.invoke(messages)
        messages.append(response)

        # Check for tool calls
        if not response.tool_calls:
            # No tool calls, task complete
            return response.content

        # Execute all tool calls
        for tool_call in response.tool_calls:
            tool = next(t for t in tools if t.name == tool_call["name"])
            tool_result = tool.invoke(tool_call["args"])

            # Add tool result to conversation
            messages.append(ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            ))

    return "Max iterations reached"

# Test
result = run_agent("What is the length of 'hello' multiplied by 3?")
print(result)
```

**Agent Execution Flow:**
```
User: "What is the length of 'hello' multiplied by 3?"
    ↓
AI: "Let me check the length first"
    → tool_call: get_word_length("hello")
    ↓
ToolMessage: "5"
    ↓
AI: "Now multiply 5 by 3"
    → tool_call: multiply(5, 3)
    ↓
ToolMessage: "15"
    ↓
AI: "The length of 'hello' is 5, and 5 multiplied by 3 equals 15."
```

## 7.4 LangGraph (Advanced Agent Framework)

For complex agents, we recommend **LangGraph** (part of the LangChain ecosystem):

```python
from langgraph.prebuilt import create_react_agent

# Create ReAct Agent (reasoning + action loop)
agent_executor = create_react_agent(
    model=model,
    tools=tools
)

# Stream execution
for event in agent_executor.stream({"messages": [("human", "What is 2+2?")]}):
    print(event)
```

**LangGraph Advantages:**
- ✅ State management (memory)
- ✅ Human-in-the-loop
- ✅ Workflow visualization
- ✅ Persistent checkpoints

## 🧠 Knowledge Challenge

1. What are the three required properties of a tool?
2. What is the essential difference between an Agent and a regular Chain?
3. Design a tool: Check if a given URL is accessible (returns True/False)

---

# Module 8: Advanced Features

## 📝 Module 7 Answers

1. **Three Tool Essentials:**
   - `name` - Unique identifier
   - `description` - Functionality description (AI uses to decide when to call)
   - `_run()` method - Actual execution logic

2. **Essential Difference:**
   - **Chain** - Predefined execution flow, fixed sequence
   - **Agent** - AI **dynamically decides** next action, including whether/when to call tools

3. **URL Check Tool:**
```python
import requests
from langchain_core.tools import tool

@tool
def check_url(url: str) -> bool:
    """Check if a URL is accessible.

    Args:
        url: The URL to check

    Returns:
        True if accessible, False otherwise
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False
```

## 8.1 Callbacks (Callback System)

**Purpose:** Tracing, logging, debugging, monitoring

**File Location:** `libs/core/langchain_core/callbacks/`

```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage

class MyCallbackHandler(BaseCallbackHandler):
    """Custom callback handler"""

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"[LLM Start] Prompts: {prompts}")

    def on_llm_end(self, response, **kwargs):
        print(f"[LLM End] Response: {response}")

    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"[Chain Start] Inputs: {inputs}")

# Using callbacks
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

result = model.invoke(
    "Hello",
    config={"callbacks": [MyCallbackHandler()]}
)

# Output:
# [LLM Start] Prompts: ['Hello']
# [LLM End] Response: ...
```

### Built-in Callbacks

```python
from langchain.callbacks import StdOutCallbackHandler

# Print all intermediate steps to stdout
handler = StdOutCallbackHandler()

chain = prompt | model
chain.invoke("Hello", config={"callbacks": [handler]})
```

## 8.2 Streaming

### Streaming Text Output

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Token-by-token streaming
for chunk in model.stream("Tell me a long story"):
    print(chunk.content, end="", flush=True)
```

### Streaming Intermediate Steps in Chains

```python
chain = prompt | model | StrOutputParser()

# Use astream_events to get all events
async for event in chain.astream_events("Tell me a joke", version="v2"):
    kind = event["event"]
    if kind == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
    elif kind == "on_parser_stream":
        print(f"[Parser]: {event['data']['chunk']}")
```

## 8.3 Memory

**File Location:** `libs/core/langchain_core/chat_history.py`

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# Memory store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Create chain with memory
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

chain = prompt | model

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Use (automatically saves history)
chain_with_history.invoke(
    {"input": "Hi, I'm Alice"},
    config={"configurable": {"session_id": "user-123"}}
)
# → "Hello Alice! How can I help you?"

chain_with_history.invoke(
    {"input": "What's my name?"},
    config={"configurable": {"session_id": "user-123"}}
)
# → "Your name is Alice!"
```

## 8.4 Caching

**File Location:** `libs/core/langchain_core/caches.py`

```python
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache

# Enable global cache
set_llm_cache(InMemoryCache())

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# First call (slow)
result1 = model.invoke("What is 2+2?")

# Second call (fast! reads from cache)
result2 = model.invoke("What is 2+2?")  # Same input returns cached result
```

## 8.5 Retrieval (RAG)

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import Embeddings

# Create vector database
vectorstore = InMemoryVectorStore.from_texts(
    ["LangChain is a framework for LLMs", "Paris is the capital of France"],
    embedding=embeddings  # Needs embedding model
)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# RAG chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
Answer based on context:

Context: {context}

Question: {question}
""")

rag_chain = (
    {"context": retriever, "question": lambda x: x}
    | prompt
    | model
    | StrOutputParser()
)

rag_chain.invoke("What is LangChain?")
# → "LangChain is a framework for LLMs..."
```

## 8.6 Output Parsers

**File Location:** `libs/core/langchain_core/output_parsers/`

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

# 1. String parser
str_parser = StrOutputParser()
chain = model | str_parser
chain.invoke("Hello")  # Returns str instead of AIMessage

# 2. JSON parser
json_parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template(
    "Output a JSON with 'name' and 'age' for: {person}"
)
chain = prompt | model | json_parser
chain.invoke({"person": "a 30-year-old named Alice"})
# → {"name": "Alice", "age": 30}

# 3. Pydantic parser (type-safe)
class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")

model_with_structure = model.with_structured_output(Person)
result = model_with_structure.invoke("Tell me about a 30-year-old named Bob")
# → Person(name="Bob", age=30)
```

## 🧠 Final Comprehensive Challenge

Design a complete LangChain application with the following features:

1. **Requirements:** Technical documentation Q&A system
2. **Features:**
   - User uploads documents (PDF/TXT)
   - System builds vector index
   - User asks questions, system answers based on documents
   - If answer not in documents, call search tool
   - Save conversation history

**Hints:** You'll need:
- `ChatPromptTemplate`
- `VectorStore` + `Retriever`
- `Tools` (search tool)
- `Agent` or `RunnableWithMessageHistory`
- `Callbacks` (optional, for tracing)

**Think:** How would you design this system's architecture? Draw a data flow diagram.

---

## 🎓 Learning Complete!

Congratulations on completing all 8 modules! You should now:

✅ Understand LangChain's architecture and design philosophy
✅ Master Messages, Prompts, and Runnables
✅ Build complex chains using LCEL
✅ Understand how tools and agents work
✅ Know how to apply advanced features (Streaming, Memory, RAG)

**Next Steps:**
1. Read official docs to deepen understanding of specific topics
2. Study test cases in `libs/core/tests/` to learn best practices
3. Build real projects to solidify knowledge

**Recommended Practice Projects:**
- Personal knowledge base Q&A system
- Multimodal chatbot (supports images)
- Automated research assistant (with search and summarization)
- Code analysis tool (using AST and LLM)

Best of luck on your LangChain development journey! 🚀
