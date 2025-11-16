# 📚 Module 2: `Runnable` Composition - RunnableSequence

## 🎯 Learning Objectives

By the end of this module, you will be able to:
1. **Understand** the internal structure of `RunnableSequence` (first/middle/last)
2. **Explain** how chain invocation is implemented in `invoke`
3. **Analyze** the type inference mechanism (why `A | B | C` has the correct type)
4. **Predict** how the `batch` method intelligently batches the entire sequence

---

## 📁 File Context

**File Path:** `libs/core/langchain_core/runnables/base.py`
**Key Class:** `RunnableSequence` (starts at line 2789)
**Position in Architecture:** LangChain's most important **composition primitive**, used in virtually every chain

---

## 🧩 Part 1: Why Do We Need `RunnableSequence`? (Design Motivation)

### Reviewing Module 1 Knowledge

In Module 1, we learned that the `|` operator creates a `RunnableSequence`:

```python
# When you write:
chain = prompt | model | parser

# Python calls:
temp = prompt.__or__(model)      # Returns RunnableSequence
chain = temp.__or__(parser)      # Returns RunnableSequence
```

### Core Question: How Does `RunnableSequence` Implement `invoke`?

```python
# User code:
result = chain.invoke("Tell me a joke")

# What needs to happen internally?
# 1. prompt.invoke("Tell me a joke") → PromptValue
# 2. model.invoke(PromptValue) → AIMessage
# 3. parser.invoke(AIMessage) → str

# Key Challenge: How to automatically pass intermediate results?
```

**LangChain's Solution:** `RunnableSequence` is itself a `Runnable`, and its `invoke` method implements **automatic chain invocation**.

---

## 📐 Part 2: Data Structure Design (first/middle/last)

Let's look at the class definition of `RunnableSequence`:

```python
# libs/core/langchain_core/runnables/base.py:2789-2881
class RunnableSequence(RunnableSerializable[Input, Output]):
    """Sequence of `Runnable` objects, where the output of one is the input of the next."""

    # Key fields:
    first: Runnable[Input, Any]
    """The first `Runnable` in the sequence."""

    middle: list[Runnable[Any, Any]] = Field(default_factory=list)
    """The middle `Runnable` in the sequence."""

    last: Runnable[Any, Output]
    """The last `Runnable` in the sequence."""
```

### Deep Design Philosophy Analysis

**Why not just use a `list[Runnable]`?**

```python
# ❌ Simple but type-unsafe design:
class RunnableSequence:
    steps: list[Runnable[Any, Any]]  # Lost type information!

# ✅ LangChain's design:
class RunnableSequence(RunnableSerializable[Input, Output]):
    first: Runnable[Input, Any]      # Knows input type is Input
    middle: list[Runnable[Any, Any]]
    last: Runnable[Any, Output]      # Knows output type is Output
```

**Key Insights:**

1. **The `first` field preserves the input type `Input`**
   - So `RunnableSequence[str, int]` knows it accepts `str` input

2. **The `last` field preserves the output type `Output`**
   - So `RunnableSequence[str, int]` knows it produces `int` output

3. **`middle` has type `Any → Any`**
   - Because middle step types cannot be determined at compile time
   - But at runtime, types naturally match (previous output is next input)

### The Magic of Type Inference

```python
# libs/core/langchain_core/runnables/base.py:2954-2963
@property
def InputType(self) -> type[Input]:
    """The type of the input to the `Runnable`."""
    return self.first.InputType  # Directly returns first step's input type

@property
def OutputType(self) -> type[Output]:
    """The type of the output of the `Runnable`."""
    return self.last.OutputType  # Directly returns last step's output type
```

**Example:**

```python
A: Runnable[str, int]        # String → Integer
B: Runnable[int, float]      # Integer → Float
C: Runnable[float, bool]     # Float → Boolean

sequence = A | B | C
# sequence type: RunnableSequence[str, bool]
# Because:
#   - first = A, InputType = str
#   - middle = [B]
#   - last = C, OutputType = bool
```

---

## 🔍 Part 3: Smart Constructor (Flattening Optimization)

Let's look at the `__init__` method of `RunnableSequence`:

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
            steps_flat.extend(step.steps)  # Key: Flatten nested sequences!
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

### Design Philosophy: Flattening Optimization

**Why special handling for nested `RunnableSequence`?**

```python
# Without flattening:
A = runnable1 | runnable2           # RunnableSequence([r1, r2])
B = runnable3 | runnable4           # RunnableSequence([r3, r4])
C = A | B                            # RunnableSequence([Sequence([r1,r2]), Sequence([r3,r4])])
# When calling C.invoke():
#   → Call Sequence([r1,r2]).invoke()
#     → Call r1.invoke(), then r2.invoke()
#   → Call Sequence([r3,r4]).invoke()
#     → Call r3.invoke(), then r4.invoke()
# There's extra nesting!

# With flattening:
C = A | B                            # RunnableSequence([r1, r2, r3, r4])
# When calling C.invoke():
#   → Directly call r1, r2, r3, r4 invoke()
# No extra nesting!
```

**Key Insight:**
> Flattening avoids unnecessary nesting, improving performance and simplifying debugging traces.

---

## ⚙️ Part 4: `invoke` Implementation (Core of Chain Invocation)

This is the most core method of `RunnableSequence`:

```python
# libs/core/langchain_core/runnables/base.py:3103-3136
@override
def invoke(
    self, input: Input, config: RunnableConfig | None = None, **kwargs: Any
) -> Output:
    # Setup callbacks and context
    config = ensure_config(config)
    callback_manager = get_callback_manager_for_config(config)

    # Start root run
    run_manager = callback_manager.on_chain_start(
        None,
        input,
        name=config.get("run_name") or self.get_name(),
        run_id=config.pop("run_id", None),
    )
    input_ = input  # Current intermediate result

    # Invoke all steps in sequence
    try:
        for i, step in enumerate(self.steps):
            # Mark each step as a child run
            config = patch_config(
                config, callbacks=run_manager.get_child(f"seq:step:{i + 1}")
            )
            with set_config_context(config) as context:
                if i == 0:
                    input_ = context.run(step.invoke, input_, config, **kwargs)
                else:
                    input_ = context.run(step.invoke, input_, config)
        # Finish root run
    except BaseException as e:
        run_manager.on_chain_error(e)
        raise
    else:
        run_manager.on_chain_end(input_)
        return cast("Output", input_)
```

### Line-by-Line Deep Analysis

**1. Callback Manager Setup**

```python
callback_manager = get_callback_manager_for_config(config)
run_manager = callback_manager.on_chain_start(None, input, ...)
```

**Why is this needed?**
- This is LangChain's **observability** system
- Each chain execution generates a "run record"
- Can track: input, output, execution time, errors, etc.

**2. Core Loop for Chain Invocation**

```python
input_ = input  # Initial input
for i, step in enumerate(self.steps):
    input_ = context.run(step.invoke, input_, config)  # Key: Output becomes next input!
```

**Visualization:**

```
Input: "Hello"
  ↓
step[0].invoke("Hello") → result1 = {"text": "Hello"}
  ↓
step[1].invoke(result1) → result2 = AIMessage(content="Hi there!")
  ↓
step[2].invoke(result2) → result3 = "Hi there!"
  ↓
Return: "Hi there!"
```

**3. Hierarchical Structure of Child Runs**

```python
config = patch_config(
    config, callbacks=run_manager.get_child(f"seq:step:{i + 1}")
)
```

**This creates a tree-structured trace:**

```
RunnableSequence (root run)
├── seq:step:1 (prompt)
├── seq:step:2 (model)
└── seq:step:3 (parser)
```

You'll see this visualization in LangSmith!

---

## 🔗 Part 5: Optimized `__or__` Implementation

Let's see how `RunnableSequence` overrides the `__or__` operator:

```python
# libs/core/langchain_core/runnables/base.py:3048-3073
@override
def __or__(
    self,
    other: Runnable[Any, Other] | ...,
) -> RunnableSerializable[Input, Other]:
    if isinstance(other, RunnableSequence):
        # Optimization: If other is also RunnableSequence, flatten!
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

### Design Philosophy: Smart Flattening

**Example:**

```python
seq1 = A | B | C              # RunnableSequence(first=A, middle=[B], last=C)
seq2 = D | E                  # RunnableSequence(first=D, middle=[], last=E)

combined = seq1 | seq2
# Without optimization, you'd get:
#   RunnableSequence(first=seq1, middle=[], last=seq2)  # Nested!

# With optimization, you get:
#   RunnableSequence(first=A, middle=[B, C, D], last=E)  # Flat!
```

**Key Insight:**
> The `__or__` optimization ensures that no matter how you compose chains, the result is always a flat sequence with no unnecessary nesting.

---

## 📊 Part 6: Architecture Visualization (Dual Coding)

Let me show the execution flow of `RunnableSequence` with a Mermaid diagram:

```mermaid
graph TD
    Start[User calls chain.invoke input] --> Setup[Setup callback manager]
    Setup --> RootRun[Start root run]
    RootRun --> Loop{Loop through all steps}

    Loop -->|i=0| Step1[step[0].invoke input]
    Step1 --> Result1[result1]

    Loop -->|i=1| Step2[step[1].invoke result1]
    Step2 --> Result2[result2]

    Loop -->|i=2| Step3[step[2].invoke result2]
    Step3 --> Result3[result3]

    Loop -->|Done| Finish[End root run]
    Finish --> Return[Return final result]

    style Loop fill:#f9f,stroke:#333,stroke-width:2px
    style Step1 fill:#bfb,stroke:#333,stroke-width:2px
    style Step2 fill:#bfb,stroke:#333,stroke-width:2px
    style Step3 fill:#bfb,stroke:#333,stroke-width:2px
```

**Type Flow Diagram:**

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

## 🧠 Knowledge Retrieval Challenge

### Challenge 1: Structural Understanding (Generative Questions)

1. **Explain in your own words: Why does `RunnableSequence` need three fields `first`/`middle`/`last` instead of a simple `list[Runnable]`?**

2. **What is the core logic of `RunnableSequence`'s `invoke` method? Describe it in one sentence.**

3. **Explain the purpose of the "flattening" optimization. What problems would occur without flattening?**

### Challenge 2: Source Code Reasoning (Analytical Questions)

4. **Look at this code:**
   ```python
   for i, step in enumerate(self.steps):
       input_ = context.run(step.invoke, input_, config)
   ```

   **Question:** Why is the `input_` variable repeatedly reassigned? How does this implement "chain invocation"?

5. **Suppose we have:**
   ```python
   A: Runnable[dict, str]
   B: Runnable[str, int]
   C: Runnable[int, list[int]]

   seq = A | B | C
   ```

   **Questions:**
   - What is `seq.first`?
   - What is `seq.middle`?
   - What is `seq.last`?
   - What is `seq.InputType`?
   - What is `seq.OutputType`?

### Challenge 3: Design Analysis (Deep Questions)

6. **Look at the `__or__` implementation:**
   ```python
   if isinstance(other, RunnableSequence):
       return RunnableSequence(
           self.first, *self.middle, self.last,
           other.first, *other.middle, other.last,
       )
   ```

   **Question:** Suppose `seq1 = A | B | C` and `seq2 = D | E`, what is the internal structure of `seq1 | seq2`? Draw out the specific values of `first`/`middle`/`last`.

7. **Predict:** What happens if one step's output type doesn't match the next step's input type?
   ```python
   A: Runnable[str, int]
   B: Runnable[str, float]  # Note: Expects input str, but will receive int!

   chain = A | B
   chain.invoke("hello")  # What happens?
   ```

---

## 📝 Module 2 Summary

You have now deeply understood:

✅ **Data Structure Design**: `first`/`middle`/`last` preserve type information
✅ **Type Inference**: `InputType` from `first`, `OutputType` from `last`
✅ **Chain Invocation**: Loop in `invoke` automatically passes intermediate results
✅ **Flattening Optimization**: `__init__` and `__or__` avoid nested sequences
✅ **Observability**: Callback manager creates hierarchical run traces

**Next Step:** Module 3 will analyze concrete `Runnable` implementations - Prompts (`prompts/base.py`)
