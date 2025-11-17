"""
Example 3: RunnableParallel - Parallel Execution
示例 3：RunnableParallel - 并行执行

This example demonstrates how to use RunnableParallel to execute multiple
operations concurrently.
本示例演示如何使用 RunnableParallel 并行执行多个操作。

Run: python docs/examples/03_runnable_parallel.py
"""

from langchain_core.runnables import RunnableParallel, RunnableLambda


def example_1_basic_parallel():
    """Basic parallel execution with multiple branches.

    基础并行执行，多个分支。
    """
    print("\n" + "=" * 60)
    print("Example 1: Basic Parallel Execution")
    print("示例 1：基础并行执行")
    print("=" * 60)

    # Create parallel runnable with named branches
    # 创建带命名分支的并行 runnable
    parallel = RunnableParallel(
        doubled=RunnableLambda(lambda x: x * 2),
        tripled=RunnableLambda(lambda x: x * 3),
        squared=RunnableLambda(lambda x: x ** 2),
    )

    # All branches receive the same input
    # 所有分支接收相同的输入
    result = parallel.invoke(5)
    print(f"\nInput: 5")
    print(f"Output: {result}")
    print(f"  - doubled: {result['doubled']}")
    print(f"  - tripled: {result['tripled']}")
    print(f"  - squared: {result['squared']}")


def example_2_dict_syntax():
    """Using dict syntax for parallel execution (syntactic sugar).

    使用字典语法进行并行执行（语法糖）。
    """
    print("\n" + "=" * 60)
    print("Example 2: Dict Syntax (Syntactic Sugar)")
    print("示例 2：字典语法（语法糖）")
    print("=" * 60)

    # Dict syntax automatically creates RunnableParallel
    # 字典语法会自动创建 RunnableParallel
    parallel = {
        "add_10": RunnableLambda(lambda x: x + 10),
        "multiply_5": RunnableLambda(lambda x: x * 5),
    }

    result = parallel.invoke(3)
    print(f"\nInput: 3")
    print(f"Output: {result}")


def example_3_parallel_in_chain():
    """Using parallel execution within a larger chain.

    在更大的链中使用并行执行。
    """
    print("\n" + "=" * 60)
    print("Example 3: Parallel Execution in Chain")
    print("示例 3：链中的并行执行")
    print("=" * 60)

    # Step 1: Parallel processing
    # 步骤 1：并行处理
    parallel_step = RunnableParallel(
        sum_result=RunnableLambda(lambda x: x["a"] + x["b"]),
        product_result=RunnableLambda(lambda x: x["a"] * x["b"]),
    )

    # Step 2: Combine results
    # 步骤 2：合并结果
    combine_step = RunnableLambda(
        lambda x: f"Sum: {x['sum_result']}, Product: {x['product_result']}"
    )

    # Create chain: parallel -> combine
    # 创建链：并行 -> 合并
    chain = parallel_step | combine_step

    result = chain.invoke({"a": 3, "b": 4})
    print(f"\nInput: {{'a': 3, 'b': 4}}")
    print(f"Output: {result}")


def example_4_nested_parallel():
    """Nested parallel execution.

    嵌套的并行执行。
    """
    print("\n" + "=" * 60)
    print("Example 4: Nested Parallel Execution")
    print("示例 4：嵌套并行执行")
    print("=" * 60)

    # Inner parallel: arithmetic operations
    # 内层并行：算术运算
    arithmetic_ops = RunnableParallel(
        add=RunnableLambda(lambda x: x + 10),
        multiply=RunnableLambda(lambda x: x * 2),
    )

    # Outer parallel: different transformations
    # 外层并行：不同的转换
    outer_parallel = RunnableParallel(
        arithmetic=arithmetic_ops,
        power=RunnableLambda(lambda x: x ** 2),
        negative=RunnableLambda(lambda x: -x),
    )

    result = outer_parallel.invoke(5)
    print(f"\nInput: 5")
    print(f"Output structure: {result}")
    print(f"  - arithmetic.add: {result['arithmetic']['add']}")
    print(f"  - arithmetic.multiply: {result['arithmetic']['multiply']}")
    print(f"  - power: {result['power']}")
    print(f"  - negative: {result['negative']}")


def example_5_passthrough():
    """Using RunnablePassthrough to preserve original input.

    使用 RunnablePassthrough 保留原始输入。
    """
    print("\n" + "=" * 60)
    print("Example 5: RunnablePassthrough")
    print("示例 5：RunnablePassthrough")
    print("=" * 60)

    from langchain_core.runnables import RunnablePassthrough

    # Parallel: process and preserve original
    # 并行：处理并保留原始值
    parallel = RunnableParallel(
        original=RunnablePassthrough(),
        doubled=RunnableLambda(lambda x: x * 2),
        info=RunnableLambda(lambda x: f"The number is {x}"),
    )

    result = parallel.invoke(7)
    print(f"\nInput: 7")
    print(f"Output: {result}")


def example_6_real_world_scenario():
    """Real-world scenario: Multi-stage data processing.

    真实场景：多阶段数据处理。
    """
    print("\n" + "=" * 60)
    print("Example 6: Real-world Scenario - Data Analysis")
    print("示例 6：真实场景 - 数据分析")
    print("=" * 60)

    def calculate_statistics(numbers):
        """Calculate basic statistics."""
        return {
            "mean": sum(numbers) / len(numbers),
            "max": max(numbers),
            "min": min(numbers),
        }

    def categorize_values(numbers):
        """Categorize values."""
        return {
            "positive": [n for n in numbers if n > 0],
            "negative": [n for n in numbers if n < 0],
            "zero": [n for n in numbers if n == 0],
        }

    def count_items(numbers):
        """Count total items."""
        return {"total_count": len(numbers)}

    # Parallel analysis pipeline
    # 并行分析管道
    analysis_pipeline = RunnableParallel(
        statistics=RunnableLambda(calculate_statistics),
        categories=RunnableLambda(categorize_values),
        count=RunnableLambda(count_items),
    )

    # Input data
    # 输入数据
    data = [5, -3, 8, 0, -1, 12, 7]

    result = analysis_pipeline.invoke(data)
    print(f"\nInput data: {data}")
    print(f"\nAnalysis results:")
    print(f"  Statistics: {result['statistics']}")
    print(f"  Categories: {result['categories']}")
    print(f"  Count: {result['count']}")


def main():
    print("=" * 60)
    print("RunnableParallel Examples")
    print("RunnableParallel 示例")
    print("=" * 60)

    example_1_basic_parallel()
    example_2_dict_syntax()
    example_3_parallel_in_chain()
    example_4_nested_parallel()
    example_5_passthrough()
    example_6_real_world_scenario()

    print("\n" + "=" * 60)
    print("Key Takeaways / 核心要点:")
    print("=" * 60)
    print("1. RunnableParallel runs branches concurrently")
    print("   RunnableParallel 并发运行分支")
    print("2. All branches receive the SAME input")
    print("   所有分支接收相同的输入")
    print("3. Output is a dict with branch names as keys")
    print("   输出是以分支名为键的字典")
    print("4. Use {} dict syntax as shorthand")
    print("   使用 {} 字典语法作为简写")
    print("5. Can be nested and combined in chains")
    print("   可以嵌套并在链中组合")
    print("=" * 60)


if __name__ == "__main__":
    main()
