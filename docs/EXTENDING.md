# 扩展 UNNCLang：添加新的语法组件（宏 / 预处理器）

本文件说明如何为本仓库添加新的教学语法元素，包括两类支持：

- 作为“语句宏”（statement macro）注入到 Python 名称空间（裸名字如 `endif`）。这解决了裸名字未定义的问题。
- 作为预处理规则（preprocessor）把教学语法源（例如 `then:`、`otherwise`、`endwhile`）转换为合法的 Python 语法再执行。这样可以支持无法被 Python 直接解析的语法糖。

仓库里已有的实现参考：
- 语句宏实现：`src/unnclang/registry.py` 与 `src/unnclang/macros/core.py`（其中已定义 `endif`）。
- 预处理实现：`src/unnclang/runner.py` 中的 `_preprocess()` 函数，默认支持 `if ... then:`、`otherwise` 和 `endif`。

下面分步骤说明如何添加新的语法元素。

## 一、添加 statement macro（裸名字）

用途：当你只需要让一个名字在脚本中可用（不会作为函数调用），例如 `endif`、`endwhile`，可以用 statement macro。它不会改变语义，只是让名字存在，避免 NameError。

步骤：

1. 在 `src/unnclang/macros/` 新建或编辑模块（例如 `loop.py`）：

```python
from unnclang import statement_macro

@statement_macro(doc="Marks the end of a while-loop in UNNCLang-style code.")
def endwhile():
    """Placeholder for `endwhile` statement."""
    return None
```

2. 确保你的模块在 `src/unnclang/macros/__init__.py` 中被导入（或把 `from . import loop` 写进去），这样当 `import unnclang` 时模块会被加载并注册宏。

3. 导入包后（例如学生脚本里 `import unnclang`），宏会自动注入到 `builtins`（默认行为）。如果不希望注入到全局，可以在脚本中调用 `unnclang.disable_builtin_macros()`。

示例：

```python
import unnclang

value = 0
while value < 3:
    value += 1
endwhile  # 作为占位符存在，不会报错
```

注意：上面 `endwhile` 只是名字存在，不会把 `while` 块结束或改变控制流。若要实现语义上的 `endwhile`，需要结合预处理器或 AST 转换。

## 二、添加预处理规则（把教学语法转换为 Python）

用途：当语法在 Python 中本身不是合法的（例如 `if a>1 then:`），必须在执行前把源文件转换为合法的 Python 源。

位置：`src/unnclang/runner.py` 的 `_preprocess(text: str) -> str`。

原则：

- 以行为单位进行转换，保留缩进；
- 应对嵌套时小心保持缩进与结构一致；
- 更复杂的转换建议使用 `tokenize` 或构建小型解析器，而不是仅行级替换。

简单示例：添加对 `endwhile`（作为语句行）-> 删除行（仅占位）的支持，或把 `repeat`/`until` 转为 Python 等。

编辑示例（在 `_preprocess` 中加入规则）：

```python
def _preprocess(text: str) -> str:
    out_lines = []
    for raw in text.splitlines():
        stripped = raw.lstrip()
        indent = raw[: len(raw) - len(stripped)]

        # 支持 `if ... then:` -> `if ...:`
        if stripped.startswith("if") and stripped.endswith("then:"):
            out_lines.append(indent + stripped[:-5].rstrip() + ":")
            continue

        # 支持 `otherwise` -> `else:`
        if stripped == "otherwise":
            out_lines.append(indent + "else:")
            continue

        # 支持 `endwhile` 占位符 -> 删除行（如果你只是想保留课堂语感）
        if stripped == "endwhile":
            continue

        out_lines.append(raw)

    return "\n".join(out_lines)
```

提示：如果你要支持 `then`、`otherwise` 和 `endif`，仓库当前的 `_preprocess` 已经示范过这些转换；你只需在其中加入新的条件分支。

## 三、添加测试

每次修改都应添加测试（建议使用 pytest）：

1. 在 `tests/` 下写一个新的测试文件（例如 `test_endwhile.py`），用 `exec` 在受控命名空间运行预处理后的源文件或直接调用 `run_uncl()`，断言行为或输出。
2. 在 CI（`.github/workflows/publish.yml`）中会运行 pytest，确保新规则不会破坏现有行为。

示例测试片段：

```python
def test_endwhile_placeholder():
    from unnclang import run_uncl
    src = """
    x = 0
    while x < 1:
        x += 1
    endwhile
    """
    # 将临时写入文件并运行，或将 _preprocess 直接作用于字符串
    # 这里仅检查运行不会抛出 NameError
    run_uncl(write_temp_file(src))

    # 断言根据你的语义修改内容
```

## 四、更复杂的替换：使用 tokenize/ast

行级替换足够应付大多数教学示例，但会在注释、字符串字面量或复杂嵌套中出现误判。若要更健壮，请考虑：

- 使用 `tokenize` 来遍历 token，精确地替换在代码位置出现的关键字；
- 或者读取源并构建更专门的解析器（例如简单的 LL(1) 解析器）来处理块结构，然后输出合法 Python 源。

## 五、最佳实践

- 对于只需保留课堂书写风格的占位符，使用 statement macro（@statement_macro）即可；
- 对于需要改变语义（例如把 `otherwise` 变成 Python 的 `else`），在 `runner._preprocess` 里做行级转换；
- 始终为新的语法规则添加测试；
- 将注入到 `builtins` 的行为作为可选项（仓库已提供 `disable_builtin_macros()`）。

如果你把要支持的新语法告诉我（比如 `repeat..until`、`endfor`、`then` 的变体），我可以直接帮你把 `_preprocess` 扩展并添加对应的示例与测试。
