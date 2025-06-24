#!/usr/bin/env python3
"""
PyInstaller构建配置脚本
处理CI环境中的特殊需求
"""

import os
import sys
import subprocess

def build_executable():
    """构建可执行文件"""
    print("🔨 开始构建FileMover可执行文件...")
    
    # 根据环境选择主文件
    main_file = 'main_ci.py' if os.getenv('CI') else 'main.py'

    # PyInstaller参数
    args = [
        'pyinstaller',
        '--onefile',                    # 单文件模式
        '--windowed',                   # 无控制台窗口
        '--name=FileMover',             # 输出文件名
        '--clean',                      # 清理临时文件
        '--noconfirm',                  # 不询问覆盖
        main_file                       # 主文件
    ]

    # 在CI环境中添加特殊配置
    if os.getenv('CI'):
        print("ℹ️ 检测到CI环境，添加特殊配置...")
        args.extend([
            '--log-level=INFO',         # 详细日志
            '--distpath=dist',          # 输出目录
            '--workpath=build',         # 工作目录
            '--exclude-module=tkinter', # 在CI中排除tkinter
            '--exclude-module=tkinter.ttk',
            '--exclude-module=tkinter.filedialog',
            '--exclude-module=tkinter.messagebox',
        ])
    else:
        # 本地环境包含tkinter相关模块
        args.extend([
            '--add-data=*.md;.',           # 包含文档文件
            '--hidden-import=tkinter',      # 确保包含tkinter
            '--hidden-import=tkinter.ttk',  # 确保包含ttk
            '--hidden-import=tkinter.filedialog',  # 确保包含文件对话框
            '--hidden-import=tkinter.messagebox',  # 确保包含消息框
        ])
    
    try:
        print(f"🚀 执行命令: {' '.join(args)}")
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        
        print("✅ 构建成功！")
        print(f"📄 输出:\n{result.stdout}")
        
        # 验证构建结果
        exe_path = os.path.join('dist', 'FileMover.exe')
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path)
            print(f"📦 生成文件: {exe_path}")
            print(f"📏 文件大小: {size:,} bytes ({size/1024/1024:.1f} MB)")
            return True
        else:
            print("❌ 构建文件未找到")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"📄 错误输出:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 构建异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 FileMover构建脚本")
    print("=" * 50)
    
    # 检查环境
    if os.getenv('CI'):
        print("🔧 CI环境构建模式")
    else:
        print("🏠 本地环境构建模式")
    
    # 检查依赖
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装")
        return 1
    
    # 执行构建
    if build_executable():
        print("\n🎉 构建完成！")
        return 0
    else:
        print("\n❌ 构建失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())
