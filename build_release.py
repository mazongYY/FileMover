#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileMover v4.0 自动化打包脚本
用于生成独立的Windows可执行文件和发布包
"""

import os
import sys
import shutil
import subprocess
import zipfile
import datetime
from pathlib import Path

class ReleaseBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.version = "v4.0"
        self.app_name = "FileMover"
        self.release_name = f"{self.app_name}_{self.version}"
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 目录配置
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.release_dir = self.project_root / "release"
        self.portable_dir = self.project_root / "portable_release"
        
    def clean_build_dirs(self):
        """清理构建目录"""
        print("🧹 清理构建目录...")
        
        dirs_to_clean = [self.dist_dir, self.build_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   ✅ 已清理: {dir_path}")
        
    def check_dependencies(self):
        """检查依赖是否安装"""
        print("🔍 检查依赖...")
        
        required_packages = ['pyinstaller', 'rarfile', 'py7zr']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"   ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"   ❌ {package} (缺失)")
        
        if missing_packages:
            print(f"\n⚠️  缺少依赖包: {', '.join(missing_packages)}")
            print("请运行: pip install -r requirements.txt")
            return False
        
        return True
    
    def build_executable(self):
        """使用PyInstaller构建可执行文件"""
        print("🔨 构建可执行文件...")
        
        # 检查spec文件
        spec_file = self.project_root / "file_filter_tool.spec"
        if not spec_file.exists():
            print("❌ 找不到spec文件，请先创建file_filter_tool.spec")
            return False
        
        # 运行PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            str(spec_file)
        ]
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, 
                                  capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print("   ✅ 可执行文件构建成功")
                return True
            else:
                print(f"   ❌ 构建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ 构建异常: {e}")
            return False
    
    def create_portable_release(self):
        """创建便携版发布包"""
        print("📦 创建便携版发布包...")
        
        # 创建便携版目录
        if self.portable_dir.exists():
            shutil.rmtree(self.portable_dir)
        self.portable_dir.mkdir(parents=True)
        
        # 复制可执行文件
        exe_source = self.dist_dir / "文件筛选与移动工具.exe"
        if exe_source.exists():
            shutil.copy2(exe_source, self.portable_dir / f"{self.app_name}.exe")
            print(f"   ✅ 复制可执行文件: {self.app_name}.exe")
        else:
            print("   ❌ 找不到可执行文件")
            return False
        
        # 复制文档文件
        docs_to_copy = [
            ("README.md", "使用说明.md"),
            ("CHANGELOG.md", "更新日志.md"),
            ("LICENSE", "许可证.txt"),
        ]
        
        for src_name, dst_name in docs_to_copy:
            src_file = self.project_root / src_name
            if src_file.exists():
                shutil.copy2(src_file, self.portable_dir / dst_name)
                print(f"   ✅ 复制文档: {dst_name}")
        
        # 创建快速开始指南
        quick_start = self.portable_dir / "快速开始.txt"
        with open(quick_start, 'w', encoding='utf-8') as f:
            f.write(f"""FileMover {self.version} - 快速开始指南

🚀 使用步骤：
1. 双击运行 {self.app_name}.exe
2. 选择要处理的压缩包文件
3. 输入筛选关键字（每行一个）
4. 配置高级过滤选项（可选）
5. 点击"预览匹配文件"查看结果
6. 点击"开始处理"执行文件操作

📁 输出目录：
- 默认在桌面创建 extracted_files 文件夹
- 命中文件：extracted_files/命中文件/
- 未命中文件：extracted_files/未命中文件/

⚙️ 主要功能：
- 支持ZIP、RAR、7Z压缩包
- 智能关键字搜索
- 多种操作模式（移动/复制/链接）
- 高级过滤选项
- 自动主题适配

📞 技术支持：
- 项目地址：https://gitee.com/m6773/FileMover
- 问题反馈：请在项目页面提交Issue

构建时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
        print("   ✅ 创建快速开始指南")
        
        return True
    
    def create_release_archive(self):
        """创建发布压缩包"""
        print("📦 创建发布压缩包...")
        
        # 创建release目录
        self.release_dir.mkdir(exist_ok=True)
        
        # 创建带时间戳的发布包名称
        archive_name = f"{self.release_name}_{datetime.datetime.now().strftime('%Y%m%d')}"
        archive_path = self.release_dir / f"{archive_name}.zip"
        
        # 创建ZIP压缩包
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.portable_dir.rglob('*'):
                if file_path.is_file():
                    arcname = archive_name / file_path.relative_to(self.portable_dir)
                    zipf.write(file_path, arcname)
                    print(f"   📄 添加文件: {file_path.name}")
        
        print(f"   ✅ 发布包已创建: {archive_path}")
        return archive_path
    
    def show_summary(self, archive_path=None):
        """显示构建摘要"""
        print("\n" + "="*60)
        print(f"🎉 {self.app_name} {self.version} 打包完成！")
        print("="*60)
        
        print(f"\n📁 便携版目录: {self.portable_dir}")
        if self.portable_dir.exists():
            files = list(self.portable_dir.iterdir())
            for file_path in files:
                size = file_path.stat().st_size if file_path.is_file() else 0
                size_mb = size / (1024 * 1024)
                print(f"   📄 {file_path.name} ({size_mb:.1f} MB)")
        
        if archive_path:
            size_mb = archive_path.stat().st_size / (1024 * 1024)
            print(f"\n📦 发布包: {archive_path} ({size_mb:.1f} MB)")
        
        print(f"\n⏰ 构建时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n🚀 可以开始分发了！")
    
    def build(self):
        """执行完整的构建流程"""
        print(f"🚀 开始构建 {self.app_name} {self.version}")
        print("="*60)
        
        # 1. 检查依赖
        if not self.check_dependencies():
            return False
        
        # 2. 清理构建目录
        self.clean_build_dirs()
        
        # 3. 构建可执行文件
        if not self.build_executable():
            return False
        
        # 4. 创建便携版
        if not self.create_portable_release():
            return False
        
        # 5. 创建发布压缩包
        archive_path = self.create_release_archive()
        
        # 6. 显示摘要
        self.show_summary(archive_path)
        
        return True

def main():
    """主函数"""
    builder = ReleaseBuilder()
    
    try:
        success = builder.build()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  构建被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 构建过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
