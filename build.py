#!/usr/bin/env python3
"""
FileMover编译脚本
用于生成Windows可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理.spec文件
    for spec_file in Path('.').glob('*.spec'):
        print(f"删除spec文件: {spec_file}")
        spec_file.unlink()

def build_modern_version():
    """编译现代化版本"""
    print("开始编译FileMover现代化版本...")
    
    # PyInstaller命令参数
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个exe文件
        '--windowed',                   # 无控制台窗口
        '--name=FileMover_Modern',      # 可执行文件名
        '--icon=icon.ico',              # 图标文件（如果存在）
        '--add-data=config.json;.',     # 包含配置文件
        '--hidden-import=tkinter',      # 确保tkinter被包含
        '--hidden-import=tkinter.ttk',  # 确保ttk被包含
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--clean',                      # 清理临时文件
        'main_modern.py'               # 主程序文件
    ]
    
    try:
        # 执行编译
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("编译成功！")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"编译失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def build_classic_version():
    """编译经典版本"""
    print("开始编译FileMover经典版本...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=FileMover_Classic',
        '--icon=icon.ico',
        '--add-data=config.json;.',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--clean',
        'main.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("编译成功！")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"编译失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_icon():
    """创建简单的图标文件"""
    icon_content = """
    # 这里可以放置图标文件内容
    # 或者使用在线工具生成.ico文件
    """
    # 如果没有图标文件，创建一个占位符
    if not os.path.exists('icon.ico'):
        print("未找到icon.ico文件，将跳过图标设置")
        return False
    return True

def copy_dependencies():
    """复制依赖文件到dist目录"""
    dist_dir = Path('dist')
    if not dist_dir.exists():
        return
    
    # 复制配置文件
    files_to_copy = [
        'config.json',
        'README.md'
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir)
            print(f"复制文件: {file_name} -> dist/")

def main():
    """主函数"""
    print("FileMover Windows可执行文件编译工具")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        return
    
    # 清理构建目录
    clean_build_dirs()
    
    # 创建图标
    has_icon = create_icon()
    
    # 询问用户要编译哪个版本
    print("\n请选择要编译的版本:")
    print("1. 现代化版本 (main_modern.py)")
    print("2. 经典版本 (main.py)")
    print("3. 两个版本都编译")
    
    choice = input("请输入选择 (1/2/3): ").strip()
    
    success = False
    
    if choice == '1':
        success = build_modern_version()
    elif choice == '2':
        success = build_classic_version()
    elif choice == '3':
        success1 = build_modern_version()
        success2 = build_classic_version()
        success = success1 and success2
    else:
        print("无效选择")
        return
    
    if success:
        # 复制依赖文件
        copy_dependencies()
        
        print("\n" + "=" * 50)
        print("编译完成！")
        print("可执行文件位置: dist/")
        
        # 显示生成的文件
        dist_dir = Path('dist')
        if dist_dir.exists():
            print("\n生成的文件:")
            for file in dist_dir.iterdir():
                if file.is_file():
                    size = file.stat().st_size / (1024 * 1024)  # MB
                    print(f"  {file.name} ({size:.1f} MB)")
    else:
        print("\n编译失败，请检查错误信息")

if __name__ == "__main__":
    main()
