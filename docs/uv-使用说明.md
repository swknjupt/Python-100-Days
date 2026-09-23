# uv 使用说明

> 更新时间：2026-09
> 适用环境：Ubuntu 20.04 / 系统默认 Python 3.8.10

## 1. uv 简介

[uv](https://github.com/astral-sh/uv) 是 Astral 公司（Ruff 的作者）用 Rust 编写的 Python 包管理和环境管理工具，定位是 **pip + venv + pip-tools + pyenv** 的合体替代品。

核心特点：

- **极快**：依赖解析和安装速度比 pip 快 10~100 倍
- **一体化**：管理 Python 解释器版本、虚拟环境、依赖、项目，一个工具全搞定
- **无侵入**：安装的 Python 解释器放在用户目录，完全不碰系统 Python
- **兼容 pip**：`uv pip install ...` 等命令与 pip 用法一致，迁移成本极低

## 2. 安装与升级

```bash
# 安装（脚本方式，装到 ~/.local/bin）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者用 pip 安装
pip install --user uv
```

```bash
# 查看版本
uv --version

# 升级 uv 自身
uv self update
```

安装后如果找不到 `uv` 命令，确认 `~/.local/bin` 在 `PATH` 中：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 3. Python 版本管理

uv 可以下载和管理独立的 Python 解释器（来自
[python-build-standalone](https://github.com/astral-sh/python-build-standalone) 项目），
安装在 `~/.local/share/uv/python/` 下，与系统 Python 互不干扰。

```bash
# 查看已安装和可安装的版本
uv python list

# 安装指定版本
uv python install 3.13

# 查看某个版本解释器的路径
uv python find 3.13

# 将当前项目的 Python 版本固定到 .python-version 文件
uv python pin 3.13
```

> **说明**：`uv python install` 不需要 sudo，也不会修改 `python3` 命令的指向，
> 系统 Python 保持原样。

## 4. 虚拟环境管理

```bash
# 在当前目录创建 .venv（默认名）
uv venv

# 指定 Python 版本创建
uv venv --python 3.13 .venv

# 激活 / 退出（与普通 venv 相同）
source .venv/bin/activate
deactivate
```

也可以不激活，直接用完整路径执行：

```bash
.venv/bin/python main.py
```

> **注意**：venv 无法跨 Python 小版本"原地升级"（如 3.8 → 3.13），
> 只能删除后用新解释器重建，再重新安装依赖。

## 5. 包管理

### 5.1 兼容 pip 的用法

```bash
uv pip install requests          # 安装单个包
uv pip install -r requirements.txt
uv pip install -e .              # 以可编辑模式安装当前项目
uv pip list                      # 已安装的包
uv pip freeze > requirements.txt
uv pip uninstall requests
```

### 5.2 项目模式（推荐，自动管理 pyproject.toml + lock 文件）

```bash
uv init                          # 初始化新项目
uv add requests                  # 添加依赖（写入 pyproject.toml 并更新 uv.lock）
uv add --dev pytest              # 添加开发依赖
uv remove requests               # 移除依赖
uv sync                          # 按 uv.lock 精确同步环境
uv run python main.py            # 在项目环境中执行命令（无需手动激活）
```

## 6. 实战案例：本项目 .venv 从 3.8 升级到 3.13

本项目（Ubuntu 20.04，系统 Python 3.8.10）将 `.venv` 升级到 3.13 的完整过程：

```bash
# 1. 安装 Python 3.13 独立解释器（用户目录，不影响系统）
uv python install 3.13

# 2. 删除旧 venv
rm -rf .venv

# 3. 用 3.13 重建 venv
uv venv --python 3.13 .venv

# 4. 验证
.venv/bin/python --version    # Python 3.13.9
/usr/bin/python3 --version    # Python 3.8.10（系统不受影响）
```

### 网络问题处理

国内网络直连 GitHub 下载解释器容易超时，报错形如
`Request failed after 3 retries ... python-build-standalone ... timed out`。
此时可通过镜像加速：

```bash
export UV_PYTHON_INSTALL_MIRROR="https://ghfast.top/https://github.com/astral-sh/python-build-standalone/releases/download"
uv python install 3.13
```

PyPI 下载慢时，可换国内镜像源：

```bash
# 方式一：临时指定
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple requests

# 方式二：环境变量
export UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"
```

## 7. uv 与 pip/venv 常用命令对照

| 功能 | 传统方式 | uv 方式 |
|------|---------|---------|
| 安装 Python 版本 | pyenv install 3.13 | `uv python install 3.13` |
| 创建虚拟环境 | `python3.13 -m venv .venv` | `uv venv --python 3.13` |
| 安装包 | `pip install requests` | `uv pip install requests` |
| 安装依赖文件 | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| 导出依赖 | `pip freeze > requirements.txt` | `uv pip freeze > requirements.txt` |
| 卸载包 | `pip uninstall requests` | `uv pip uninstall requests` |
| 锁定依赖版本 | pip-tools / poetry lock | `uv lock` |
| 同步环境 | pip install -r + 手动核对 | `uv sync` |

## 8. 常见问题

**Q：uv 安装的 Python 和系统 Python 冲突吗？**
不冲突。uv 的解释器在 `~/.local/share/uv/python/`，仅在 uv 创建的 venv 内使用，
系统 `python3`（/usr/bin/python3）不受任何影响。想彻底删除时，
`rm -rf ~/.local/share/uv/python` 即可。

**Q：新建 venv 后，之前打开的终端里 `python` 还是旧版本？**
那是因为旧 shell 的 PATH 还指向重建前的 venv。重新
`source .venv/bin/activate`，或新开一个终端即可。

**Q：为什么 `uv venv` 创建的环境里没有 pip？**
uv 创建的 venv 默认不装 pip（更快更省空间），用 `uv pip` 命令代替即可；
确实需要时执行 `uv venv --seed .venv`。

**Q：`.python-version` 文件是干什么的？**
`uv python pin 3.13` 会把它写入项目根目录，之后 `uv venv`、`uv sync`、
`uv run` 都会自动使用该版本，方便团队统一环境。
