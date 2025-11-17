# 📚 模块 2：`Runnable` 的组合 - RunnableSequence

## 🎯 学习目标

在本模块结束时，您将能够：
1. **理解** `RunnableSequence` 的内部结构（first/middle/last）
2. **解释** 链式调用是如何在 `invoke` 中实现的
3. **分析** 类型推导机制（为什么 `A | B | C` 的类型是正确的）
4. **预测** `batch` 方法如何智能地批处理整个序列

---

## 📁 文件上下文

**文件路径：** `libs/core/langchain_core/runnables/base.py`
**关键类：** `RunnableSequence` (第 2789 行开始)
**在架构中的位置：** LangChain 最重要的**组合原语**，几乎每个链都用到它

---

## 🧩 第一部分：为什么需要 `RunnableSequence`？（设计动机）

### 回顾模块1的知识

在模块 1 中，我们学到了 `|` 操作符会创建一个 `RunnableSequence`：

```python
# 当你写：
chain = prompt | model | parser

# Python 调用：
temp = prompt.__or__(model)      # 返回 RunnableSequence
chain = temp.__or__(parser)      # 返回 RunnableSequence
```

### 核心问题：`RunnableSequence` 如何实现 `invoke`？

```python
# 用户代码：
result = chain.invoke("Tell me a joke")

# 内部需要做什么？
# 1. prompt.invoke("Tell me a joke") → PromptValue
# 2. model.invoke(PromptValue) → AIMessage
# 3. parser.invoke(AIMessage) → str

# 关键挑战：如何自动传递中间结果？
```

**LangChain 的解决方案：** `RunnableSequence` 本身也是一个 `Runnable`，它的 `invoke` 方法实现了**自动的链式调用**。

---

## 📐 第二部分：数据结构设计（first/middle/last）

让我们看看 `RunnableSequence` 的类定义：

```python
# libs/core/langchain_core/runnables/base.py:2789-2881
class RunnableSequence(RunnableSerializable[Input, Output]):
    """Sequence of `Runnable` objects, where the output of one is the input of the next."""

    # 关键字段：
    first: Runnable[Input, Any]
    """The first `Runnable` in the sequence."""

    middle: list[Runnable[Any, Any]] = Field(default_factory=list)
    """The middle `Runnable` in the sequence."""

    last: Runnable[Any, Output]
    """The last `Runnable` in the sequence."""
```

### 设计哲学深度解析

**为什么不直接用一个 `list[Runnable]`？**

```python
# ❌ 简单但类型不安全的设计：
class RunnableSequence:
    steps: list[Runnable[Any, Any]]  # 丢失了类型信息！

# ✅ LangChain 的设计：
class RunnableSequence(RunnableSerializable[Input, Output]):
    first: Runnable[Input, Any]      # 知道输入类型是 Input
    middle: list[Runnable[Any, Any]]
    last: Runnable[Any, Output]      # 知道输出类型是 Output
```

**关键洞察：**

1. **`first` 字段保留了输入类型 `Input`**
   - 这样 `RunnableSequence[str, int]` 就知道它接受 `str` 输入

2. **`last` 字段保留了输出类型 `Output`**
   - 这样 `RunnableSequence[str, int]` 就知道它产生 `int` 输出

3. **`middle` 的类型是 `Any → Any`**
   - 因为中间步骤的类型在编译时无法确定
   - 但在运行时，类型会自然匹配（前一个的输出是后一个的输入）

### 类型推导的魔法

```python
# libs/core/langchain_core/runnables/base.py:2954-2963
@property
def InputType(self) -> type[Input]:
    """The type of the input to the `Runnable`."""
    return self.first.InputType  # 直接返回第一个步骤的输入类型

@property
def OutputType(self) -> type[Output]:
    """The type of the output of the `Runnable`."""
    return self.last.OutputType  # 直接返回最后一个步骤的输出类型
```

**示例：**

```python
A: Runnable[str, int]        # 字符串 → 整数
B: Runnable[int, float]      # 整数 → 浮点数
C: Runnable[float, bool]     # 浮点数 → 布尔值

sequence = A | B | C
# sequence 的类型：RunnableSequence[str, bool]
# 因为：
#   - first = A，InputType = str
#   - middle = [B]
#   - last = C，OutputType = bool
```

---

## 🔍 第三部分：构造函数的智能（扁平化优化）

让我们看看 `RunnableSequence` 的 `__init__` 方法：

```python
# libs/core/langchain_core/runnables/base.py:2883-2922
def __init__(
    self,
    *steps: RunnableLike,
    name: str | None = None,
    first: Runnable[Any, Any] | None = None,
    middle: list[Runnable[Any, Any]] | None = None,
    last: Runnable[Any, Any] | None = None,
) -> None:
    """Create a new `RunnableSequence`."""
    steps_flat: list[Runnable] = []
    if not steps and first is not None and last is not None:
        steps_flat = [first] + (middle or []) + [last]
    for step in steps:
        if isinstance(step, RunnableSequence):
            steps_flat.extend(step.steps)  # 关键：扁平化嵌套的序列！
        else:
            steps_flat.append(coerce_to_runnable(step))
    if len(steps_flat) < 2:
        raise ValueError("RunnableSequence must have at least 2 steps")
    super().__init__(
        first=steps_flat[0],
        middle=list(steps_flat[1:-1]),
        last=steps_flat[-1],
        name=name,
    )
```

### 设计哲学：扁平化优化

**为什么要特殊处理嵌套的 `RunnableSequence`？**

```python
# 没有扁平化：
A = runnable1 | runnable2           # RunnableSequence([r1, r2])
B = runnable3 | runnable4           # RunnableSequence([r3, r4])
C = A | B                            # RunnableSequence([Sequence([r1,r2]), Sequence([r3,r4])])
# 调用 C.invoke() 时：
#   → 调用 Sequence([r1,r2]).invoke()
#     → 调用 r1.invoke()，然后 r2.invoke()
#   → 调用 Sequence([r3,r4]).invoke()
#     → 调用 r3.invoke()，然后 r4.invoke()
# 这里有额外的嵌套层次！

# 有扁平化：
C = A | B                            # RunnableSequence([r1, r2, r3, r4])
# 调用 C.invoke() 时：
#   → 直接调用 r1, r2, r3, r4 的 invoke()
# 没有额外的嵌套！
```

**关键洞察：**
> 扁平化避免了不必要的嵌套，提高了性能并简化了调试追踪。

---

## ⚙️ 第四部分：`invoke` 的实现（链式调用的核心）

这是 `RunnableSequence` 最核心的方法：

```python
# libs/core/langchain_core/runnables/base.py:3103-3136
@override
def invoke(
    self, input: Input, config: RunnableConfig | None = None, **kwargs: Any
) -> Output:
    # 设置回调和上下文
    config = ensure_config(config)
    callback_manager = get_callback_manager_for_config(config)

    # 启动根运行（root run）
    run_manager = callback_manager.on_chain_start(
        None,
        input,
        name=config.get("run_name") or self.get_name(),
        run_id=config.pop("run_id", None),
    )
    input_ = input  # 当前的中间结果

    # 依次调用所有步骤
    try:
        for i, step in enumerate(self.steps):
            # 将每个步骤标记为子运行（child run）
            config = patch_config(
                config, callbacks=run_manager.get_child(f"seq:step:{i + 1}")
            )
            with set_config_context(config) as context:
                if i == 0:
                    input_ = context.run(step.invoke, input_, config, **kwargs)
                else:
                    input_ = context.run(step.invoke, input_, config)
        # 完成根运行
    except BaseException as e:
        run_manager.on_chain_error(e)
        raise
    else:
        run_manager.on_chain_end(input_)
        return cast("Output", input_)
```

### 逐行深度解析

**1. 回调管理器的设置**

```python
callback_manager = get_callback_manager_for_config(config)
run_manager = callback_manager.on_chain_start(None, input, ...)
```

**为什么需要这个？**
- 这是 LangChain 的**可观测性**系统
- 每次链的执行都会生成一个"运行记录"（run）
- 可以追踪：输入、输出、执行时间、错误等

**2. 链式调用的核心循环**

```python
input_ = input  # 初始输入
for i, step in enumerate(self.steps):
    input_ = context.run(step.invoke, input_, config)  # 关键：输出变成下一个的输入！
```

**可视化：**

```
输入: "Hello"
  ↓
step[0].invoke("Hello") → result1 = {"text": "Hello"}
  ↓
step[1].invoke(result1) → result2 = AIMessage(content="Hi there!")
  ↓
step[2].invoke(result2) → result3 = "Hi there!"
  ↓
返回: "Hi there!"
```

**3. 子运行的层次结构**

```python
config = patch_config(
    config, callbacks=run_manager.get_child(f"seq:step:{i + 1}")
)
```

**这创建了一个树形的追踪结构：**

```
RunnableSequence (root run)
├── seq:step:1 (prompt)
├── seq:step:2 (model)
└── seq:step:3 (parser)
```

在 LangSmith 中，你会看到这样的可视化！

---

## 🔗 第五部分：`__or__` 的优化实现

让我们看看 `RunnableSequence` 如何覆盖 `__or__` 操作符：

```python
# libs/core/langchain_core/runnables/base.py:3048-3073
@override
def __or__(
    self,
    other: Runnable[Any, Other] | ...,
) -> RunnableSerializable[Input, Other]:
    if isinstance(other, RunnableSequence):
        # 优化：如果 other 也是 RunnableSequence，扁平化！
        return RunnableSequence(
            self.first,
            *self.middle,
            self.last,
            other.first,
            *other.middle,
            other.last,
            name=self.name or other.name,
        )
    return RunnableSequence(
        self.first,
        *self.middle,
        self.last,
        coerce_to_runnable(other),
        name=self.name,
    )
```

### 设计哲学：智能扁平化

**示例：**

```python
seq1 = A | B | C              # RunnableSequence(first=A, middle=[B], last=C)
seq2 = D | E                  # RunnableSequence(first=D, middle=[], last=E)

combined = seq1 | seq2
# 如果没有优化，会得到：
#   RunnableSequence(first=seq1, middle=[], last=seq2)  # 嵌套！

# 有了优化，得到：
#   RunnableSequence(first=A, middle=[B, C, D], last=E)  # 扁平！
```

**关键洞察：**
> `__or__` 的优化确保无论你如何组合链，最终都是一个扁平的序列，没有不必要的嵌套层次。

---

## 📊 第六部分：架构可视化（双重编码）

让我用 Mermaid 图表展示 `RunnableSequence` 的执行流程：

```mermaid
graph TD
    Start[用户调用 chain.invoke input] --> Setup[设置回调管理器]
    Setup --> RootRun[启动根运行 root run]
    RootRun --> Loop{遍历所有 steps}

    Loop -->|i=0| Step1[step[0].invoke input]
    Step1 --> Result1[result1]

    Loop -->|i=1| Step2[step[1].invoke result1]
    Step2 --> Result2[result2]

    Loop -->|i=2| Step3[step[2].invoke result2]
    Step3 --> Result3[result3]

    Loop -->|完成| Finish[结束根运行]
    Finish --> Return[返回最终结果]

    style Loop fill:#f9f,stroke:#333,stroke-width:2px
    style Step1 fill:#bfb,stroke:#333,stroke-width:2px
    style Step2 fill:#bfb,stroke:#333,stroke-width:2px
    style Step3 fill:#bfb,stroke:#333,stroke-width:2px
```

**类型流转图：**

```mermaid
graph LR
    A[Runnable&lt;str, int&gt;] -->|first| Seq[RunnableSequence]
    B[Runnable&lt;int, float&gt;] -->|middle[0]| Seq
    C[Runnable&lt;float, bool&gt;] -->|last| Seq

    Seq -->|InputType| Input[str]
    Seq -->|OutputType| Output[bool]

    style Seq fill:#f9f,stroke:#333,stroke-width:4px
    style Input fill:#ff9,stroke:#333,stroke-width:2px
    style Output fill:#9f9,stroke:#333,stroke-width:2px
```

---

## 🧠 知识提取挑战

### 挑战 1：结构理解（生成性问题）

1. **用您自己的话解释：为什么 `RunnableSequence` 需要 `first`/`middle`/`last` 三个字段，而不是简单的 `list[Runnable]`？**

2. **`RunnableSequence` 的 `invoke` 方法的核心逻辑是什么？用一句话描述。**

3. **解释"扁平化"优化的作用。如果没有扁平化，会有什么问题？**

### 挑战 2：源码推理（分析性问题）

4. **查看这段代码：**
   ```python
   for i, step in enumerate(self.steps):
       input_ = context.run(step.invoke, input_, config)
   ```

   **问题：** 为什么 `input_` 变量会被重复赋值？这是如何实现"链式调用"的？

5. **假设我们有：**
   ```python
   A: Runnable[dict, str]
   B: Runnable[str, int]
   C: Runnable[int, list[int]]

   seq = A | B | C
   ```

   **问题：**
   - `seq.first` 是什么？
   - `seq.middle` 是什么？
   - `seq.last` 是什么？
   - `seq.InputType` 是什么？
   - `seq.OutputType` 是什么？

### 挑战 3：设计分析（深度问题）

6. **查看 `__or__` 的实现：**
   ```python
   if isinstance(other, RunnableSequence):
       return RunnableSequence(
           self.first, *self.middle, self.last,
           other.first, *other.middle, other.last,
       )
   ```

   **问题：** 假设 `seq1 = A | B | C` 和 `seq2 = D | E`，那么 `seq1 | seq2` 的内部结构是什么？绘制出 `first`/`middle`/`last` 的具体值。

7. **预测：** 如果一个步骤的输出类型与下一个步骤的输入类型不匹配会发生什么？
   ```python
   A: Runnable[str, int]
   B: Runnable[str, float]  # 注意：期望输入 str，但会收到 int！

   chain = A | B
   chain.invoke("hello")  # 会发生什么？
   ```

---

## 📝 模块 2 总结

您已经深入理解了：

✅ **数据结构设计**：`first`/`middle`/`last` 保留类型信息
✅ **类型推导**：`InputType` 来自 `first`，`OutputType` 来自 `last`
✅ **链式调用**：`invoke` 中的循环自动传递中间结果
✅ **扁平化优化**：`__init__` 和 `__or__` 避免嵌套序列
✅ **可观测性**：回调管理器创建层次化的运行追踪

**下一步：** 模块 3 将分析 `Runnable` 的具体实现 - Prompts (`prompts/base.py`)
