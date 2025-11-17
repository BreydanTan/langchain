# Module 8: `RunnableLambda` - Converting Arbitrary Functions to Runnables

> **Learning Objectives**
> - Understand how to integrate regular Python functions into LCEL chains
> - Master sync and async function handling mechanisms
> - Learn type inference and dependency analysis implementation details

---

## 📍 Core Purpose

`RunnableLambda` is the **glue component** that converts arbitrary Python functions into Runnable-compliant objects, enabling them to:
- Participate in LCEL chain composition (`|` operator)
- Automatically support `invoke()`, `batch()`, `stream()`, etc.
- Integrate with LangChain's tracing and callback system

---

## 🏗️ Source Code Analysis

### 📄 File Location
**`libs/core/langchain_core/runnables/base.py:4370-4750`**

### 1️⃣ Initialization: Supporting Multiple Function Signatures

```python
class RunnableLambda(Runnable[Input, Output]):
    def __init__(
        self,
        func: Callable[[Input], Output]
            | Callable[[Input, RunnableConfig], Output]
            | Callable[[Input, CallbackManagerForChainRun], Output]
            | ...,  # Many more signatures supported
        afunc: Callable[[Input], Awaitable[Output]] | None = None,
        name: str | None = None,
    ):
        # 1. Detect async functions
        if is_async_callable(func) or is_async_generator(func):
            self.afunc = func  # Async function
        elif callable(func):
            self.func = func   # Sync function
        else:
            raise TypeError("Expected a callable")

        # 2. Auto-infer name
        if name is not None:
            self.name = name
        elif func.__name__ != "<lambda>":
            self.name = func.__name__  # Use function name
```

**Key Design:**
- **Flexible signatures**: Functions can accept just `input`, or also `config`, `run_manager`, etc.
- **Auto-detection**: Automatically identifies sync vs async functions
- **Dual support**: Can provide both `func` (sync) and `afunc` (async) for optimized implementations

---

### 2️⃣ Type Inference: Extracting Types from Function Signatures

```python
@property
def InputType(self) -> Any:
    """Infer input type from function signature"""
    func = getattr(self, "func", None) or self.afunc
    try:
        params = inspect.signature(func).parameters
        first_param = next(iter(params.values()), None)
        if first_param and first_param.annotation != inspect.Parameter.empty:
            return first_param.annotation  # Return type annotation
    except ValueError:
        pass
    return Any  # Default to Any

@property
def OutputType(self) -> Any:
    """Infer output type from function return type"""
    func = getattr(self, "func", None) or self.afunc
    try:
        sig = inspect.signature(func)
        if sig.return_annotation != inspect.Signature.empty:
            # Unwrap Iterator types
            if getattr(sig.return_annotation, "__origin__", None) in {
                collections.abc.Iterator,
                collections.abc.AsyncIterator,
            }:
                return getattr(sig.return_annotation, "__args__", (Any,))[0]
            return sig.return_annotation
    except ValueError:
        pass
    return Any
```

**Example:**
```python
def process(input: dict) -> str:
    return input["text"].upper()

runnable = RunnableLambda(process)
print(runnable.InputType)   # <class 'dict'>
print(runnable.OutputType)  # <class 'str'>
```

---

### 3️⃣ Core Method: `_invoke()` - Smart Invocation

```python
def _invoke(
    self,
    input_: Input,
    run_manager: CallbackManagerForChainRun,
    config: RunnableConfig,
    **kwargs,
) -> Output:
    # 1. Handle generator functions (for streaming)
    if inspect.isgeneratorfunction(self.func):
        output = None
        for chunk in call_func_with_variable_args(
            self.func, input_, config, run_manager, **kwargs
        ):
            if output is None:
                output = chunk
            else:
                try:
                    output = output + chunk  # Accumulate chunks
                except TypeError:
                    output = chunk  # Replace if can't add
    else:
        # 2. Regular functions
        output = call_func_with_variable_args(
            self.func, input_, config, run_manager, **kwargs
        )

    # 3. Special handling: if returns Runnable, invoke it recursively
    if isinstance(output, Runnable):
        recursion_limit = config["recursion_limit"]
        if recursion_limit <= 0:
            raise RecursionError("Recursion limit reached")
        output = output.invoke(
            input_,
            patch_config(config, callbacks=run_manager.get_child(), recursion_limit=recursion_limit - 1)
        )

    return output
```

**Key Features:**
1. **`call_func_with_variable_args()`**: Automatically matches function signature, injecting `config`, `run_manager` as needed
2. **Generator support**: Automatically accumulates generator output (for streaming scenarios)
3. **Recursive Runnable**: If function returns a Runnable, automatically invokes it (dynamic chain building)

---

## 🧩 Real-World Patterns

### Pattern 1: Data Preprocessing

```python
from langchain_core.runnables import RunnableLambda

def extract_question(input_dict):
    """Extract question from complex input"""
    return {
        "question": input_dict["user_message"],
        "context": input_dict.get("history", [])
    }

chain = (
    RunnableLambda(extract_question)  # Preprocessing
    | prompt
    | model
)
```

### Pattern 2: Post-processing

```python
def format_output(ai_message):
    """Convert AIMessage to JSON"""
    return {
        "content": ai_message.content,
        "tokens": len(ai_message.content.split()),
        "timestamp": datetime.now().isoformat()
    }

chain = prompt | model | RunnableLambda(format_output)
```

### Pattern 3: Conditional Routing (Dynamic Runnable Return)

```python
def route_by_language(input_dict):
    """Select different chains based on language"""
    lang = input_dict.get("language", "en")
    if lang == "zh":
        return chinese_chain
    elif lang == "fr":
        return french_chain
    else:
        return english_chain

router = RunnableLambda(route_by_language)

# Usage: router.invoke({"language": "zh", "text": "..."})
# Automatically invokes chinese_chain
```

### Pattern 4: Async Optimization

```python
import aiohttp

async def async_fetch(url):
    """Async HTTP request"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

runnable = RunnableLambda(async_fetch)

# Async invocation
await runnable.ainvoke("https://example.com")
```

---

## 🎓 Auto-Conversion vs Explicit RunnableLambda

### Auto-Conversion (Dict Syntax)
```python
chain = {"result": lambda x: x * 2} | other_runnable
```
**Pros:** Concise
**Cons:**
- Can't customize name
- No complex type annotations
- Can't provide separate async implementation

### Explicit RunnableLambda
```python
def process(x: int) -> int:
    """Double the input"""
    return x * 2

chain = RunnableLambda(process, name="doubler") | other_runnable
```
**Pros:**
- Clear name and docstring
- Full type annotations
- Better testability
- Can provide `afunc` for async optimization

---

## 🧠 Knowledge Check

### Question 1: Type Inference
```python
def my_func(x):  # No type annotations
    return x.upper()

runnable = RunnableLambda(my_func)
print(runnable.InputType)   # ?
print(runnable.OutputType)  # ?
```

<details>
<summary>Answer</summary>

**InputType:** `Any` (no annotation, defaults to Any)
**OutputType:** `Any` (no return type annotation)

**Recommendation:** Always add type annotations for better type safety!
</details>

### Question 2: Recursive Runnable
```python
def router(input):
    if input["type"] == "short":
        return short_chain
    else:
        return long_chain

runnable = RunnableLambda(router)
result = runnable.invoke({"type": "short", "text": "Hi"})
```
**What is `result`?**

<details>
<summary>Answer</summary>

**Answer:** The result of `short_chain.invoke({"type": "short", "text": "Hi"})`

**Explanation:** `RunnableLambda` detects that the return value is a `Runnable` and automatically invokes it. This enables dynamic routing!
</details>

---

## 📚 Related Links

- **Previous Module:** [Module 7 - RunnableParallel](module-07-runnable-parallel-EN.md)
- **Next Module:** [Module 9 - OutputParser](module-09-output-parser-EN.md)
- **Code Examples:** [examples/01_basic_runnable.py](examples/01_basic_runnable.py)
- **Glossary:** [GLOSSARY.md](GLOSSARY.md#runnablelambda--lambda-可运行组件)

---

**Progress:** ✅ Modules 1-8 Completed

**Key Takeaway:** `RunnableLambda` lets you seamlessly integrate **any** Python function into the LangChain ecosystem!
