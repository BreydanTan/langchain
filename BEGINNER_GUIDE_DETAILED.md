# 🚀 LangChain 零基础入门指南（超详细版）

> **写给完全不懂的初学者**：这份指南假设你只会基本的 Python，其他一切都会从零开始解释。

---

## 📖 目录

1. [LangChain 是什么？](#langchain-是什么)
2. [环境配置（如何开始使用）](#环境配置如何开始使用)
3. [核心概念详解](#核心概念详解)
4. [你的第一个 LangChain 程序](#你的第一个-langchain-程序)
5. [学习路径建议](#学习路径建议)

---

## LangChain 是什么？

### 用人话说

**LangChain = 搭积木的工具箱，用来构建 AI 应用**

想象一下：
- 你想做一个能**回答问题的 AI 客服**
- 你想做一个能**读懂你的文档并总结**的助手
- 你想做一个能**自动搜索网络并给你答案**的 AI

这些都需要把很多"零件"组合在一起：
- 大语言模型（如 GPT、Claude）
- 搜索工具
- 数据库
- 提示词模板

**LangChain 就是帮你把这些零件轻松组装在一起的框架。**

### 打个比方

如果你要做菜：
- **没有 LangChain**：你需要自己去菜市场买菜、洗菜、切菜、炒菜，每一步都要自己写代码
- **有了 LangChain**：它给你提供了切好的菜、调好的酱料、标准的炒菜步骤，你只需要按照说明组合就行

---

## 环境配置（如何开始使用）

### 第一步：安装 Python

LangChain 需要 **Python 3.9 或更高版本**。

检查你的 Python 版本：
```bash
python --version
# 或
python3 --version
```

如果版本太低或没有安装，去 [python.org](https://www.python.org/downloads/) 下载安装。

---

### 第二步：安装 LangChain

#### 方式 1：最小安装（推荐新手）

```bash
# 安装核心包
pip install langchain-core

# 安装一个 LLM 提供商（选一个）
pip install langchain-openai      # 如果用 OpenAI (GPT)
pip install langchain-anthropic   # 如果用 Anthropic (Claude)
pip install langchain-ollama      # 如果用本地模型 Ollama
```

#### 方式 2：完整安装（包含所有工具）

```bash
pip install langchain
```

**为什么有两种方式？**
- `langchain-core` 只包含基础功能，轻量级
- `langchain` 包含所有额外工具（文档加载器、数据库集成等），比较大

**新手建议**：先装 `langchain-core` + 一个 LLM 包，需要其他功能时再装。

---

### 第三步：获取 API Key

LangChain 需要调用 AI 模型（如 GPT、Claude），你需要一个 API 密钥。

#### 选项 1：使用 OpenAI (GPT)
1. 去 [OpenAI 网站](https://platform.openai.com/api-keys) 注册
2. 创建 API Key
3. 设置环境变量：
   ```bash
   # macOS/Linux
   export OPENAI_API_KEY="你的密钥"

   # Windows (PowerShell)
   $env:OPENAI_API_KEY="你的密钥"
   ```

#### 选项 2：使用 Anthropic (Claude)
1. 去 [Anthropic 网站](https://console.anthropic.com/) 注册
2. 获取 API Key
3. 设置环境变量：
   ```bash
   # macOS/Linux
   export ANTHROPIC_API_KEY="你的密钥"

   # Windows (PowerShell)
   $env:ANTHROPIC_API_KEY="你的密钥"
   ```

#### 选项 3：使用本地模型（免费，但需要好的电脑）
1. 安装 [Ollama](https://ollama.com/)
2. 下载模型：`ollama pull llama2`
3. 不需要 API Key！

**新手建议**：先用 Anthropic Claude（比较便宜且好用），或 Ollama（免费但需要配置）。

---

### 第四步：验证安装

创建一个测试文件 `test_langchain.py`：

```python
# 测试 1：检查 langchain-core 是否安装成功
try:
    from langchain_core.messages import HumanMessage
    print("✅ langchain-core 安装成功！")
except ImportError:
    print("❌ langchain-core 未安装，请运行: pip install langchain-core")

# 测试 2：检查 LLM 提供商是否安装（以 Anthropic 为例）
try:
    from langchain_anthropic import ChatAnthropic
    print("✅ langchain-anthropic 安装成功！")

    # 测试 3：尝试调用 AI（需要 API Key）
    model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    response = model.invoke("Say hello!")
    print(f"✅ AI 调用成功！回复: {response.content}")

except ImportError:
    print("❌ langchain-anthropic 未安装，请运行: pip install langchain-anthropic")
except Exception as e:
    print(f"❌ AI 调用失败: {e}")
    print("   请检查你的 API Key 是否设置正确")
```

运行：
```bash
python test_langchain.py
```

如果看到 ✅，恭喜你配置成功！

---

## 核心概念详解

### 概念 1：Monorepo 结构 - 一个仓库管理多个包

#### 什么是 Monorepo？

**传统方式（多个仓库）：**
```
langchain-repo-1/  (主包)
langchain-repo-2/  (OpenAI 集成)
langchain-repo-3/  (Anthropic 集成)
...
```
每个功能都是独立的代码库，更新很麻烦。

**Monorepo 方式（一个仓库）：**
```
langchain/
├─ libs/core/          (核心代码)
├─ libs/partners/openai/
├─ libs/partners/anthropic/
└─ ...
```
所有代码在一个仓库里，但发布成独立的包。

#### 为什么这样做？

**类比**：就像宜家的仓库
- **Monorepo = 一个大仓库**，里面有不同区域（家具、厨具、装饰品）
- 每个区域可以**单独销售**，但都在同一个地方管理
- 好处：更新一个区域时，可以确保和其他区域兼容

**LangChain 的 Monorepo 结构：**

```
/home/user/langchain/libs/
│
├─ core/                    ← 🏗️ 地基（所有功能的基础）
│  └─ langchain_core/
│     ├─ runnables/        ← 可组合的执行单元
│     ├─ messages/         ← 消息对象
│     ├─ prompts/          ← 提示模板
│     └─ language_models/  ← AI 模型接口
│
├─ partners/                ← 🔌 插件（各种 AI 提供商）
│  ├─ openai/              ← OpenAI (GPT) 集成
│  ├─ anthropic/           ← Anthropic (Claude) 集成
│  └─ ollama/              ← 本地模型集成
│
├─ langchain_v1/            ← 📦 主包（高级功能）
└─ text-splitters/          ← ✂️ 工具（文本分割等）
```

**你只需要记住**：
- `langchain-core` = 必装的基础包
- `langchain-anthropic` / `langchain-openai` = 根据你用的 AI 选一个装
- `langchain` = 可选的完整包（包含额外工具）

---

### 概念 2：Runnable - 统一的"可执行对象"

#### 什么是 Runnable？

**简单理解**：Runnable = 任何可以"运行"的东西

**类比**：就像电器的"电源插头"
- 无论是电视、冰箱、风扇，都有**统一的插头**
- 你不需要关心内部怎么工作，只需要**插上电源就能用**

在 LangChain 中：
- 提示模板 = Runnable
- AI 模型 = Runnable
- 工具 = Runnable
- 整个复杂的 AI 流程 = 也是 Runnable

它们都有**相同的使用方式**！

#### Runnable 的 4 个核心方法

```python
# 假设 `component` 是任何 Runnable 对象

# 1. invoke() - 单次调用
result = component.invoke(input)
# 类比：按一次按钮

# 2. batch() - 批量处理
results = component.batch([input1, input2, input3])
# 类比：一次性处理多个任务（并行）

# 3. stream() - 流式输出
for chunk in component.stream(input):
    print(chunk, end="")
# 类比：边生成边显示（像 ChatGPT 打字效果）

# 4. ainvoke() - 异步调用
result = await component.ainvoke(input)
# 类比：后台运行，不阻塞其他操作
```

#### 为什么 Runnable 重要？

**没有 Runnable（传统方式）：**
```python
# 每个组件调用方式不同
prompt_result = prompt.format(input)          # 方法名叫 format
model_result = model.generate(prompt_result)  # 方法名叫 generate
parser_result = parser.parse(model_result)    # 方法名叫 parse
```

**有了 Runnable（LangChain 方式）：**
```python
# 所有组件都用 invoke
prompt_result = prompt.invoke(input)
model_result = model.invoke(prompt_result)
parser_result = parser.invoke(model_result)

# 甚至可以直接连起来！
chain = prompt | model | parser
result = chain.invoke(input)  # 一行搞定
```

---

### 概念 3：设计原则 - LangChain 的"三大哲学"

#### 原则 1：一切皆 Runnable（统一接口）

**解释**：所有组件都用相同的方式调用

**类比**：
- 就像所有 USB 设备（鼠标、键盘、U盘）都用同样的 USB 接口
- 你不需要为每个设备学习不同的插法

**好处**：
- 学习一次，终身受用
- 组件可以互换（今天用 GPT，明天换 Claude 只需改一行代码）

---

#### 原则 2：声明式组合（用 `|` 连接）

**解释**：用管道符号 `|` 把组件像积木一样连接起来

**类比**：
- 就像工厂的**流水线**：原料 → 加工 → 包装 → 成品
- 或者做菜：洗菜 → 切菜 → 炒菜 → 装盘

**代码示例**：
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

# 组件 1：提示模板（告诉 AI 要做什么）
prompt = ChatPromptTemplate.from_template("给我讲一个关于{topic}的笑话")

# 组件 2：AI 模型
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# 用 | 连接（声明式组合）
chain = prompt | model

# 调用
result = chain.invoke({"topic": "程序员"})
print(result.content)
```

**执行流程**：
```
用户输入 {"topic": "程序员"}
    ↓
prompt 生成：ChatPromptValue([HumanMessage("给我讲一个关于程序员的笑话")])
    ↓
model 调用 AI 生成笑话
    ↓
返回：AIMessage("为什么程序员分不清万圣节和圣诞节？...")
```

**为什么叫"声明式"？**
- **命令式**（传统）：你告诉计算机**怎么做**（step by step）
- **声明式**（LangChain）：你告诉计算机**做什么**（连接好就行，细节自动处理）

---

#### 原则 3：插件式架构（依赖倒置）

**解释**：核心代码定义"接口"，具体实现由插件提供

**类比**：
- 就像**手机壳**：手机定义了"外壳的形状"（接口）
- 厂商可以做各种材质的壳（硅胶、金属、皮革），但都能装上

**在 LangChain 中**：
```
langchain-core 定义：
"聊天模型必须有 invoke() 方法，接收消息，返回回复"
    ↓
各家 AI 公司实现：
- langchain-openai 实现：ChatOpenAI
- langchain-anthropic 实现：ChatAnthropic
- langchain-ollama 实现：ChatOllama

它们都遵循相同的接口！
```

**好处**：
```python
# 今天用 OpenAI
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4")

# 明天想换 Claude，只需改这两行！
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# 其他代码完全不用改
chain = prompt | model  # 这行代码不变
```

---

## 你的第一个 LangChain 程序

### 程序 1：最简单的问答

```python
from langchain_anthropic import ChatAnthropic

# 1. 创建 AI 模型
model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7  # 0=严肃, 1=创意
)

# 2. 调用
response = model.invoke("你好！")
print(response.content)
```

**运行**：
```bash
python your_file.py
```

**输出**：
```
你好！很高兴见到你。有什么我可以帮助你的吗？
```

---

### 程序 2：带提示模板的问答

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

# 1. 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{role}。"),
    ("human", "{question}")
])

# 2. 创建模型
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# 3. 组合
chain = prompt | model

# 4. 调用
response = chain.invoke({
    "role": "Python 老师",
    "question": "什么是列表推导式？"
})

print(response.content)
```

**执行流程图**：
```
输入: {"role": "Python 老师", "question": "什么是列表推导式？"}
    ↓
prompt 生成消息:
  SystemMessage("你是一个专业的Python老师。")
  HumanMessage("什么是列表推导式？")
    ↓
model 调用 AI
    ↓
返回: AIMessage("列表推导式是 Python 中一种简洁的创建列表的方法...")
```

---

### 程序 3：对话机器人（带历史记录）

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_anthropic import ChatAnthropic

# 1. 创建带历史记录的提示
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。"),
    MessagesPlaceholder("history"),  # 这里会插入历史对话
    ("human", "{input}")
])

# 2. 创建模型
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# 3. 组合
chain = prompt | model

# 4. 对话
conversation_history = []

def chat(user_input):
    # 调用链
    response = chain.invoke({
        "history": conversation_history,
        "input": user_input
    })

    # 保存到历史
    from langchain_core.messages import HumanMessage, AIMessage
    conversation_history.append(HumanMessage(content=user_input))
    conversation_history.append(response)

    return response.content

# 使用
print(chat("我叫小明"))
# 输出: 你好小明！很高兴认识你...

print(chat("我叫什么名字？"))
# 输出: 你叫小明！
```

---

## 学习路径建议

### 阶段 1：基础概念（1-2 天）

**目标**：理解核心概念，能跑通简单示例

**学习内容**：
1. ✅ 完成环境配置
2. ✅ 理解 Runnable 是什么
3. ✅ 跑通上面的 3 个示例程序

**检验标准**：
- [ ] 能用自己的话解释什么是 Runnable
- [ ] 能写一个简单的问答程序
- [ ] 能使用提示模板

---

### 阶段 2：消息系统（1 天）

**目标**：理解 LangChain 如何表示对话

**学习内容**：
1. 学习 `HumanMessage`（用户消息）
2. 学习 `AIMessage`（AI 回复）
3. 学习 `SystemMessage`（系统指令）

**实践项目**：
- 做一个角色扮演聊天机器人（如：海盗、莎士比亚、程序员）

---

### 阶段 3：提示工程（2-3 天）

**目标**：学会设计好的提示词

**学习内容**：
1. `PromptTemplate`（简单模板）
2. `ChatPromptTemplate`（聊天模板）
3. `MessagesPlaceholder`（插入历史对话）

**实践项目**：
- 做一个客服机器人（带历史记录）

---

### 阶段 4：链式组合（3-5 天）

**目标**：学会用 `|` 组合复杂流程

**学习内容**：
1. Pipe 操作符 `|`
2. 并行执行（用字典 `{}`）
3. 条件分支

**实践项目**：
- 做一个"翻译+总结"工具（输入文章，输出翻译和摘要）

---

### 阶段 5：工具与代理（5-7 天）

**目标**：让 AI 能调用外部工具（搜索、计算器等）

**学习内容**：
1. 创建工具（`@tool` 装饰器）
2. Agent 的工作原理
3. LangGraph（高级 Agent 框架）

**实践项目**：
- 做一个能搜索网络并回答问题的 AI

---

### 阶段 6：高级功能（按需学习）

- **RAG（检索增强生成）**：让 AI 读懂你的文档
- **Streaming（流式输出）**：像 ChatGPT 一样逐字显示
- **Memory（记忆系统）**：长期记住用户信息

---

## 🎯 总结

### 记住这 5 个关键点

1. **Runnable = 统一接口**
   - 所有组件都用 `invoke()` 调用

2. **`|` = 连接组件**
   - `prompt | model | parser` 就像流水线

3. **Messages = 对话的"信封"**
   - `HumanMessage`、`AIMessage`、`SystemMessage`

4. **Prompt = 告诉 AI 怎么做**
   - 用模板避免重复写提示词

5. **Tools = 给 AI 装上手脚**
   - 让 AI 能搜索、计算、访问数据库

---

### 下一步

1. 完成环境配置
2. 跑通"你的第一个程序"
3. 按照学习路径，每天学一点
4. 遇到问题随时查看这份文档

**记住**：学编程最好的方式是**动手做项目**！不要只看文档，一定要写代码！

祝你学习顺利！🚀
