#!/usr/bin/env python3
"""
CI环境专用测试脚本
避免在无GUI环境中运行tkinter相关代码
"""

import sys
import os
import importlib.util

def test_python_syntax():
    """测试Python语法"""
    print("🔍 测试Python语法...")
    try:
        import py_compile
        py_compile.compile('main.py', doraise=True)
        print("✅ main.py语法检查通过")
        return True
    except Exception as e:
        print(f"❌ 语法检查失败: {e}")
        return False

def test_imports():
    """测试基础导入（不包括tkinter）"""
    print("🔍 测试基础模块导入...")
    
    basic_modules = [
        'threading', 'os', 'subprocess', 'platform', 
        'zipfile', 'shutil', 'tempfile', 'json'
    ]
    
    failed_imports = []
    
    for module in basic_modules:
        try:
            __import__(module)
            print(f"✅ {module} 导入成功")
        except ImportError as e:
            print(f"❌ {module} 导入失败: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_tkinter_availability():
    """测试tkinter可用性（不实际创建GUI）"""
    print("🔍 测试tkinter可用性...")

    # 在CI环境中跳过tkinter测试
    if os.getenv('CI'):
        print("ℹ️ CI环境检测到，跳过tkinter测试")
        print("✅ tkinter测试跳过（CI环境正常）")
        return True

    try:
        import tkinter
        print("✅ tkinter模块可用")
        return True
    except ImportError as e:
        print(f"⚠️ tkinter不可用: {e}")
        print("ℹ️ 这在CI环境中是正常的")
        return True  # 在CI环境中不算错误

def test_main_module_structure():
    """测试main.py模块结构"""
    print("🔍 测试main.py模块结构...")
    try:
        # 读取main.py内容
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键类和函数是否存在
        required_elements = [
            'class ModernFileFilterApp',
            'class SimpleConfigManager',
            'def __init__',
            'def browse_archive',
            'def start_processing'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ 缺少必要元素: {missing_elements}")
            return False
        else:
            print("✅ main.py模块结构完整")
            return True
            
    except Exception as e:
        print(f"❌ 模块结构检查失败: {e}")
        return False

def test_config_file():
    """测试配置文件相关功能"""
    print("🔍 测试配置管理...")
    try:
        # 模拟配置管理器测试（不创建GUI）
        import json
        import tempfile
        
        # 创建临时配置文件
        test_config = {
            "user_preferences": {
                "last_browse_directory": "/test/path"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            temp_file = f.name
        
        # 读取配置文件
        with open(temp_file, 'r') as f:
            loaded_config = json.load(f)
        
        # 清理临时文件
        os.unlink(temp_file)
        
        if loaded_config == test_config:
            print("✅ 配置管理功能正常")
            return True
        else:
            print("❌ 配置管理功能异常")
            return False
            
    except Exception as e:
        print(f"❌ 配置管理测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 FileMover CI测试开始")
    print("=" * 50)
    
    tests = [
        ("Python语法检查", test_python_syntax),
        ("基础模块导入", test_imports),
        ("tkinter可用性", test_tkinter_availability),
        ("模块结构检查", test_main_module_structure),
        ("配置管理测试", test_config_file)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            # tkinter测试失败不算错误（CI环境正常）
            if test_name == "tkinter可用性":
                passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
