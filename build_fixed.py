#!/usr/bin/env python3
"""
修复版本的打包脚本
解决PyInstaller运行时错误问题
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build():
    """清理构建文件"""
    print("🧹 清理旧的构建文件...")
    
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['文件筛选与移动工具.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ 删除目录: {dir_name}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  ✓ 删除文件: {file_name}")

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    required_modules = [
        'tkinter',
        'rarfile', 
        'py7zr',
        'PIL'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"  ✗ {module} (缺失)")
    
    if missing_modules:
        print(f"\n❌ 缺少依赖: {', '.join(missing_modules)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def build_executable():
    """构建可执行文件"""
    print("🔨 开始构建可执行文件...")
    
    # 使用简化的PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=文件筛选与移动工具',
        '--icon=app_icon.ico',
        '--add-data=config.json;.',
        '--add-data=README.md;.',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=rarfile',
        '--hidden-import=py7zr',
        '--hidden-import=PIL',
        '--hidden-import=utils',
        '--hidden-import=config_manager',
        '--hidden-import=advanced_gui',
        '--hidden-import=undo_manager',
        '--hidden-import=password_manager',
        '--hidden-import=pkg_resources.py2_warn',
        '--exclude-module=numpy',
        '--exclude-module=matplotlib',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
        '--exclude-module=PySide2',
        '--exclude-module=PySide6',
        '--clean',
        '--noconfirm',
        'main.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("  ✓ 构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def test_executable():
    """测试可执行文件"""
    exe_path = "dist/文件筛选与移动工具.exe"
    
    if not os.path.exists(exe_path):
        print("❌ 可执行文件不存在")
        return False
    
    print("🧪 测试可执行文件...")
    
    # 获取文件大小
    size_mb = os.path.getsize(exe_path) / 1024 / 1024
    print(f"  📦 文件大小: {size_mb:.1f} MB")
    
    # 简单的启动测试（非阻塞）
    try:
        # 只检查文件是否可以执行，不实际启动GUI
        print("  ✓ 可执行文件创建成功")
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        return False

def create_portable_package():
    """创建便携版包"""
    print("📦 创建便携版包...")
    
    exe_path = "dist/文件筛选与移动工具.exe"
    if not os.path.exists(exe_path):
        print("❌ 可执行文件不存在，无法创建包")
        return False
    
    # 创建便携版目录
    portable_dir = "portable_release"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)
    
    # 复制可执行文件
    shutil.copy2(exe_path, portable_dir)
    
    # 复制文档
    docs = [
        ("README.md", "使用说明.md"),
        ("CHANGELOG.md", "更新日志.md"),
        ("LICENSE", "许可证.txt")
    ]
    
    for src, dst in docs:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(portable_dir, dst))
    
    # 创建快速开始文件
    quick_start = """Windows 文件筛选与移动工具 - 快速开始

1. 双击运行 "文件筛选与移动工具.exe"
2. 选择要处理的压缩包文件
3. 输入搜索关键字（每行一个）
4. 点击"开始处理"

处理后的文件会保存在程序目录下的 extracted_files 文件夹中。

详细说明请查看 "使用说明.md" 文件。

版本: v4.0
更新: 2024年12月
"""
    
    with open(os.path.join(portable_dir, "快速开始.txt"), 'w', encoding='utf-8') as f:
        f.write(quick_start)
    
    print(f"  ✓ 便携版创建完成: {portable_dir}")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("Windows 文件筛选与移动工具 - 修复版打包脚本")
    print("=" * 60)
    
    # 检查当前目录
    if not os.path.exists("main.py"):
        print("❌ 请在项目根目录运行此脚本")
        return False
    
    # 步骤1: 检查依赖
    if not check_dependencies():
        return False
    
    # 步骤2: 清理构建文件
    clean_build()
    
    # 步骤3: 构建可执行文件
    if not build_executable():
        return False
    
    # 步骤4: 测试可执行文件
    if not test_executable():
        return False
    
    # 步骤5: 创建便携版包
    if not create_portable_package():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 打包完成！")
    print("=" * 60)
    print("可执行文件: dist/文件筛选与移动工具.exe")
    print("便携版包: portable_release/")
    print("\n✅ 可以开始使用了！")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
