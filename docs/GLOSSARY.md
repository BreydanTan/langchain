# 📖 LangChain Glossary | LangChain 术语表

A comprehensive bilingual glossary of core LangChain terminology and concepts.

LangChain 核心术语和概念的全面双语术语表。

---

## 🔤 Alphabetical Index | 字母索引

[A](#a) | [B](#b) | [C](#c) | [D](#d) | [E](#e) | [F](#f) | [I](#i) | [L](#l) | [M](#m) | [O](#o) | [P](#p) | [R](#r) | [S](#s) | [T](#t) | [V](#v)

---

## A

### Agent | 代理

**English:** An autonomous system that uses LLMs to decide which actions to take, execute tools, and reason about results. Unlike chains with fixed sequences, agents dynamically determine their next steps.

**中文：** 一个自主系统，使用 LLM 决定采取哪些操作、执行工具并对结果进行推理。与固定序列的链不同，代理动态确定其下一步操作。

**Related:** Tool, Chain, ReAct

**Code Reference:** `libs/langchain/langchain/agents/`

---

### AIMessage | AI 消息

**English:** A message type representing AI-generated responses in a conversation. Contains the model's output and optional metadata like tool calls.

**中文：** 表示对话中 AI 生成响应的消息类型。包含模型的输出和可选的元数据，如工具调用。

**Related:** HumanMessage, SystemMessage, BaseMessage

**Code Reference:** `libs/core/langchain_core/messages/ai.py`

---

## B

### BaseMessage | 基础消息

**English:** The abstract base class for all message types in LangChain. Defines common attributes like content, type, and additional metadata.

**中文：** LangChain 中所有消息类型的抽象基类。定义了通用属性，如内容、类型和附加元数据。

**Related:** AIMessage, HumanMessage, SystemMessage

**Code Reference:** `libs/core/langchain_core/messages/base.py`

---

### BaseChatModel | 基础聊天模型

**English:** Abstract base class for chat-based language models. Defines the interface that all chat model implementations must follow (e.g., ChatOpenAI, ChatAnthropic).

**中文：** 基于聊天的语言模型的抽象基类。定义所有聊天模型实现必须遵循的接口（例如 ChatOpenAI、ChatAnthropic）。

**Related:** BaseLLM, Runnable

**Code Reference:** `libs/core/langchain_core/language_models/chat_models.py`

---

### BaseLLM | 基础 LLM

**English:** Abstract base class for traditional language models that take strings as input and return strings as output (as opposed to chat models that use message objects).

**中文：** 传统语言模型的抽象基类，接受字符串作为输入并返回字符串作为输出（与使用消息对象的聊天模型相对）。

**Related:** BaseChatModel, Runnable

**Code Reference:** `libs/core/langchain_core/language_models/llms.py`

---

### BasePromptTemplate | 基础提示模板

**English:** Abstract base class for all prompt templates. Implements the Runnable interface and provides input validation and formatting logic.

**中文：** 所有提示模板的抽象基类。实现 Runnable 接口并提供输入验证和格式化逻辑。

**Related:** PromptTemplate, ChatPromptTemplate, Runnable

**Code Reference:** `libs/core/langchain_core/prompts/base.py`

---

### Batch Processing | 批处理

**English:** Processing multiple inputs in a single operation, often more efficient than sequential individual calls. All Runnables support `batch()` method.

**中文：** 在单个操作中处理多个输入，通常比顺序单独调用更高效。所有 Runnable 都支持 `batch()` 方法。

**Related:** Runnable, invoke(), stream()

**Code Reference:** `libs/core/langchain_core/runnables/base.py:863-911`

---

## C

### Callback | 回调

**English:** A mechanism to observe and react to events during chain execution (e.g., LLM start, tool execution, errors). Used for logging, monitoring, and debugging.

**中文：** 在链执行期间观察和响应事件的机制（例如，LLM 启动、工具执行、错误）。用于日志记录、监控和调试。

**Related:** RunnableConfig, BaseCallbackHandler

**Code Reference:** `libs/core/langchain_core/callbacks/`

---

### Chain | 链

**English:** A sequence of components (prompts, models, parsers, etc.) composed together to perform a task. Created using the `|` operator in LCEL.

**中文：** 组合在一起执行任务的组件序列（提示、模型、解析器等）。使用 LCEL 中的 `|` 操作符创建。

**Related:** LCEL, RunnableSequence, Runnable

**Code Reference:** `libs/core/langchain_core/runnables/base.py:2789-3136`

---

### ChatPromptTemplate | 聊天提示模板

**English:** A prompt template for chat-based conversations. Structures prompts as a sequence of messages (system, human, AI) rather than plain strings.

**中文：** 用于基于聊天的对话的提示模板。将提示结构化为消息序列（系统、人类、AI），而不是纯字符串。

**Related:** PromptTemplate, BasePromptTemplate, Messages

**Code Reference:** `libs/core/langchain_core/prompts/chat.py`

---

### Config Propagation | 配置传播

**English:** The automatic passing of RunnableConfig through a chain, enabling callbacks, tags, and metadata to flow to all components.

**中文：** 通过链自动传递 RunnableConfig，使回调、标签和元数据能够流向所有组件。

**Related:** RunnableConfig, Callbacks

---

## D

### Default Implementation | 默认实现

**English:** Methods in the Runnable interface that have default implementations based on the abstract `invoke()` method (e.g., `batch()`, `stream()`, `ainvoke()`).

**中文：** Runnable 接口中基于抽象 `invoke()` 方法具有默认实现的方法（例如 `batch()`、`stream()`、`ainvoke()`）。

**Related:** Runnable, invoke(), Abstract Method

**Code Reference:** `libs/core/langchain_core/runnables/base.py:840-911`

---

## E

### Embeddings | 嵌入

**English:** Vector representations of text that capture semantic meaning. Used in retrieval systems to find similar documents.

**中文：** 捕获语义含义的文本向量表示。用于检索系统以查找相似文档。

**Related:** VectorStore, Retrieval, RAG

**Code Reference:** `libs/core/langchain_core/embeddings/`

---

## F

### Flattening Optimization | 扁平化优化

**English:** The process of preventing nested RunnableSequences by merging adjacent sequences into a single flat sequence during composition.

**中文：** 通过在组合期间将相邻序列合并为单个扁平序列来防止嵌套 RunnableSequence 的过程。

**Related:** RunnableSequence, Composition

**Code Reference:** `libs/core/langchain_core/runnables/base.py:2881-2900`

---

### Function Calling | 函数调用

**English:** The ability of LLMs to generate structured calls to external functions/tools based on their descriptions. Also called "tool calling".

**中文：** LLM 根据外部函数/工具的描述生成对它们的结构化调用的能力。也称为"工具调用"。

**Related:** Tool, bind_tools(), ToolMessage

---

## I

### Input Validation | 输入验证

**English:** The process of checking and transforming user input to ensure it matches the expected format. Includes auto-wrapping single values for single-variable templates.

**中文：** 检查和转换用户输入以确保其与预期格式匹配的过程。包括为单变量模板自动包装单个值。

**Related:** BasePromptTemplate, _validate_input

**Code Reference:** `libs/core/langchain_core/prompts/base.py:155-187`

---

### invoke() | 调用

**English:** The core abstract method of the Runnable interface. Transforms a single input into an output synchronously.

**中文：** Runnable 接口的核心抽象方法。同步地将单个输入转换为输出。

**Related:** Runnable, batch(), stream(), ainvoke()

**Code Reference:** `libs/core/langchain_core/runnables/base.py:817-838`

---

## L

### LCEL (LangChain Expression Language) | LangChain 表达式语言

**English:** A declarative syntax for composing LangChain components using the `|` operator for sequential composition and `{}` for parallel composition.

**中文：** 一种声明式语法，用于使用 `|` 操作符进行顺序组合和 `{}` 进行并行组合来组合 LangChain 组件。

**Related:** RunnableSequence, RunnableParallel, Chain

---

## M

### MessagesPlaceholder | 消息占位符

**English:** A special prompt component that dynamically inserts a list of messages (e.g., conversation history) into a chat prompt template.

**中文：** 一个特殊的提示组件，动态地将消息列表（例如，对话历史）插入到聊天提示模板中。

**Related:** ChatPromptTemplate, Conversation History

**Code Reference:** `libs/core/langchain_core/prompts/chat.py`

---

## O

### OutputParser | 输出解析器

**English:** A component that transforms LLM output into structured formats (e.g., extracting content string, parsing JSON, validating against Pydantic models).

**中文：** 将 LLM 输出转换为结构化格式的组件（例如，提取内容字符串、解析 JSON、根据 Pydantic 模型验证）。

**Related:** StrOutputParser, JsonOutputParser, PydanticOutputParser

**Code Reference:** `libs/core/langchain_core/output_parsers/`

---

## P

### Partial Variables | 部分变量

**English:** Pre-filled template variables that are set once and reused across multiple invocations. Supports both static values and lazy functions.

**中文：** 预填充的模板变量，设置一次并在多次调用中重用。支持静态值和惰性函数。

**Related:** BasePromptTemplate, PromptTemplate

**Code Reference:** `libs/core/langchain_core/prompts/base.py`

---

### Pipe Operator (`|`) | 管道操作符

**English:** The operator used in LCEL to compose Runnables sequentially. `a | b` creates a RunnableSequence where output of `a` becomes input of `b`.

**中文：** LCEL 中用于顺序组合 Runnable 的操作符。`a | b` 创建一个 RunnableSequence，其中 `a` 的输出成为 `b` 的输入。

**Related:** LCEL, RunnableSequence, Composition

**Code Reference:** `libs/core/langchain_core/runnables/base.py:1165-1200`

---

### PromptTemplate | 提示模板

**English:** A template for generating string-based prompts with variable substitution. Uses Python's `str.format()` style syntax.

**中文：** 用于生成带变量替换的基于字符串的提示的模板。使用 Python 的 `str.format()` 风格语法。

**Related:** ChatPromptTemplate, BasePromptTemplate

**Code Reference:** `libs/core/langchain_core/prompts/prompt.py`

---

### PromptValue | 提示值

**English:** The output type of prompt templates. Can be converted to strings or message lists depending on the downstream component's requirements.

**中文：** 提示模板的输出类型。可以根据下游组件的要求转换为字符串或消息列表。

**Related:** StringPromptValue, ChatPromptValue

**Code Reference:** `libs/core/langchain_core/prompt_values.py`

---

## R

### RAG (Retrieval-Augmented Generation) | 检索增强生成

**English:** A pattern where relevant documents are retrieved from a knowledge base and provided as context to the LLM for generating more accurate, grounded responses.

**中文：** 一种模式，从知识库中检索相关文档并将其作为上下文提供给 LLM，以生成更准确、有根据的响应。

**Related:** Retriever, VectorStore, Embeddings

---

### ReAct | 推理-行动

**English:** A prompting strategy where the LLM alternates between Reasoning (thinking about what to do) and Acting (executing tools), iteratively solving complex tasks.

**中文：** 一种提示策略，LLM 在推理（思考要做什么）和行动（执行工具）之间交替，迭代解决复杂任务。

**Related:** Agent, Tool, LangGraph

---

### Retriever | 检索器

**English:** A component that searches and returns relevant documents based on a query. Common implementations use vector similarity search.

**中文：** 根据查询搜索并返回相关文档的组件。常见实现使用向量相似度搜索。

**Related:** VectorStore, RAG, Embeddings

**Code Reference:** `libs/core/langchain_core/retrievers.py`

---

### Runnable | 可运行组件

**English:** The core abstraction in LangChain. Any component implementing `invoke()` and supporting composition via `|`. Generic type: `Runnable[Input, Output]`.

**中文：** LangChain 中的核心抽象。任何实现 `invoke()` 并支持通过 `|` 进行组合的组件。泛型类型：`Runnable[Input, Output]`。

**Related:** invoke(), RunnableSequence, RunnableParallel

**Code Reference:** `libs/core/langchain_core/runnables/base.py:124`

---

### RunnableConfig | 可运行配置

**English:** Configuration object passed through chains to control execution (callbacks, tags, metadata, max_concurrency, etc.).

**中文：** 通过链传递以控制执行的配置对象（回调、标签、元数据、最大并发等）。

**Related:** Runnable, Callbacks, Config Propagation

**Code Reference:** `libs/core/langchain_core/runnables/config.py`

---

### RunnableLambda | Lambda 可运行组件

**English:** A wrapper that converts arbitrary Python functions into Runnables, enabling them to be used in LCEL chains.

**中文：** 将任意 Python 函数转换为 Runnable 的包装器，使它们能够在 LCEL 链中使用。

**Related:** Runnable, LCEL, Custom Functions

**Code Reference:** `libs/core/langchain_core/runnables/base.py`

---

### RunnableParallel | 并行可运行组件

**English:** A Runnable that executes multiple branches concurrently, each receiving the same input. Returns a dictionary with branch names as keys.

**中文：** 并发执行多个分支的 Runnable，每个分支接收相同的输入。返回以分支名为键的字典。

**Related:** RunnableSequence, Parallel Execution, `{}`

**Code Reference:** `libs/core/langchain_core/runnables/base.py:3537-3750`

---

### RunnablePassthrough | 透传可运行组件

**English:** A Runnable that passes its input through unchanged. Often used in parallel branches to preserve the original input.

**中文：** 将其输入原封不动地传递的 Runnable。通常在并行分支中用于保留原始输入。

**Related:** RunnableParallel, LCEL

**Code Reference:** `libs/core/langchain_core/runnables/passthrough.py`

---

### RunnableSequence | 序列可运行组件

**English:** A Runnable that executes steps sequentially. Structured as `first`, `middle` (list), and `last` components. Created automatically by the `|` operator.

**中文：** 顺序执行步骤的 Runnable。结构为 `first`、`middle`（列表）和 `last` 组件。由 `|` 操作符自动创建。

**Related:** Runnable, LCEL, Pipe Operator

**Code Reference:** `libs/core/langchain_core/runnables/base.py:2789-3136`

---

## S

### Streaming | 流式处理

**English:** Progressive output delivery where results are returned incrementally (e.g., token-by-token) rather than waiting for complete generation.

**中文：** 渐进式输出传递，结果以增量方式返回（例如，逐个令牌），而不是等待完整生成。

**Related:** stream(), astream(), Runnable

**Code Reference:** `libs/core/langchain_core/runnables/base.py`

---

### StrOutputParser | 字符串输出解析器

**English:** An output parser that extracts the `.content` field from AIMessage objects, returning plain strings.

**中文：** 从 AIMessage 对象中提取 `.content` 字段的输出解析器，返回纯字符串。

**Related:** OutputParser, AIMessage

**Code Reference:** `libs/core/langchain_core/output_parsers/string.py`

---

### Structured Output | 结构化输出

**English:** Forcing LLM output to conform to a specific schema (e.g., Pydantic model, JSON schema) using `with_structured_output()`.

**中文：** 使用 `with_structured_output()` 强制 LLM 输出符合特定架构（例如，Pydantic 模型、JSON 架构）。

**Related:** Pydantic, with_structured_output(), OutputParser

---

### SystemMessage | 系统消息

**English:** A message type used to set the AI's behavior, persona, or instructions. Typically the first message in a chat conversation.

**中文：** 用于设置 AI 行为、角色或指令的消息类型。通常是聊天对话中的第一条消息。

**Related:** BaseMessage, HumanMessage, AIMessage

**Code Reference:** `libs/core/langchain_core/messages/system.py`

---

## T

### Tool | 工具

**English:** A function that an Agent or LLM can invoke to perform actions (e.g., search, calculation, API calls). Defined with name, description, and implementation.

**中文：** Agent 或 LLM 可以调用以执行操作的函数（例如，搜索、计算、API 调用）。使用名称、描述和实现定义。

**Related:** Agent, Function Calling, @tool decorator

**Code Reference:** `libs/core/langchain_core/tools/`

---

### ToolMessage | 工具消息

**English:** A message type containing the result of a tool execution, returned to the LLM for further reasoning.

**中文：** 包含工具执行结果的消息类型，返回给 LLM 进行进一步推理。

**Related:** Tool, AIMessage, Function Calling

**Code Reference:** `libs/core/langchain_core/messages/tool.py`

---

### Type Safety | 类型安全

**English:** The use of Python's type hints (`Generic[Input, Output]`) in Runnable to ensure composition correctness at development time.

**中文：** 在 Runnable 中使用 Python 的类型提示（`Generic[Input, Output]`）以确保开发时的组合正确性。

**Related:** Runnable, Generic, Type Hints

---

## V

### VectorStore | 向量存储

**English:** A database optimized for storing and searching high-dimensional vectors (embeddings). Used in RAG for semantic similarity search.

**中文：** 为存储和搜索高维向量（嵌入）而优化的数据库。在 RAG 中用于语义相似度搜索。

**Related:** Embeddings, Retriever, RAG

**Code Reference:** `libs/core/langchain_core/vectorstores/`

---

## 📚 See Also | 另见

- **[Official LangChain Documentation](https://docs.langchain.com/)** - Complete API reference and guides
- **[Module 1: Runnable Core](module-01-runnable-core-EN.md)** - Deep-dive into Runnable abstraction
- **[Module 2: RunnableSequence](module-02-runnable-sequence-EN.md)** - Understanding composition
- **[Examples Directory](examples/)** - Runnable code examples

---

## 🤝 Contributing | 贡献

Found a missing term or error? Please contribute:
发现缺失的术语或错误？请贡献：

1. Add the term in **both English and Chinese**
2. Include a code reference if applicable
3. Link to related terms
4. Keep definitions concise but complete

---

**Last Updated:** 2025-11-17
**维护者:** LangChain Learning Series Contributors
