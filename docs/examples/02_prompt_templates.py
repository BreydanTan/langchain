"""
Example 2: Prompt Templates
示例 2：提示模板

This example demonstrates how to use PromptTemplate and ChatPromptTemplate.
本示例演示如何使用 PromptTemplate 和 ChatPromptTemplate。

Run: python docs/examples/02_prompt_templates.py
"""

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import HumanMessage, AIMessage


def example_1_basic_prompt_template():
    """Basic string prompt template.

    基础字符串提示模板。
    """
    print("\n" + "=" * 60)
    print("Example 1: PromptTemplate (String-based)")
    print("示例 1：PromptTemplate（基于字符串）")
    print("=" * 60)

    # Create template with variables
    # 创建带变量的模板
    prompt = PromptTemplate.from_template(
        "Tell me a {adjective} joke about {topic}."
    )

    # Method 1: format() - returns string
    # 方法 1：format() - 返回字符串
    result_str = prompt.format(adjective="funny", topic="programming")
    print(f"\nformat() output (str):\n{result_str}")

    # Method 2: invoke() - returns PromptValue (Runnable interface)
    # 方法 2：invoke() - 返回 PromptValue（Runnable 接口）
    result_prompt = prompt.invoke({"adjective": "funny", "topic": "programming"})
    print(f"\ninvoke() output type: {type(result_prompt)}")
    print(f"to_string(): {result_prompt.to_string()}")


def example_2_chat_prompt_template():
    """Chat-based prompt template with multiple message types.

    基于聊天的提示模板，支持多种消息类型。
    """
    print("\n" + "=" * 60)
    print("Example 2: ChatPromptTemplate (Message-based)")
    print("示例 2：ChatPromptTemplate（基于消息）")
    print("=" * 60)

    # Create chat template with system and human messages
    # 创建包含系统消息和用户消息的聊天模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a {role}. Respond in {language}."),
        ("human", "{input}"),
    ])

    # Invoke the template
    # 调用模板
    result = prompt.invoke({
        "role": "helpful chef",
        "language": "English",
        "input": "How do I make pasta?"
    })

    print(f"\nGenerated messages:")
    for msg in result.to_messages():
        print(f"  - {msg.__class__.__name__}: {msg.content}")


def example_3_messages_placeholder():
    """Using MessagesPlaceholder for conversation history.

    使用 MessagesPlaceholder 处理对话历史。
    """
    print("\n" + "=" * 60)
    print("Example 3: MessagesPlaceholder (Conversation History)")
    print("示例 3：MessagesPlaceholder（对话历史）")
    print("=" * 60)

    # Template with placeholder for chat history
    # 包含聊天历史占位符的模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ])

    # Simulate conversation history
    # 模拟对话历史
    conversation_history = [
        HumanMessage(content="What's 5 + 3?"),
        AIMessage(content="5 + 3 equals 8."),
        HumanMessage(content="What about times 2?"),
        AIMessage(content="8 times 2 equals 16."),
    ]

    # Invoke with history
    # 使用历史记录调用
    result = prompt.invoke({
        "history": conversation_history,
        "question": "And divided by 4?"
    })

    print(f"\nFull conversation context ({len(result.to_messages())} messages):")
    for i, msg in enumerate(result.to_messages(), 1):
        content_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
        print(f"  {i}. {msg.__class__.__name__}: {content_preview}")


def example_4_partial_variables():
    """Using partial variables for default or lazy values.

    使用部分变量设置默认值或惰性求值。
    """
    print("\n" + "=" * 60)
    print("Example 4: Partial Variables")
    print("示例 4：部分变量")
    print("=" * 60)

    from datetime import datetime

    def get_current_time():
        """Function to get current time lazily."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create template with partial variables
    # 创建带部分变量的模板
    prompt = PromptTemplate(
        template="Current time: {time}\nUser question: {question}",
        input_variables=["question"],
        partial_variables={
            "time": get_current_time  # Function will be called on each invoke
        }
    )

    # The time function is called automatically
    # 时间函数会自动调用
    result1 = prompt.format(question="What is Python?")
    print(f"\nFirst call:\n{result1}")

    import time
    time.sleep(1)

    result2 = prompt.format(question="What is LangChain?")
    print(f"\nSecond call (1 second later):\n{result2}")


def example_5_input_validation():
    """Demonstrates automatic input validation and wrapping.

    演示自动输入验证和包装。
    """
    print("\n" + "=" * 60)
    print("Example 5: Input Validation & Auto-wrapping")
    print("示例 5：输入验证与自动包装")
    print("=" * 60)

    # Single input variable template
    # 单输入变量模板
    prompt = PromptTemplate.from_template("Translate to French: {text}")

    # Method 1: Pass as dict (standard)
    # 方法 1：作为字典传递（标准方式）
    result1 = prompt.invoke({"text": "Hello world"})
    print(f"\nDict input: {result1.to_string()}")

    # Method 2: Pass string directly (auto-wrapped)
    # 方法 2：直接传递字符串（自动包装）
    result2 = prompt.invoke("Hello world")
    print(f"String input (auto-wrapped): {result2.to_string()}")

    print("\nNote: Auto-wrapping only works with single input variable templates!")
    print("注意：自动包装仅适用于单输入变量模板！")


def main():
    print("=" * 60)
    print("Prompt Templates Examples")
    print("提示模板示例")
    print("=" * 60)

    example_1_basic_prompt_template()
    example_2_chat_prompt_template()
    example_3_messages_placeholder()
    example_4_partial_variables()
    example_5_input_validation()

    print("\n" + "=" * 60)
    print("Key Takeaways / 核心要点:")
    print("=" * 60)
    print("1. PromptTemplate: For string-based prompts")
    print("   PromptTemplate：用于字符串提示")
    print("2. ChatPromptTemplate: For structured conversations")
    print("   ChatPromptTemplate：用于结构化对话")
    print("3. MessagesPlaceholder: For dynamic history insertion")
    print("   MessagesPlaceholder：用于动态插入历史")
    print("4. Prompts are Runnables - use invoke(), batch(), etc.")
    print("   提示是 Runnable - 可使用 invoke()、batch() 等")
    print("=" * 60)


if __name__ == "__main__":
    main()
