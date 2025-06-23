import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import logging
from utils import (find_and_move_files, validate_directory, count_matching_files,
                   find_and_move_files_from_archive, validate_archive,
                   count_matching_files_in_archive, cleanup_temp_directory,
                   setup_logging, initialize_project_directories)
from config_manager import ConfigManager
from advanced_gui import FileTypeSelector, AdvancedFilters
from undo_manager import UndoManager
from password_manager import PasswordManager
from icon_manager import icon_manager


class FileFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件筛选与移动工具 v4.0 - 原始UI")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 初始化配置管理器
        self.config_manager = ConfigManager()

        # 初始化撤销管理器
        self.undo_manager = UndoManager()

        # 初始化密码管理器
        self.password_manager = PasswordManager()

        # 初始化日志系统
        self.logger = setup_logging()
        self.logger.info("程序启动 v4.0 - 原始UI版本")

        # 初始化项目目录
        try:
            # 获取extracted_files目录位置配置
            location = self.config_manager.get("user_preferences.ui_settings.extracted_files_location", "current")
            self.extracted_dir, self.matched_dir, self.unmatched_dir = initialize_project_directories(location)
            self.logger.info(f"项目目录初始化完成，位置: {location}")
        except Exception as e:
            self.logger.error(f"项目目录初始化失败: {e}")
            messagebox.showerror("初始化错误", f"无法初始化项目目录: {e}")

        # 检查压缩格式支持
        self.check_format_support()

        # 添加临时目录跟踪
        self.temp_extract_dir = None

        # 设置原始样式（浅色主题）
        self.setup_original_styles()

        # 加载用户配置
        self.load_user_settings()

        self.setup_ui()

    def setup_original_styles(self):
        """设置原始浅色样式主题"""
        self.style = ttk.Style()
        
        # 使用系统默认主题
        self.style.theme_use('winnative')  # Windows原生样式
        
        # 定义原始配色方案（浅色）
        self.colors = {
            'primary': '#0078D4',          # Windows蓝色
            'success': '#107C10',          # Windows绿色
            'warning': '#FF8C00',          # Windows橙色
            'error': '#D13438',            # Windows红色
            'background': 'SystemButtonFace',  # 系统默认背景
            'surface': 'SystemButtonFace',     # 系统默认表面
            'text_primary': 'SystemButtonText', # 系统默认文字
            'text_secondary': 'SystemGrayText', # 系统灰色文字
            'border': 'SystemButtonShadow',     # 系统边框色
            'input_bg': 'SystemWindow',         # 系统输入框背景
        }

    def setup_button_styles(self):
        """配置原始按钮样式"""
        # Primary Button
        self.style.configure(
            "Primary.TButton",
            background=self.colors['primary'],
            foreground='white',
            borderwidth=1,
            focuscolor='none',
            padding=(20, 8),
            font=('Microsoft YaHei UI', 9)
        )

        self.style.map(
            "Primary.TButton",
            background=[
                ('active', '#106EBE'),
                ('pressed', '#005A9E')
            ]
        )

        # Success Button
        self.style.configure(
            "Success.TButton",
            background=self.colors['success'],
            foreground='white',
            borderwidth=1,
            focuscolor='none',
            padding=(20, 8),
            font=('Microsoft YaHei UI', 9)
        )

        self.style.map(
            "Success.TButton",
            background=[
                ('active', '#0E6A0E'),
                ('pressed', '#0C5A0C')
            ]
        )

        # Warning Button
        self.style.configure(
            "Warning.TButton",
            background=self.colors['warning'],
            foreground='white',
            borderwidth=1,
            focuscolor='none',
            padding=(16, 6),
            font=('Microsoft YaHei UI', 9)
        )

        self.style.map(
            "Warning.TButton",
            background=[
                ('active', '#E67C00'),
                ('pressed', '#CC6600')
            ]
        )

    def load_user_settings(self):
        """加载用户设置"""
        try:
            # 加载窗口位置和大小
            window_config = self.config_manager.get("user_preferences.window", {})
            if window_config.get("remember_position", False):
                geometry = window_config.get("geometry")
                if geometry:
                    self.root.geometry(geometry)

            # 加载其他用户偏好设置
            ui_settings = self.config_manager.get("user_preferences.ui_settings", {})
            
            self.logger.info("用户设置加载完成")
        except Exception as e:
            self.logger.error(f"加载用户设置失败: {e}")

    def check_format_support(self):
        """检查压缩格式支持"""
        try:
            import rarfile
            self.rar_support = True
            self.logger.info("RAR格式支持已启用")
        except ImportError:
            self.rar_support = False
            self.logger.warning("RAR格式支持未安装")

        try:
            import py7zr
            self.seven_zip_support = True
            self.logger.info("7Z格式支持已启用")
        except ImportError:
            self.seven_zip_support = False
            self.logger.warning("7Z格式支持未安装")

    def setup_ui(self):
        """设置用户界面"""
        # 设置按钮样式
        self.setup_button_styles()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建顶部控制区域
        self.create_top_controls(main_frame)

        # 创建中间内容区域
        self.create_middle_content(main_frame)

        # 创建底部状态区域
        self.create_bottom_status(main_frame)

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_top_controls(self, parent):
        """创建顶部控制区域"""
        # 顶部控制框架
        top_frame = ttk.LabelFrame(parent, text="文件选择与操作", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # 第一行：文件选择
        file_frame = ttk.Frame(top_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(file_frame, text="压缩包路径:").pack(side=tk.LEFT)
        
        self.archive_var = tk.StringVar()
        self.archive_entry = ttk.Entry(file_frame, textvariable=self.archive_var, width=60)
        self.archive_entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)

        self.browse_button = ttk.Button(file_frame, text="浏览...", 
                                       command=self.browse_archive,
                                       style="Primary.TButton")
        self.browse_button.pack(side=tk.RIGHT)

        # 第二行：操作按钮
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(fill=tk.X)

        self.preview_button = ttk.Button(button_frame, text="预览匹配文件", 
                                        command=self.preview_files,
                                        style="Primary.TButton")
        self.preview_button.pack(side=tk.LEFT, padx=(0, 10))

        self.process_button = ttk.Button(button_frame, text="开始处理", 
                                        command=self.start_processing,
                                        style="Success.TButton")
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))

        self.undo_button = ttk.Button(button_frame, text="撤销上次操作", 
                                     command=self.undo_last_operation,
                                     style="Warning.TButton")
        self.undo_button.pack(side=tk.LEFT, padx=(0, 10))

        # 右侧：设置按钮
        self.settings_button = ttk.Button(button_frame, text="设置", 
                                         command=self.open_settings)
        self.settings_button.pack(side=tk.RIGHT)

    def create_middle_content(self, parent):
        """创建中间内容区域"""
        # 创建左右分栏
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧：关键字输入
        left_frame = ttk.LabelFrame(content_frame, text="关键字设置", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # 关键字输入说明
        ttk.Label(left_frame, text="请输入搜索关键字，每行一个:").pack(anchor=tk.W, pady=(0, 5))

        # 关键字文本框
        text_frame = ttk.Frame(left_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.keyword_text = tk.Text(text_frame, height=15, wrap=tk.WORD, 
                                   font=('Microsoft YaHei UI', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.keyword_text.yview)
        self.keyword_text.configure(yscrollcommand=scrollbar.set)

        self.keyword_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 关键字操作按钮
        keyword_button_frame = ttk.Frame(left_frame)
        keyword_button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(keyword_button_frame, text="清空", 
                  command=self.clear_keywords,
                  style="Warning.TButton").pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(keyword_button_frame, text="示例", 
                  command=self.load_example_keywords).pack(side=tk.LEFT)

        # 右侧：高级选项
        right_frame = ttk.LabelFrame(content_frame, text="高级选项", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # 操作模式选择
        mode_frame = ttk.LabelFrame(right_frame, text="操作模式", padding=5)
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        self.operation_var = tk.StringVar(value="move")
        ttk.Radiobutton(mode_frame, text="移动文件", variable=self.operation_var, 
                       value="move").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="复制文件", variable=self.operation_var, 
                       value="copy").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="创建链接", variable=self.operation_var, 
                       value="link").pack(anchor=tk.W)

        # 文件类型过滤
        self.file_type_selector = FileTypeSelector(right_frame)

        # 高级过滤选项
        self.advanced_filters = AdvancedFilters(right_frame)

    def create_bottom_status(self, parent):
        """创建底部状态区域"""
        # 状态框架
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding=5)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        # 状态标签
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT)

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          maximum=100, length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))

    # 占位方法，后续实现
    def browse_archive(self):
        """浏览压缩包"""
        pass

    def preview_files(self):
        """预览匹配文件"""
        pass

    def start_processing(self):
        """开始处理"""
        pass

    def undo_last_operation(self):
        """撤销上次操作"""
        pass

    def open_settings(self):
        """打开设置"""
        pass

    def clear_keywords(self):
        """清空关键字"""
        self.keyword_text.delete(1.0, tk.END)

    def load_example_keywords(self):
        """加载示例关键字"""
        examples = ["图片", "文档", "视频", "音频", "压缩包"]
        self.keyword_text.delete(1.0, tk.END)
        self.keyword_text.insert(1.0, "\n".join(examples))

    def on_closing(self):
        """窗口关闭事件"""
        # 保存窗口位置和大小
        try:
            geometry = self.root.geometry()
            self.config_manager.set("user_preferences.window.geometry", geometry)
            self.config_manager.save_config()
        except Exception as e:
            self.logger.error(f"保存窗口配置失败: {e}")

        # 清理临时目录
        if self.temp_extract_dir:
            cleanup_temp_directory(self.temp_extract_dir)

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileFilterApp(root)
    root.mainloop()
