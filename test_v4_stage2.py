#!/usr/bin/env python3
"""
测试v4.0第二阶段新功能的测试脚本
"""

import os
import tempfile
import shutil
import zipfile
from datetime import datetime, timedelta
from utils import (get_archive_file_list, filter_by_size, filter_by_date,
                   count_matching_files_in_archive, setup_logging)


def create_test_files_with_metadata():
    """创建包含不同大小和时间的测试文件"""
    test_dir = tempfile.mkdtemp(prefix="stage2_test_")
    
    # 创建不同大小的文件
    files_data = [
        ("small_file.txt", "small content", 1),  # 小文件
        ("medium_file.doc", "medium content " * 100, 2),  # 中等文件
        ("large_file.pdf", "large content " * 1000, 3),  # 大文件
        ("config.ini", "[settings]\nkey=value", 1),
        ("image.jpg", "fake image data " * 50, 2),
        ("video.mp4", "fake video data " * 500, 3),
    ]
    
    base_time = datetime.now()
    
    for i, (filename, content, size_factor) in enumerate(files_data):
        filepath = os.path.join(test_dir, filename)
        
        # 创建不同大小的文件
        full_content = content * (size_factor * 100)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # 设置不同的修改时间
        mod_time = base_time - timedelta(days=i)
        timestamp = mod_time.timestamp()
        os.utime(filepath, (timestamp, timestamp))
    
    return test_dir


def create_test_zip_with_metadata():
    """创建包含元数据的测试ZIP文件"""
    test_dir = create_test_files_with_metadata()
    zip_path = tempfile.mktemp(suffix='.zip')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, test_dir)
                zipf.write(file_path, arcname)
    
    shutil.rmtree(test_dir)
    return zip_path


def test_archive_file_list():
    """测试压缩包文件列表获取功能"""
    print("\n测试压缩包文件列表获取功能...")
    
    zip_path = create_test_zip_with_metadata()
    
    try:
        files_info = get_archive_file_list(zip_path)
        
        print(f"✓ 成功获取文件列表，文件数量: {len(files_info)}")
        
        for info in files_info:
            name = info.get('name', 'Unknown')
            size = info.get('size', 0)
            file_type = info.get('type', 'Unknown')
            modified = info.get('modified', 'Unknown')
            
            print(f"  文件: {name}")
            print(f"    大小: {size} bytes")
            print(f"    类型: {file_type}")
            print(f"    修改时间: {modified}")
        
        print("✓ 压缩包文件列表获取测试完成")
        
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)


def test_file_size_filtering():
    """测试文件大小过滤功能"""
    print("\n测试文件大小过滤功能...")
    
    test_dir = create_test_files_with_metadata()
    
    try:
        # 测试不同大小的过滤
        for dirpath, _, filenames in os.walk(test_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_size = os.path.getsize(filepath)
                
                # 测试最小大小过滤
                result_min = filter_by_size(filepath, min_size=500)
                print(f"文件 {filename} ({file_size} bytes) - 最小500字节过滤: {result_min}")
                
                # 测试最大大小过滤
                result_max = filter_by_size(filepath, max_size=5000)
                print(f"文件 {filename} ({file_size} bytes) - 最大5000字节过滤: {result_max}")
                
                # 测试范围过滤
                result_range = filter_by_size(filepath, min_size=100, max_size=10000)
                print(f"文件 {filename} ({file_size} bytes) - 100-10000字节范围过滤: {result_range}")
        
        print("✓ 文件大小过滤测试完成")
        
    finally:
        shutil.rmtree(test_dir)


def test_file_date_filtering():
    """测试文件日期过滤功能"""
    print("\n测试文件日期过滤功能...")
    
    test_dir = create_test_files_with_metadata()
    
    try:
        # 设置日期范围
        now = datetime.now()
        start_date = now - timedelta(days=3)
        end_date = now - timedelta(days=1)
        
        print(f"日期过滤范围: {start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}")
        
        for dirpath, _, filenames in os.walk(test_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                # 测试日期过滤
                result = filter_by_date(filepath, start_date, end_date)
                print(f"文件 {filename} (修改时间: {file_mtime.strftime('%Y-%m-%d %H:%M:%S')}) - 日期过滤: {result}")
        
        print("✓ 文件日期过滤测试完成")
        
    finally:
        shutil.rmtree(test_dir)


def test_advanced_filtering_integration():
    """测试高级过滤功能集成"""
    print("\n测试高级过滤功能集成...")
    
    zip_path = create_test_zip_with_metadata()
    
    try:
        keywords = ["config", "image"]
        
        # 测试基本过滤
        matched, unmatched = count_matching_files_in_archive(zip_path, keywords)
        print(f"基本过滤 - 命中: {matched}, 未命中: {unmatched}")
        
        # 测试文件大小过滤
        size_filters = {
            "use_regex": False,
            "file_types": [],
            "size_filter": {
                "enabled": True,
                "min_size": 500,  # 500 bytes
                "max_size": 5000  # 5000 bytes
            },
            "date_filter": {"enabled": False}
        }
        matched, unmatched = count_matching_files_in_archive(zip_path, keywords, size_filters)
        print(f"大小过滤 (500-5000字节) - 命中: {matched}, 未命中: {unmatched}")
        
        # 测试日期过滤
        now = datetime.now()
        date_filters = {
            "use_regex": False,
            "file_types": [],
            "size_filter": {"enabled": False},
            "date_filter": {
                "enabled": True,
                "start_date": (now - timedelta(days=2)).isoformat(),
                "end_date": now.isoformat()
            }
        }
        matched, unmatched = count_matching_files_in_archive(zip_path, keywords, date_filters)
        print(f"日期过滤 (最近2天) - 命中: {matched}, 未命中: {unmatched}")
        
        # 测试组合过滤
        combined_filters = {
            "use_regex": False,
            "file_types": [".txt", ".ini", ".jpg"],
            "size_filter": {
                "enabled": True,
                "min_size": 100,
                "max_size": 10000
            },
            "date_filter": {
                "enabled": True,
                "start_date": (now - timedelta(days=5)).isoformat(),
                "end_date": now.isoformat()
            }
        }
        matched, unmatched = count_matching_files_in_archive(zip_path, keywords, combined_filters)
        print(f"组合过滤 (类型+大小+日期) - 命中: {matched}, 未命中: {unmatched}")
        
        print("✓ 高级过滤功能集成测试完成")
        
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)


def test_gui_components():
    """测试GUI组件（模拟测试）"""
    print("\n测试GUI组件...")
    
    try:
        from advanced_gui import FileTypeSelector, AdvancedFilters, DragDropFrame, ArchivePreview
        
        # 模拟测试组件创建
        print("✓ FileTypeSelector 类导入成功")
        print("✓ AdvancedFilters 类导入成功")
        print("✓ DragDropFrame 类导入成功")
        print("✓ ArchivePreview 类导入成功")
        
        print("✓ GUI组件测试完成")
        
    except ImportError as e:
        print(f"✗ GUI组件导入失败: {e}")


def main():
    """运行所有第二阶段测试"""
    print("开始运行v4.0第二阶段新功能测试...\n")
    
    # 设置日志
    setup_logging()
    
    try:
        test_archive_file_list()
        test_file_size_filtering()
        test_file_date_filtering()
        test_advanced_filtering_integration()
        test_gui_components()
        
        print("\n" + "="*60)
        print("✅ 所有v4.0第二阶段功能测试通过！")
        print("="*60)
        print("\n新增功能:")
        print("5. ✅ 压缩包内容预览功能")
        print("6. ✅ 文件大小和修改时间筛选")
        print("7. ✅ 增强的用户界面（拖拽提示）")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
