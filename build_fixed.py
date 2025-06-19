#!/usr/bin/env python3
"""
修复版编译脚本
解决pkg_resources相关问题
"""

import subprocess
import sys
import os
import shutil

def clean_build():
    """清理构建目录"""
    dirs = ['build', 'dist']
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    # 删除spec文件
    for f in os.listdir('.'):
        if f.endswith('.spec'):
            os.remove(f)

def create_hook_file():
    """创建自定义hook文件来修复pkg_resources问题"""
    hook_content = '''
# hook-pkg_resources.py
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = collect_data_files('pkg_resources')
hiddenimports = collect_submodules('pkg_resources')
'''
    
    # 创建hooks目录
    if not os.path.exists('hooks'):
        os.makedirs('hooks')
    
    with open('hooks/hook-pkg_resources.py', 'w') as f:
        f.write(hook_content)

def build_with_fixes():
    """使用修复参数编译"""
    
    # 创建hook文件
    create_hook_file()
    
    # 编译命令
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=FileMover_Fixed',
        '--additional-hooks-dir=hooks',
        '--exclude-module=numpy',
        '--exclude-module=matplotlib', 
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        '--clean',
        '--noconfirm',
        'main_simple.py'
    ]
    
    print("开始编译修复版本...")
    print("命令:", ' '.join(cmd))
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("编译成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"编译失败: {e}")
        print("错误输出:", e.stderr)
        return False

def main():
    print("FileMover 修复版编译工具")
    print("=" * 40)
    
    # 清理
    print("清理旧文件...")
    clean_build()
    
    # 编译
    if build_with_fixes():
        print("\n编译完成!")
        print("可执行文件: dist/FileMover_Fixed.exe")
        
        # 显示文件信息
        exe_path = "dist/FileMover_Fixed.exe"
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"文件大小: {size:.1f} MB")
    else:
        print("\n编译失败!")

if __name__ == "__main__":
    main()
