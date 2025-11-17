# ❓ Frequently Asked Questions (FAQ) | 常见问题解答

A bilingual collection of frequently asked questions about LangChain's core concepts and architecture.

关于 LangChain 核心概念和架构的常见问题双语集合。

---

## 📚 Table of Contents | 目录

### Runnable & LCEL
1. [What's the difference between `invoke()` and `__call__()`?](#q1-invoke-vs-call)
2. [When should I use RunnableSequence vs RunnableParallel?](#q2-sequence-vs-parallel)
3. [Can I use regular Python functions in LCEL chains?](#q3-python-functions-in-lcel)
4. [How does the `|` operator work?](#q4-pipe-operator)

### Prompts
5. [PromptTemplate vs ChatPromptTemplate - which to use?](#q5-prompt-templates)
6. [How do I handle conversation history?](#q6-conversation-history)
7. [What are partial_variables used for?](#q7-partial-variables)

### Models
8. [BaseLLM vs BaseChatModel - what's the difference?](#q8-llm-vs-chatmodel)
9. [How do I stream responses?](#q9-streaming)
10. [What is bind_tools() for?](#q10-bind-tools)

### Performance & Optimization
11. [How can I speed up my chains?](#q11-performance)
12. [When should I use batch() vs individual invoke()?](#q12-batch-vs-invoke)
13. [Does RunnableParallel really run in parallel?](#q13-parallel-execution)

### Error Handling & Debugging
14. [How do I debug a chain?](#q14-debugging)
15. [How to handle errors in chains?](#q15-error-handling)
16. [Why is my chain not working as expected?](#q16-chain-not-working)

---

## Runnable & LCEL

<a name="q1-invoke-vs-call"></a>
### 1. What's the difference between `invoke()` and `__call__()`?
### 1. `invoke()` 和 `__call__()` 有什么区别？

**English:**
- `invoke()` is the **official method** defined in the Runnable interface. It accepts a `config` parameter for callbacks, tags, and metadata.
- `__call__()` is a **convenience wrapper** that internally calls `invoke()`. It doesn't support `config`.

**Use `invoke()`** when you need to pass configuration (callbacks, tags, etc.).

**中文：**
- `invoke()` 是 Runnable 接口中定义的**官方方法**。它接受 `config` 参数用于回调、标签和元数据。
- `__call__()` 是一个**便捷包装器**，内部调用 `invoke()`。它不支持 `config`。

**当需要传递配置时使用 `invoke()`**（回调、标签等）。

**Example:**
```python
# Both work
result1 = chain.invoke(input)
result2 = chain(input)

# Only invoke() supports config
result3 = chain.invoke(input, config={"callbacks": [my_callback]})
```

**Code Reference:** `libs/core/langchain_core/runnables/base.py:1289-1292`

---

<a name="q2-sequence-vs-parallel"></a>
### 2. When should I use RunnableSequence vs RunnableParallel?
### 2. 何时使用 RunnableSequence 还是 RunnableParallel？

**English:**
- **RunnableSequence (`|`)**: When output of one step becomes input of the next (sequential dependency)
- **RunnableParallel (`{}`)**: When multiple operations need the same input and you want them to run concurrently

**中文：**
- **RunnableSequence (`|`)**：当一步的输出成为下一步的输入时（顺序依赖）
- **RunnableParallel (`{}`)**：当多个操作需要相同输入且你希望它们并发运行时

**Example:**
```python
# Sequential: output flows through steps
chain = prompt | model | parser  # prompt output → model input → parser input

# Parallel: same input to all branches
parallel = {
    "summary": summarize_chain,
    "translation": translate_chain
}  # Both chains receive the same input
```

---

<a name="q3-python-functions-in-lcel"></a>
### 3. Can I use regular Python functions in LCEL chains?
### 3. 可以在 LCEL 链中使用普通 Python 函数吗？

**English:**
Yes! LangChain automatically converts functions to `RunnableLambda`:

1. **Automatic conversion** in dict syntax:
   ```python
   chain = {"result": lambda x: x * 2} | other_runnable
   ```

2. **Explicit wrapping** with `RunnableLambda`:
   ```python
   from langchain_core.runnables import RunnableLambda

   def my_function(x):
       return x.upper()

   chain = prompt | RunnableLambda(my_function) | model
   ```

**中文：**
可以！LangChain 会自动将函数转换为 `RunnableLambda`：

1. **自动转换**（字典语法）：
   ```python
   chain = {"result": lambda x: x * 2} | other_runnable
   ```

2. **显式包装**（使用 `RunnableLambda`）：
   ```python
   from langchain_core.runnables import RunnableLambda

   def my_function(x):
       return x.upper()

   chain = prompt | RunnableLambda(my_function) | model
   ```

---

<a name="q4-pipe-operator"></a>
### 4. How does the `|` operator work?
### 4. `|` 操作符是如何工作的？

**English:**
The `|` operator is overloaded via the `__or__()` method in the Runnable class. It creates a `RunnableSequence`:

```python
a | b  →  RunnableSequence(first=a, last=b)
a | b | c  →  RunnableSequence(first=a, middle=[b], last=c)
```

**Flattening optimization:** If you pipe two sequences, LangChain flattens them into one instead of nesting.

**中文：**
`|` 操作符通过 Runnable 类中的 `__or__()` 方法重载。它创建一个 `RunnableSequence`：

```python
a | b  →  RunnableSequence(first=a, last=b)
a | b | c  →  RunnableSequence(first=a, middle=[b], last=c)
```

**扁平化优化：** 如果你管道两个序列，LangChain 会将它们扁平化为一个而不是嵌套。

**Code Reference:** `libs/core/langchain_core/runnables/base.py:1165-1200`

---

## Prompts

<a name="q5-prompt-templates"></a>
### 5. PromptTemplate vs ChatPromptTemplate - which to use?
### 5. PromptTemplate 还是 ChatPromptTemplate - 该用哪个？

**English:**
| Template | Output | Use When |
|----------|--------|----------|
| **PromptTemplate** | String (`StringPromptValue`) | Legacy LLMs (text in → text out) |
| **ChatPromptTemplate** | Message list (`ChatPromptValue`) | Modern chat models (messages in → message out) |

**Recommendation:** Use `ChatPromptTemplate` for all new projects with chat models (ChatOpenAI, ChatAnthropic, etc.).

**中文：**
| 模板 | 输出 | 使用场景 |
|------|------|----------|
| **PromptTemplate** | 字符串 (`StringPromptValue`) | 传统 LLM（文本输入 → 文本输出） |
| **ChatPromptTemplate** | 消息列表 (`ChatPromptValue`) | 现代聊天模型（消息输入 → 消息输出） |

**建议：** 对于所有使用聊天模型的新项目使用 `ChatPromptTemplate`（ChatOpenAI、ChatAnthropic 等）。

**Example:**
```python
# PromptTemplate (old-school)
prompt = PromptTemplate.from_template("Tell me about {topic}")
prompt.invoke({"topic": "AI"})  # → StringPromptValue

# ChatPromptTemplate (modern)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Tell me about {topic}")
])
prompt.invoke({"topic": "AI"})  # → ChatPromptValue
```

---

<a name="q6-conversation-history"></a>
### 6. How do I handle conversation history?
### 6. 如何处理对话历史？

**English:**
Use **MessagesPlaceholder** to dynamically inject conversation history:

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("history"),  # Dynamic history insertion
    ("human", "{question}"),
])

prompt.invoke({
    "history": [
        ("human", "What's 2+2?"),
        ("ai", "2+2 equals 4."),
    ],
    "question": "What about 2+3?"
})
```

**中文：**
使用 **MessagesPlaceholder** 动态注入对话历史：

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("history"),  # 动态历史插入
    ("human", "{question}"),
])

prompt.invoke({
    "history": [
        ("human", "What's 2+2?"),
        ("ai", "2+2 equals 4."),
    ],
    "question": "What about 2+3?"
})
```

**See Also:** [Module 3 - Prompts Implementation](module-03-prompts-implementation-EN.md)

---

<a name="q7-partial-variables"></a>
### 7. What are partial_variables used for?
### 7. partial_variables 用于什么？

**English:**
**partial_variables** allow you to pre-fill template variables with:
1. **Static values** (constants)
2. **Functions** (evaluated lazily on each invoke)

**Common use cases:**
- Current timestamp
- User ID from context
- System version info

**中文：**
**partial_variables** 允许你预填充模板变量，使用：
1. **静态值**（常量）
2. **函数**（每次调用时惰性求值）

**常见用例：**
- 当前时间戳
- 上下文中的用户 ID
- 系统版本信息

**Example:**
```python
from datetime import datetime

prompt = PromptTemplate(
    template="[{time}] User question: {question}",
    input_variables=["question"],
    partial_variables={
        "time": lambda: datetime.now().strftime("%H:%M:%S")  # Called on each invoke
    }
)

prompt.format(question="What is AI?")
# [14:23:45] User question: What is AI?
```

**Code Reference:** `libs/core/langchain_core/prompts/base.py`

---

## Models

<a name="q8-llm-vs-chatmodel"></a>
### 8. BaseLLM vs BaseChatModel - what's the difference?
### 8. BaseLLM 和 BaseChatModel 有什么区别？

**English:**
| Feature | BaseLLM | BaseChatModel |
|---------|---------|---------------|
| **Input** | String | List of messages |
| **Output** | String | AIMessage |
| **Use Case** | Legacy completion models | Modern chat models (GPT-4, Claude, etc.) |
| **Example** | Text completion | Conversational AI |

**Recommendation:** Use `BaseChatModel` for new projects.

**中文：**
| 特性 | BaseLLM | BaseChatModel |
|------|---------|---------------|
| **输入** | 字符串 | 消息列表 |
| **输出** | 字符串 | AIMessage |
| **用例** | 传统补全模型 | 现代聊天模型（GPT-4、Claude 等） |
| **示例** | 文本补全 | 对话式 AI |

**建议：** 新项目使用 `BaseChatModel`。

**See Also:** [Module 4-6 Summary](module-04-05-06-summary-EN.md)

---

<a name="q9-streaming"></a>
### 9. How do I stream responses?
### 9. 如何流式传输响应？

**English:**
Use the `stream()` method to get incremental output:

```python
for chunk in model.stream("Tell me a long story"):
    print(chunk.content, end="", flush=True)
```

**For chains:**
```python
chain = prompt | model | StrOutputParser()

for chunk in chain.stream({"topic": "AI"}):
    print(chunk, end="", flush=True)
```

**中文：**
使用 `stream()` 方法获取增量输出：

```python
for chunk in model.stream("Tell me a long story"):
    print(chunk.content, end="", flush=True)
```

**对于链：**
```python
chain = prompt | model | StrOutputParser()

for chunk in chain.stream({"topic": "AI"}):
    print(chunk, end="", flush=True)
```

---

<a name="q10-bind-tools"></a>
### 10. What is bind_tools() for?
### 10. bind_tools() 用于什么？

**English:**
`bind_tools()` enables **function calling** - allowing the LLM to generate structured calls to external tools/functions.

**中文：**
`bind_tools()` 启用**函数调用** - 允许 LLM 生成对外部工具/函数的结构化调用。

**Example:**
```python
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny"

model_with_tools = model.bind_tools([get_weather])

response = model_with_tools.invoke("What's the weather in Paris?")
print(response.tool_calls)
# [{"name": "get_weather", "args": {"location": "Paris"}, "id": "..."}]
```

**See Also:** [GLOSSARY.md - Function Calling](GLOSSARY.md#function-calling--函数调用)

---

## Performance & Optimization

<a name="q11-performance"></a>
### 11. How can I speed up my chains?
### 11. 如何加速我的链？

**English:**
1. **Use RunnableParallel** for independent operations
2. **Enable caching** with `set_llm_cache()`
3. **Batch processing** with `batch()` for multiple inputs
4. **Async execution** with `ainvoke()` / `abatch()`
5. **Optimize prompts** to reduce token usage

**中文：**
1. **对独立操作使用 RunnableParallel**
2. **使用 `set_llm_cache()` 启用缓存**
3. **使用 `batch()` 批处理**多个输入
4. **使用 `ainvoke()` / `abatch()` 异步执行**
5. **优化提示**以减少令牌使用

**Example:**
```python
# Slow: Sequential execution
summary = summarize.invoke(text)
translation = translate.invoke(text)

# Fast: Parallel execution
parallel = RunnableParallel(
    summary=summarize,
    translation=translate
)
result = parallel.invoke(text)  # Both run concurrently
```

---

<a name="q12-batch-vs-invoke"></a>
### 12. When should I use batch() vs individual invoke()?
### 12. 何时使用 batch() 而非单独的 invoke()？

**English:**
Use `batch()` when:
- ✅ You have multiple independent inputs to process
- ✅ API supports batch requests (efficiency gains)
- ✅ You want automatic parallelization

Use individual `invoke()` when:
- ✅ Inputs depend on previous results
- ✅ You need fine-grained control over execution

**中文：**
使用 `batch()` 当：
- ✅ 有多个独立输入要处理
- ✅ API 支持批处理请求（效率提升）
- ✅ 希望自动并行化

使用单独的 `invoke()` 当：
- ✅ 输入依赖于之前的结果
- ✅ 需要对执行进行细粒度控制

**Example:**
```python
# Batch processing (efficient)
inputs = ["doc1", "doc2", "doc3"]
results = chain.batch(inputs)  # Processes all in parallel/batch

# Individual processing (when needed)
results = []
for inp in inputs:
    result = chain.invoke(inp)  # Sequential, controlled
    if result.score > 0.8:  # Can make decisions between invocations
        results.append(result)
```

---

<a name="q13-parallel-execution"></a>
### 13. Does RunnableParallel really run in parallel?
### 13. RunnableParallel 真的并行运行吗？

**English:**
**It depends:**

| Method | Parallelism Type | True Parallel? |
|--------|------------------|----------------|
| `invoke()` | Thread pool (`ThreadPoolExecutor`) | ✅ Yes (for I/O-bound tasks) |
| `ainvoke()` | Async coroutines (`asyncio.gather`) | ✅ Yes (for async I/O) |
| Python GIL | Limitation | ⚠️ Not for CPU-bound tasks |

**CPU-bound tasks:** Use `ProcessPoolExecutor` instead.

**中文：**
**取决于情况：**

| 方法 | 并行类型 | 真正并行？ |
|------|----------|------------|
| `invoke()` | 线程池 (`ThreadPoolExecutor`) | ✅ 是（对于 I/O 密集型任务） |
| `ainvoke()` | 异步协程 (`asyncio.gather`) | ✅ 是（对于异步 I/O） |
| Python GIL | 限制 | ⚠️ 对于 CPU 密集型任务不适用 |

**CPU 密集型任务：** 使用 `ProcessPoolExecutor`。

**See Also:** [Module 7 - RunnableParallel](module-07-runnable-parallel-EN.md)

---

## Error Handling & Debugging

<a name="q14-debugging"></a>
### 14. How do I debug a chain?
### 14. 如何调试链？

**English:**
**Method 1: Enable verbose output**
```python
chain = prompt | model
result = chain.invoke(input, config={"verbose": True})
```

**Method 2: Use callbacks**
```python
from langchain.callbacks import StdOutCallbackHandler

chain.invoke(input, config={"callbacks": [StdOutCallbackHandler()]})
```

**Method 3: LangSmith (production)**
- Sign up at https://www.langchain.com/langsmith
- Enable tracing with environment variables

**中文：**
**方法 1：启用详细输出**
```python
chain = prompt | model
result = chain.invoke(input, config={"verbose": True})
```

**方法 2：使用回调**
```python
from langchain.callbacks import StdOutCallbackHandler

chain.invoke(input, config={"callbacks": [StdOutCallbackHandler()]})
```

**方法 3：LangSmith（生产环境）**
- 在 https://www.langchain.com/langsmith 注册
- 使用环境变量启用追踪

---

<a name="q15-error-handling"></a>
### 15. How to handle errors in chains?
### 15. 如何在链中处理错误？

**English:**
**Option 1: try-except**
```python
try:
    result = chain.invoke(input)
except Exception as e:
    print(f"Chain failed: {e}")
    result = fallback_chain.invoke(input)
```

**Option 2: with_fallbacks()**
```python
chain_with_fallback = primary_chain.with_fallbacks([backup_chain])
result = chain_with_fallback.invoke(input)  # Automatically uses backup if primary fails
```

**Option 3: with_retry()**
```python
chain = (prompt | model).with_retry(stop_after_attempt=3)
```

**中文：**
**选项 1：try-except**
```python
try:
    result = chain.invoke(input)
except Exception as e:
    print(f"Chain failed: {e}")
    result = fallback_chain.invoke(input)
```

**选项 2：with_fallbacks()**
```python
chain_with_fallback = primary_chain.with_fallbacks([backup_chain])
result = chain_with_fallback.invoke(input)  # 主链失败时自动使用备用链
```

**选项 3：with_retry()**
```python
chain = (prompt | model).with_retry(stop_after_attempt=3)
```

---

<a name="q16-chain-not-working"></a>
### 16. Why is my chain not working as expected?
### 16. 为什么我的链没有按预期工作？

**English:**
**Common issues:**

1. **Type mismatch**
   - Check if output type of step N matches input type of step N+1
   - Use `chain.get_input_schema()` and `chain.get_output_schema()`

2. **Wrong operator**
   - `|` for sequential (output → input)
   - `{}` for parallel (same input to all)

3. **Missing input variables**
   - Ensure all template variables are provided in `invoke()`

4. **Config not propagating**
   - Use `invoke(input, config={...})`, not `invoke(input, {...})`

**Debug checklist:**
```python
# 1. Check schemas
print(chain.get_input_schema())
print(chain.get_output_schema())

# 2. Test each step individually
step1_output = step1.invoke(input)
step2_output = step2.invoke(step1_output)  # Does this work?

# 3. Enable verbose logging
chain.invoke(input, config={"verbose": True})
```

**中文：**
**常见问题：**

1. **类型不匹配**
   - 检查步骤 N 的输出类型是否与步骤 N+1 的输入类型匹配
   - 使用 `chain.get_input_schema()` 和 `chain.get_output_schema()`

2. **错误的操作符**
   - `|` 用于顺序（输出 → 输入）
   - `{}` 用于并行（相同输入到所有分支）

3. **缺少输入变量**
   - 确保在 `invoke()` 中提供所有模板变量

4. **配置未传播**
   - 使用 `invoke(input, config={...})`，而非 `invoke(input, {...})`

**调试清单：**
```python
# 1. 检查模式
print(chain.get_input_schema())
print(chain.get_output_schema())

# 2. 单独测试每个步骤
step1_output = step1.invoke(input)
step2_output = step2.invoke(step1_output)  # 这能工作吗？

# 3. 启用详细日志
chain.invoke(input, config={"verbose": True})
```

---

## 📚 Additional Resources | 其他资源

- **[Official Documentation](https://docs.langchain.com/)** - Complete guides and API reference
- **[Learning Series](README.md)** - Deep-dive modules on core concepts
- **[Examples Directory](examples/)** - Runnable code examples
- **[Glossary](GLOSSARY.md)** - Comprehensive terminology reference

---

## 🤝 Contributing | 贡献

Have a question not covered here? Please contribute!

这里没有涵盖的问题？请贡献！

1. Add your question in **both English and Chinese**
2. Provide a clear, concise answer with code examples
3. Link to relevant modules or documentation
4. Keep answers beginner-friendly

---

**Last Updated:** 2025-11-17
