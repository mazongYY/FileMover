#!/usr/bin/env python3
"""
测试工具函数的简单测试脚本
"""

import os
import tempfile
import shutil
import zipfile
from utils import (find_and_move_files, validate_directory, count_matching_files, get_unique_filename,
                   extract_archive, validate_archive, count_matching_files_in_archive,
                   find_and_move_files_from_archive, cleanup_temp_directory, setup_logging,
                   initialize_project_directories, classify_and_move_files)


def create_test_files():
    """创建测试文件和目录结构"""
    # 创建临时目录
    test_dir = tempfile.mkdtemp(prefix="file_filter_test_")

    # 创建测试文件
    test_files = [
        "document.txt",
        "image.jpg",
        "report_2023.pdf",
        "config.ini",
        "backup_file.bak",
        "photo_vacation.png",
        "settings.json"
    ]

    # 创建子目录
    sub_dir = os.path.join(test_dir, "subfolder")
    os.makedirs(sub_dir)

    # 在根目录创建文件
    for filename in test_files[:4]:
        filepath = os.path.join(test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"这是测试文件: {filename}")

    # 在子目录创建文件
    for filename in test_files[4:]:
        filepath = os.path.join(sub_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"这是子目录测试文件: {filename}")

    return test_dir


def create_test_zip():
    """创建测试ZIP文件"""
    test_dir = create_test_files()

    # 创建ZIP文件
    zip_path = tempfile.mktemp(suffix='.zip')

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, test_dir)
                zipf.write(file_path, arcname)

    # 清理原始目录
    shutil.rmtree(test_dir)

    return zip_path


def test_validate_directory():
    """测试目录验证功能"""
    print("测试目录验证功能...")

    # 测试有效目录
    temp_dir = tempfile.mkdtemp()
    assert validate_directory(temp_dir) == True
    print("✓ 有效目录验证通过")

    # 测试无效目录
    assert validate_directory("/nonexistent/path") == False
    print("✓ 无效目录验证通过")

    # 清理
    shutil.rmtree(temp_dir)


def test_count_matching_files():
    """测试文件计数功能"""
    print("\n测试文件计数功能...")

    test_dir = create_test_files()

    try:
        # 测试单个关键字
        count = count_matching_files(test_dir, ["config"])
        print(f"✓ 关键字 'config' 匹配文件数: {count}")

        # 测试多个关键字
        count = count_matching_files(test_dir, ["photo", "image"])
        print(f"✓ 关键字 'photo, image' 匹配文件数: {count}")

        # 测试不存在的关键字
        count = count_matching_files(test_dir, ["nonexistent"])
        print(f"✓ 关键字 'nonexistent' 匹配文件数: {count}")

    finally:
        shutil.rmtree(test_dir)


def test_get_unique_filename():
    """测试唯一文件名生成功能"""
    print("\n测试唯一文件名生成功能...")

    temp_dir = tempfile.mkdtemp()

    try:
        # 创建测试文件
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")

        # 测试唯一文件名生成
        unique_name = get_unique_filename(test_file)
        print(f"✓ 原文件: {os.path.basename(test_file)}")
        print(f"✓ 唯一文件名: {os.path.basename(unique_name)}")

        # 测试不存在的文件
        non_existent = os.path.join(temp_dir, "new_file.txt")
        unique_name = get_unique_filename(non_existent)
        assert unique_name == non_existent
        print("✓ 不存在文件的唯一名称测试通过")

    finally:
        shutil.rmtree(temp_dir)


def test_find_and_move_files():
    """测试文件查找和移动功能（模拟测试）"""
    print("\n测试文件查找和移动功能...")

    test_dir = create_test_files()

    try:
        # 显示测试目录内容
        print(f"测试目录: {test_dir}")
        print("测试目录内容:")
        for root, dirs, files in os.walk(test_dir):
            level = root.replace(test_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")

        # 测试文件计数而不实际移动
        keywords = ["config", "photo"]
        count = count_matching_files(test_dir, keywords)
        print(f"\n关键字 '{', '.join(keywords)}' 匹配的文件数: {count}")

        # 注意：这里不实际执行移动操作，因为会影响桌面
        print("✓ 文件查找功能测试完成（未执行实际移动）")

    finally:
        shutil.rmtree(test_dir)


def test_validate_archive():
    """测试压缩包验证功能"""
    print("\n测试压缩包验证功能...")

    # 创建测试ZIP文件
    zip_path = create_test_zip()

    try:
        # 测试有效压缩包
        assert validate_archive(zip_path) == True
        print("✓ 有效ZIP文件验证通过")

        # 测试无效文件
        assert validate_archive("/nonexistent/file.zip") == False
        print("✓ 无效文件验证通过")

        # 测试不支持的格式
        temp_file = tempfile.mktemp(suffix='.txt')
        with open(temp_file, 'w') as f:
            f.write("test")

        assert validate_archive(temp_file) == False
        print("✓ 不支持格式验证通过")

        os.remove(temp_file)

    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)


def test_extract_archive():
    """测试压缩包解压功能"""
    print("\n测试压缩包解压功能...")

    zip_path = create_test_zip()

    try:
        # 测试解压
        extract_dir = extract_archive(zip_path)
        print(f"✓ 解压成功到: {extract_dir}")

        # 验证解压内容
        files_found = []
        for root, dirs, files in os.walk(extract_dir):
            files_found.extend(files)

        print(f"✓ 解压文件数量: {len(files_found)}")
        print(f"✓ 解压文件列表: {files_found}")

        # 清理
        cleanup_temp_directory(extract_dir)

    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)


def test_count_matching_files_in_archive():
    """测试压缩包中文件计数功能"""
    print("\n测试压缩包中文件计数功能...")

    zip_path = create_test_zip()

    try:
        # 测试单个关键字
        matched, unmatched = count_matching_files_in_archive(zip_path, ["config"])
        print(f"✓ 关键字 'config' - 命中: {matched}, 未命中: {unmatched}")

        # 测试多个关键字
        matched, unmatched = count_matching_files_in_archive(zip_path, ["photo", "image"])
        print(f"✓ 关键字 'photo, image' - 命中: {matched}, 未命中: {unmatched}")

        # 测试不存在的关键字
        matched, unmatched = count_matching_files_in_archive(zip_path, ["nonexistent"])
        print(f"✓ 关键字 'nonexistent' - 命中: {matched}, 未命中: {unmatched}")

    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)


def test_logging_system():
    """测试日志系统"""
    print("\n测试日志系统...")

    # 设置日志
    logger = setup_logging()
    print("✓ 日志系统初始化成功")

    # 测试不同级别的日志
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
    print("✓ 日志记录测试完成")

    # 检查日志文件是否创建
    log_file = os.path.join(os.getcwd(), "logs", "file_filter.log")
    if os.path.exists(log_file):
        print("✓ 日志文件创建成功")
    else:
        print("✗ 日志文件未找到")


def test_directory_initialization():
    """测试目录初始化功能"""
    print("\n测试目录初始化功能...")

    try:
        extracted_dir, matched_dir, unmatched_dir = initialize_project_directories()

        # 检查目录是否创建
        directories = [extracted_dir, matched_dir, unmatched_dir]
        for directory in directories:
            if os.path.exists(directory):
                print(f"✓ 目录创建成功: {os.path.basename(directory)}")
            else:
                print(f"✗ 目录创建失败: {directory}")

        print("✓ 目录初始化测试完成")

    except Exception as e:
        print(f"✗ 目录初始化失败: {e}")


def test_file_classification():
    """测试文件分类功能"""
    print("\n测试文件分类功能...")

    # 创建测试文件
    test_dir = create_test_files()

    try:
        # 初始化目录
        extracted_dir, matched_dir, unmatched_dir = initialize_project_directories()

        # 测试文件分类
        keywords = ["config", "photo"]
        matched_files, unmatched_files = classify_and_move_files(
            test_dir, keywords, matched_dir, unmatched_dir
        )

        print(f"✓ 文件分类完成 - 命中: {len(matched_files)}, 未命中: {len(unmatched_files)}")
        print(f"✓ 命中文件: {matched_files}")
        print(f"✓ 未命中文件: {unmatched_files[:3]}...")  # 只显示前3个

    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def main():
    """运行所有测试"""
    print("开始运行工具函数测试...\n")

    try:
        # 基础功能测试
        test_validate_directory()
        test_count_matching_files()
        test_get_unique_filename()
        test_find_and_move_files()

        # 压缩包功能测试
        test_validate_archive()
        test_extract_archive()
        test_count_matching_files_in_archive()

        # 新增功能测试
        test_logging_system()
        test_directory_initialization()
        test_file_classification()

        print("\n" + "="*50)
        print("✅ 所有测试通过！")
        print("="*50)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
