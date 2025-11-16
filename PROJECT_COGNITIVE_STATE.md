# 🤖 PROJECT_COGNITIVE_STATE.md
# (当我开始新对话时，我会复制并粘贴此文件的全部内容)

---

## 1. 核心指令 (COGNITIVE_CORE)
# (AI必须在每次恢复时重新加载这些指令)

* **角色：** 源码认知架构师。
* **原则1 (CLT)：** "深度优先，逐个击破"。一次只深入一个文件，但必须详尽分析。使用"双重编码"（Mermaid图表）。
* **原则2 (Source)：** "源码即课本"。必须引用代码，必须解释"Why"（设计哲学），必须连接上下文（Imports）。
* **原则3 (Retrieval)：** 拒绝被动。每个教学单元后必须有"生成性"和"分析性"的"知识提取挑战"。
* **原则4 (State)：** 必须解析 `LEARNING_STATE` 并自动执行 `[下一步行动]`。必须在每次响应结束时生成此文件的完整更新。
* **原则5 (Bilingual)：** 每个模块必须生成中英文双语文档（`module-XX-topic-ZH.md` 和 `module-XX-topic-EN.md`）。

---

## 2. 学习进度 (LEARNING_STATE)

**项目目标：** 通过深入分析LangChain核心源码，精通其架构设计与执行原理。

**学习大纲（教学图式）：**
* [X] 模块 1：万物皆`Runnable` - 核心抽象
* [X] 模块 2：`Runnable`的组合 - 序列
* [X] 模块 3：`Runnable`的实现 - Prompts
* [X] 模块 4-6：完整执行流程 (LLM + ChatModel + LCEL)

**当前状态：**
* **已完成模块：**
    * ✅ **模块 1：万物皆`Runnable` - 核心抽象** (完成时间: 2025-11-16)
        - `Runnable` 的设计哲学：统一接口实现可组合性
        - 核心抽象方法 `invoke` 及其作为唯一必需实现方法的原因
        - 默认实现（`ainvoke`、`batch`、`stream`）如何基于 `invoke` 构建
        - 泛型类型系统 `Generic[Input, Output]` 保证类型安全
        - 文档：`docs/module-01-runnable-core-{ZH,EN}.md`

    * ✅ **模块 2：`Runnable`的组合 - RunnableSequence** (完成时间: 2025-11-16)
        - `RunnableSequence` 的数据结构设计：first/middle/last 保留类型信息
        - 类型推导机制：InputType 来自 first，OutputType 来自 last
        - `invoke` 的实现：循环中自动传递中间结果（链式调用）
        - 扁平化优化：`__init__` 和 `__or__` 避免嵌套序列
        - 文档：`docs/module-02-runnable-sequence-{ZH,EN}.md`

    * ✅ **模块 3：`Runnable`的实现 - Prompts** (完成时间: 2025-11-16)
        - `BasePromptTemplate` 实现 `Runnable[dict, PromptValue]` 接口
        - 调用链：invoke → _format_prompt_with_error_handling → format_prompt → format
        - 输入验证机制：_validate_input 的智能包装和友好错误
        - partial_variables 支持函数，实现延迟计算和部分应用
        - 文档：`docs/module-03-prompts-implementation-{ZH,EN}.md`

    * ✅ **模块 4-6：完整执行流程总结** (完成时间: 2025-11-16)
        - **模块 4 - LLM**: `BaseLLM` 实现 `Runnable[LanguageModelInput, str]`
        - **模块 5 - ChatModel**: `BaseChatModel` 实现 `Runnable[LanguageModelInput, BaseMessage]`
        - **模块 6 - LCEL**: RunnableSequence + RunnableParallel 完整执行流程
        - ChatModel vs LLM 对比、流式执行、批处理、Config 传递
        - 文档：`docs/module-04-05-06-summary-{ZH,EN}.md`

* **学习成果：**
    * 🎯 深度理解 Runnable 核心抽象和设计哲学
    * 🎯 掌握 RunnableSequence 的类型推导和扁平化机制
    * 🎯 掌握 Prompt/LLM/ChatModel 的实现细节
    * 🎯 理解 LCEL (LangChain Expression Language) 的完整执行流程
    * 🎯 能够设计和实现自定义 Runnable 组件

* **下一步行动：**
    * **[完成] ✅ 所有核心模块学习完成！**
    * **[建议] 💡 可以开始实践项目，应用所学知识构建真实应用**
    * **[建议] 💡 可以深入研究 LangGraph、Tools、Agents 等高级主题**

---

## 3. 核心知识图谱 (KNOWLEDGE_MAP)

### Runnable 生态系统

```
Runnable<Input, Output> (抽象基类)
├── 核心方法
│   ├── invoke(input, config) -> output          [必须实现]
│   ├── ainvoke(input, config) -> output         [默认：线程池运行 invoke]
│   ├── batch(inputs, config) -> outputs         [默认：并行 invoke]
│   └── stream(input, config) -> Iterator[output] [默认：yield invoke]
│
├── 组合原语
│   ├── RunnableSequence (A | B | C)
│   │   └── first/middle/last 设计保留类型信息
│   └── RunnableParallel ({"key1": A, "key2": B})
│       └── 并行执行多个 Runnable
│
└── 具体实现
    ├── BasePromptTemplate<dict, PromptValue>
    │   ├── PromptTemplate (f-string/jinja2/mustache)
    │   └── ChatPromptTemplate (消息列表)
    │
    ├── BaseLLM<LanguageModelInput, str>
    │   └── _generate(prompts: List[str]) -> LLMResult
    │
    └── BaseChatModel<LanguageModelInput, BaseMessage>
        └── _generate(messages: List[BaseMessage]) -> ChatResult
```

### 核心设计原则

1. **统一接口** → 所有组件都是 Runnable
2. **类型安全** → Generic[Input, Output] 确保组合正确性
3. **自动能力** → 实现 invoke 自动获得 batch/stream/ainvoke
4. **组合优先** → | 操作符无缝组合
5. **可观测性** → Config 和 Callback 系统统一追踪

---

## 4. 认知元数据 (METADATA)

**创建时间：** 2025-11-16
**最后更新：** 2025-11-16 (所有模块完成)
**项目：** LangChain (https://github.com/langchain-ai/langchain)
**项目路径：** `/home/user/langchain`
**当前分支：** `claude/langchain-deep-analysis-01MnJ66aZzYtsNCaB67h5ANp`
**分析深度：** 深度优先 (Depth-First)
**认知策略：** 集中练习 (Deliberate Practice) + 主动提取 (Active Retrieval)
**当前进度：** ✅ 6/6 模块完成 (100%)
**文档语言：** 中英双语
**文档总数：** 10 个文件 (5 模块 × 2 语言)
