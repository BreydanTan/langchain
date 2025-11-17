# 🎓 LangChain 核心源码深度分析系列

## 📚 学习路径概览

本系列文档采用**深度优先、源码驱动**的方式，带您从零到精通 LangChain 的核心架构。

### 🎯 学习成果

完成本系列后，您将能够：
- ✅ 深度理解 `Runnable` 接口的设计哲学
- ✅ 掌握 LangChain 的组合机制（`|` 操作符）
- ✅ 理解 Prompt、LLM、ChatModel 的实现细节
- ✅ 能够设计和实现自定义 Runnable 组件
- ✅ 构建复杂的 LCEL (LangChain Expression Language) 链

---

## 📖 模块列表

### [模块 1：万物皆 Runnable - 核心抽象](./module-01-runnable-core-ZH.md)
**英文版**：[Module 1: Runnable Core Abstraction](./module-01-runnable-core-EN.md)

**核心内容**：
- `Runnable[Input, Output]` 的设计哲学
- `invoke` 作为唯一抽象方法的原因
- 默认实现：`ainvoke`、`batch`、`stream`
- 泛型类型系统保证组合安全

**关键洞察**：
> 只要实现 `invoke`，就自动获得异步、批处理、流式的支持！

---

### [模块 2：Runnable 的组合 - RunnableSequence](./module-02-runnable-sequence-ZH.md)
**英文版**：[Module 2: RunnableSequence Composition](./module-02-runnable-sequence-EN.md)

**核心内容**：
- `first`/`middle`/`last` 数据结构设计
- 类型推导机制（`InputType` 和 `OutputType`）
- 链式调用的实现细节
- 扁平化优化避免嵌套

**关键洞察**：
> `A | B | C` 自动创建 `RunnableSequence[A.Input, C.Output]`，类型安全！

---

### [模块 3：Runnable 的实现 - Prompts](./module-03-prompts-implementation-ZH.md)
**英文版**：[Module 3: Prompts Implementation](./module-03-prompts-implementation-EN.md)

**核心内容**：
- `BasePromptTemplate` 实现 `Runnable[dict, PromptValue]`
- 调用链：`invoke` → `_validate_input` → `format_prompt` → `format`
- 智能输入验证（单值自动包装）
- `partial_variables` 的函数支持（延迟计算）

**关键洞察**：
> `PromptValue` 抽象使提示可以转换为字符串或消息列表！

---

### [模块 4-6：完整执行流程总结](./module-04-05-06-summary-ZH.md)
**英文版**：[Modules 4-6: Complete Execution Flow](./module-04-05-06-summary-EN.md)

**核心内容**：

#### 模块 4：LLM 实现
- `BaseLLM` 实现 `Runnable[LanguageModelInput, str]`
- `_generate(prompts: List[str])` 批处理接口
- 流式输出支持

#### 模块 5：ChatModel 实现
- `BaseChatModel` 实现 `Runnable[LanguageModelInput, BaseMessage]`
- 工具调用：`bind_tools()`
- 结构化输出：`with_structured_output()`

#### 模块 6：LCEL 完整流程
- `RunnableSequence` 的执行流程
- `RunnableParallel` 的并行执行
- Config 传递机制
- 流式和批处理示例

**关键洞察**：
> ChatModel 支持工具调用，LLM 不支持。根据需求选择正确的抽象！

---

### [模块 7：RunnableParallel - 并行执行深度剖析](./module-07-runnable-parallel-ZH.md)
**英文版**：[Module 7: RunnableParallel Deep-Dive](./module-07-runnable-parallel-EN.md)

**核心内容**：
- 并行执行的设计思想和使用场景
- `invoke()` vs `ainvoke()` 的并行实现机制
- 线程池和异步协程的性能对比
- RAG、多模型对比等实战模式
- 嵌套并行和复杂数据流构建

**关键洞察**：
> `RunnableParallel` 所有分支接收相同输入，并发执行，返回字典结果！

---

### [模块 8：RunnableLambda - 将任意函数转换为 Runnable](./module-08-runnable-lambda-ZH.md)
**英文版**：[Module 8: RunnableLambda - Converting Functions to Runnables](./module-08-runnable-lambda-EN.md)

**核心内容**：
- 将普通 Python 函数集成到 LCEL 链中
- 同步和异步函数的处理机制
- 类型推断：从函数签名提取类型信息
- 依赖分析：自动检测嵌套 Runnable
- 递归 Runnable：动态链构建

**关键洞察**：
> `RunnableLambda` 是胶水组件，让任意 Python 函数无缝集成到 LangChain 生态！

---

### [模块 9：OutputParser - 结构化输出解析](./module-09-output-parser-ZH.md)
**英文版**：[Module 9: OutputParser - Structured Output Parsing](./module-09-output-parser-EN.md)

**核心内容**：
- OutputParser 类型层次和核心接口
- StrOutputParser、JsonOutputParser、PydanticOutputParser 详解
- 创建自定义 OutputParser
- 类型安全的数据提取
- OutputParser vs `with_structured_output()` 对比

**关键洞察**：
> OutputParser 将 LLM 输出从非结构化文本转换为类型安全的数据结构！

---

## 🎨 架构总览

```
Runnable<Input, Output>
│
├── BasePromptTemplate<dict, PromptValue>
│   ├── PromptTemplate
│   └── ChatPromptTemplate
│
├── BaseLLM<LanguageModelInput, str>
│   └── OpenAI
│
├── BaseChatModel<LanguageModelInput, BaseMessage>
│   └── ChatOpenAI
│
├── RunnableSequence
│   └── 通过 | 操作符创建
│
└── RunnableParallel
    └── 通过 dict 字面量创建
```

---

## 🚀 快速开始

### 1. 阅读顺序建议

**初学者**：
1. 模块 1 → 理解核心抽象
2. 模块 2 → 理解组合机制
3. 模块 3 → 理解第一个具体实现
4. 模块 4-6 → 理解完整生态

**有经验者**：
- 可以直接跳到感兴趣的模块
- 每个模块都包含完整的上下文

### 2. 实践项目

完成学习后，尝试这些实践项目：

**项目 1：翻译缓存系统**
```python
class TranslationCache(Runnable[dict, str]):
    def invoke(self, input: dict) -> str:
        # 检查缓存
        # 未命中则调用 LLM
        pass
```

**项目 2：RAG 系统**
```python
rag_chain = (
    RunnableParallel(
        context=retriever,
        question=RunnablePassthrough()
    )
    | prompt
    | model
    | output_parser
)
```

**项目 3：多语言翻译器**
```python
translator = RunnableParallel(
    french=prompt_fr | model,
    spanish=prompt_es | model,
    german=prompt_de | model,
)
```

---

## 📊 学习统计

- **总模块数**：9 个核心模块
- **文档数量**：18+ 个文件（中英双语）
- **代码示例**：90+ 个实际例子
- **Mermaid 图表**：25+ 个架构可视化
- **知识挑战**：50+ 个测试问题
- **可运行示例**：4 个完整示例程序

---

## 🛠️ 辅助资源

### [术语表 (GLOSSARY.md)](./GLOSSARY.md)
**Bilingual glossary** covering all core LangChain concepts:
- Runnable, RunnableSequence, RunnableParallel
- Prompts, Messages, Templates
- LLM, ChatModel, OutputParser
- Tools, Agents, RAG
- Type safety, Config propagation, Callbacks

**双语术语表**，涵盖所有核心 LangChain 概念。

---

### [常见问题 (FAQ.md)](./FAQ.md)
**Bilingual FAQ** answering 16 common questions:
- How does the `|` operator work?
- When to use PromptTemplate vs ChatPromptTemplate?
- How to debug chains?
- Performance optimization tips
- Error handling strategies

**双语常见问题**，回答 16 个常见问题。

---

### [代码示例 (examples/)](./examples/)
**Runnable example programs** (no API keys required):

| File | Topic | Description |
|------|-------|-------------|
| [01_basic_runnable.py](./examples/01_basic_runnable.py) | Runnable Interface | Core abstraction, composition with `\|` |
| [02_prompt_templates.py](./examples/02_prompt_templates.py) | Prompt Templates | PromptTemplate, ChatPromptTemplate, MessagesPlaceholder |
| [03_runnable_parallel.py](./examples/03_runnable_parallel.py) | Parallel Execution | RunnableParallel, concurrent branches |
| [04_complete_chain.py](./examples/04_complete_chain.py) | Complete Chains | LCEL chains, RAG pattern, conditional logic |

**All examples use mock components** - learn offline without API keys!

**所有示例使用模拟组件** - 无需 API 密钥即可离线学习！

See [examples/README.md](./examples/README.md) for usage instructions.

---

## 🤝 贡献指南

如果您发现文档中的错误或有改进建议，欢迎：
1. 提交 Issue
2. 创建 Pull Request
3. 分享您的学习心得

---

## 📝 许可证

本文档系列遵循 MIT 许可证。

---

## 🙏 致谢

感谢 LangChain 团队创建了如此优秀的框架，以及开源社区的持续贡献。

---

## 📚 延伸阅读

- [LangChain 官方文档](https://python.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [LangSmith 文档](https://docs.smith.langchain.com/)

---

**Happy Learning! 🎉**

---

## 📌 快速导航

### 核心模块 | Core Modules

| 模块 | 中文 | English | 主题 |
|------|------|---------|------|
| 1 | [链接](./module-01-runnable-core-ZH.md) | [Link](./module-01-runnable-core-EN.md) | Runnable 核心 |
| 2 | [链接](./module-02-runnable-sequence-ZH.md) | [Link](./module-02-runnable-sequence-EN.md) | 序列组合 |
| 3 | [链接](./module-03-prompts-implementation-ZH.md) | [Link](./module-03-prompts-implementation-EN.md) | Prompts 实现 |
| 4-6 | [链接](./module-04-05-06-summary-ZH.md) | [Link](./module-04-05-06-summary-EN.md) | 完整流程 |
| 7 | [链接](./module-07-runnable-parallel-ZH.md) | [Link](./module-07-runnable-parallel-EN.md) | 并行执行 |
| 8 | [链接](./module-08-runnable-lambda-ZH.md) | [Link](./module-08-runnable-lambda-EN.md) | 函数集成 |
| 9 | [链接](./module-09-output-parser-ZH.md) | [Link](./module-09-output-parser-EN.md) | 输出解析 |

### 辅助资源 | Supporting Resources

| 资源 | 链接 | 说明 |
|------|------|------|
| 术语表 | [GLOSSARY.md](./GLOSSARY.md) | 双语术语表，涵盖所有核心概念 |
| 常见问题 | [FAQ.md](./FAQ.md) | 16+ 个常见问题解答（双语） |
| 代码示例 | [examples/](./examples/) | 4 个可运行示例程序 |
| 示例说明 | [examples/README.md](./examples/README.md) | 示例使用指南 |
