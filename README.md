# yoapi-cli

WaveYo-API 命令行工具 - 统一的项目管理和插件开发工具

## 📦 功能特性

- 🚀 **项目初始化** - 从GitHub一键初始化WaveYo-API项目
- 🔧 **虚拟环境管理** - 自动创建和管理Python虚拟环境
- 🔌 **插件管理** - 下载、安装、管理插件
- ⚡ **项目运行** - 快速启动开发服务器（支持热重载）
- 📦 **包管理** - 依赖包安装和卸载
- 🎨 **美观界面** - 使用Rich库提供漂亮的命令行界面

## 🛠️ 安装方式

### 使用 pip 安装

```bash
pip install yoapi-cli
```

### 使用 pipx 安装（推荐）

```bash
pipx install yoapi-cli
```

### 从源码安装

```bash
git clone https://github.com/WaveYo/yoapi-cli.git
cd yoapi-cli
pip install -e .
```

## 🚀 快速开始

### 1. 初始化新项目

```bash
# 创建默认名称的项目
yoapi init

# 创建指定名称的项目
yoapi init my-api-project

# 从特定分支初始化
yoapi init --branch develop
```

### 2. 创建虚拟环境

```bash
cd my-api-project
yoapi venv create
```

### 3. 运行项目

```bash
# 正常模式运行
yoapi run

# 热重载模式运行
yoapi run --reload
```

## 📋 命令参考

### 项目初始化

```bash
yoapi init [PROJECT_NAME] [--branch BRANCH]
```

- `PROJECT_NAME`: 项目目录名称（默认为 `waveyo-api-project`）
- `--branch`, `-b`: GitHub分支名称（默认为 `main`）

### 虚拟环境管理

```bash
yoapi venv create
```

### 项目运行

```bash
yoapi run [--reload]
```

- `--reload`, `-r`: 启用热重载模式

### 插件管理

```bash
yoapi plugin download [REPO_NAME]
yoapi plugin list
yoapi plugin remove [PLUGIN_NAME]
yoapi plugin new [PLUGIN_NAME]
```

### 版本信息

```bash
yoapi version
```

## 🏗️ 项目结构

```
yoapi-cli/
├── src/
│   └── yoapi_cli/
│       ├── __init__.py
│       ├── cli.py          # 主CLI程序
│       ├── commands/       # 命令模块
│       │   ├── init.py     # 项目初始化
│       │   ├── plugin.py   # 插件管理
│       │   └── run.py      # 运行命令
│       └── utils/          # 工具函数
│           ├── git.py      # Git操作
│           └── package.py  # 包管理
├── pyproject.toml         # 项目配置
├── README.md              # 说明文档
└── requirements.txt       # 依赖声明
```

## 🔧 开发指南

### 环境设置

```bash
# 克隆项目
git clone https://github.com/WaveYo/yoapi-cli.git
cd yoapi-cli

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Unix/Linux/Mac
source .venv/bin/activate

# 安装开发依赖
pip install -e .[dev]
```

### 运行测试

```bash
pytest tests/
```

#### 测试方法说明

yoapi-cli 使用 pytest 框架进行单元测试，测试覆盖了核心功能：

- **项目初始化测试**：验证从GitHub克隆项目的功能，包括成功初始化、目录冲突处理、Git错误处理等场景
- **包管理器检测**：测试uv和pip的可用性检测逻辑
- **虚拟环境管理**：验证虚拟环境的创建、激活状态检测等功能
- **插件管理**：测试插件的下载、安装、移除等操作

测试使用临时目录进行隔离，确保测试环境干净且不会影响实际文件系统。所有测试都包含详细的错误处理和模拟，确保在各种边界条件下都能正确工作。

测试文件结构：
```
tests/
├── test_cli.py          # 主CLI功能测试
└── __pycache__/         # 编译缓存
```

### 代码格式化

```bash
black src/
isort src/
flake8 src/
```

### 构建发布

```bash
# 构建分发包
python -m build

# 上传到PyPI
twine upload dist/*
```

## 📦 打包为可执行文件

使用Nuitka打包为独立可执行文件：

```bash
# 安装Nuitka
pip install nuitka

# 打包为单文件可执行程序
python -m nuitka --onefile --standalone --enable-console --remove-output src/yoapi_cli/cli.py
```

## 🌟 特性详情

### 项目初始化

- 从GitHub克隆WaveYo-API官方仓库
- 支持指定分支和标签
- 自动检测目录冲突
- 提供详细的项目结构预览

### 虚拟环境管理

- 自动检测和优先使用uv包管理器
- 支持标准venv作为备选方案
- 提供清晰的激活指令
- 智能的环境检测机制

### 插件管理

- 符合yoapi-plugin-xxx命名规范
- 支持从GitHub下载插件
- 插件依赖自动安装
- 完整的插件生命周期管理

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 支持

如有问题或建议，请创建 [Issue](https://github.com/WaveYo/yoapi-cli/issues) 或联系开发团队。

---

*版本: 0.1.03*
*最后更新: 2025-09-04*
