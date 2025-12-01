# UNNCLang Interpreter Helpers

为 UNNC CELEN086 课程准备的一个 Python 包，利用“宏”式占位符让 UNNCLang 伪代码可以直接由 Python 解释器处理。核心思路是把 `endif` 等语句定义成特殊对象，它们在运行时什么也不做，但可以出现在源代码中，从而保留课堂上的书写风格。

## 快速开始

1. 安装依赖（建议使用虚拟环境）：
   ```bash
   pip install -e .
   ```
2. 在你的脚本中导入并暴露宏：
   ```python
   from unnclang import load_macros

   load_macros(globals())  # 或者 from unnclang import endif 逐个导入
   ```

现在就可以在 Python 文件里写出 UNNCLang 风格的结构：

```python
from unnclang import load_macros

load_macros(globals())

value = 5
if value > 0:
    ## 快速开始（适合新手）

    下面给出一个最短、最直接的上手流程——零基础同学看着做就行。

    1) 推荐方式：从 PyPI 安装（你已在 PyPI 注册了 `unnclang`）

    ```bash
    pip install unnclang
    ```

    2) 或者开发者/贡献者模式（在源码目录）：

    ```bash
    # 创建并激活虚拟环境（可选但推荐）
    python3 -m venv .venv
    source .venv/bin/activate
    # 安装当前源码为可编辑包（便于开发）
    pip install -e .
    ```

    3) 写一个最小的 UNNCLang 文件（文件名可以是 `demo.uncl`）：

    ```text
    import unnclang
    if a>1 then:
        print("1")
    endif
    ```

    说明：这个文件不是标准 Python（`then:` / `endif` 不是 Python 语法），因此我们用工具把它转换后再运行。`import unnclang` 在这里只是表示你在使用这个包提供的语法风格。

    4) 运行它：

    ```bash
    # 推荐：安装后可以直接运行 `uncl` 命令（来自 pip 安装）
    uncl demo.uncl

    # 或者不安装时，用模块方式运行（在仓库根）
    python -m unnclang.cli demo.uncl
    ```

    5) 变量控制：如果文件中引用了未定义的变量（例如 `a`)，Python 会抛出 `NameError`。如果你想预置变量，可以使用 `-s`：

    ```bash
    uncl demo.uncl -s a=2
    ```

    这样会让 `a` 在执行前被设置为数字 2，程序就会打印 `1`。

    ---
1. 打开 `src/unnclang/macros/core.py`（或者在 `src/unnclang/macros/` 新建模块）。
2. 使用 `@statement_macro` 装饰器声明一个新的 UNNCLang 语句：
   ```python
   from unnclang import statement_macro

   @statement_macro()
   def endwhile():
       """结束 while 循环。"""
       return None
   ```
3. 确保模块被 `unnclang/macros/__init__.py` 导入，这样一 `import unnclang` 就会注册到全局表里。
4. 在用户代码里 `load_macros(globals())` 或 `from unnclang import endwhile` 即可直接使用。

> 🎯 小贴士：`statement_macro` 会保留你的 Python 函数作为 `handler` 字段，未来如果要做真正的源码重写或静态检查，可以利用这些处理器实现更加复杂的行为。

## 项目结构

```
pyproject.toml          # 包配置
src/unnclang/           # 包源码
  ├── __init__.py       # 对外 API（load_macros、statement_macro 等）
  ├── registry.py       # 宏注册与导出逻辑
  └── macros/           # 内置的 UNNCLang 语句定义
       └── core.py      # 已存在的 endif 定义
README.md               # 本说明文档
docs/                   # 开发与扩展文档（如何添加宏与预处理规则）
tests/                  # pytest 用例与示例脚本
    └── test_macros.py
```

 # UNNCLang — 教学伪代码到 Python 的轻量工具

UNNCLang 是为教学（例如 UNNC CELEN086）准备的一个轻量 Python 包，目标是让课堂上书写的伪代码（例如带 `endif`、`then:`、`otherwise` 的风格）能更方便地在 Python 环境里测试与运行。

本项目采用两条策略：
- 语句宏（statement macros）：把像 `endif` 这样的裸名字注册为占位符（不会改变运行时语义，只是避免 NameError）。
- 预处理（preprocessor）：把不可被 Python 直接解析的语法糖（例如 `if a>1 then:`）转换成合法的 Python 源再执行。

这个仓库已包含示例实现、一个 CLI（`uncl`），以及扩展指南，适合拿来做课堂演示或二次开发。

---

## 快速开始

建议使用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

安装后你将获得：
- Python 包 `unnclang` 可用于脚本导入；
- 命令行工具 `uncl`，用于运行 UNNCLang 风格的源文件。

示例：

在仓库根有一个最小示例 `demo.uncl`（四行）：

```text
import unnclang
if a>1 then:
    print("1")
endif
```

直接运行：

```bash
# 方式 A：已安装为脚本
uncl demo.uncl

# 或者（不安装）
python -m unnclang.cli demo.uncl
```

如果未定义 `a`，程序会抛出标准的 Python `NameError`；如需在运行时传入变量：

```bash
uncl demo.uncl -s a=2
```

---

## 包内 API（快速参考）

- `unnclang.run_uncl(path, set_vars=None)`：读取并预处理 UNNCLang 源文件，再以 Python 执行。`set_vars` 为可选字典，预置执行命名空间。
- `unnclang.statement_macro`：装饰器，用于注册 statement-style 宏（占位的裸名字）。
- `unnclang.disable_builtin_macros()`：如果你不想让宏被注入到全局 `builtins`，可以调用此函数移除注入的名字。

注意：包导入时默认会把注册的 statement macros 注入到 `builtins`（为了教学方便）。如果你要避免污染全局命名空间，请在导入后调用 `disable_builtin_macros()`。

---

## CLI：`uncl`

安装后会有 `uncl` 命令，其基本用法：

```bash
uncl FILE [--set-var name=value]...
```

示例：

```bash
uncl demo.uncl -s a=2
```

`uncl` 只是把 UNNCLang 源预处理为合法 Python 并执行；若源引用未定义的变量（如 `a`），会抛出 Python 的 NameError。

---

## 如何添加新的语法支持（概览）

详见 `docs/EXTENDING.md`。简要步骤：

1. 若只是要让某个裸名字存在（例如 `endwhile`），在 `src/unnclang/macros/` 中用 `@statement_macro` 注册一个占位函数；导入包时会自动注册并注入到 `builtins`（可用 `disable_builtin_macros()` 取消）。
2. 若要支持无法被 Python 直接解析的语法糖（例如 `then:`、`otherwise`、`repeat/until`），修改 `src/unnclang/runner.py` 中的 `_preprocess(text)`，在执行前把教学语法转换成合法 Python。对于更复杂的语法建议使用 `tokenize` 或写小型解析器以避免误替换注释/字符串。
3. 为新语法添加测试（`tests/`），并在 CI 中运行 `pytest`。

---

## 发布到 PyPI（简要）

仓库已包含一个 GitHub Actions workflow（`.github/workflows/publish.yml`），当你把 tag 推到仓库（例如 `v0.1.0`）时会自动构建并发布到 PyPI。发布前需要在仓库 Secrets 中配置 `PYPI_API_TOKEN`。

本地发布流程示例：

```bash
# 更新版本号（pyproject.toml）并提交
git tag v0.1.0
git push origin v0.1.0
```

Actions 将在检测到 tag 时触发构建并上传到 PyPI（需要配置好 secrets）。

---

## 开发

- 源码位于 `src/unnclang/`；内置宏在 `src/unnclang/macros/`。
- 运行测试：
  ```bash
  pip install -e .[dev]
  pytest
  ```

---

如果你想把更多课堂语法（例如 `repeat..until`、`endfor`）直接支持成语义等价的 Python，我可以帮你把 `_preprocess` 改成基于 `tokenize` 的更健壮实现并添加对应测试。欢迎继续告诉我你想要的关键字列表。

---

许可证：MIT
