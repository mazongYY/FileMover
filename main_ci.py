#!/usr/bin/env python3
"""
FileMover - CI版本
专门用于CI环境构建，最小化依赖
"""

import os
import sys

class FileMoverCore:
    """FileMover核心功能类（CI最小化版本）"""

    def __init__(self):
        self.version = "1.0.0-ci"

    def get_version(self):
        """获取版本信息"""
        return self.version

    def validate_environment(self):
        """验证CI环境"""
        checks = {
            "Python版本": sys.version_info >= (3, 6),
            "操作系统": os.name in ['nt', 'posix'],
            "文件系统": os.path.exists('.'),
        }
        return checks

def main():
    """主函数 - CI环境版本"""
    print("🚀 FileMover CI版本")
    print("ℹ️ 这是专门用于CI环境构建的版本")
    print("ℹ️ 不包含GUI功能，仅用于验证核心逻辑")

    # 创建核心功能实例
    core = FileMoverCore()

    # 测试基础功能
    print(f"✅ 核心功能类创建成功 - 版本: {core.get_version()}")

    # 验证环境
    checks = core.validate_environment()
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}: {result}")

    print("🎉 CI版本验证完成！")
    return 0

if __name__ == "__main__":
    sys.exit(main())
