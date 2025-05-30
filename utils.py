import os
import shutil
import time
import zipfile
import rarfile
import py7zr
import tempfile
import logging
import re
from logging.handlers import RotatingFileHandler
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
from pathlib import Path


def setup_logging() -> logging.Logger:
    """
    设置日志系统

    Returns:
        logging.Logger: 配置好的日志器
    """
    # 创建logs目录
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 创建日志器
    logger = logging.getLogger("FileFilterTool")
    logger.setLevel(logging.DEBUG)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 创建文件处理器（轮转日志）
    log_file = os.path.join(log_dir, "file_filter.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器到日志器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def initialize_project_directories() -> Tuple[str, str, str]:
    """
    初始化项目目录结构

    Returns:
        Tuple[str, str, str]: (解压目录, 命中文件目录, 未命中文件目录)
    """
    logger = logging.getLogger("FileFilterTool")

    # 项目根目录
    project_root = os.getcwd()

    # 创建主要目录
    extracted_dir = os.path.join(project_root, "extracted_files")
    matched_dir = os.path.join(extracted_dir, "命中文件")
    unmatched_dir = os.path.join(extracted_dir, "未命中文件")
    temp_extract_dir = os.path.join(project_root, "temp_extract")

    # 创建目录
    directories = [extracted_dir, matched_dir, unmatched_dir, temp_extract_dir]
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"目录已创建或已存在: {directory}")
        except OSError as e:
            logger.error(f"创建目录失败 {directory}: {e}")
            raise

    return extracted_dir, matched_dir, unmatched_dir


def extract_archive(archive_path: str, password: Optional[str] = None) -> str:
    """
    解压压缩包到项目临时目录

    Args:
        archive_path: 压缩包路径
        password: 解压密码（可选）

    Returns:
        str: 解压后的目录路径

    Raises:
        ValueError: 不支持的压缩格式
        OSError: 解压失败
    """
    logger = logging.getLogger("FileFilterTool")

    if not os.path.exists(archive_path):
        error_msg = f"压缩包不存在: {archive_path}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # 获取文件扩展名
    _, ext = os.path.splitext(archive_path.lower())
    logger.info(f"开始解压 {ext} 格式的压缩包: {os.path.basename(archive_path)}")

    # 使用项目根目录下的临时目录
    project_root = os.getcwd()
    temp_base_dir = os.path.join(project_root, "temp_extract")
    os.makedirs(temp_base_dir, exist_ok=True)

    # 创建唯一的解压目录
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    temp_dir = os.path.join(temp_base_dir, f"extract_{timestamp}")

    try:
        os.makedirs(temp_dir, exist_ok=True)

        if ext == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                if password:
                    zip_ref.setpassword(password.encode('utf-8'))
                zip_ref.extractall(temp_dir)
                logger.info(f"ZIP文件解压完成，文件数量: {len(zip_ref.namelist())}")
        elif ext == '.rar':
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                if password:
                    rar_ref.setpassword(password)
                rar_ref.extractall(temp_dir)
                logger.info(f"RAR文件解压完成，文件数量: {len(rar_ref.namelist())}")
        elif ext == '.7z':
            with py7zr.SevenZipFile(archive_path, mode='r', password=password) as archive:
                archive.extractall(temp_dir)
                logger.info("7Z文件解压完成")
        else:
            error_msg = f"不支持的压缩格式: {ext}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"解压成功到目录: {temp_dir}")
        return temp_dir

    except Exception as e:
        # 清理临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        error_msg = f"解压失败: {e}"
        logger.error(error_msg)
        raise OSError(error_msg)


def validate_archive(archive_path: str) -> bool:
    """
    验证压缩包是否有效且可访问

    Args:
        archive_path: 压缩包路径

    Returns:
        bool: 压缩包是否有效
    """
    if not os.path.exists(archive_path) or not os.path.isfile(archive_path):
        return False

    _, ext = os.path.splitext(archive_path.lower())
    supported_formats = ['.zip', '.rar', '.7z']

    return ext in supported_formats and os.access(archive_path, os.R_OK)


def match_keywords(filename: str, keywords: List[str], use_regex: bool = False) -> bool:
    """
    检查文件名是否匹配关键字

    Args:
        filename: 文件名
        keywords: 关键字列表
        use_regex: 是否使用正则表达式

    Returns:
        bool: 是否匹配
    """
    if not keywords:
        return False

    if use_regex:
        # 正则表达式模式
        for keyword in keywords:
            if not keyword.strip():
                continue
            try:
                if re.search(keyword.strip(), filename, re.IGNORECASE):
                    return True
            except re.error:
                # 如果正则表达式无效，回退到普通匹配
                if keyword.strip().lower() in filename.lower():
                    return True
    else:
        # 普通字符串匹配
        for keyword in keywords:
            if keyword.strip() and keyword.strip().lower() in filename.lower():
                return True

    return False


def filter_by_file_type(filename: str, allowed_types: List[str]) -> bool:
    """
    根据文件类型过滤文件

    Args:
        filename: 文件名
        allowed_types: 允许的文件扩展名列表

    Returns:
        bool: 是否通过过滤
    """
    if not allowed_types:
        return True  # 如果没有指定类型，则通过所有文件

    file_ext = os.path.splitext(filename.lower())[1]
    return file_ext in [ext.lower() for ext in allowed_types]


def filter_by_size(file_path: str, min_size: int = 0, max_size: int = 0) -> bool:
    """
    根据文件大小过滤文件

    Args:
        file_path: 文件路径
        min_size: 最小大小（字节）
        max_size: 最大大小（字节），0表示无限制

    Returns:
        bool: 是否通过过滤
    """
    try:
        file_size = os.path.getsize(file_path)

        if min_size > 0 and file_size < min_size:
            return False

        if max_size > 0 and file_size > max_size:
            return False

        return True
    except OSError:
        return False


def filter_by_date(file_path: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> bool:
    """
    根据修改时间过滤文件

    Args:
        file_path: 文件路径
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        bool: 是否通过过滤
    """
    try:
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))

        if start_date and file_mtime < start_date:
            return False

        if end_date and file_mtime > end_date:
            return False

        return True
    except OSError:
        return False


def perform_file_operation(src_file: str, dst_file: str, operation: str = "move", undo_manager=None) -> bool:
    """
    执行文件操作（移动/复制/链接）

    Args:
        src_file: 源文件路径
        dst_file: 目标文件路径
        operation: 操作类型 ("move", "copy", "link")
        undo_manager: 撤销管理器（可选）

    Returns:
        bool: 操作是否成功
    """
    logger = logging.getLogger("FileFilterTool")

    try:
        # 确保目标目录存在
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)

        # 记录操作到撤销管理器（在执行操作前）
        if undo_manager:
            undo_manager.record_operation(operation, src_file, dst_file)

        if operation == "move":
            shutil.move(src_file, dst_file)
            logger.debug(f"文件已移动: {os.path.basename(src_file)}")
        elif operation == "copy":
            shutil.copy2(src_file, dst_file)
            logger.debug(f"文件已复制: {os.path.basename(src_file)}")
        elif operation == "link":
            # 创建硬链接（Windows支持）
            if os.name == 'nt':  # Windows
                os.link(src_file, dst_file)
            else:  # Unix-like系统
                os.link(src_file, dst_file)
            logger.debug(f"文件已链接: {os.path.basename(src_file)}")
        else:
            logger.error(f"不支持的操作类型: {operation}")
            return False

        return True

    except Exception as e:
        logger.error(f"文件操作失败 {operation} {os.path.basename(src_file)}: {e}")
        return False


def classify_and_move_files(source_dir: str, keywords: List[str], matched_dir: str, unmatched_dir: str,
                           filters: Optional[Dict[str, Any]] = None, operation: str = "move", undo_manager=None) -> Tuple[List[str], List[str]]:
    """
    分类并移动文件到对应目录

    Args:
        source_dir: 源目录
        keywords: 关键字列表
        matched_dir: 命中文件目录
        unmatched_dir: 未命中文件目录
        filters: 过滤条件字典
        operation: 操作类型 ("move", "copy", "link")
        undo_manager: 撤销管理器（可选）

    Returns:
        Tuple[List[str], List[str]]: (命中文件列表, 未命中文件列表)
    """
    logger = logging.getLogger("FileFilterTool")

    matched_files = []
    unmatched_files = []

    # 解析过滤条件
    if filters is None:
        filters = {}

    use_regex = filters.get("use_regex", False)
    file_types = filters.get("file_types", [])
    size_filter = filters.get("size_filter", {})
    date_filter = filters.get("date_filter", {})

    # 清空目标目录
    for target_dir in [matched_dir, unmatched_dir]:
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir, exist_ok=True)

    logger.info(f"开始分类文件，关键字: {keywords}, 操作模式: {operation}")
    if use_regex:
        logger.info("使用正则表达式模式")
    if file_types:
        logger.info(f"文件类型过滤: {file_types}")

    # 遍历源目录中的所有文件
    for dirpath, _, filenames in os.walk(source_dir):
        for filename in filenames:
            src_file = os.path.join(dirpath, filename)

            # 应用文件类型过滤
            if not filter_by_file_type(filename, file_types):
                logger.debug(f"文件类型过滤跳过: {filename}")
                continue

            # 应用文件大小过滤
            if size_filter.get("enabled", False):
                min_size = size_filter.get("min_size", 0)
                max_size = size_filter.get("max_size", 0)
                if not filter_by_size(src_file, min_size, max_size):
                    logger.debug(f"文件大小过滤跳过: {filename}")
                    continue

            # 应用日期过滤
            if date_filter.get("enabled", False):
                start_date = date_filter.get("start_date")
                end_date = date_filter.get("end_date")
                if start_date:
                    start_date = datetime.fromisoformat(start_date) if isinstance(start_date, str) else start_date
                if end_date:
                    end_date = datetime.fromisoformat(end_date) if isinstance(end_date, str) else end_date
                if not filter_by_date(src_file, start_date, end_date):
                    logger.debug(f"日期过滤跳过: {filename}")
                    continue

            # 检查文件名是否匹配关键字
            is_matched = match_keywords(filename, keywords, use_regex)

            if is_matched:
                # 命中关键字，移动到命中文件夹
                dst_file = os.path.join(matched_dir, filename)
                dst_file = get_unique_filename(dst_file)

                if perform_file_operation(src_file, dst_file, operation, undo_manager):
                    matched_files.append(filename)
                    logger.debug(f"命中文件已{operation}: {filename}")
            else:
                # 未命中关键字，移动到未命中文件夹
                dst_file = os.path.join(unmatched_dir, filename)
                dst_file = get_unique_filename(dst_file)

                if perform_file_operation(src_file, dst_file, operation, undo_manager):
                    unmatched_files.append(filename)
                    logger.debug(f"未命中文件已{operation}: {filename}")

    logger.info(f"文件分类完成 - 命中: {len(matched_files)}, 未命中: {len(unmatched_files)}")
    return matched_files, unmatched_files


def find_and_move_files_from_archive(archive_path: str, keywords: List[str],
                                    filters: Optional[Dict[str, Any]] = None,
                                    operation: str = "move", undo_manager=None, password_manager=None) -> Tuple[List[str], List[str], str, str]:
    """
    从压缩包中查找并分类文件

    Args:
        archive_path: 压缩包路径
        keywords: 关键字列表
        filters: 过滤条件字典
        operation: 操作类型 ("move", "copy", "link")
        undo_manager: 撤销管理器（可选）
        password_manager: 密码管理器（可选）

    Returns:
        Tuple[List[str], List[str], str, str]: (命中文件列表, 未命中文件列表, 命中目录, 未命中目录)

    Raises:
        OSError: 文件操作失败
        ValueError: 参数无效
    """
    logger = logging.getLogger("FileFilterTool")

    if not validate_archive(archive_path):
        error_msg = f"无效的压缩包: {archive_path}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if not keywords or all(not keyword.strip() for keyword in keywords):
        error_msg = "请提供有效的关键字"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # 初始化项目目录
    extracted_dir, matched_dir, unmatched_dir = initialize_project_directories()

    # 自动清理extracted_files目录
    logger.info("检测到新压缩包，开始自动清理...")
    auto_cleanup_on_new_archive(archive_path, matched_dir.replace("matched", ""))

    # 检查密码保护
    password = None
    if password_manager and password_manager.is_password_protected(archive_path):
        password = password_manager.get_password(archive_path)
        if not password:
            raise ValueError("需要密码但未提供有效密码")

    # 解压压缩包
    temp_extract_dir = extract_archive(archive_path, password)

    try:
        logger.info(f"开始处理压缩包: {os.path.basename(archive_path)}")

        # 分类并移动文件
        matched_files, unmatched_files = classify_and_move_files(
            temp_extract_dir, keywords, matched_dir, unmatched_dir, filters, operation, undo_manager
        )

        logger.info(f"处理完成 - 命中文件: {len(matched_files)}, 未命中文件: {len(unmatched_files)}")

        return matched_files, unmatched_files, matched_dir, unmatched_dir

    except Exception as e:
        logger.error(f"处理压缩包时发生错误: {e}")
        raise e

    finally:
        # 清理临时目录
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir, ignore_errors=True)
            logger.info(f"已清理临时目录: {temp_extract_dir}")


def find_and_move_files(root_dir: str, keywords: List[str]) -> Tuple[List[str], str]:
    """
    在指定目录中查找包含关键字的文件并移动到桌面

    Args:
        root_dir: 要搜索的根目录
        keywords: 关键字列表

    Returns:
        Tuple[List[str], str]: (移动的文件列表, 目标文件夹路径)

    Raises:
        OSError: 文件操作失败
        ValueError: 参数无效
    """
    if not os.path.exists(root_dir):
        raise ValueError(f"指定的目录不存在: {root_dir}")

    if not keywords or all(not keyword.strip() for keyword in keywords):
        raise ValueError("请提供有效的关键字")

    # 创建桌面目标文件夹
    desktop_path = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    if not os.path.exists(desktop_path):
        raise OSError("无法找到桌面路径")

    timestamp = time.strftime('%Y%m%d_%H%M%S')
    target_folder = os.path.join(desktop_path, f"筛选文件_{timestamp}")

    try:
        os.makedirs(target_folder, exist_ok=True)
    except OSError as e:
        raise OSError(f"无法创建目标文件夹: {e}")

    matched_files = []

    # 遍历目录查找匹配文件
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # 检查文件名是否包含任何关键字（不区分大小写）
            if any(keyword.strip().lower() in filename.lower() for keyword in keywords if keyword.strip()):
                src_file = os.path.join(dirpath, filename)
                dst_file = os.path.join(target_folder, filename)

                # 处理重名文件，避免覆盖
                dst_file = get_unique_filename(dst_file)

                try:
                    shutil.move(src_file, dst_file)
                    matched_files.append(filename)
                except (OSError, shutil.Error) as e:
                    print(f"移动文件失败 {filename}: {e}")
                    continue

    return matched_files, target_folder


def get_unique_filename(filepath: str) -> str:
    """
    生成唯一的文件名，避免重名覆盖

    Args:
        filepath: 原始文件路径

    Returns:
        str: 唯一的文件路径
    """
    if not os.path.exists(filepath):
        return filepath

    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)

    counter = 1
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_filepath = os.path.join(directory, new_filename)
        if not os.path.exists(new_filepath):
            return new_filepath
        counter += 1


def validate_directory(directory: str) -> bool:
    """
    验证目录是否有效且可访问

    Args:
        directory: 目录路径

    Returns:
        bool: 目录是否有效
    """
    return os.path.exists(directory) and os.path.isdir(directory) and os.access(directory, os.R_OK)


def count_matching_files(root_dir: str, keywords: List[str]) -> int:
    """
    统计匹配关键字的文件数量（预览功能）

    Args:
        root_dir: 要搜索的根目录
        keywords: 关键字列表

    Returns:
        int: 匹配的文件数量
    """
    if not validate_directory(root_dir) or not keywords:
        return 0

    count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(keyword.strip().lower() in filename.lower() for keyword in keywords if keyword.strip()):
                count += 1

    return count


def count_matching_files_in_archive(archive_path: str, keywords: List[str],
                                   filters: Optional[Dict[str, Any]] = None) -> Tuple[int, int]:
    """
    统计压缩包中匹配和未匹配关键字的文件数量（预览功能）

    Args:
        archive_path: 压缩包路径
        keywords: 关键字列表
        filters: 过滤条件字典

    Returns:
        Tuple[int, int]: (匹配文件数量, 未匹配文件数量)
    """
    logger = logging.getLogger("FileFilterTool")

    if not validate_archive(archive_path) or not keywords:
        return 0, 0

    # 解析过滤条件
    if filters is None:
        filters = {}

    use_regex = filters.get("use_regex", False)
    file_types = filters.get("file_types", [])
    size_filter = filters.get("size_filter", {})
    date_filter = filters.get("date_filter", {})

    temp_extract_dir = None
    try:
        # 解压到临时目录
        temp_extract_dir = extract_archive(archive_path)

        matched_count = 0
        unmatched_count = 0

        # 遍历所有文件进行统计
        for dirpath, _, filenames in os.walk(temp_extract_dir):
            for filename in filenames:
                src_file = os.path.join(dirpath, filename)

                # 应用文件类型过滤
                if not filter_by_file_type(filename, file_types):
                    continue

                # 应用文件大小过滤
                if size_filter.get("enabled", False):
                    min_size = size_filter.get("min_size", 0)
                    max_size = size_filter.get("max_size", 0)
                    if not filter_by_size(src_file, min_size, max_size):
                        continue

                # 应用日期过滤
                if date_filter.get("enabled", False):
                    start_date = date_filter.get("start_date")
                    end_date = date_filter.get("end_date")
                    if start_date:
                        start_date = datetime.fromisoformat(start_date) if isinstance(start_date, str) else start_date
                    if end_date:
                        end_date = datetime.fromisoformat(end_date) if isinstance(end_date, str) else end_date
                    if not filter_by_date(src_file, start_date, end_date):
                        continue

                # 检查关键字匹配
                is_matched = match_keywords(filename, keywords, use_regex)

                if is_matched:
                    matched_count += 1
                else:
                    unmatched_count += 1

        logger.info(f"预览统计完成 - 命中: {matched_count}, 未命中: {unmatched_count}")
        return matched_count, unmatched_count

    except Exception as e:
        logger.error(f"预览统计失败: {e}")
        return 0, 0

    finally:
        # 清理临时目录
        if temp_extract_dir and os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir, ignore_errors=True)


def cleanup_temp_directory(temp_dir: str) -> None:
    """
    清理临时目录

    Args:
        temp_dir: 临时目录路径
    """
    if temp_dir and os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass  # 忽略清理错误


def cleanup_extracted_files_directory(extracted_dir: str = None) -> bool:
    """
    清理extracted_files目录下的所有文件和子文件夹

    Args:
        extracted_dir: extracted_files目录路径，如果为None则使用默认路径

    Returns:
        bool: 清理是否成功
    """
    logger = logging.getLogger("FileFilterTool")

    if extracted_dir is None:
        extracted_dir = os.path.join(os.getcwd(), "extracted_files")

    if not os.path.exists(extracted_dir):
        logger.info(f"extracted_files目录不存在，无需清理: {extracted_dir}")
        return True

    try:
        # 获取目录下的所有内容
        items_to_remove = []
        for item in os.listdir(extracted_dir):
            item_path = os.path.join(extracted_dir, item)
            items_to_remove.append(item_path)

        if not items_to_remove:
            logger.info("extracted_files目录已经是空的")
            return True

        logger.info(f"开始清理extracted_files目录，共{len(items_to_remove)}个项目")

        # 清理所有文件和文件夹
        removed_count = 0
        for item_path in items_to_remove:
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    logger.debug(f"删除文件: {os.path.basename(item_path)}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    logger.debug(f"删除文件夹: {os.path.basename(item_path)}")
                removed_count += 1
            except Exception as e:
                logger.warning(f"删除失败 {item_path}: {e}")

        logger.info(f"extracted_files目录清理完成，成功删除{removed_count}/{len(items_to_remove)}个项目")
        return removed_count == len(items_to_remove)

    except Exception as e:
        logger.error(f"清理extracted_files目录失败: {e}")
        return False


def auto_cleanup_on_new_archive(archive_path: str, extracted_dir: str = None) -> bool:
    """
    当导入新压缩包时自动清理extracted_files目录

    Args:
        archive_path: 新压缩包的路径
        extracted_dir: extracted_files目录路径

    Returns:
        bool: 清理是否成功
    """
    logger = logging.getLogger("FileFilterTool")

    if not archive_path or not os.path.exists(archive_path):
        logger.warning("无效的压缩包路径，跳过自动清理")
        return False

    logger.info(f"检测到新压缩包: {os.path.basename(archive_path)}")
    logger.info("开始自动清理extracted_files目录...")

    success = cleanup_extracted_files_directory(extracted_dir)

    if success:
        logger.info("自动清理完成，准备处理新压缩包")
    else:
        logger.warning("自动清理部分失败，但继续处理新压缩包")

    return success


def get_archive_file_list(archive_path: str) -> List[Dict[str, Any]]:
    """
    获取压缩包文件列表（不解压）

    Args:
        archive_path: 压缩包路径

    Returns:
        List[Dict[str, Any]]: 文件信息列表

    Raises:
        ValueError: 不支持的压缩格式
        OSError: 读取失败
    """
    logger = logging.getLogger("FileFilterTool")

    if not os.path.exists(archive_path):
        raise ValueError(f"压缩包不存在: {archive_path}")

    _, ext = os.path.splitext(archive_path.lower())
    files_info = []

    try:
        if ext == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                for info in zip_ref.infolist():
                    if not info.is_dir():  # 只处理文件，不处理目录
                        file_info = {
                            'name': info.filename,
                            'size': info.file_size,
                            'type': os.path.splitext(info.filename)[1].lower(),
                            'modified': datetime(*info.date_time).strftime('%Y-%m-%d %H:%M:%S') if info.date_time else ''
                        }
                        files_info.append(file_info)

        elif ext == '.rar':
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                for info in rar_ref.infolist():
                    if not info.is_dir():
                        file_info = {
                            'name': info.filename,
                            'size': info.file_size,
                            'type': os.path.splitext(info.filename)[1].lower(),
                            'modified': info.date_time.strftime('%Y-%m-%d %H:%M:%S') if info.date_time else ''
                        }
                        files_info.append(file_info)

        elif ext == '.7z':
            with py7zr.SevenZipFile(archive_path, mode='r') as archive:
                for info in archive.list():
                    if not info.is_directory:
                        file_info = {
                            'name': info.filename,
                            'size': info.uncompressed if hasattr(info, 'uncompressed') else 0,
                            'type': os.path.splitext(info.filename)[1].lower(),
                            'modified': info.creationtime.strftime('%Y-%m-%d %H:%M:%S') if hasattr(info, 'creationtime') and info.creationtime else ''
                        }
                        files_info.append(file_info)

        else:
            raise ValueError(f"不支持的压缩格式: {ext}")

        logger.info(f"获取压缩包文件列表成功，文件数量: {len(files_info)}")
        return files_info

    except Exception as e:
        error_msg = f"读取压缩包文件列表失败: {e}"
        logger.error(error_msg)
        raise OSError(error_msg)
