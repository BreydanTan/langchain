# 模块 8：`RunnableLambda` - 将任意函数转换为 Runnable

> **学习目标**
> - 理解如何将普通 Python 函数集成到 LCEL 链中
> - 掌握同步和异步函数的处理机制
> - 学习类型推断和依赖分析的实现细节

---

## 📍 核心作用

`RunnableLambda` 是**胶水组件**，将任意 Python 函数转换为符合 Runnable 接口的对象，使其能够：
- 参与 LCEL 链式组合（`|` 操作符）
- 自动支持 `invoke()`、`batch()`、`stream()` 等方法
- 集成 LangChain 的追踪和回调系统

---

## 🏗️ 源码剖析

### 📄 文件位置
**`libs/core/langchain_core/runnables/base.py:4370-4750`**

### 1️⃣ 初始化：支持多种函数签名

```python
class RunnableLambda(Runnable[Input, Output]):
    def __init__(
        self,
        func: Callable[[Input], Output]
            | Callable[[Input, RunnableConfig], Output]
            | Callable[[Input, CallbackManagerForChainRun], Output]
            | ...,  # 还支持更多签名
        afunc: Callable[[Input], Awaitable[Output]] | None = None,
        name: str | None = None,
    ):
        # 1. 检测是否为异步函数
        if is_async_callable(func) or is_async_generator(func):
            self.afunc = func  # 异步函数
        elif callable(func):
            self.func = func   # 同步函数
        else:
            raise TypeError("Expected a callable")

        # 2. 自动推断名称
        if name is not None:
            self.name = name
        elif func.__name__ != "<lambda>":
            self.name = func.__name__  # 使用函数名
```

**关键设计：**
- **灵活签名**：函数可以只接受 `input`，也可以接受 `config`、`run_manager` 等
- **自动检测**：自动识别同步 vs 异步函数
- **双重支持**：可同时提供 `func`（同步）和 `afunc`（异步）的优化实现

---

### 2️⃣ 类型推断：从函数签名提取类型

```python
@property
def InputType(self) -> Any:
    """从函数签名推断输入类型"""
    func = getattr(self, "func", None) or self.afunc
    try:
        params = inspect.signature(func).parameters
        first_param = next(iter(params.values()), None)
        if first_param and first_param.annotation != inspect.Parameter.empty:
            return first_param.annotation  # 返回类型注解
    except ValueError:
        pass
    return Any  # 默认 Any

@property
def OutputType(self) -> Any:
    """从函数返回类型推断输出类型"""
    func = getattr(self, "func", None) or self.afunc
    try:
        sig = inspect.signature(func)
        if sig.return_annotation != inspect.Signature.empty:
            # 展开 Iterator 类型
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

**示例：**
```python
def process(input: dict) -> str:
    return input["text"].upper()

runnable = RunnableLambda(process)
print(runnable.InputType)   # <class 'dict'>
print(runnable.OutputType)  # <class 'str'>
```

---

### 3️⃣ 核心方法：`_invoke()` - 智能调用

```python
def _invoke(
    self,
    input_: Input,
    run_manager: CallbackManagerForChainRun,
    config: RunnableConfig,
    **kwargs,
) -> Output:
    # 1. 检测生成器函数（用于流式）
    if inspect.isgeneratorfunction(self.func):
        output = None
        for chunk in call_func_with_variable_args(
            self.func, input_, config, run_manager, **kwargs
        ):
            if output is None:
                output = chunk
            else:
                try:
                    output = output + chunk  # 累加块
                except TypeError:
                    output = chunk  # 无法累加则替换
    else:
        # 2. 普通函数
        output = call_func_with_variable_args(
            self.func, input_, config, run_manager, **kwargs
        )

    # 3. 特殊处理：如果返回 Runnable，则递归调用
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

**关键特性：**
1. **`call_func_with_variable_args()`**：自动匹配函数签名，注入 `config`、`run_manager` 等参数
2. **生成器支持**：自动累加生成器输出（用于流式场景）
3. **递归 Runnable**：如果函数返回 Runnable，自动调用它（动态链构建）

---

### 4️⃣ 依赖分析：自动检测嵌套 Runnable

```python
@functools.cached_property
def deps(self) -> list[Runnable]:
    """提取函数中引用的 Runnable 对象"""
    if hasattr(self, "func"):
        objects = get_function_nonlocals(self.func)  # 获取闭包变量
    elif hasattr(self, "afunc"):
        objects = get_function_nonlocals(self.afunc)
    else:
        objects = []

    deps = []
    for obj in objects:
        if isinstance(obj, Runnable):
            deps.append(obj)  # 收集 Runnable 依赖
        elif isinstance(getattr(obj, "__self__", None), Runnable):
            deps.append(obj.__self__)  # 绑定方法的对象
    return deps
```

**示例：**
```python
# 外部 Runnable
summarizer = some_chain

def my_function(text):
    return summarizer.invoke(text)  # 闭包引用

runnable = RunnableLambda(my_function)
print(runnable.deps)  # [summarizer]
```

**用途：** 用于构建执行图（`get_graph()`），追踪组件依赖关系。

---

## 🧩 实战应用

### 模式 1：数据预处理

```python
from langchain_core.runnables import RunnableLambda

def extract_question(input_dict):
    """从复杂输入中提取问题"""
    return {
        "question": input_dict["user_message"],
        "context": input_dict.get("history", [])
    }

chain = (
    RunnableLambda(extract_question)  # 预处理
    | prompt
    | model
)
```

### 模式 2：后处理

```python
def format_output(ai_message):
    """将 AIMessage 转换为 JSON"""
    return {
        "content": ai_message.content,
        "tokens": len(ai_message.content.split()),
        "timestamp": datetime.now().isoformat()
    }

chain = prompt | model | RunnableLambda(format_output)
```

### 模式 3：条件路由（动态返回 Runnable）

```python
def route_by_language(input_dict):
    """根据语言选择不同的链"""
    lang = input_dict.get("language", "en")
    if lang == "zh":
        return chinese_chain
    elif lang == "fr":
        return french_chain
    else:
        return english_chain

router = RunnableLambda(route_by_language)

# 使用：router.invoke({"language": "zh", "text": "..."})
# 自动调用 chinese_chain
```

### 模式 4：异步优化

```python
import aiohttp

async def async_fetch(url):
    """异步 HTTP 请求"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

runnable = RunnableLambda(async_fetch)

# 同步调用（自动包装为异步）
await runnable.ainvoke("https://example.com")
```

---

## 🎓 与自动转换的对比

### 自动转换（字典语法）
```python
chain = {"result": lambda x: x * 2} | other_runnable
```
**优点：** 简洁
**缺点：**
- 无法自定义名称
- 不支持复杂类型注解
- 无法提供独立的异步实现

### 显式 RunnableLambda
```python
def process(x: int) -> int:
    """Double the input"""
    return x * 2

chain = RunnableLambda(process, name="doubler") | other_runnable
```
**优点：**
- 清晰的名称和文档字符串
- 完整的类型注解
- 可测试性更好
- 可提供 `afunc` 优化异步性能

---

## 🧠 知识检验

### 问题 1：类型推断
```python
def my_func(x):  # 无类型注解
    return x.upper()

runnable = RunnableLambda(my_func)
print(runnable.InputType)   # ?
print(runnable.OutputType)  # ?
```

<details>
<summary>答案</summary>

**InputType:** `Any`（无注解，默认 Any）
**OutputType:** `Any`（无返回类型注解）

**建议：** 始终添加类型注解以获得更好的类型安全！
</details>

### 问题 2：递归 Runnable
```python
def router(input):
    if input["type"] == "short":
        return short_chain
    else:
        return long_chain

runnable = RunnableLambda(router)
result = runnable.invoke({"type": "short", "text": "Hi"})
```
**`result` 是什么？**

<details>
<summary>答案</summary>

**答案：** `short_chain.invoke({"type": "short", "text": "Hi"})` 的结果

**解释：** `RunnableLambda` 检测到返回值是 `Runnable`，自动调用它。这允许动态路由！
</details>

### 问题 3：依赖分析
```python
# 场景 1
def func1(x):
    return x * 2

# 场景 2
external_chain = prompt | model
def func2(x):
    return external_chain.invoke(x)

r1 = RunnableLambda(func1)
r2 = RunnableLambda(func2)

print(r1.deps)  # ?
print(r2.deps)  # ?
```

<details>
<summary>答案</summary>

**r1.deps:** `[]`（无外部依赖）
**r2.deps:** `[external_chain]`（闭包引用的 Runnable）

**用途：** LangChain 使用 `deps` 构建执行图。
</details>

---

## 📚 相关链接

- **前置模块：** [模块 7 - RunnableParallel](module-07-runnable-parallel-ZH.md)
- **下一模块：** [模块 9 - OutputParser](module-09-output-parser-ZH.md)
- **代码示例：** [examples/01_basic_runnable.py](examples/01_basic_runnable.py)
- **术语表：** [GLOSSARY.md](GLOSSARY.md#runnablelambda--lambda-可运行组件)

---

**学习进度：** ✅ 模块 1-8 已完成

**核心要点：** `RunnableLambda` 让你能将**任何** Python 函数无缝集成到 LangChain 生态中！
