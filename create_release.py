#!/usr/bin/env python3
"""
创建发布包脚本
将可执行文件和相关文档打包成发布版本
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_release_package():
    """创建发布包"""
    
    # 发布信息
    version = "v4.0"
    release_name = f"Windows文件筛选与移动工具_{version}_{datetime.now().strftime('%Y%m%d')}"
    
    # 创建发布目录
    release_dir = f"release/{release_name}"
    if os.path.exists("release"):
        shutil.rmtree("release")
    os.makedirs(release_dir, exist_ok=True)
    
    print(f"创建发布包: {release_name}")
    
    # 复制主程序
    exe_path = "dist/文件筛选与移动工具.exe"
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, release_dir)
        print("✓ 复制主程序")
    else:
        print("✗ 未找到主程序文件")
        return False
    
    # 复制文档文件
    docs = [
        ("README.md", "项目说明.md"),
        ("安装说明.md", "安装说明.md"),
        ("使用手册.md", "使用手册.md"),
        ("CHANGELOG.md", "更新日志.md"),
        ("LICENSE", "许可证.txt"),
        ("Windows 文件筛选与移动工具开发文档.md", "开发文档.md")
    ]
    
    for src, dst in docs:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(release_dir, dst))
            print(f"✓ 复制文档: {dst}")
    
    # 创建示例配置文件
    example_config = {
        "version": "4.0.0",
        "user_preferences": {
            "keywords_history": [
                "报告",
                "文档", 
                "2024",
                "重要"
            ],
            "file_types": {
                "enabled": False,
                "selected_types": ["文档", "图片"],
                "custom_types": []
            },
            "regex_mode": False,
            "operation_mode": "move"
        }
    }
    
    import json
    with open(os.path.join(release_dir, "配置示例.json"), 'w', encoding='utf-8') as f:
        json.dump(example_config, f, ensure_ascii=False, indent=2)
    print("✓ 创建配置示例")
    
    # 创建快速开始指南
    quick_start = """# 快速开始指南

## 🚀 立即使用

1. **运行程序**
   双击 `文件筛选与移动工具.exe` 启动程序

2. **选择压缩包**
   点击"选择压缩包"按钮，选择要处理的ZIP/RAR/7Z文件

3. **输入关键字**
   在关键字输入框中输入要搜索的关键字，每行一个

4. **开始处理**
   点击"开始处理"按钮，程序会自动筛选和分类文件

## 📁 输出位置

处理后的文件会保存在程序目录下的 `extracted_files` 文件夹中：
- `matched/` - 匹配关键字的文件
- `unmatched/` - 未匹配的文件

## 🔧 高级功能

- **正则表达式**: 启用复杂的匹配模式
- **文件类型过滤**: 按文件类型筛选
- **撤销功能**: 可以撤销操作
- **拖拽支持**: 直接拖拽压缩包到程序界面

## 📖 详细说明

请查看以下文档了解更多信息：
- `安装说明.md` - 安装和系统要求
- `使用手册.md` - 详细使用说明
- `项目说明.md` - 项目介绍和功能特性

## ⚠️ 注意事项

1. 首次运行可能被杀毒软件误报，请添加信任
2. 处理重要文件前请先备份
3. 确保有足够的磁盘空间

---
版本: v4.0 | 更新: 2024年12月
"""
    
    with open(os.path.join(release_dir, "快速开始.txt"), 'w', encoding='utf-8') as f:
        f.write(quick_start)
    print("✓ 创建快速开始指南")
    
    # 创建版本信息文件
    version_info = f"""Windows 文件筛选与移动工具 {version}

构建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Python版本: 3.8.6
PyInstaller版本: 3.6

包含文件:
- 文件筛选与移动工具.exe (主程序)
- 项目说明.md
- 安装说明.md  
- 使用手册.md
- 更新日志.md
- 许可证.txt
- 开发文档.md
- 配置示例.json
- 快速开始.txt
- 版本信息.txt

系统要求:
- Windows 7/8/10/11 (64位)
- 最少 512MB RAM
- 最少 100MB 磁盘空间

支持格式:
- ZIP压缩包
- RAR压缩包 (需要WinRAR)
- 7Z压缩包

开发者: mazongYY
项目地址: https://github.com/mazongYY/tools
"""
    
    with open(os.path.join(release_dir, "版本信息.txt"), 'w', encoding='utf-8') as f:
        f.write(version_info)
    print("✓ 创建版本信息")
    
    # 创建ZIP压缩包
    zip_path = f"release/{release_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✓ 创建压缩包: {zip_path}")
    
    # 显示发布包信息
    print("\n" + "="*50)
    print("发布包创建完成！")
    print("="*50)
    print(f"发布目录: {release_dir}")
    print(f"压缩包: {zip_path}")
    
    # 计算文件大小
    exe_size = os.path.getsize(os.path.join(release_dir, "文件筛选与移动工具.exe"))
    zip_size = os.path.getsize(zip_path)
    
    print(f"程序大小: {exe_size / 1024 / 1024:.1f} MB")
    print(f"压缩包大小: {zip_size / 1024 / 1024:.1f} MB")
    
    print("\n文件列表:")
    for file in os.listdir(release_dir):
        print(f"  - {file}")
    
    print(f"\n发布包已准备就绪，可以分发 {zip_path}")
    return True

if __name__ == "__main__":
    try:
        success = create_release_package()
        if success:
            print("\n✅ 发布包创建成功！")
        else:
            print("\n❌ 发布包创建失败！")
    except Exception as e:
        print(f"\n❌ 创建发布包时出错: {e}")
