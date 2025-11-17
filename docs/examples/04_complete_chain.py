"""
Example 4: Complete LCEL Chain (Without API Keys)
示例 4：完整的 LCEL 链（无需 API 密钥）

This example demonstrates a complete LCEL chain using mock components
to avoid requiring API keys.
本示例使用模拟组件演示完整的 LCEL 链，无需 API 密钥。

Run: python docs/examples/04_complete_chain.py
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser


class MockChatModel:
    """Mock chat model to avoid requiring API keys.

    模拟聊天模型，避免需要 API 密钥。
    """

    def invoke(self, messages):
        """Simulate LLM response."""
        # Extract the last user message
        last_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])

        # Generate mock response based on keywords
        if "joke" in last_message.lower():
            response = "Why did the programmer quit? Because they didn't get arrays!"
        elif "translate" in last_message.lower():
            response = "Bonjour le monde!"  # Mock French translation
        elif "summarize" in last_message.lower():
            response = "This is a concise summary of the content."
        else:
            response = f"I received your message: {last_message}"

        return AIMessage(content=response)

    def __or__(self, other):
        """Support pipe operator."""
        from langchain_core.runnables import RunnableSequence
        return RunnableSequence(first=self, last=other)


def example_1_simple_chain():
    """Simple prompt -> model -> parser chain.

    简单的 提示 -> 模型 -> 解析器 链。
    """
    print("\n" + "=" * 60)
    print("Example 1: Simple Chain (Prompt | Model | Parser)")
    print("示例 1：简单链（提示 | 模型 | 解析器）")
    print("=" * 60)

    # Components
    # 组件
    prompt = ChatPromptTemplate.from_template("Tell me a {adjective} joke")
    model = MockChatModel()
    parser = StrOutputParser()

    # Chain composition
    # 链组合
    chain = prompt | model | parser

    # Execute
    # 执行
    result = chain.invoke({"adjective": "programming"})
    print(f"\nInput: {{'adjective': 'programming'}}")
    print(f"Output: {result}")


def example_2_parallel_branches():
    """Chain with parallel branches.

    带并行分支的链。
    """
    print("\n" + "=" * 60)
    print("Example 2: Chain with Parallel Branches")
    print("示例 2：带并行分支的链")
    print("=" * 60)

    # Two different prompts
    # 两个不同的提示
    joke_prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
    translate_prompt = ChatPromptTemplate.from_template("Translate '{text}' to French")

    model = MockChatModel()
    parser = StrOutputParser()

    # Parallel branches
    # 并行分支
    parallel = RunnableParallel(
        joke=joke_prompt | model | parser,
        translation=translate_prompt | model | parser,
    )

    # Execute
    # 执行
    result = parallel.invoke({"topic": "Python", "text": "Hello world"})
    print(f"\nInput: {{'topic': 'Python', 'text': 'Hello world'}}")
    print(f"Output:")
    print(f"  - Joke: {result['joke']}")
    print(f"  - Translation: {result['translation']}")


def example_3_multi_stage_processing():
    """Multi-stage processing pipeline.

    多阶段处理管道。
    """
    print("\n" + "=" * 60)
    print("Example 3: Multi-stage Processing Pipeline")
    print("示例 3：多阶段处理管道")
    print("=" * 60)

    # Stage 1: Prepare input
    # 阶段 1：准备输入
    prepare_stage = RunnableLambda(
        lambda x: {
            "processed_text": x["text"].upper(),
            "word_count": len(x["text"].split()),
        }
    )

    # Stage 2: Analyze in parallel
    # 阶段 2：并行分析
    analyze_stage = RunnableParallel(
        text_info=RunnableLambda(
            lambda x: f"Text has {x['word_count']} words"
        ),
        processed=RunnableLambda(
            lambda x: f"Processed: {x['processed_text']}"
        ),
    )

    # Stage 3: Combine results
    # 阶段 3：合并结果
    combine_stage = RunnableLambda(
        lambda x: f"{x['text_info']} | {x['processed']}"
    )

    # Full pipeline
    # 完整管道
    pipeline = prepare_stage | analyze_stage | combine_stage

    # Execute
    # 执行
    result = pipeline.invoke({"text": "LangChain is awesome"})
    print(f"\nInput: {{'text': 'LangChain is awesome'}}")
    print(f"Output: {result}")


def example_4_conditional_logic():
    """Chain with conditional logic using RunnableBranch.

    使用 RunnableBranch 的条件逻辑链。
    """
    print("\n" + "=" * 60)
    print("Example 4: Conditional Logic (RunnableBranch)")
    print("示例 4：条件逻辑（RunnableBranch）")
    print("=" * 60)

    from langchain_core.runnables import RunnableBranch

    # Define conditions and handlers
    # 定义条件和处理器
    branch = RunnableBranch(
        # Condition 1: short text
        # 条件 1：短文本
        (
            lambda x: len(x["text"]) < 10,
            RunnableLambda(lambda x: f"Short text: {x['text']}")
        ),
        # Condition 2: medium text
        # 条件 2：中等文本
        (
            lambda x: len(x["text"]) < 50,
            RunnableLambda(lambda x: f"Medium text: {x['text'][:20]}...")
        ),
        # Default: long text
        # 默认：长文本
        RunnableLambda(lambda x: f"Long text: {x['text'][:30]}..."),
    )

    # Test with different lengths
    # 测试不同长度
    test_cases = [
        {"text": "Hi"},
        {"text": "Hello, this is a test"},
        {"text": "This is a very long text that exceeds the medium threshold and will be truncated"},
    ]

    for i, test in enumerate(test_cases, 1):
        result = branch.invoke(test)
        print(f"\nTest {i}: Length={len(test['text'])}")
        print(f"Output: {result}")


def example_5_with_context():
    """RAG-style chain with context retrieval (mocked).

    RAG 风格的链，包含上下文检索（模拟）。
    """
    print("\n" + "=" * 60)
    print("Example 5: RAG-style Chain (with Context)")
    print("示例 5：RAG 风格的链（包含上下文）")
    print("=" * 60)

    # Mock retriever
    # 模拟检索器
    def mock_retriever(question):
        """Simulate document retrieval."""
        docs = {
            "langchain": "LangChain is a framework for building LLM applications.",
            "python": "Python is a high-level programming language.",
            "default": "No specific information found.",
        }
        for key, value in docs.items():
            if key in question.lower():
                return value
        return docs["default"]

    # Build RAG chain
    # 构建 RAG 链
    rag_chain = (
        # Step 1: Retrieve context and prepare input
        # 步骤 1：检索上下文并准备输入
        RunnableParallel(
            context=RunnableLambda(lambda x: mock_retriever(x["question"])),
            question=RunnableLambda(lambda x: x["question"]),
        )
        # Step 2: Create prompt with context
        # 步骤 2：使用上下文创建提示
        | ChatPromptTemplate.from_template(
            "Context: {context}\n\nQuestion: {question}\n\nAnswer based on context:"
        )
        # Step 3: Generate response
        # 步骤 3：生成响应
        | MockChatModel()
        # Step 4: Parse output
        # 步骤 4：解析输出
        | StrOutputParser()
    )

    # Execute
    # 执行
    result = rag_chain.invoke({"question": "What is LangChain?"})
    print(f"\nQuestion: What is LangChain?")
    print(f"Answer: {result}")


def main():
    print("=" * 60)
    print("Complete LCEL Chain Examples")
    print("完整的 LCEL 链示例")
    print("=" * 60)
    print("\nNote: Using mock components - no API keys required!")
    print("注意：使用模拟组件 - 无需 API 密钥！")

    example_1_simple_chain()
    example_2_parallel_branches()
    example_3_multi_stage_processing()
    example_4_conditional_logic()
    example_5_with_context()

    print("\n" + "=" * 60)
    print("Key Takeaways / 核心要点:")
    print("=" * 60)
    print("1. Use | to compose sequential operations")
    print("   使用 | 组合顺序操作")
    print("2. Use {} or RunnableParallel for parallel execution")
    print("   使用 {} 或 RunnableParallel 进行并行执行")
    print("3. RunnableBranch enables conditional logic")
    print("   RunnableBranch 启用条件逻辑")
    print("4. All chains are Runnables (invoke, batch, stream, etc.)")
    print("   所有链都是 Runnable（invoke、batch、stream 等）")
    print("5. Chains are composable - can be nested and reused")
    print("   链是可组合的 - 可以嵌套和重用")
    print("=" * 60)


if __name__ == "__main__":
    main()
