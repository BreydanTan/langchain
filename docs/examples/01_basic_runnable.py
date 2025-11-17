"""
Example 1: Basic Runnable Interface
示例 1：基础 Runnable 接口

This example demonstrates the core Runnable interface with a simple custom implementation.
本示例演示如何使用简单的自定义实现来理解核心 Runnable 接口。

Run: python docs/examples/01_basic_runnable.py
"""

from typing import Any
from langchain_core.runnables import Runnable, RunnableConfig


class DoubleRunnable(Runnable[int, int]):
    """A simple Runnable that doubles the input number.

    一个简单的 Runnable，将输入数字翻倍。
    """

    def invoke(self, input: int, config: RunnableConfig | None = None) -> int:
        """The core abstract method - must be implemented.

        核心抽象方法 - 必须实现。
        """
        print(f"Input: {input}")
        result = input * 2
        print(f"Output: {result}")
        return result


class AddTenRunnable(Runnable[int, int]):
    """A simple Runnable that adds 10 to the input.

    一个简单的 Runnable，给输入加 10。
    """

    def invoke(self, input: int, config: RunnableConfig | None = None) -> int:
        print(f"Adding 10 to {input}")
        result = input + 10
        print(f"Result: {result}")
        return result


def main():
    print("=" * 60)
    print("Example 1: Basic Runnable Interface")
    print("示例 1：基础 Runnable 接口")
    print("=" * 60)

    # Create instances
    # 创建实例
    doubler = DoubleRunnable()
    adder = AddTenRunnable()

    print("\n1. Single invocation / 单次调用:")
    print("-" * 40)
    result = doubler.invoke(5)
    print(f"Final result: {result}\n")

    print("\n2. Composing with pipe operator / 使用管道操作符组合:")
    print("-" * 40)
    # Chain: input -> double -> add 10
    # 链：输入 -> 翻倍 -> 加 10
    chain = doubler | adder
    result = chain.invoke(5)  # (5 * 2) + 10 = 20
    print(f"Chain result: {result}\n")

    print("\n3. Batch processing / 批量处理:")
    print("-" * 40)
    results = doubler.batch([1, 2, 3, 4, 5])
    print(f"Batch results: {results}\n")

    print("\n4. Async invocation / 异步调用:")
    print("-" * 40)
    import asyncio

    async def async_example():
        result = await doubler.ainvoke(7)
        print(f"Async result: {result}")

    asyncio.run(async_example())

    print("\n" + "=" * 60)
    print("Key Takeaways / 核心要点:")
    print("=" * 60)
    print("1. Only invoke() is required - other methods have defaults")
    print("   只需实现 invoke() - 其他方法有默认实现")
    print("2. Use | operator to compose Runnables")
    print("   使用 | 操作符组合 Runnable")
    print("3. Composition creates a new Runnable (RunnableSequence)")
    print("   组合会创建新的 Runnable (RunnableSequence)")
    print("=" * 60)


if __name__ == "__main__":
    main()
