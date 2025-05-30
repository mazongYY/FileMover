#!/usr/bin/env python3
"""
测试自动清理功能
"""

import os
import sys
import shutil
import tempfile
import zipfile
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (cleanup_extracted_files_directory, auto_cleanup_on_new_archive, 
                   initialize_project_directories, setup_logging)


def create_test_files():
    """创建测试文件和目录结构"""
    print("🔧 创建测试环境...")
    
    # 确保extracted_files目录存在
    extracted_dir, matched_dir, unmatched_dir = initialize_project_directories()
    
    # 在extracted_files目录中创建一些测试文件和文件夹
    test_files = [
        "test_file1.txt",
        "test_file2.pdf",
        "old_document.docx"
    ]
    
    test_dirs = [
        "old_folder1",
        "old_folder2/subfolder",
        "命中文件",
        "未命中文件"
    ]
    
    # 创建测试文件
    for file_name in test_files:
        file_path = os.path.join(extracted_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"这是测试文件: {file_name}")
        print(f"  ✅ 创建文件: {file_name}")
    
    # 创建测试目录和子文件
    for dir_name in test_dirs:
        dir_path = os.path.join(extracted_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        
        # 在每个目录中创建一个文件
        test_file = os.path.join(dir_path, "test_content.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(f"目录 {dir_name} 中的测试内容")
        print(f"  ✅ 创建目录: {dir_name}")
    
    return extracted_dir


def create_test_archive():
    """创建测试压缩包"""
    print("📦 创建测试压缩包...")
    
    # 创建临时压缩包
    archive_path = "test_archive.zip"
    
    with zipfile.ZipFile(archive_path, 'w') as zf:
        # 添加一些测试文件到压缩包
        test_content = [
            ("readme.txt", "这是一个测试压缩包"),
            ("data/info.txt", "数据文件内容"),
            ("docs/manual.pdf", "手册内容")
        ]
        
        for file_name, content in test_content:
            zf.writestr(file_name, content)
    
    print(f"  ✅ 创建压缩包: {archive_path}")
    return archive_path


def test_cleanup_function():
    """测试清理函数"""
    print("\n🧪 测试1: 基础清理功能")
    
    # 创建测试环境
    extracted_dir = create_test_files()
    
    # 显示清理前的状态
    print(f"\n📋 清理前的extracted_files目录内容:")
    items_before = os.listdir(extracted_dir)
    for item in items_before:
        item_path = os.path.join(extracted_dir, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
        else:
            print(f"  📄 {item}")
    
    print(f"  总计: {len(items_before)} 个项目")
    
    # 执行清理
    print(f"\n🧹 执行清理...")
    success = cleanup_extracted_files_directory(extracted_dir)
    
    # 显示清理后的状态
    print(f"\n📋 清理后的extracted_files目录内容:")
    items_after = os.listdir(extracted_dir) if os.path.exists(extracted_dir) else []
    if items_after:
        for item in items_after:
            item_path = os.path.join(extracted_dir, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
        print(f"  总计: {len(items_after)} 个项目")
    else:
        print("  目录为空 ✅")
    
    # 验证结果
    if success and len(items_after) == 0:
        print("✅ 测试1通过: 清理功能正常工作")
        return True
    else:
        print("❌ 测试1失败: 清理功能有问题")
        return False


def test_auto_cleanup_on_new_archive():
    """测试新压缩包自动清理功能"""
    print("\n🧪 测试2: 新压缩包自动清理功能")
    
    # 创建测试环境
    extracted_dir = create_test_files()
    archive_path = create_test_archive()
    
    # 显示清理前的状态
    print(f"\n📋 自动清理前的extracted_files目录内容:")
    items_before = os.listdir(extracted_dir)
    print(f"  总计: {len(items_before)} 个项目")
    
    # 执行自动清理
    print(f"\n🤖 执行自动清理 (模拟导入新压缩包)...")
    success = auto_cleanup_on_new_archive(archive_path, extracted_dir)
    
    # 显示清理后的状态
    print(f"\n📋 自动清理后的extracted_files目录内容:")
    items_after = os.listdir(extracted_dir) if os.path.exists(extracted_dir) else []
    if items_after:
        print(f"  总计: {len(items_after)} 个项目")
    else:
        print("  目录为空 ✅")
    
    # 清理测试文件
    if os.path.exists(archive_path):
        os.remove(archive_path)
        print(f"  🗑️ 清理测试压缩包: {archive_path}")
    
    # 验证结果
    if success and len(items_after) == 0:
        print("✅ 测试2通过: 自动清理功能正常工作")
        return True
    else:
        print("❌ 测试2失败: 自动清理功能有问题")
        return False


def test_edge_cases():
    """测试边界情况"""
    print("\n🧪 测试3: 边界情况测试")
    
    # 测试空目录清理
    print("  📝 测试3.1: 空目录清理")
    extracted_dir, _, _ = initialize_project_directories()
    
    # 确保目录为空
    for item in os.listdir(extracted_dir):
        item_path = os.path.join(extracted_dir, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    
    success1 = cleanup_extracted_files_directory(extracted_dir)
    if success1:
        print("    ✅ 空目录清理测试通过")
    else:
        print("    ❌ 空目录清理测试失败")
    
    # 测试不存在的目录
    print("  📝 测试3.2: 不存在目录清理")
    non_existent_dir = os.path.join(os.getcwd(), "non_existent_extracted_files")
    success2 = cleanup_extracted_files_directory(non_existent_dir)
    if success2:
        print("    ✅ 不存在目录清理测试通过")
    else:
        print("    ❌ 不存在目录清理测试失败")
    
    # 测试无效压缩包路径
    print("  📝 测试3.3: 无效压缩包路径")
    success3 = auto_cleanup_on_new_archive("non_existent_archive.zip", extracted_dir)
    if not success3:  # 应该返回False
        print("    ✅ 无效压缩包路径测试通过")
    else:
        print("    ❌ 无效压缩包路径测试失败")
    
    return success1 and success2 and not success3


def test_integration():
    """集成测试"""
    print("\n🧪 测试4: 集成测试")
    
    # 模拟完整的用户操作流程
    print("  📝 模拟用户操作流程:")
    
    # 1. 初始化项目目录
    print("    1. 初始化项目目录...")
    extracted_dir, matched_dir, unmatched_dir = initialize_project_directories()
    
    # 2. 创建一些"旧"文件（模拟之前的操作结果）
    print("    2. 创建旧文件（模拟之前的操作）...")
    old_files = ["old_result1.txt", "old_result2.pdf"]
    for file_name in old_files:
        file_path = os.path.join(matched_dir, file_name)
        with open(file_path, 'w') as f:
            f.write("旧的处理结果")
    
    # 3. 用户选择新的压缩包
    print("    3. 用户选择新压缩包...")
    new_archive = create_test_archive()
    
    # 4. 自动清理触发
    print("    4. 触发自动清理...")
    success = auto_cleanup_on_new_archive(new_archive, extracted_dir)
    
    # 5. 验证清理结果
    print("    5. 验证清理结果...")
    remaining_items = []
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            remaining_items.append(os.path.join(root, file))
        for dir in dirs:
            remaining_items.append(os.path.join(root, dir))
    
    # 清理测试文件
    if os.path.exists(new_archive):
        os.remove(new_archive)
    
    if success and len(remaining_items) == 0:
        print("    ✅ 集成测试通过: 完整流程正常工作")
        return True
    else:
        print(f"    ❌ 集成测试失败: 仍有 {len(remaining_items)} 个项目未清理")
        return False


def main():
    """主测试函数"""
    print("🚀 开始自动清理功能测试")
    print("=" * 50)
    
    # 设置日志
    setup_logging()
    
    # 运行所有测试
    test_results = []
    
    try:
        test_results.append(test_cleanup_function())
        test_results.append(test_auto_cleanup_on_new_archive())
        test_results.append(test_edge_cases())
        test_results.append(test_integration())
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 汇总测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    test_names = [
        "基础清理功能",
        "新压缩包自动清理",
        "边界情况测试",
        "集成测试"
    ]
    
    passed_count = 0
    for i, (name, result) in enumerate(zip(test_names, test_results), 1):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  测试{i}: {name} - {status}")
        if result:
            passed_count += 1
    
    print(f"\n🎯 总体结果: {passed_count}/{len(test_results)} 个测试通过")
    
    if passed_count == len(test_results):
        print("🎉 所有测试通过！自动清理功能工作正常。")
        return True
    else:
        print("⚠️ 部分测试失败，请检查自动清理功能。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
