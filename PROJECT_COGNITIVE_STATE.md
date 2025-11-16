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
* [X] 模块 1：万物皆`Runnable` - 核心抽象 (文件: `libs/core/langchain_core/runnables/base.py`)
* [X] 模块 2：`Runnable`的组合 - 序列 (文件: `libs/core/langchain_core/runnables/base.py` - RunnableSequence)
* [ ] 模块 3：`Runnable`的实现 - Prompts (文件: `libs/core/langchain_core/prompts/base.py`)
* [ ] 模块 4：`Runnable`的实现 - LLMs (文件: `libs/core/langchain_core/language_models/llms.py`)
* [ ] 模块 5：`Runnable`的实现 - ChatModels (文件: `libs/core/langchain_core/language_models/chat_models.py`)
* [ ] 模块 6：(交叉练习) LangChain表达式语言(LCEL)的完整流程

**当前状态：**
* **已完成模块：**
    * ✅ **模块 1：万物皆`Runnable` - 核心抽象** (完成时间: 2025-11-16)
        - 学习内容：
          * `Runnable` 的设计哲学：统一接口实现可组合性
          * 核心抽象方法 `invoke` 及其作为唯一必需实现方法的原因
          * 默认实现（`ainvoke`、`batch`、`stream`）如何基于 `invoke` 构建
          * 泛型类型系统 `Generic[Input, Output]` 保证类型安全
          * `__or__` 操作符的组合魔法：创建 `RunnableSequence`
        - 关键源码位置：
          * `libs/core/langchain_core/runnables/base.py:123` - `Runnable` 类定义
          * `libs/core/langchain_core/runnables/base.py:817` - `invoke` 抽象方法
          * `libs/core/langchain_core/runnables/base.py:840` - `ainvoke` 默认实现
          * `libs/core/langchain_core/runnables/base.py:863` - `batch` 默认实现
          * `libs/core/langchain_core/runnables/base.py:1126` - `stream` 默认实现
          * `libs/core/langchain_core/runnables/base.py:616` - `__or__` 操作符
        - 核心洞察：
          * 只要实现 `invoke`，就自动获得异步、批处理、流式的支持
          * `config` 参数实现了横切关注点的优雅分离
          * 线程池的使用使批处理对 I/O 密集型任务高效
        - 文档：
          * `docs/module-01-runnable-core-ZH.md`
          * `docs/module-01-runnable-core-EN.md`

    * ✅ **模块 2：`Runnable`的组合 - RunnableSequence** (完成时间: 2025-11-16)
        - 学习内容：
          * `RunnableSequence` 的数据结构设计：first/middle/last 保留类型信息
          * 类型推导机制：InputType 来自 first，OutputType 来自 last
          * `invoke` 的实现：循环中自动传递中间结果（链式调用）
          * 扁平化优化：`__init__` 和 `__or__` 避免嵌套序列
          * 可观测性：回调管理器创建层次化的运行追踪
        - 关键源码位置：
          * `libs/core/langchain_core/runnables/base.py:2789` - `RunnableSequence` 类定义
          * `libs/core/langchain_core/runnables/base.py:2876-2881` - first/middle/last 字段
          * `libs/core/langchain_core/runnables/base.py:2883-2922` - `__init__` 扁平化逻辑
          * `libs/core/langchain_core/runnables/base.py:2954-2963` - InputType/OutputType 推导
          * `libs/core/langchain_core/runnables/base.py:3103-3136` - `invoke` 链式调用实现
          * `libs/core/langchain_core/runnables/base.py:3048-3073` - `__or__` 优化
        - 核心洞察：
          * first/middle/last 设计保留了端到端的类型信息
          * 扁平化确保无论如何组合，最终都是单层序列
          * `invoke` 中的 for 循环通过重复赋值 `input_` 实现自动链式传递
          * 回调系统创建树形追踪结构（root run → child runs）
        - 文档：
          * `docs/module-02-runnable-sequence-ZH.md`
          * `docs/module-02-runnable-sequence-EN.md`

* **下一步行动：**
    * **[待执行] -> 模块 3：`Runnable`的实现 - Prompts (文件: `libs/core/langchain_core/prompts/base.py`)** - *回复"继续"开始下一模块的深入教学。*

---

## 3. 学习笔记 (LEARNING_NOTES)
# (此区域记录您的个人笔记、疑问和关键洞察)

### 模块 1 关键记忆点
* **核心契约：** `invoke(input: Input) -> Output` 是唯一必须实现的方法
* **类型参数：** `Runnable[Input, Output]` - 两个泛型参数确保组合的类型安全
* **4 个核心方法：** `invoke`（同步）、`ainvoke`（异步）、`batch`（批处理）、`stream`（流式）
* **组合符号：** `A | B` 等价于 `RunnableSequence(A, B)`
* **设计哲学：** "统一接口 → 自由组合 → 自动继承能力"

### 模块 2 关键记忆点
* **数据结构：** `first: Runnable[Input, Any]`, `middle: list[Runnable[Any, Any]]`, `last: Runnable[Any, Output]`
* **类型推导：** `seq.InputType = seq.first.InputType`, `seq.OutputType = seq.last.OutputType`
* **链式调用：** `for step in steps: input_ = step.invoke(input_)` - 输出成为下一个输入
* **扁平化：** `isinstance(step, RunnableSequence)` 时展开其 steps
* **可视化：** 树形追踪 - root run 包含 seq:step:1, seq:step:2, ...

### 待回答的挑战问题

**模块 1：**
1. 为什么需要 Runnable？
2. 核心契约是什么？
3. 为什么 ainvoke/batch/stream 可以有默认实现？
4. SQLExecutor 应该如何声明类型？
5. 如果 invoke 不是抽象方法会怎样？
6. executor.map 的优势是什么？
7. Runnable 组合的类型推导？

**模块 2：**
1. 为什么需要 first/middle/last 而不是 list[Runnable]？
2. invoke 的核心逻辑是什么？
3. 扁平化优化的作用？
4. input_ 重复赋值如何实现链式调用？
5. seq = A | B | C 的内部结构？
6. seq1 | seq2 的扁平化结果？
7. 类型不匹配时会发生什么？

---

## 4. 认知元数据 (METADATA)

**创建时间：** 2025-11-16
**最后更新：** 2025-11-16 (模块 2 完成)
**项目：** LangChain (https://github.com/langchain-ai/langchain)
**项目路径：** `/home/user/langchain`
**当前分支：** `claude/langchain-deep-analysis-01MnJ66aZzYtsNCaB67h5ANp`
**分析深度：** 深度优先 (Depth-First)
**认知策略：** 集中练习 (Deliberate Practice) + 主动提取 (Active Retrieval)
**当前进度：** 2/6 模块完成 (33.3%)
**文档语言：** 中英双语
