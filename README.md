# UNNCLang — A Lightweight Tool for Converting Teaching Pseudocode to Python

<div align="center">

[![CI](https://github.com/Gentle-Lijie/UNNCLang-Intepreter/actions/workflows/publish.yml/badge.svg)](https://github.com/Gentle-Lijie/UNNCLang-Intepreter/actions) [![PyPI version](https://img.shields.io/pypi/v/unnclang.svg)](https://pypi.org/project/unnclang/) [![Python versions](https://img.shields.io/pypi/pyversions/unnclang.svg)](https://pypi.org/project/unnclang/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div


This is a compiler prepared for UNNC CELEN086, enabling quick testing of pseudocode provided in the course within Python.

Key Features:

- Registers “statement macros” (e.g., `endif`) to prevent NameErrors during runtime when using bare names;
- Preprocesses teaching syntax (like `then:`, `otherwise`, `endif`) into valid Python before execution;

We recommend running UNNCLang source files using the command-line tool `uncl`:

```bash
uncl code.uncl
```

Below is a brief, beginner-friendly getting started guide.

## Quick Start (3 Steps)

1) Installation (recommended using a virtual environment)

```bash
git clone https://github.com/Gentle-Lijie/UNNCLang-Interpreter.git
cd UNNCLang-Interpreter
python3 -m venv .venv
source .venv/bin/activate
pip install -e 
```

Or (future installation from PyPI):

```bash
pip install unnclang
```

1) Write a minimal example `code.uncl`:

```text
import unnclang

if a>1 then:
    print(“a is greater than 1”)
endif
```

3) Run

```bash
uncl code.uncl

# If packages aren't installed, you can also run:
python -m unnclang.cli code.uncl
```

If an undefined variable (e.g., `a`) is referenced in the source code, Python will raise a `NameError`. To inject variables before execution, use `-s`:

```bash
uncl code.uncl -s a=2
```

---

## CLI: `uncl`

Usage:

```text
uncl FILE [ -s name=value ]...
```

- `FILE`: UNNCLang source file (e.g., `code.uncl`);
- `-s name=value`: Pre-set runtime variables (can be passed multiple times).

Example:

```bash
uncl code.uncl -s a=2 -s debug=True
```

---

## Concise Interface for Generating Automated Tests

- `unnclang.run_uncl(path, set_vars=None)`: Reads and preprocesses files, then executes them in an isolated namespace;
- `unnclang.statement_macro`: Used to register statement-style macros (e.g., `endif`);
- `unnclang.disable_builtin_macros()`: Disables automatic injection into `builtins` (if you wish to avoid polluting the global namespace).

---

## Development and Testing

- Source code is located in `src/unnclang/`; built-in macros reside in `src/unnclang/macros/`;
- Run tests:

```bash
pip install -e .[dev]
pytest
```


# UNNCLang — 教学伪代码到 Python 的轻量工具

这是为UNNC CELEN086准备的一个编译器，以将该课程提供的伪代码快速在 Python 里运行测试。

主要特性：

- 注册“语句宏”（statement macros），例如 `endif`，使裸名字在运行时不会报 NameError；
- 预处理教学语法（如 `then:`、`otherwise`、`endif`）为合法的 Python 再执行；

推荐使用命令行工具 `uncl` 运行 UNNCLang 源文件：

```bash
uncl code.uncl
```

下面是一个简短且适合新手的上手指南。

## 快速开始（3 步）

1) 安装（推荐使用虚拟环境）

```bash
git clone https://github.com/Gentle-Lijie/UNNCLang-Interpreter.git
cd UNNCLang-Interpreter
python3 -m venv .venv
source .venv/bin/activate
pip install -e 
```

或（未来从 PyPI 安装）：

```bash
pip install unnclang
```

1) 写一个最小示例 `code.uncl`：

```text
import unnclang

if a>1 then:
    print("a is greater than 1")
endif
```

3) 运行

```bash
uncl code.uncl

# 如果未安装包，也可以：
python -m unnclang.cli code.uncl
```

如果在源码中引用了未定义变量（例如 `a`），Python 会抛出 `NameError`。要在执行前注入变量，使用 `-s`：

```bash
uncl code.uncl -s a=2
```

---

## CLI：`uncl`

用法：

```text
uncl FILE [ -s name=value ]...
```

- `FILE`：UNNCLang 源文件（如 `code.uncl`）；
- `-s name=value`：预置运行时变量（可多次传入）。

示例：

```bash
uncl code.uncl -s a=2 -s debug=True
```

---

## 用于生成自动化测试的简要接口

- `unnclang.run_uncl(path, set_vars=None)`：读取并预处理文件，再在隔离的命名空间中执行；
- `unnclang.statement_macro`：用于注册 statement-style 宏（如 `endif`）；
- `unnclang.disable_builtin_macros()`：取消自动注入到 `builtins`（如果你不想污染全局命名空间）。

---

## 开发与测试

- 源码位于 `src/unnclang/`；内置宏放在 `src/unnclang/macros/`；
- 运行测试：

```bash
pip install -e .[dev]
pytest
```


