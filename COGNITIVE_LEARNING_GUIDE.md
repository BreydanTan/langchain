# 🧠 认知学习引擎使用指南 / Cognitive Learning Engine Guide

[English version below](#english-version)

---

## 中文版本

### 📖 这是什么？

这是一套基于**认知科学**设计的 LangChain 学习材料，旨在将你从"新手"培养成"专家"。

### 🎯 学习原则

本课程基于以下认知科学原则设计：

1. **认知负荷理论 (CLT)** - 最小化外在负荷，使用"少即是多"和双重编码（文本+图表）
2. **专长反转效应** - 使用直接指导和集中练习（而非探究式学习）
3. **主动学习与生成** - 每个模块包含"知识提取挑战"来强化记忆
4. **上下文持久化** - 使用状态文件在多次对话中保持学习进度

### 📚 文件说明

| 文件 | 用途 | 语言 |
|------|------|------|
| `PROJECT_COGNITIVE_STATE.md` | 学习进度追踪器 | 中文 |
| `PROJECT_COGNITIVE_STATE_EN.md` | 学习进度追踪器 | English |
| `LEARNING_MODULES_COMPLETE.md` | 完整的 8 个学习模块 | 中文 |
| `LEARNING_MODULES_COMPLETE_EN.md` | 完整的 8 个学习模块 | English |

### 🚀 如何使用

#### 方式 1：自学模式（推荐）

1. 打开 `LEARNING_MODULES_COMPLETE.md`（或英文版 `LEARNING_MODULES_COMPLETE_EN.md`）
2. 按顺序阅读每个模块
3. **重要：** 每个模块末尾有"知识提取挑战"
   - 先尝试回答（不要看下一模块！）
   - 在下一个模块开头查看答案
   - 这种"延迟反馈"会增强记忆

#### 方式 2：AI 辅助模式

1. 将 `PROJECT_COGNITIVE_STATE.md` 的内容复制到新的 AI 对话中
2. AI 会自动解析你的学习进度
3. AI 会继续教学并提问
4. 每次对话结束时，AI 会更新状态文件

### 📋 学习路径概览

```
模块 1: 项目架构与核心理念 [✅ 已完成]
  └─ Monorepo 结构、三大设计原则

模块 2: 消息系统 (Messages) [✅ 已完成]
  └─ HumanMessage、AIMessage、SystemMessage

模块 3: 提示工程 (Prompts) [✅ 已完成]
  └─ PromptTemplate、ChatPromptTemplate、MessagesPlaceholder

模块 4: 核心抽象 Runnable [✅ 已完成]
  └─ invoke/batch/stream、组合原语

模块 5: 聊天模型 (Chat Models) [✅ 已完成]
  └─ BaseChatModel、工具调用、结构化输出

模块 6: 链式组合 (LCEL) [✅ 已完成]
  └─ Pipe 操作符、并行组合、RAG 链

模块 7: 工具与代理 (Tools & Agents) [✅ 已完成]
  └─ @tool 装饰器、Agent 循环、LangGraph

模块 8: 高级特性 [✅ 已完成]
  └─ Callbacks、Streaming、Memory、Caching
```

### 💡 学习建议

1. **按顺序学习** - 模块设计遵循"集中练习"原则，从简单到复杂
2. **主动思考** - 在看答案前先尝试回答挑战问题
3. **实践为王** - 每学完 2-3 个模块，尝试构建一个小项目
4. **定期复习** - 使用"知识提取挑战"定期自测

### 🎓 推荐实践项目

完成所有模块后，尝试构建以下项目：

- [ ] 个人知识库问答系统（RAG）
- [ ] 多模态聊天机器人（支持图片）
- [ ] 自动化研究助手（带搜索和总结）
- [ ] 代码分析工具（使用 AST 和 LLM）

### 🔗 相关资源

- [LangChain 官方文档](https://docs.langchain.com/oss/python/langchain/overview)
- [API 参考](https://reference.langchain.com/python)
- [核心代码位置](./libs/core/langchain_core/)

---

## English Version

### 📖 What is This?

This is a set of LangChain learning materials designed based on **cognitive science** principles, aiming to develop you from a "novice" to an "expert".

### 🎯 Learning Principles

This curriculum is designed based on the following cognitive science principles:

1. **Cognitive Load Theory (CLT)** - Minimize extraneous load using "less is more" and dual coding (text + diagrams)
2. **Expertise Reversal Effect** - Use direct instruction and blocked practice (not inquiry-based learning)
3. **Active Learning & Generation** - Each module includes "knowledge retrieval challenges" to reinforce memory
4. **Context Persistence** - Use state files to maintain learning progress across multiple conversations

### 📚 File Descriptions

| File | Purpose | Language |
|------|---------|----------|
| `PROJECT_COGNITIVE_STATE.md` | Learning progress tracker | 中文 |
| `PROJECT_COGNITIVE_STATE_EN.md` | Learning progress tracker | English |
| `LEARNING_MODULES_COMPLETE.md` | Complete 8 learning modules | 中文 |
| `LEARNING_MODULES_COMPLETE_EN.md` | Complete 8 learning modules | English |

### 🚀 How to Use

#### Method 1: Self-Study Mode (Recommended)

1. Open `LEARNING_MODULES_COMPLETE_EN.md` (or Chinese version `LEARNING_MODULES_COMPLETE.md`)
2. Read each module in sequence
3. **Important:** Each module ends with "Knowledge Challenges"
   - Try to answer first (don't peek at the next module!)
   - Check answers at the beginning of the next module
   - This "delayed feedback" enhances memory retention

#### Method 2: AI-Assisted Mode

1. Copy the contents of `PROJECT_COGNITIVE_STATE_EN.md` into a new AI conversation
2. AI will automatically parse your learning progress
3. AI will continue teaching and asking questions
4. At the end of each conversation, AI will update the state file

### 📋 Learning Path Overview

```
Module 1: Architecture & Core Concepts [✅ Complete]
  └─ Monorepo structure, three design principles

Module 2: Message System [✅ Complete]
  └─ HumanMessage, AIMessage, SystemMessage

Module 3: Prompt Engineering [✅ Complete]
  └─ PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

Module 4: Core Runnable Abstraction [✅ Complete]
  └─ invoke/batch/stream, composition primitives

Module 5: Chat Models [✅ Complete]
  └─ BaseChatModel, tool calling, structured output

Module 6: Chain Composition (LCEL) [✅ Complete]
  └─ Pipe operator, parallel composition, RAG chains

Module 7: Tools & Agents [✅ Complete]
  └─ @tool decorator, agent loops, LangGraph

Module 8: Advanced Features [✅ Complete]
  └─ Callbacks, Streaming, Memory, Caching
```

### 💡 Learning Tips

1. **Sequential Learning** - Modules are designed with "blocked practice" principle, from simple to complex
2. **Active Thinking** - Try to answer challenge questions before looking at answers
3. **Practice Makes Perfect** - After every 2-3 modules, try building a small project
4. **Regular Review** - Use "Knowledge Retrieval Challenges" for periodic self-testing

### 🎓 Recommended Practice Projects

After completing all modules, try building:

- [ ] Personal knowledge base Q&A system (RAG)
- [ ] Multimodal chatbot (supports images)
- [ ] Automated research assistant (with search and summarization)
- [ ] Code analysis tool (using AST and LLM)

### 🔗 Related Resources

- [LangChain Official Docs](https://docs.langchain.com/oss/python/langchain/overview)
- [API Reference](https://reference.langchain.com/python)
- [Core Code Location](./libs/core/langchain_core/)

---

## 🤝 Contributing

If you find errors or have suggestions for improvement, please open an issue or submit a PR.

## 📄 License

This learning material follows the same license as the LangChain project (MIT).
