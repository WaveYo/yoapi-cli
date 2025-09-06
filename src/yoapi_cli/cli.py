#!/usr/bin/env python3
"""
WaveYo-API CLI 主程序
统一的项目管理和插件开发工具
"""

import argparse
import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

import click
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import git

# 导入venv命令模块
from yoapi_cli.commands.venv import VenvCommand

# 创建控制台实例
console = Console()

app = typer.Typer(
    help="WaveYo-API CLI Tool - 统一的项目管理和插件开发工具",
    add_completion=False,
    no_args_is_help=True,
)

class YoAPICLI:
    """WaveYo-API CLI 工具类"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.plugins_dir = self.project_root / "plugins"
        self.venv_dir = self.project_root / ".venv"
        self.config_file = self.project_root / ".yoapirc"
        
    def check_uv_available(self) -> bool:
        """检查uv包管理器是否可用"""
        try:
            result = subprocess.run(["uv", "--version"], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    def get_package_manager(self) -> Tuple[str, str]:
        """获取包管理器 - 只支持UV"""
        if self.check_uv_available():
            return ("uv", "uv pip")
        else:
            console.print("❌ uv包管理器不可用", style="red")
            console.print("💡 请安装uv以获得更好的性能:", style="yellow")
            console.print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
            console.print("   或者使用pip安装: pip install uv")
            raise RuntimeError("UV package manager not available")
    
    
    def ensure_venv_activated(self) -> bool:
        """确保虚拟环境已激活"""
        # 检查是否在虚拟环境目录中
        python_executable = Path(sys.executable)
        
        # 检查是否在虚拟环境目录中
        if self.venv_dir.exists() and python_executable.is_relative_to(self.venv_dir):
            return True
        
        # 检查传统的虚拟环境标志
        if (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
            return True
        
        # 检查VIRTUAL_ENV环境变量
        if os.environ.get('VIRTUAL_ENV'):
            return True
        
        # 检查是否存在虚拟环境目录
        if self.venv_dir.exists():
            # 提供正确的激活命令
            if os.name == 'nt':  # Windows
                activate_cmd = ".venv\\Scripts\\activate"
                console.print("⚠️  检测到虚拟环境但未激活，请手动激活:", style="yellow")
                console.print(f"    {activate_cmd}")
                console.print("或者使用: .\\.venv\\Scripts\\activate")
            else:  # Unix/Linux/Mac
                activate_cmd = "source .venv/bin/activate"
                console.print("⚠️  检测到虚拟环境但未激活，请手动激活:", style="yellow")
                console.print(f"    {activate_cmd}")
            
            return False
        
        console.print("❌ 未检测到虚拟环境，请先创建并激活虚拟环境", style="red")
        console.print("使用 uv: uv venv .venv", style="yellow")
        return False

    def init_project(self, project_name: str = None, branch: str = "dev") -> int:
        """
        从GitHub初始化WaveYo-API项目
        
        Args:
            project_name: 项目名称（目录名）
            branch: GitHub分支名称
            
        Returns:
            int: 退出代码
        """
        if project_name is None:
            project_name = "waveyo-api-project"
        
        target_dir = self.project_root / project_name
        
        if target_dir.exists():
            console.print(f"❌ 目录 '{project_name}' 已存在", style="red")
            return 1
        
        repo_url = "https://github.com/WaveYo/WaveYo-API.git"
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="正在克隆项目...", total=None)
                
                # 克隆项目
                git.Repo.clone_from(repo_url, target_dir, branch=branch)
            
            console.print(f"✅ 项目初始化成功: {target_dir}", style="green")
            
            # 检查目录是否存在再显示结构
            if target_dir.exists():
                console.print("📁 项目结构:", style="blue")
                
                # 显示项目结构
                for item in target_dir.iterdir():
                    if item.is_dir():
                        console.print(f"   📂 {item.name}/")
                    else:
                        console.print(f"   📄 {item.name}")
            
            console.print("\n🚀 下一步:", style="yellow")
            console.print(f"   cd {project_name}")
            console.print("   yoapi venv create")
            console.print("   yoapi venv install")
            console.print("   yoapi run")
            
            return 0
            
        except git.exc.GitCommandError as e:
            console.print(f"❌ 克隆项目失败: {e}", style="red")
            return 1
        except Exception as e:
            console.print(f"❌ 初始化项目时出错: {e}", style="red")
            # 清理创建的文件
            if target_dir.exists():
                shutil.rmtree(target_dir)
            return 1

# 创建全局CLI实例
cli = YoAPICLI()

@app.command()
def init(
    project_name: str = typer.Argument(
        "waveyo-api-project", 
        help="项目名称（目录名）"
    ),
    branch: str = typer.Option(
        "dev", 
        "--branch", "-b", 
        help="GitHub分支名称，默认为dev分支"
    )
):
    """从GitHub初始化WaveYo-API项目"""
    return cli.init_project(project_name, branch)

@app.command()
def run(
    reload: bool = typer.Option(
        False, 
        "--reload", "-r", 
        help="启用热重载模式"
    ),
    port: int = typer.Option(
        8000,
        "--port", "-p",
        help="服务器端口号"
    )
):
    """运行WaveYo-API项目"""
    # 导入运行命令模块
    from yoapi_cli.commands.run import RunCommand
    
    # 创建运行命令实例并执行
    run_cmd = RunCommand()
    return run_cmd.run_project(reload=reload, port=port)

@app.command()
def venv(
    command: str = typer.Argument(
        ..., 
        help="虚拟环境命令: create, install"
    )
):
    """虚拟环境管理"""
    venv_cmd = VenvCommand()
    
    if command == "create":
        return venv_cmd.create_venv()
    elif command == "install":
        return venv_cmd.install_dependencies()
    else:
        console.print(f"❌ 未知的虚拟环境命令: {command}", style="red")
        console.print("可用命令: create, install", style="yellow")
        return 1

@app.command()
def plugin(
    command: str = typer.Argument(
        ..., 
        help="插件命令: download, list, remove, new"
    ),
    name: str = typer.Argument(
        None, 
        help="插件名称或GitHub仓库名"
    )
):
    """插件管理"""
    # 导入插件命令模块
    from yoapi_cli.commands.plugin import app as plugin_app
    
    # 调用插件命令
    try:
        plugin_app([command, name] if name else [command])
    except SystemExit as e:
        return e.code
    return 0

@app.command()
def version():
    """显示版本信息"""
    from yoapi_cli import __version__
    console.print(f"📦 yoapi-cli v{__version__}", style="green")
    return 0

def main():
    """主入口函数"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n🛑 操作已取消", style="yellow")
        return 1
    except Exception as e:
        console.print(f"❌ 发生错误: {e}", style="red")
        return 1

if __name__ == "__main__":
    sys.exit(main())
