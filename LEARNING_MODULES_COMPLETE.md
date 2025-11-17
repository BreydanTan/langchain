# 🧠 LangChain 认知学习引擎 - 完整教学模块

> [!NOTE]
> **📚 新的深度学习系列现已推出！**
>
> 本文档提供 LangChain 的**广度优先**学习路径，涵盖 8 个主题的快速概览。
>
> 如果你想进行**深度优先**的源码级学习，请访问新的学习系列：
> - **[深度学习系列（中英双语）](docs/README.md)**
> - 特点：逐文件深入分析、设计哲学解释、源码引用、Mermaid 图表、知识挑战
> - 涵盖：`Runnable` 核心抽象、`RunnableSequence` 组合机制、Prompts 实现、LLM/ChatModel、LCEL 执行流程
>
> **两种学习路径对比：**
> - **本文档（广度优先）**：快速了解 LangChain 全貌，适合初学者入门
> - **新系列（深度优先）**：深入理解架构设计，适合进阶学习和源码贡献

---

本文档包含所有 8 个学习模块的完整内容。每个模块都包含上一模块的答案，方便你先思考再验证。

---

## 📚 目录

1. [模块 1：项目架构与核心理念](#模块-1项目架构与核心理念)
2. [模块 2：消息系统 (Messages)](#模块-2消息系统-messages)
3. [模块 3：提示工程 (Prompts)](#模块-3提示工程-prompts)
4. [模块 4：核心抽象 Runnable](#模块-4核心抽象-runnable)
5. [模块 5：聊天模型 (Chat Models)](#模块-5聊天模型-chat-models)
6. [模块 6：链式组合 (Chains & LCEL)](#模块-6链式组合-chains--lcel)
7. [模块 7：工具与代理 (Tools & Agents)](#模块-7工具与代理-tools--agents)
8. [模块 8：高级特性](#模块-8高级特性)

---

# 模块 1：项目架构与核心理念

## 1.1 Monorepo 结构

```
/home/user/langchain/libs/
├─ core/              ⭐ 核心抽象层（最重要）
├─ langchain_v1/      📦 主包
├─ partners/          🔌 官方集成
└─ text-splitters/    ✂️  工具库
```

## 1.2 三大设计原则

### 原则 1：一切皆 Runnable
```python
class Runnable(ABC, Generic[Input, Output]):
    def invoke(self, input: Input) -> Output
    def batch(self, inputs: list[Input]) -> list[Output]
    def stream(self, input: Input) -> Iterator[Output]
    async def ainvoke(self, input: Input) -> Output
```

### 原则 2：声明式组合（Pipe `|`）
```python
chain = component1 | component2 | component3
chain.invoke(input)  # 自动串联执行
```

### 原则 3：插件式集成
```
langchain_core 定义接口
    ↓
langchain_anthropic/openai 实现接口
```

## 🧠 知识挑战

1. 哪个包是"地基"？为什么？
2. Runnable 的 4 个核心方法？
3. `prompt | llm` 执行时发生什么？

---

# 模块 2：消息系统 (Messages)

## 📝 模块 1 答案

1. **地基：** `libs/core/` - 所有包依赖它，定义稳定接口
2. **4个方法：** `invoke()` (单次), `batch()` (批量), `stream()` (流式), `ainvoke()` (异步)
3. **执行流程：**
   ```
   用户输入 → prompt.invoke() → Prompt对象
           → llm.invoke() → AIMessage
   ```

## 2.1 消息类型层次

```
BaseMessage
├─ HumanMessage (type="human")    # 用户输入
├─ AIMessage (type="ai")          # AI回复
├─ SystemMessage (type="system")  # 系统指令
└─ ToolMessage (type="tool")      # 工具结果
```

**文件位置：**
- `libs/core/langchain_core/messages/base.py:93`
- `libs/core/langchain_core/messages/human.py:9`
- `libs/core/langchain_core/messages/ai.py`

## 2.2 核心用法

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 典型对话结构
conversation = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is 2+2?"),
    AIMessage(content="2+2 equals 4."),
]

# 多模态内容
msg = HumanMessage(content=[
    {"type": "text", "text": "What's in this image?"},
    {"type": "image_url", "image_url": {"url": "..."}}
])

# AI 消息带工具调用
ai_msg = AIMessage(
    content="Let me check the weather.",
    tool_calls=[{"name": "get_weather", "args": {"city": "SF"}}]
)
```

## 🧠 知识挑战

1. 三种核心消息类型及其用途？
2. 如何构建客服机器人的提示？（伪代码）
3. AIMessage 的 `tool_calls` 字段作用？

---

# 模块 3：提示工程 (Prompts)

## 📝 模块 2 答案

1. **三种类型：**
   - `SystemMessage` - 设定AI行为
   - `HumanMessage` - 用户输入
   - `AIMessage` - AI回复

2. **客服机器人：**
```python
messages = [
    SystemMessage(content="你是专业客服，规则：1)保持礼貌 2)不知道就转人工"),
    HumanMessage(content="我的订单在哪？")
]
```

3. **tool_calls：** 让AI调用外部工具（搜索、计算器等），突破LLM的知识限制

## 3.1 Prompt 模板类型

```
BasePromptTemplate
├─ PromptTemplate        # 字符串模板
└─ ChatPromptTemplate    # 聊天模板
   └─ MessagesPlaceholder # 历史占位符
```

**文件位置：**
- `libs/core/langchain_core/prompts/prompt.py:24`
- `libs/core/langchain_core/prompts/chat.py`

## 3.2 核心用法

### PromptTemplate（简单字符串）
```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {topic}."
)
prompt.format(adjective="funny", topic="cats")
# → "Tell me a funny joke about cats."

# 作为 Runnable
prompt.invoke({"adjective": "funny", "topic": "cats"})
# → StringPromptValue(...)
```

### ChatPromptTemplate（聊天模板）
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

### MessagesPlaceholder（历史对话）
```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    MessagesPlaceholder("history"),  # 插入历史
    ("human", "{question}"),
])

prompt.invoke({
    "history": [("human", "5+2?"), ("ai", "7")],
    "question": "multiply by 4"
})
# → 自动展开 history 到完整消息列表
```

## 3.3 实战：组合 Prompt + Model

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a comedian."),
    ("human", "Joke about {topic}"),
])

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

chain = prompt | model  # LCEL 组合

chain.invoke({"topic": "programming"})
# → AIMessage("Why do programmers prefer dark mode?...")
```

**执行流程：**
```
{"topic": "programming"}
    ↓ prompt.invoke()
ChatPromptValue([SystemMessage(...), HumanMessage(...)])
    ↓ model.invoke()
AIMessage("...")
```

## 🧠 知识挑战

1. `PromptTemplate` vs `ChatPromptTemplate` 区别？
2. `MessagesPlaceholder` 解决什么问题？
3. 预测输出：`(prompt | model).invoke({"role": "chef", "input": "pasta?"})`

---

# 模块 4：核心抽象 Runnable

## 📝 模块 3 答案

1. **区别：**
   - `PromptTemplate` → 生成字符串 (StringPromptValue)
   - `ChatPromptTemplate` → 生成消息列表 (ChatPromptValue)

2. **MessagesPlaceholder：** 动态插入对话历史，避免手动拼接消息列表

3. **预测输出：**
```python
# 步骤 1: prompt.invoke() 生成消息
# 步骤 2: model.invoke() 调用 Claude
# 最终输出: AIMessage(content="To make pasta, first boil water...")
```

## 4.1 Runnable 协议深度解析

**文件位置：** `libs/core/langchain_core/runnables/base.py:124`

```python
class Runnable(ABC, Generic[Input, Output]):
    """可调用、批处理、流式处理、转换和组合的工作单元"""

    # 🔑 核心方法（必须实现）
    @abstractmethod
    def invoke(self, input: Input, config: RunnableConfig | None = None) -> Output:
        """单次同步调用"""

    # 🔑 默认实现（可选重写优化）
    def batch(
        self,
        inputs: list[Input],
        config: RunnableConfig | None = None
    ) -> list[Output]:
        """批量处理（默认并行调用 invoke）"""

    def stream(
        self,
        input: Input,
        config: RunnableConfig | None = None
    ) -> Iterator[Output]:
        """流式输出（默认一次性返回）"""

    async def ainvoke(
        self,
        input: Input,
        config: RunnableConfig | None = None
    ) -> Output:
        """异步调用（默认在线程池执行 invoke）"""
```

## 4.2 为什么 Runnable 如此重要？

### 原因 1：统一接口
所有组件都实现 Runnable → 一致的调用方式

```python
# 这些都有相同的方法！
prompt.invoke(...)
model.invoke(...)
chain.invoke(...)
retriever.invoke(...)
```

### 原因 2：自动组合
使用 `|` 创建的链会**自动继承**所有 Runnable 方法

```python
chain = prompt | model | output_parser

# 自动支持：
chain.invoke(input)
chain.batch([input1, input2])
chain.stream(input)
await chain.ainvoke(input)
```

### 原因 3：配置传递
`RunnableConfig` 自动在链中传递（用于回调、标签、元数据等）

```python
chain.invoke(
    input,
    config={
        "tags": ["experiment"],
        "metadata": {"user_id": "123"}
    }
)
# config 会传递给链中的每个组件
```

## 4.3 Runnable 组合原语

### RunnableSequence（顺序执行）
```python
from langchain_core.runnables import RunnableLambda

# 使用 | 创建（推荐）
seq = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 2)
seq.invoke(5)  # (5+1)*2 = 12

# 等价于
from langchain_core.runnables import RunnableSequence
seq = RunnableSequence(steps=[...])
```

**执行流程：**
```
Input(5) → [step1: +1] → 6 → [step2: *2] → Output(12)
```

### RunnableParallel（并行执行）
```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    add=RunnableLambda(lambda x: x + 1),
    mul=RunnableLambda(lambda x: x * 2),
)
parallel.invoke(5)
# {"add": 6, "mul": 10}

# 在链中使用
chain = parallel | RunnableLambda(lambda d: d["add"] + d["mul"])
chain.invoke(5)  # 6 + 10 = 16
```

**执行流程：**
```
Input(5) ┬→ [add: +1] → 6  ┐
         └→ [mul: *2] → 10 ┘→ {"add": 6, "mul": 10}
```

### RunnableLambda（自定义函数）
```python
from langchain_core.runnables import RunnableLambda

def my_function(input_dict):
    return input_dict["x"] * 2

runnable_fn = RunnableLambda(my_function)
runnable_fn.invoke({"x": 5})  # 10

# 或使用装饰器
@RunnableLambda
def my_function(x):
    return x * 2
```

## 4.4 实战：构建复杂链

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_anthropic import ChatAnthropic

# 步骤 1: 创建两个并行分支
branch_a = ChatPromptTemplate.from_template("Summarize: {text}") | model
branch_b = ChatPromptTemplate.from_template("Translate to French: {text}") | model

# 步骤 2: 并行执行
parallel_chain = RunnableParallel(summary=branch_a, translation=branch_b)

# 步骤 3: 合并结果
def combine(results):
    return f"Summary: {results['summary'].content}\n\nFrench: {results['translation'].content}"

final_chain = parallel_chain | RunnableLambda(combine)

# 执行
final_chain.invoke({"text": "LangChain is awesome!"})
```

**流程图：**
```
{"text": "..."}
    ┌→ [Summarize prompt] → [Model] → summary ┐
    └→ [Translate prompt] → [Model] → translation ┘
                    ↓
              [Combine function]
                    ↓
        "Summary: ...\nFrench: ..."
```

## 🧠 知识挑战

1. Runnable 的 4 个核心方法，哪个是抽象方法（必须实现）？
2. `RunnableSequence` 和 `RunnableParallel` 的区别？举例说明
3. 预测输出：
```python
chain = RunnableLambda(lambda x: x["a"] + x["b"]) | RunnableLambda(lambda x: x * 3)
chain.invoke({"a": 2, "b": 3})
```

---

# 模块 5：聊天模型 (Chat Models)

## 📝 模块 4 答案

1. **抽象方法：** `invoke()` 是唯一的抽象方法，其他方法有默认实现

2. **区别：**
   - `RunnableSequence` - 顺序执行，输出→输入链式传递
   - `RunnableParallel` - 并行执行，所有分支接收相同输入，返回字典

3. **预测输出：**
```python
# 步骤1: lambda x: x["a"] + x["b"] → 2 + 3 = 5
# 步骤2: lambda x: x * 3 → 5 * 3 = 15
# 输出: 15
```

## 5.1 BaseChatModel 架构

**文件位置：** `libs/core/langchain_core/language_models/chat_models.py`

```python
class BaseChatModel(BaseLanguageModel[BaseMessage], ABC):
    """聊天模型的抽象基类

    所有聊天模型提供商（OpenAI、Anthropic等）都继承这个类
    """

    @abstractmethod
    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """核心生成方法（子类必须实现）"""

    # 高级特性
    def bind_tools(
        self,
        tools: Sequence[BaseTool | dict],
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        """绑定工具以支持函数调用"""

    def with_structured_output(
        self,
        schema: type[BaseModel] | dict,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseModel | dict]:
        """强制输出符合特定结构"""
```

## 5.2 使用聊天模型

### 基本调用
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=1024,
)

# 方式 1: 使用消息列表
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?"),
]
response = model.invoke(messages)
# → AIMessage(content="The capital of France is Paris.")

# 方式 2: 使用字符串（自动转为 HumanMessage）
response = model.invoke("What is 2+2?")
# → AIMessage(content="2+2 equals 4.")
```

### 流式输出
```python
for chunk in model.stream("Tell me a long story"):
    print(chunk.content, end="", flush=True)
# 输出: Once... upon... a... time...
```

### 批量处理
```python
results = model.batch([
    "What is 1+1?",
    "What is 2+2?",
    "What is 3+3?",
])
# → [AIMessage("2"), AIMessage("4"), AIMessage("6")]
```

## 5.3 工具调用（Function Calling）

```python
from langchain_core.tools import tool

# 定义工具
@tool
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny."

# 绑定工具到模型
model_with_tools = model.bind_tools([get_weather])

# AI 会生成工具调用
response = model_with_tools.invoke("What's the weather in SF?")
print(response.tool_calls)
# → [{"name": "get_weather", "args": {"location": "SF"}, "id": "..."}]

# 执行工具并返回结果
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

**工具调用流程：**
```
用户问题 → AI生成tool_call → 执行工具 → 返回ToolMessage → AI生成最终回答
```

## 5.4 结构化输出

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

print(result.setup)      # 类型安全的访问
print(result.punchline)
```

## 🧠 知识挑战

1. `BaseChatModel` 的核心抽象方法是什么？
2. `bind_tools()` 和 `with_structured_output()` 的区别？
3. 工具调用的完整流程是什么？（用流程图描述）

---

# 模块 6：链式组合 (Chains & LCEL)

## 📝 模块 5 答案

1. **核心抽象方法：** `_generate()` - 子类必须实现这个方法来生成响应

2. **区别：**
   - `bind_tools()` - 让AI能调用外部工具（AI决定是否调用）
   - `with_structured_output()` - 强制AI输出符合特定结构（Pydantic模型）

3. **工具调用流程：**
```
用户问题
  → AI分析并生成 tool_call
  → 你的代码执行工具函数
  → 将结果作为 ToolMessage 返回
  → AI 基于工具结果生成最终回答
```

## 6.1 什么是 LCEL？

**LCEL = LangChain Expression Language**

这是 LangChain 的"管道语法"，用于以声明式方式组合组件。

**核心思想：** 使用 `|` 操作符连接 Runnable 对象

```python
# 传统方式（命令式）
prompt_result = prompt.invoke(input)
model_result = model.invoke(prompt_result)
parser_result = parser.invoke(model_result)

# LCEL 方式（声明式）
chain = prompt | model | parser
result = chain.invoke(input)
```

**为什么 LCEL 更好？**
- ✅ **自动支持所有 Runnable 方法**（invoke、batch、stream、ainvoke）
- ✅ **可组合** - 链可以作为其他链的组件
- ✅ **自动错误处理和重试**
- ✅ **内置追踪和调试**

## 6.2 LCEL 核心操作符

### 1️⃣ 管道操作符 `|`（顺序组合）

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
parser = StrOutputParser()  # 提取 AIMessage.content

chain = prompt | model | parser

result = chain.invoke({"topic": "cats"})
# → "Why did the cat sit on the computer? ..." (直接是字符串)
```

**数据流：**
```
{"topic": "cats"}
  → prompt → ChatPromptValue([HumanMessage("Tell me a joke about cats")])
  → model  → AIMessage(content="Why did the cat...")
  → parser → "Why did the cat..." (str)
```

### 2️⃣ 字典操作符 `{}`（并行组合）

```python
from langchain_core.runnables import RunnablePassthrough

chain = {
    "context": retriever,  # 并行分支 1
    "question": RunnablePassthrough()  # 并行分支 2（直接传递输入）
} | prompt | model

chain.invoke("What is LangChain?")
```

**数据流：**
```
"What is LangChain?"
    ┌→ retriever.invoke() → 检索到的文档 ┐
    └→ RunnablePassthrough() → "What is LangChain?" ┘
              ↓
    {"context": "...", "question": "What is LangChain?"}
              ↓
          prompt | model
```

### 3️⃣ 条件分支 `RunnableBranch`

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

def is_short(input):
    return len(input) < 10

branch = RunnableBranch(
    (is_short, RunnableLambda(lambda x: f"Short: {x}")),
    (lambda x: len(x) < 50, RunnableLambda(lambda x: f"Medium: {x}")),
    RunnableLambda(lambda x: f"Long: {x}")  # 默认分支
)

branch.invoke("Hi")        # → "Short: Hi"
branch.invoke("Hello world!")  # → "Medium: Hello world!"
```

## 6.3 实战：RAG 链（检索增强生成）

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 假设你有一个向量数据库检索器
# retriever = ...

prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context:

Context: {context}

Question: {question}
""")

# 构建 RAG 链
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

**流程图：**
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

## 6.4 LCEL 高级特性

### Fallbacks（故障转移）
```python
primary_model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
backup_model = ChatOpenAI(model="gpt-4")

chain = primary_model.with_fallbacks([backup_model])

# 如果 primary_model 失败，自动使用 backup_model
result = chain.invoke("Hello")
```

### Retry（重试）
```python
chain = (prompt | model).with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)
```

### Configurable Alternatives（可配置替代）
```python
from langchain_core.runnables import ConfigurableField

model = ChatAnthropic(model="claude-3-5-sonnet-20241022").configurable_fields(
    model=ConfigurableField(id="model_name")
)

chain = prompt | model

# 运行时切换模型
chain.invoke(
    {"topic": "cats"},
    config={"configurable": {"model_name": "claude-3-opus-20240229"}}
)
```

## 🧠 知识挑战

1. LCEL 的 `|` 操作符和 Python 字典 `{}` 在链中分别代表什么？
2. 为什么 `StrOutputParser` 有用？不用它会怎样？
3. 设计一个 LCEL 链，实现以下功能：
   - 输入用户问题
   - 并行执行：翻译成法语 + 生成回答
   - 合并结果输出

---

# 模块 7：工具与代理 (Tools & Agents)

## 📝 模块 6 答案

1. **操作符含义：**
   - `|` - 顺序执行（管道），输出传递给下一个组件
   - `{}` - 并行执行，相同输入到多个分支，输出合并为字典

2. **StrOutputParser：**
   - 作用：提取 `AIMessage.content` 为纯字符串
   - 不用它：`invoke()` 返回完整的 `AIMessage` 对象

3. **设计方案：**
```python
chain = (
    {
        "translation": translate_prompt | model,
        "answer": answer_prompt | model
    }
    | RunnableLambda(lambda d: f"Answer: {d['answer'].content}\nFrench: {d['translation'].content}")
)
```

## 7.1 什么是 Tool？

**Tool = 可供 AI 调用的 Python 函数**

**文件位置：** `libs/core/langchain_core/tools/base.py`

```python
from langchain_core.tools import BaseTool

class BaseTool(ABC, RunnableSerializable[str, Any]):
    """工具的抽象基类

    工具让 AI 能够执行外部操作（搜索、计算、API调用等）
    """

    name: str
    """工具的唯一名称"""

    description: str
    """工具功能描述（AI 通过这个决定何时调用）"""

    @abstractmethod
    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """工具的执行逻辑"""
```

## 7.2 创建工具的三种方式

### 方式 1：使用 @tool 装饰器（推荐）

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

# 自动生成的属性
print(multiply.name)         # "multiply"
print(multiply.description)  # "Multiply two numbers..."
print(multiply.args_schema)  # Pydantic 模型（从类型注解生成）

# 调用
result = multiply.invoke({"a": 3, "b": 4})  # 12
```

### 方式 2：使用 StructuredTool

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

### 方式 3：继承 BaseTool

```python
from langchain_core.tools import BaseTool
from typing import Type

class CustomTool(BaseTool):
    name: str = "custom_calculator"
    description: str = "Performs advanced calculations"

    def _run(self, expression: str) -> str:
        try:
            return str(eval(expression))  # 注意：生产环境不要用 eval！
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, expression: str) -> str:
        # 异步版本
        return self._run(expression)

tool = CustomTool()
tool.invoke({"expression": "2 + 2"})  # "4"
```

## 7.3 Agent 架构

**Agent = 能够使用工具的自主 AI 系统**

**核心概念：**
1. AI 接收任务
2. AI **决定**需要调用哪些工具
3. 执行工具
4. AI 根据结果继续推理
5. 循环直到任务完成

### 简单 Agent 实现（使用 LCEL）

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic

# 定义工具
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [get_word_length, multiply]

# 创建支持工具的模型
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
model_with_tools = model.bind_tools(tools)

# Agent 提示
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when necessary."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),  # 工具调用记录
])

# Agent 循环逻辑
from langchain_core.messages import AIMessage, ToolMessage

def run_agent(user_input: str, max_iterations: int = 5):
    messages = [("human", user_input)]

    for i in range(max_iterations):
        # AI 生成响应（可能包含工具调用）
        response = model_with_tools.invoke(messages)
        messages.append(response)

        # 检查是否有工具调用
        if not response.tool_calls:
            # 没有工具调用，任务完成
            return response.content

        # 执行所有工具调用
        for tool_call in response.tool_calls:
            tool = next(t for t in tools if t.name == tool_call["name"])
            tool_result = tool.invoke(tool_call["args"])

            # 将工具结果添加到对话
            messages.append(ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            ))

    return "Max iterations reached"

# 测试
result = run_agent("What is the length of 'hello' multiplied by 3?")
print(result)
```

**Agent 执行流程：**
```
用户: "What is the length of 'hello' multiplied by 3?"
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

## 7.4 LangGraph（高级 Agent 框架）

对于复杂的 Agent，推荐使用 **LangGraph**（LangChain 生态系统的一部分）：

```python
from langgraph.prebuilt import create_react_agent

# 创建 ReAct Agent（推理+行动循环）
agent_executor = create_react_agent(
    model=model,
    tools=tools
)

# 流式执行
for event in agent_executor.stream({"messages": [("human", "What is 2+2?")]}):
    print(event)
```

**LangGraph 优势：**
- ✅ 状态管理（记忆）
- ✅ 人机协同（Human-in-the-loop）
- ✅ 可视化工作流
- ✅ 持久化检查点

## 🧠 知识挑战

1. 工具的三个必需属性是什么？
2. Agent 和普通 Chain 的本质区别是什么？
3. 设计一个工具：检查给定URL是否可访问（返回True/False）

---

# 模块 8：高级特性

## 📝 模块 7 答案

1. **工具三要素：**
   - `name` - 唯一标识符
   - `description` - 功能描述（AI 用于判断何时调用）
   - `_run()` 方法 - 实际执行逻辑

2. **本质区别：**
   - **Chain** - 预定义的执行流程，固定顺序
   - **Agent** - AI **动态决定**下一步行动，包括是否/何时调用工具

3. **URL检查工具：**
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

## 8.1 Callbacks（回调系统）

**用途：** 追踪、日志、调试、监控

**文件位置：** `libs/core/langchain_core/callbacks/`

```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage

class MyCallbackHandler(BaseCallbackHandler):
    """自定义回调处理器"""

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"[LLM Start] Prompts: {prompts}")

    def on_llm_end(self, response, **kwargs):
        print(f"[LLM End] Response: {response}")

    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"[Chain Start] Inputs: {inputs}")

# 使用回调
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

result = model.invoke(
    "Hello",
    config={"callbacks": [MyCallbackHandler()]}
)

# 输出:
# [LLM Start] Prompts: ['Hello']
# [LLM End] Response: ...
```

### 内置回调

```python
from langchain.callbacks import StdOutCallbackHandler

# 打印所有中间步骤到标准输出
handler = StdOutCallbackHandler()

chain = prompt | model
chain.invoke("Hello", config={"callbacks": [handler]})
```

## 8.2 Streaming（流式处理）

### 流式输出文本

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# 逐 token 流式输出
for chunk in model.stream("Tell me a long story"):
    print(chunk.content, end="", flush=True)
```

### 流式处理链中的中间步骤

```python
chain = prompt | model | StrOutputParser()

# 使用 astream_events 获取所有事件
async for event in chain.astream_events("Tell me a joke", version="v2"):
    kind = event["event"]
    if kind == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
    elif kind == "on_parser_stream":
        print(f"[Parser]: {event['data']['chunk']}")
```

## 8.3 Memory（记忆系统）

**文件位置：** `libs/core/langchain_core/chat_history.py`

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# 内存存储
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 创建带记忆的链
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

# 使用（自动保存历史）
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

## 8.4 Caching（缓存）

**文件位置：** `libs/core/langchain_core/caches.py`

```python
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache

# 启用全局缓存
set_llm_cache(InMemoryCache())

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# 第一次调用（慢）
result1 = model.invoke("What is 2+2?")

# 第二次调用（快！从缓存读取）
result2 = model.invoke("What is 2+2?")  # 相同输入直接返回缓存
```

## 8.5 Retrieval（检索增强生成 RAG）

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import Embeddings

# 创建向量数据库
vectorstore = InMemoryVectorStore.from_texts(
    ["LangChain is a framework for LLMs", "Paris is the capital of France"],
    embedding=embeddings  # 需要嵌入模型
)

# 创建检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# RAG 链
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

## 8.6 Output Parsers（输出解析器）

**文件位置：** `libs/core/langchain_core/output_parsers/`

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

# 1. 字符串解析器
str_parser = StrOutputParser()
chain = model | str_parser
chain.invoke("Hello")  # 返回 str 而不是 AIMessage

# 2. JSON 解析器
json_parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template(
    "Output a JSON with 'name' and 'age' for: {person}"
)
chain = prompt | model | json_parser
chain.invoke({"person": "a 30-year-old named Alice"})
# → {"name": "Alice", "age": 30}

# 3. Pydantic 解析器（类型安全）
class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")

model_with_structure = model.with_structured_output(Person)
result = model_with_structure.invoke("Tell me about a 30-year-old named Bob")
# → Person(name="Bob", age=30)
```

## 🧠 最终综合挑战

设计一个完整的 LangChain 应用，包含以下功能：

1. **需求：** 技术文档问答系统
2. **功能：**
   - 用户上传文档（PDF/TXT）
   - 系统建立向量索引
   - 用户提问，系统基于文档回答
   - 如果文档中没有答案，调用搜索工具
   - 保存对话历史

**提示：** 你需要用到：
- `ChatPromptTemplate`
- `VectorStore` + `Retriever`
- `Tools` (搜索工具)
- `Agent` 或 `RunnableWithMessageHistory`
- `Callbacks` (可选，用于追踪)

**思考：** 你会如何设计这个系统的架构？画出数据流图。

---

## 🎓 学习完成！

恭喜你完成了所有 8 个模块！现在你应该：

✅ 理解 LangChain 的架构和设计哲学
✅ 掌握 Messages、Prompts、Runnables 的使用
✅ 能够使用 LCEL 构建复杂的链
✅ 理解工具和 Agent 的工作原理
✅ 知道如何应用高级特性（Streaming、Memory、RAG）

**下一步：**
1. 阅读官方文档深入特定主题
2. 查看 `libs/core/tests/` 中的测试用例学习最佳实践
3. 构建实际项目巩固知识

**推荐练习项目：**
- 个人知识库问答系统
- 多模态聊天机器人（支持图片）
- 自动化研究助手（带搜索和总结）
- 代码分析工具（使用 AST 和 LLM）

祝你在 LangChain 开发之旅中取得成功！🚀
