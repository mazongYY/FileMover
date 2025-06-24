# 开发环境搭建

本指南将帮助开发者搭建FileMover的开发环境，包括环境配置、依赖安装和开发工具设置。

## 📋 环境要求

### 基础要求
- **Python**: 3.8+ (推荐3.9+)
- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **内存**: 4GB+ (推荐8GB+)
- **磁盘空间**: 1GB+ 可用空间

### 推荐工具
- **IDE**: Visual Studio Code, PyCharm
- **版本控制**: Git 2.20+
- **包管理**: pip, conda (可选)
- **虚拟环境**: venv, virtualenv, conda

## 🚀 快速开始

### 1. 克隆仓库

```bash
# 克隆主仓库
git clone https://github.com/mazongYY/FileMover.git
cd FileMover

# 或者克隆您的Fork
git clone https://github.com/YOUR_USERNAME/FileMover.git
cd FileMover
```

### 2. 创建虚拟环境

#### 使用venv (推荐)
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 使用conda
```bash
# 创建conda环境
conda create -n filemover python=3.9
conda activate filemover
```

### 3. 安装依赖

```bash
# 安装基础依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装可选依赖（用于RAR和7Z支持）
pip install rarfile py7zr
```

### 4. 验证安装

```bash
# 运行程序
python main.py

# 运行测试
python -m pytest

# 检查代码风格
flake8 main.py
```

## 📦 依赖说明

### 核心依赖 (requirements.txt)
```txt
# GUI框架
tkinter  # Python内置，无需安装

# 压缩文件处理
zipfile  # Python内置
```

### 可选依赖
```txt
# RAR文件支持
rarfile>=4.0

# 7Z文件支持
py7zr>=0.20.0

# 性能优化
psutil>=5.8.0
```

### 开发依赖 (requirements-dev.txt)
```txt
# 测试框架
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# 代码质量
flake8>=5.0.0
black>=22.0.0
isort>=5.10.0

# 类型检查
mypy>=0.991

# 文档生成
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0

# 构建工具
pyinstaller>=5.0.0
setuptools>=65.0.0
wheel>=0.37.0
```

## 🛠️ 开发工具配置

### Visual Studio Code

#### 推荐扩展
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.mypy-type-checker",
    "ms-toolsai.jupyter"
  ]
}
```

#### 工作区设置 (.vscode/settings.json)
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### 调试配置 (.vscode/launch.json)
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FileMover",
      "type": "python",
      "request": "launch",
      "program": "main.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "Python: Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### PyCharm

#### 项目配置
1. **解释器设置**
   - File → Settings → Project → Python Interpreter
   - 选择虚拟环境中的Python解释器

2. **代码风格**
   - File → Settings → Editor → Code Style → Python
   - 导入项目的.editorconfig文件

3. **运行配置**
   - Run → Edit Configurations
   - 添加Python配置，脚本路径设为main.py

## 🧪 测试环境

### 测试框架配置

#### pytest配置 (pytest.ini)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --cov=main
    --cov-report=html
    --cov-report=term-missing
```

#### 测试目录结构
```
tests/
├── __init__.py
├── conftest.py
├── test_main.py
├── test_archive_handler.py
├── test_file_filter.py
├── test_ui_components.py
└── fixtures/
    ├── sample.zip
    ├── sample.rar
    └── sample.7z
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_main.py

# 运行特定测试函数
pytest tests/test_main.py::test_file_selection

# 生成覆盖率报告
pytest --cov=main --cov-report=html

# 运行性能测试
pytest tests/test_performance.py -m performance
```

## 🔧 代码质量工具

### 代码格式化

#### Black配置 (pyproject.toml)
```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

#### isort配置
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

### 代码检查

#### flake8配置 (.flake8)
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    build,
    dist,
    .venv
```

#### mypy配置 (mypy.ini)
```ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### 预提交钩子

#### pre-commit配置 (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
```

## 🏗️ 构建和打包

### 开发构建

```bash
# 安装构建依赖
pip install pyinstaller

# 创建开发版本
pyinstaller --onefile --windowed main.py

# 创建带调试信息的版本
pyinstaller --onefile --console main.py
```

### 发布构建

```bash
# 清理之前的构建
rm -rf build/ dist/

# 创建发布版本
pyinstaller --onefile --windowed --name=FileMover \
  --exclude-module=pytest \
  --exclude-module=black \
  --exclude-module=flake8 \
  main.py

# 验证构建
dist/FileMover.exe
```

### 构建脚本 (build.py)
```python
#!/usr/bin/env python3
"""构建脚本"""

import os
import shutil
import subprocess
import sys

def clean_build():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")

def build_executable():
    """构建可执行文件"""
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=FileMover',
        '--clean',
        'main.py'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("Build successful!")
        return True
    else:
        print(f"Build failed: {result.stderr}")
        return False

if __name__ == "__main__":
    clean_build()
    if build_executable():
        print("Executable created: dist/FileMover.exe")
    else:
        sys.exit(1)
```

## 🐛 调试技巧

### 日志配置

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('filemover.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 性能分析

```python
import cProfile
import pstats

# 性能分析
def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # 运行要分析的代码
    your_function()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

### 内存监控

```python
import psutil
import os

def monitor_memory():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"RSS: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"VMS: {memory_info.vms / 1024 / 1024:.2f} MB")
```

## 📚 文档生成

### Sphinx配置

```bash
# 安装Sphinx
pip install sphinx sphinx-rtd-theme

# 初始化文档
sphinx-quickstart docs

# 生成文档
cd docs
make html
```

### API文档

```python
"""
模块文档字符串示例

这个模块包含文件处理的核心功能。

Example:
    >>> from file_handler import FileHandler
    >>> handler = FileHandler()
    >>> handler.process_archive('test.zip')
"""

def process_archive(file_path: str) -> tuple:
    """
    处理压缩包文件
    
    Args:
        file_path (str): 压缩包文件路径
        
    Returns:
        tuple: (匹配文件数, 总文件数)
        
    Raises:
        FileNotFoundError: 当文件不存在时
        ValueError: 当文件格式不支持时
        
    Example:
        >>> matched, total = process_archive('test.zip')
        >>> print(f"匹配 {matched}/{total} 个文件")
    """
    pass
```

---

**下一步**: 查看[代码结构](Code-Structure)了解项目架构，或阅读[贡献指南](Contributing-Guide)开始贡献代码。
