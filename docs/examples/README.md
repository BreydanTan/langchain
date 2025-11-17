# 📝 LangChain Code Examples | LangChain 代码示例

This directory contains runnable examples demonstrating core LangChain concepts.

本目录包含演示 LangChain 核心概念的可运行示例。

## 🎯 Examples Overview | 示例概览

| File | Topic | Description |
|------|-------|-------------|
| `01_basic_runnable.py` | Runnable Interface<br>Runnable 接口 | Core Runnable abstraction, composition with `\|`<br>核心 Runnable 抽象，使用 `\|` 组合 |
| `02_prompt_templates.py` | Prompt Templates<br>提示模板 | PromptTemplate, ChatPromptTemplate, MessagesPlaceholder<br>提示模板、聊天提示模板、消息占位符 |
| `03_runnable_parallel.py` | Parallel Execution<br>并行执行 | RunnableParallel, concurrent branches<br>并行 Runnable，并发分支 |
| `04_complete_chain.py` | Complete Chains<br>完整链 | LCEL chains, RAG pattern, conditional logic<br>LCEL 链、RAG 模式、条件逻辑 |

## 🚀 How to Run | 如何运行

### Prerequisites | 前置要求

```bash
# Navigate to the project root
# 导航到项目根目录
cd /home/user/langchain

# Install dependencies (if not already installed)
# 安装依赖（如果尚未安装）
pip install langchain-core
```

### Running Examples | 运行示例

```bash
# Run individual examples
# 运行单个示例
python docs/examples/01_basic_runnable.py
python docs/examples/02_prompt_templates.py
python docs/examples/03_runnable_parallel.py
python docs/examples/04_complete_chain.py

# Or run all examples
# 或运行所有示例
for example in docs/examples/*.py; do
    echo "Running $example..."
    python "$example"
    echo ""
done
```

## 📚 Learning Path | 学习路径

**Recommended order for beginners:**
**建议初学者按以下顺序学习：**

1. **Start with `01_basic_runnable.py`**
   - Understand the Runnable interface
   - Learn about composition with `|`
   - See batch and async operations

2. **Move to `02_prompt_templates.py`**
   - Learn PromptTemplate and ChatPromptTemplate
   - Understand MessagesPlaceholder
   - See input validation

3. **Explore `03_runnable_parallel.py`**
   - Understand parallel execution
   - Learn dict syntax shorthand
   - See nested parallel structures

4. **Master `04_complete_chain.py`**
   - Combine all concepts
   - Build complex chains
   - See real-world patterns (RAG, conditional logic)

## 💡 Key Concepts Covered | 涵盖的核心概念

### 1. Runnable Interface | Runnable 接口
- `invoke()` - Single execution
- `batch()` - Batch processing
- `stream()` - Streaming output
- `ainvoke()` - Async execution

### 2. Composition Patterns | 组合模式
- Sequential: `a | b | c`
- Parallel: `{key1: a, key2: b}`
- Conditional: `RunnableBranch`

### 3. Prompt Engineering | 提示工程
- String templates with variables
- Chat message structures
- Conversation history handling
- Partial variables and lazy evaluation

### 4. Advanced Patterns | 高级模式
- RAG (Retrieval-Augmented Generation)
- Multi-stage processing pipelines
- Conditional branching
- Nested parallel execution

## 🔧 No API Keys Required | 无需 API 密钥

All examples use **mock components** to demonstrate concepts without requiring:
所有示例使用**模拟组件**演示概念，无需：

- ❌ OpenAI API keys
- ❌ Anthropic API keys
- ❌ Internet connection
- ❌ External services

This allows you to learn LangChain's architecture and patterns **offline**.
这使你可以**离线**学习 LangChain 的架构和模式。

## 📖 Related Documentation | 相关文档

For deep-dive source code analysis, see the main learning series:
有关深入的源码分析，请参阅主学习系列：

- [Module 1: Runnable Core](../module-01-runnable-core-EN.md)
- [Module 2: RunnableSequence](../module-02-runnable-sequence-EN.md)
- [Module 3: Prompts Implementation](../module-03-prompts-implementation-EN.md)
- [Module 4-6: Complete Flow](../module-04-05-06-summary-EN.md)

## 🤝 Contributing | 贡献

Feel free to add more examples! Follow these guidelines:
欢迎添加更多示例！请遵循以下准则：

1. **No API keys** - Use mock components
2. **Bilingual** - Add Chinese and English comments
3. **Self-contained** - Each example should run independently
4. **Educational** - Focus on teaching concepts, not production code
5. **Well-commented** - Explain the "why", not just the "what"

## 📝 Example Template | 示例模板

```python
"""
Example N: Topic Name
示例 N：主题名称

Brief description in English.
简短的中文描述。

Run: python docs/examples/0N_example.py
"""

def example_1():
    """Demonstration of concept.

    概念演示。
    """
    print("Example output")

def main():
    print("=" * 60)
    print("Example Title")
    print("示例标题")
    print("=" * 60)

    example_1()

    print("\nKey Takeaways / 核心要点:")
    print("1. Point one")
    print("2. Point two")

if __name__ == "__main__":
    main()
```

---

**Happy Learning! | 学习愉快！** 🚀
