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
        self.root.title("文件筛选与移动工具 v4.0")
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
        self.logger.info("程序启动 v4.0 - 第三阶段")

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

        # 初始化现代化样式
        self.setup_modern_styles()

        # 加载用户配置
        self.load_user_settings()

        self.setup_ui()

    def setup_modern_styles(self):
        """设置现代化样式主题"""
        self.style = ttk.Style()

        # 检测系统主题
        self.is_dark_theme = self.detect_system_theme()

        # 定义Material Design配色方案
        if self.is_dark_theme:
            self.colors = {
                # Material Design Dark Theme
                'primary': '#1976D2',      # Material Blue 700
                'primary_variant': '#1565C0',  # Material Blue 800
                'secondary': '#03DAC6',    # Material Teal 200
                'success': '#4CAF50',      # Material Green 500
                'warning': '#FF9800',      # Material Orange 500
                'error': '#F44336',        # Material Red 500
                'background': '#121212',   # Material Dark Background
                'surface': '#1E1E1E',      # Material Dark Surface
                'surface_variant': '#2D2D2D',  # 表面变体
                'text_primary': '#FFFFFF', # 主要文字
                'text_secondary': '#B3B3B3', # 次要文字
                'text_disabled': '#666666', # 禁用文字
                'border': '#333333',       # 边框色
                'divider': '#2D2D2D',      # 分割线
                'input_bg': '#2D2D2D',     # 输入框背景
                'input_border': '#404040', # 输入框边框
                'hover': '#333333',        # 悬停色
                'pressed': '#404040',      # 按下色
                'selected': '#1976D2',     # 选中色
            }
        else:
            self.colors = {
                # Material Design Light Theme
                'primary': '#1976D2',      # Material Blue 700
                'primary_variant': '#1565C0',  # Material Blue 800
                'secondary': '#03DAC6',    # Material Teal 200
                'success': '#4CAF50',      # Material Green 500
                'warning': '#FF9800',      # Material Orange 500
                'error': '#F44336',        # Material Red 500
                'background': '#FAFAFA',   # Material Light Background
                'surface': '#FFFFFF',      # Material Light Surface
                'surface_variant': '#F5F5F5',  # 表面变体
                'text_primary': '#212121', # 主要文字
                'text_secondary': '#757575', # 次要文字
                'text_disabled': '#BDBDBD', # 禁用文字
                'border': '#E0E0E0',       # 边框色
                'divider': '#E0E0E0',      # 分割线
                'input_bg': '#FFFFFF',     # 输入框背景
                'input_border': '#CCCCCC', # 输入框边框
                'hover': '#F5F5F5',        # 悬停色
                'pressed': '#EEEEEE',      # 按下色
                'selected': '#1976D2',     # 选中色
            }

    def detect_system_theme(self):
        """检测系统主题"""
        # 首先检查用户配置
        user_theme = self.config_manager.get("user_preferences.ui_settings.theme_mode", "auto")

        if user_theme == "dark":
            return True
        elif user_theme == "light":
            return False

        # 自动检测系统主题
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0  # 0 = 深色主题, 1 = 浅色主题
        except:
            return False  # 默认浅色主题

    def toggle_theme(self):
        """切换主题"""
        current_mode = self.config_manager.get("user_preferences.ui_settings.theme_mode", "auto")

        if current_mode == "auto":
            # 从自动切换到深色
            new_mode = "dark"
        elif current_mode == "dark":
            # 从深色切换到浅色
            new_mode = "light"
        else:
            # 从浅色切换到自动
            new_mode = "auto"

        self.config_manager.set("user_preferences.ui_settings.theme_mode", new_mode)
        self.config_manager.save_config()

        # 重新初始化主题
        self.setup_modern_styles()
        self.refresh_ui_theme()

        # 显示提示
        theme_names = {"auto": "自动", "dark": "深色", "light": "浅色"}
        messagebox.showinfo("主题切换", f"已切换到{theme_names[new_mode]}主题")

    def refresh_ui_theme(self):
        """刷新UI主题"""
        # 重新配置按钮样式
        self.setup_button_styles()

        # 更新根窗口背景
        self.root.configure(bg=self.colors['background'])

        # 递归更新所有Frame组件
        self.update_widget_theme(self.root)

    def update_widget_theme(self, widget):
        """递归更新组件主题"""
        try:
            widget_class = widget.winfo_class()

            # 更新Frame组件
            if widget_class in ['Frame', 'Toplevel']:
                widget.configure(bg=self.colors['background'])

            # 更新Label组件
            elif widget_class == 'Label':
                # 根据当前前景色判断是主要还是次要文字
                current_fg = widget.cget('fg')
                if current_fg in ['gray', 'grey', '#666666', '#757575', '#B3B3B3']:
                    widget.configure(fg=self.colors['text_secondary'], bg=self.colors['surface'])
                else:
                    widget.configure(fg=self.colors['text_primary'], bg=self.colors['surface'])

            # 更新Entry组件
            elif widget_class == 'Entry':
                widget.configure(
                    bg=self.colors['input_bg'],
                    fg=self.colors['text_primary'],
                    insertbackground=self.colors['text_primary'],
                    selectbackground=self.colors['selected'],
                    selectforeground='white'
                )

            # 更新Text组件
            elif widget_class == 'Text':
                widget.configure(
                    bg=self.colors['input_bg'],
                    fg=self.colors['text_primary'],
                    insertbackground=self.colors['text_primary'],
                    selectbackground=self.colors['selected'],
                    selectforeground='white'
                )

            # 递归处理子组件
            for child in widget.winfo_children():
                self.update_widget_theme(child)

        except Exception as e:
            # 忽略无法配置的组件
            pass

    def setup_button_styles(self):
        """配置Material Design按钮样式"""
        # Material Design Primary Button
        self.style.configure(
            "Material.TButton",
            background=self.colors['primary'],
            foreground='#FFFFFF',
            borderwidth=0,
            focuscolor='none',
            padding=(24, 12),
            font=('Microsoft YaHei UI', 10, 'normal'),
            relief='flat'
        )

        self.style.map(
            "Material.TButton",
            background=[
                ('active', self.colors['primary_variant']),
                ('pressed', self.colors['primary_variant']),
                ('disabled', self.colors['text_disabled'])
            ],
            foreground=[
                ('active', '#FFFFFF'),
                ('pressed', '#FFFFFF'),
                ('disabled', '#FFFFFF')
            ]
        )

        # Material Design Success Button
        self.style.configure(
            "MaterialSuccess.TButton",
            background=self.colors['success'],
            foreground='#FFFFFF',
            borderwidth=0,
            focuscolor='none',
            padding=(24, 12),
            font=('Microsoft YaHei UI', 10, 'normal'),
            relief='flat'
        )

        self.style.map(
            "MaterialSuccess.TButton",
            background=[
                ('active', '#45A049'),  # 深绿色悬停
                ('pressed', '#3D8B40'),  # 更深绿色按下
                ('disabled', self.colors['text_disabled'])
            ],
            foreground=[
                ('active', '#FFFFFF'),
                ('pressed', '#FFFFFF'),
                ('disabled', '#FFFFFF')
            ]
        )

        # Material Design Warning Button
        self.style.configure(
            "MaterialWarning.TButton",
            background=self.colors['warning'],
            foreground='#FFFFFF',
            borderwidth=0,
            focuscolor='none',
            padding=(20, 10),
            font=('Microsoft YaHei UI', 10, 'normal'),
            relief='flat'
        )

        self.style.map(
            "MaterialWarning.TButton",
            background=[
                ('active', '#F57C00'),  # 深橙色悬停
                ('pressed', '#EF6C00'),  # 更深橙色按下
                ('disabled', self.colors['text_disabled'])
            ],
            foreground=[
                ('active', '#FFFFFF'),
                ('pressed', '#FFFFFF'),
                ('disabled', '#FFFFFF')
            ]
        )

        # Material Design Outlined Button
        self.style.configure(
            "MaterialOutlined.TButton",
            background=self.colors['surface'],
            foreground=self.colors['primary'],
            borderwidth=1,
            focuscolor='none',
            padding=(20, 10),
            font=('Microsoft YaHei UI', 10, 'normal'),
            relief='solid'
        )

        self.style.map(
            "MaterialOutlined.TButton",
            background=[
                ('active', self.colors['hover']),
                ('pressed', self.colors['pressed']),
                ('disabled', self.colors['surface'])
            ],
            foreground=[
                ('active', self.colors['primary']),
                ('pressed', self.colors['primary']),
                ('disabled', self.colors['text_disabled'])
            ],
            bordercolor=[
                ('active', self.colors['primary']),
                ('pressed', self.colors['primary']),
                ('disabled', self.colors['text_disabled'])
            ]
        )

    def load_user_settings(self):
        """加载用户设置"""
        try:
            # 获取屏幕尺寸
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # 计算合适的默认窗口大小 (屏幕的70-80%)
            default_width = min(1200, int(screen_width * 0.75))
            default_height = min(800, int(screen_height * 0.75))
            default_geometry = f"{default_width}x{default_height}"

            # 加载用户保存的窗口几何信息，如果没有则使用智能默认值
            geometry = self.config_manager.get("user_preferences.ui_settings.window_geometry", default_geometry)

            # 验证几何信息是否合理
            try:
                # 解析几何字符串
                if 'x' in geometry and '+' not in geometry and '-' not in geometry:
                    width, height = map(int, geometry.split('x'))
                    # 确保窗口大小在合理范围内
                    width = max(800, min(width, screen_width - 100))  # 最小800px，最大不超过屏幕
                    height = max(600, min(height, screen_height - 100))  # 最小600px，最大不超过屏幕
                    geometry = f"{width}x{height}"
                else:
                    geometry = default_geometry
            except:
                geometry = default_geometry

            self.root.geometry(geometry)

            # 设置最小窗口大小
            self.root.minsize(800, 600)

            # 居中显示窗口
            self.center_window()

            self.logger.info(f"用户设置加载完成，窗口大小: {geometry}")
        except Exception as e:
            self.logger.error(f"加载用户设置失败: {e}")

    def center_window(self):
        """将窗口居中显示"""
        try:
            self.root.update_idletasks()

            # 获取窗口尺寸
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()

            # 获取屏幕尺寸
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # 计算居中位置
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            # 确保窗口不会超出屏幕边界
            x = max(0, min(x, screen_width - window_width))
            y = max(0, min(y, screen_height - window_height))

            # 设置窗口位置
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        except Exception as e:
            self.logger.debug(f"窗口居中失败: {e}")

    def save_user_settings(self):
        """保存用户设置"""
        try:
            # 保存窗口几何信息
            self.config_manager.set("user_preferences.ui_settings.window_geometry", self.root.geometry())

            # 保存其他设置
            if hasattr(self, 'operation_var'):
                self.config_manager.set("user_preferences.operation_mode", self.operation_var.get())

            if hasattr(self, 'advanced_filters'):
                filters = self.advanced_filters.get_filters()
                self.config_manager.set("user_preferences.regex_mode", filters.get("use_regex", False))

            # 保存关键字历史
            keywords = self.get_keywords()
            if keywords:
                self.config_manager.add_keyword_to_history(keywords)

            # 保存当前压缩包目录（如果有的话）
            current_archive = self.archive_var.get()
            if current_archive and os.path.exists(current_archive):
                archive_directory = os.path.dirname(current_archive)
                self.config_manager.set("user_preferences.ui_settings.last_archive_directory", archive_directory)

            self.config_manager.save_config()
            self.logger.info("用户设置保存完成")
        except Exception as e:
            self.logger.error(f"保存用户设置失败: {e}")

    def setup_ui(self):
        """设置现代化用户界面"""
        # 配置按钮样式
        self.setup_button_styles()

        # 设置根窗口背景色
        self.root.configure(bg=self.colors['background'])

        # 创建主容器
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 创建标题栏
        self.setup_header(main_container)

        # 创建主内容区域
        content_frame = tk.Frame(main_container, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # 创建左右分栏 - 重新布局功能区域
        main_paned = ttk.PanedWindow(content_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        # 左侧面板 - 30%宽度
        left_frame = tk.Frame(main_paned, bg=self.colors['background'])
        main_paned.add(left_frame, weight=30)

        # 右侧面板 - 70%宽度
        right_frame = tk.Frame(main_paned, bg=self.colors['background'])
        main_paned.add(right_frame, weight=70)

        # 设置左侧功能
        self.setup_left_functions(left_frame)

        # 设置右侧功能
        self.setup_right_functions(right_frame)

        # 创建隐藏的日志文本框用于内部日志记录
        self.log_text = tk.Text(self.root, wrap=tk.WORD, font=("Consolas", 9))

    def setup_left_functions(self, parent):
        """设置左侧功能区域"""
        # 文件选择和关键字设置
        self.setup_file_selection_card(parent)
        self.setup_keywords_card(parent)

    def setup_right_functions(self, parent):
        """设置右侧功能区域"""
        # 高级过滤和处理状态
        self.setup_filters_card(parent)
        self.setup_actions_card(parent)

    def setup_header(self, parent):
        """设置标题栏"""
        header_frame = tk.Frame(parent, bg=self.colors['surface'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        # 添加轻微阴影效果（通过边框模拟）
        header_frame.configure(relief='flat', bd=1, highlightbackground=self.colors['border'])

        # 标题区域
        title_frame = tk.Frame(header_frame, bg=self.colors['surface'])
        title_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        # 应用图标和标题
        title_label = tk.Label(title_frame,
                              text=icon_manager.get_button_text('package', 'FileMover v4.0'),
                              font=('Microsoft YaHei UI', 20, 'bold'),
                              fg=self.colors['primary'],
                              bg=self.colors['surface'])
        title_label.pack(side=tk.LEFT)

        # 副标题
        subtitle_label = tk.Label(title_frame,
                                text="现代化文件筛选与移动工具",
                                font=('Microsoft YaHei UI', 11),
                                fg=self.colors['text_secondary'],
                                bg=self.colors['surface'])
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0), pady=(5, 0))

        # 操作控制按钮区域
        action_frame = tk.Frame(title_frame, bg=self.colors['surface'])
        action_frame.pack(side=tk.RIGHT)

        # 主题切换按钮
        theme_button = ttk.Button(action_frame,
                                text=icon_manager.get_button_text('theme', '主题'),
                                style="MaterialOutlined.TButton",
                                command=self.toggle_theme)
        theme_button.pack(side=tk.RIGHT, padx=(0, 10))

        # 预览按钮
        self.preview_button = ttk.Button(action_frame,
                                       text=icon_manager.get_button_text('preview', '预览匹配文件'),
                                       style="MaterialOutlined.TButton",
                                       command=self.preview_files)
        self.preview_button.pack(side=tk.RIGHT, padx=(0, 10))

        # 开始处理按钮
        self.start_button = ttk.Button(action_frame,
                                     text=icon_manager.get_button_text('rocket', '开始处理'),
                                     style="MaterialSuccess.TButton",
                                     command=self.start_processing)
        self.start_button.pack(side=tk.RIGHT)

    def setup_footer(self, parent):
        """设置底部状态栏"""
        footer_frame = tk.Frame(parent, bg=self.colors['surface'], height=50)
        footer_frame.pack(fill=tk.X, pady=(10, 0), side=tk.BOTTOM)
        footer_frame.pack_propagate(False)

        # 添加边框
        footer_frame.configure(relief='flat', bd=1, highlightbackground=self.colors['border'])

        # 状态信息
        status_frame = tk.Frame(footer_frame, bg=self.colors['surface'])
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 版权信息
        copyright_label = tk.Label(status_frame,
                                 text="© 2024 FileMover - 专业文件处理工具",
                                 font=('Microsoft YaHei UI', 9),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['surface'])
        copyright_label.pack(side=tk.LEFT)

        # 状态指示器
        self.status_indicator = tk.Label(status_frame,
                                       text="🟢 就绪",
                                       font=('Microsoft YaHei UI', 9),
                                       fg=self.colors['success'],
                                       bg=self.colors['surface'])
        self.status_indicator.pack(side=tk.RIGHT)



    def create_card_frame(self, parent, title, icon=""):
        """创建现代化卡片框架"""
        # 卡片容器
        card_container = tk.Frame(parent, bg=self.colors['background'])
        card_container.pack(fill="x", pady=(0, 20))

        # 卡片主体
        card_frame = tk.Frame(card_container,
                            bg=self.colors['surface'],
                            relief='flat',
                            bd=1,
                            highlightbackground=self.colors['border'],
                            highlightthickness=1)
        card_frame.pack(fill="x", padx=5, pady=2)

        # 卡片标题栏
        title_frame = tk.Frame(card_frame, bg=self.colors['surface'], height=45)
        title_frame.pack(fill="x", padx=20, pady=(15, 10))
        title_frame.pack_propagate(False)

        # 标题图标和文字
        title_label = tk.Label(title_frame,
                             text=f"{icon} {title}",
                             font=('Microsoft YaHei UI', 12, 'bold'),
                             fg=self.colors['text_primary'],
                             bg=self.colors['surface'])
        title_label.pack(side=tk.LEFT, anchor='w')

        # 卡片内容区域
        content_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        return content_frame

    def setup_file_selection_card(self, parent):
        """设置文件选择卡片"""
        content_frame = self.create_card_frame(parent, "文件选择", "📁")

        # 文件路径输入区域
        path_label = tk.Label(content_frame,
                            text="压缩包路径:",
                            font=('Microsoft YaHei UI', 10),
                            fg=self.colors['text_primary'],
                            bg=self.colors['surface'])
        path_label.pack(anchor="w", pady=(0, 8))

        # 输入框容器
        input_container = tk.Frame(content_frame, bg=self.colors['surface'])
        input_container.pack(fill="x", pady=(0, 10))

        # 文件路径输入框
        self.archive_var = tk.StringVar()
        entry_frame = tk.Frame(input_container,
                             bg=self.colors['input_bg'],
                             relief='solid',
                             bd=1,
                             highlightbackground=self.colors['input_border'])
        entry_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.archive_entry = tk.Entry(entry_frame,
                                    textvariable=self.archive_var,
                                    font=('Microsoft YaHei UI', 10),
                                    bg=self.colors['input_bg'],
                                    fg=self.colors['text_primary'],
                                    relief='flat',
                                    bd=0,
                                    insertbackground=self.colors['text_primary'],
                                    selectbackground=self.colors['selected'],
                                    selectforeground='white')
        self.archive_entry.pack(fill="both", expand=True, padx=8, pady=8)

        # 浏览按钮
        browse_btn = ttk.Button(input_container,
                              text=icon_manager.get_button_text('folder', '浏览'),
                              style="Material.TButton",
                              command=self.select_archive)
        browse_btn.pack(side="right")

        # 拖拽提示
        self.drag_hint_label = tk.Label(content_frame,
                                      text="💡 提示：可以直接拖拽压缩包文件到上方输入框",
                                      font=('Microsoft YaHei UI', 9),
                                      fg=self.colors['text_secondary'],
                                      bg=self.colors['surface'])
        self.drag_hint_label.pack(anchor="w", pady=(0, 8))

        # 文件信息显示
        self.file_info_label = tk.Label(content_frame,
                                      text="",
                                      font=('Microsoft YaHei UI', 10),
                                      fg=self.colors['success'],
                                      bg=self.colors['surface'])
        self.file_info_label.pack(anchor="w")

        # 绑定拖拽事件
        self.setup_drag_drop_events(entry_frame)
        self.setup_drag_drop_events(self.archive_entry)

    def setup_keywords_card(self, parent):
        """设置关键字设置卡片"""
        content_frame = self.create_card_frame(parent, "关键字设置", "🔍")

        # 说明文字
        desc_label = tk.Label(content_frame,
                            text="输入关键字进行文件筛选 (每行一个关键字):",
                            font=('Microsoft YaHei UI', 10),
                            fg=self.colors['text_primary'],
                            bg=self.colors['surface'])
        desc_label.pack(anchor="w", pady=(0, 10))

        # 关键字输入区域
        text_container = tk.Frame(content_frame, bg=self.colors['surface'])
        text_container.pack(fill="both", expand=True)

        # 文本框容器
        text_frame = tk.Frame(text_container,
                            bg=self.colors['input_bg'],
                            relief='solid',
                            bd=1,
                            highlightbackground=self.colors['input_border'])
        text_frame.pack(fill="both", expand=True)

        # 关键字文本框
        self.keyword_text = tk.Text(text_frame,
                                  height=4,
                                  wrap=tk.WORD,
                                  font=('Microsoft YaHei UI', 10),
                                  bg=self.colors['input_bg'],
                                  fg=self.colors['text_primary'],
                                  relief='flat',
                                  bd=0,
                                  padx=8,
                                  pady=8,
                                  insertbackground=self.colors['text_primary'],
                                  selectbackground=self.colors['selected'],
                                  selectforeground='white')

        # 滚动条
        keyword_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.keyword_text.yview)
        self.keyword_text.configure(yscrollcommand=keyword_scrollbar.set)

        self.keyword_text.pack(side="left", fill="both", expand=True)
        keyword_scrollbar.pack(side="right", fill="y")

        # 快速操作按钮
        button_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        button_frame.pack(fill="x", pady=(10, 0))

        # 清空关键字按钮
        clear_keywords_btn = ttk.Button(button_frame,
                                      text=icon_manager.get_button_text('clear', '清空'),
                                      style="MaterialWarning.TButton",
                                      command=lambda: self.keyword_text.delete(1.0, tk.END))
        clear_keywords_btn.pack(side="left")

        # 绑定Ctrl+Enter快捷键
        self.keyword_text.bind('<Control-Return>', lambda e: self.start_processing())

    def setup_filters_card(self, parent):
        """设置过滤器卡片"""
        content_frame = self.create_card_frame(parent, "高级过滤", "⚙️")

        # 操作模式选择
        mode_label = tk.Label(content_frame,
                            text="操作模式:",
                            font=('Microsoft YaHei UI', 10, 'bold'),
                            fg=self.colors['text_primary'],
                            bg=self.colors['surface'])
        mode_label.pack(anchor="w", pady=(0, 8))

        mode_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        mode_frame.pack(fill="x", pady=(0, 15))

        self.operation_var = tk.StringVar(value=self.config_manager.get("user_preferences.operation_mode", "move"))

        # 操作模式单选按钮
        move_rb = tk.Radiobutton(mode_frame, text=icon_manager.get_button_text('move', '移动文件'),
                               variable=self.operation_var, value="move",
                               font=('Microsoft YaHei UI', 10),
                               fg=self.colors['text_primary'],
                               bg=self.colors['surface'],
                               selectcolor=self.colors['primary'],
                               activebackground=self.colors['surface'],
                               activeforeground=self.colors['text_primary'])
        move_rb.pack(side=tk.LEFT, padx=(0, 20))

        copy_rb = tk.Radiobutton(mode_frame, text=icon_manager.get_button_text('copy', '复制文件'),
                               variable=self.operation_var, value="copy",
                               font=('Microsoft YaHei UI', 10),
                               fg=self.colors['text_primary'],
                               bg=self.colors['surface'],
                               selectcolor=self.colors['primary'],
                               activebackground=self.colors['surface'],
                               activeforeground=self.colors['text_primary'])
        copy_rb.pack(side=tk.LEFT, padx=(0, 20))

        link_rb = tk.Radiobutton(mode_frame, text=icon_manager.get_button_text('link', '创建链接'),
                               variable=self.operation_var, value="link",
                               font=('Microsoft YaHei UI', 10),
                               fg=self.colors['text_primary'],
                               bg=self.colors['surface'],
                               selectcolor=self.colors['primary'],
                               activebackground=self.colors['surface'],
                               activeforeground=self.colors['text_primary'])
        link_rb.pack(side=tk.LEFT)

        # 高级过滤器
        self.advanced_filters = AdvancedFilters(content_frame, self.colors)
        self.advanced_filters.frame.pack(fill="x", pady=(0, 10))

        # 文件类型选择器
        file_type_presets = self.config_manager.get_file_type_presets()
        self.file_type_selector = FileTypeSelector(content_frame, file_type_presets, self.on_filter_changed)
        self.file_type_selector.frame.pack(fill="x")

    def setup_actions_card(self, parent):
        """设置操作控制卡片"""
        content_frame = self.create_card_frame(parent, "处理状态", "📊")

        # 进度显示区域
        self.setup_progress_area(content_frame)

    def insert_example_keywords(self):
        """插入示例关键字"""
        example_keywords = "图片\n文档\n视频\n音频\n压缩包"
        self.keyword_text.delete(1.0, tk.END)
        self.keyword_text.insert(1.0, example_keywords)

        # 加载用户偏好设置
        self.load_user_preferences()

    def setup_file_selection_area(self, parent):
        """设置集成的文件选择区域"""
        # 主文件选择框架
        file_frame = ttk.LabelFrame(parent, text="压缩包选择", padding="10")
        file_frame.pack(fill="x", pady=(0, 10))

        # 文件路径输入区域
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(input_frame, text="文件路径:").pack(anchor="w", pady=(0, 5))

        path_frame = ttk.Frame(input_frame)
        path_frame.pack(fill="x")

        self.archive_var = tk.StringVar()

        # 创建支持拖拽的输入框容器
        entry_container = tk.Frame(path_frame, relief="sunken", bd=1)
        entry_container.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.archive_entry = ttk.Entry(entry_container, textvariable=self.archive_var, font=("TkDefaultFont", 10))
        self.archive_entry.pack(fill="both", expand=True, padx=1, pady=1)

        ttk.Button(path_frame, text="浏览", command=self.select_archive).pack(side="right")

        # 拖拽提示标签（在输入框下方）
        self.drag_hint_label = ttk.Label(input_frame,
                                       text="💡 提示：可以直接拖拽压缩包文件到上方输入框",
                                       font=("TkDefaultFont", 8),
                                       foreground="gray")
        self.drag_hint_label.pack(anchor="w", pady=(3, 0))

        # 文件信息显示
        self.file_info_label = ttk.Label(file_frame, text="", foreground="blue")
        self.file_info_label.pack(anchor="w", pady=(8, 0))

        # 绑定拖拽事件到输入框
        self.setup_drag_drop_events(entry_container)
        self.setup_drag_drop_events(self.archive_entry)

    def setup_drag_drop_events(self, widget):
        """设置拖拽事件"""
        def on_drag_enter(event):
            # 输入框获得焦点时的视觉反馈
            if hasattr(widget, 'config'):
                try:
                    widget.config(relief="solid", highlightbackground="#4CAF50")
                except:
                    pass
            self.drag_hint_label.config(text="📦 释放文件到输入框", foreground="#4CAF50")

        def on_drag_leave(event):
            # 恢复正常状态
            if hasattr(widget, 'config'):
                try:
                    widget.config(relief="sunken", highlightbackground="")
                except:
                    pass
            self.drag_hint_label.config(text="💡 提示：可以直接拖拽压缩包文件到上方输入框", foreground="gray")

        def on_drop(event):
            # 恢复正常状态
            if hasattr(widget, 'config'):
                try:
                    widget.config(relief="sunken", highlightbackground="")
                except:
                    pass
            self.drag_hint_label.config(text="💡 提示：可以直接拖拽压缩包文件到上方输入框", foreground="gray")

            # 处理拖拽的文件
            files = self.root.tk.splitlist(event.data)
            if files:
                file_path = files[0]
                if file_path.lower().endswith(('.zip', '.rar', '.7z')):
                    self.on_archive_dropped(file_path)
                else:
                    messagebox.showwarning("文件类型错误", "请选择压缩包文件 (.zip, .rar, .7z)")

        # 绑定点击事件打开文件选择对话框
        widget.bind("<Button-1>", lambda e: self.select_archive())

    def setup_progress_area(self, parent):
        """设置美化的进度显示区域"""
        # 状态信息区域
        status_frame = tk.Frame(parent, bg=self.colors['surface'])
        status_frame.pack(fill="x", pady=(0, 15))

        # 状态图标和文本
        self.status_icon_label = tk.Label(status_frame,
                                        text="⚪",
                                        font=('Microsoft YaHei UI', 16),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['surface'])
        self.status_icon_label.pack(side="left", padx=(0, 10))

        status_text_frame = tk.Frame(status_frame, bg=self.colors['surface'])
        status_text_frame.pack(side="left", fill="x", expand=True)

        self.progress_var = tk.StringVar(value="就绪")
        self.status_text_label = tk.Label(status_text_frame,
                                        textvariable=self.progress_var,
                                        font=('Microsoft YaHei UI', 12, 'bold'),
                                        fg=self.colors['text_primary'],
                                        bg=self.colors['surface'])
        self.status_text_label.pack(anchor="w")

        # 详细信息标签
        self.detail_info_label = tk.Label(status_text_frame,
                                        text="",
                                        font=('Microsoft YaHei UI', 9),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['surface'])
        self.detail_info_label.pack(anchor="w", pady=(2, 0))

        # 进度条容器
        progress_container = tk.Frame(parent, bg=self.colors['surface'])
        progress_container.pack(fill="x")

        # 主进度条
        self.progress_bar = ttk.Progressbar(
            progress_container,
            mode='indeterminate',
            style="Material.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill="x", pady=(10, 0))

        # 配置进度条样式
        self.setup_progress_bar_style()

    def setup_progress_bar_style(self):
        """设置Material Design进度条样式"""
        try:
            # 创建自定义进度条样式
            self.style.configure(
                "Material.Horizontal.TProgressbar",
                troughcolor=self.colors['surface_variant'],
                background=self.colors['primary'],
                lightcolor=self.colors['primary'],
                darkcolor=self.colors['primary_variant'],
                borderwidth=0,
                relief="flat"
            )

            # 设置进度条动画颜色
            self.style.map(
                "Material.Horizontal.TProgressbar",
                background=[('active', self.colors['primary_variant'])]
            )
        except Exception as e:
            self.logger.debug(f"设置进度条样式失败: {e}")

    def update_progress_status(self, status, icon_name="ready", detail=""):
        """更新进度状态"""
        self.progress_var.set(status)
        icon = icon_manager.get_icon(icon_name, "⚪")
        self.status_icon_label.config(text=icon)
        self.detail_info_label.config(text=detail)



    def setup_info_card(self, parent):
        """设置应用信息卡片"""
        content_frame = self.create_card_frame(parent, "应用信息", "ℹ️")

        # 应用图标和名称
        app_header = tk.Frame(content_frame, bg=self.colors['surface'])
        app_header.pack(fill="x", pady=(0, 15))

        app_icon = tk.Label(app_header,
                          text="📦",
                          font=('Microsoft YaHei UI', 24),
                          bg=self.colors['surface'])
        app_icon.pack(side="left", padx=(0, 15))

        app_info = tk.Frame(app_header, bg=self.colors['surface'])
        app_info.pack(side="left", fill="x", expand=True)

        app_name = tk.Label(app_info,
                          text="FileMover v4.0",
                          font=('Microsoft YaHei UI', 14, 'bold'),
                          fg=self.colors['primary'],
                          bg=self.colors['surface'])
        app_name.pack(anchor="w")

        app_desc = tk.Label(app_info,
                          text="现代化文件筛选与移动工具",
                          font=('Microsoft YaHei UI', 10),
                          fg=self.colors['text_secondary'],
                          bg=self.colors['surface'])
        app_desc.pack(anchor="w")

        # 功能特性
        features_label = tk.Label(content_frame,
                                text="✨ 主要功能:",
                                font=('Microsoft YaHei UI', 10, 'bold'),
                                fg=self.colors['text_primary'],
                                bg=self.colors['surface'])
        features_label.pack(anchor="w", pady=(0, 8))

        features = [
            "🔍 智能关键字搜索",
            "📁 多种操作模式",
            "⚙️ 高级过滤选项",
            "🎯 精确文件匹配",
            "🚀 批量文件处理"
        ]

        for feature in features:
            feature_label = tk.Label(content_frame,
                                   text=feature,
                                   font=('Microsoft YaHei UI', 9),
                                   fg=self.colors['text_secondary'],
                                   bg=self.colors['surface'])
            feature_label.pack(anchor="w", pady=(2, 0))

    def setup_stats_card(self, parent):
        """设置统计信息卡片"""
        content_frame = self.create_card_frame(parent, "统计信息", "📈")

        # 统计数据容器
        stats_container = tk.Frame(content_frame, bg=self.colors['surface'])
        stats_container.pack(fill="x")

        # 创建统计项
        self.create_stat_item(stats_container, "处理文件", "0", "📄")
        self.create_stat_item(stats_container, "匹配成功", "0", "✅")
        self.create_stat_item(stats_container, "处理时间", "0s", "⏱️")

        # 快速操作
        quick_actions = tk.Frame(content_frame, bg=self.colors['surface'])
        quick_actions.pack(fill="x", pady=(15, 0))

        quick_label = tk.Label(quick_actions,
                             text="🔧 快速操作:",
                             font=('Microsoft YaHei UI', 10, 'bold'),
                             fg=self.colors['text_primary'],
                             bg=self.colors['surface'])
        quick_label.pack(anchor="w", pady=(0, 8))

        # 快速操作按钮
        action_buttons = tk.Frame(quick_actions, bg=self.colors['surface'])
        action_buttons.pack(fill="x")

        help_btn = ttk.Button(action_buttons,
                            text="❓ 帮助",
                            style="Modern.TButton",
                            command=self.show_help)
        help_btn.pack(fill="x", pady=(0, 5))

        about_btn = ttk.Button(action_buttons,
                             text="ℹ️ 关于",
                             style="Modern.TButton",
                             command=self.show_about)
        about_btn.pack(fill="x")

    def create_stat_item(self, parent, label, value, icon):
        """创建统计项"""
        item_frame = tk.Frame(parent, bg=self.colors['surface'])
        item_frame.pack(fill="x", pady=(0, 8))

        icon_label = tk.Label(item_frame,
                            text=icon,
                            font=('Microsoft YaHei UI', 12),
                            bg=self.colors['surface'])
        icon_label.pack(side="left", padx=(0, 8))

        text_frame = tk.Frame(item_frame, bg=self.colors['surface'])
        text_frame.pack(side="left", fill="x", expand=True)

        label_widget = tk.Label(text_frame,
                              text=label,
                              font=('Microsoft YaHei UI', 9),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['surface'])
        label_widget.pack(anchor="w")

        value_widget = tk.Label(text_frame,
                              text=value,
                              font=('Microsoft YaHei UI', 11, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['surface'])
        value_widget.pack(anchor="w")

        # 保存引用以便更新
        setattr(self, f"stat_{label.replace(' ', '_').lower()}_value", value_widget)

    def show_help(self):
        """显示帮助信息"""
        help_text = """FileMover 使用帮助

🔍 基本使用:
1. 选择压缩包文件
2. 输入搜索关键字
3. 选择操作模式
4. 点击预览或开始处理

⚙️ 高级功能:
• 正则表达式搜索
• 文件类型过滤
• 大小和日期过滤
• 批量关键字处理

🚀 快捷键:
• Ctrl+Enter: 开始处理
• F5: 刷新界面
• Ctrl+L: 清空输入"""

        messagebox.showinfo("使用帮助", help_text)

    def show_about(self):
        """显示关于信息"""
        about_text = """FileMover v4.0

📦 现代化文件筛选与移动工具

✨ 特性:
• 智能文件搜索和分类
• 现代化用户界面
• 多种操作模式支持
• 高级过滤功能

👨‍💻 开发者: @m6773
📅 版本: 4.0.0
🏠 项目地址: https://gitee.com/m6773/FileMover

© 2024 FileMover - 专业文件处理工具"""

        messagebox.showinfo("关于 FileMover", about_text)

    def open_settings(self):
        """打开设置对话框"""
        messagebox.showinfo("设置", "设置功能正在开发中...")

    def load_user_preferences(self):
        """加载用户偏好设置"""
        try:
            # 设置正则表达式模式
            regex_mode = self.config_manager.get("user_preferences.regex_mode", False)
            if hasattr(self.advanced_filters, 'regex_var'):
                self.advanced_filters.regex_var.set(regex_mode)
        except Exception as e:
            self.logger.error(f"加载用户偏好失败: {e}")



    def on_filter_changed(self):
        """过滤器改变事件"""
        # 可以在这里添加实时预览等功能
        pass

    def on_archive_dropped(self, file_path: str):
        """处理拖拽的压缩包文件"""
        self.archive_var.set(file_path)

        # 更新文件信息显示
        file_name = os.path.basename(file_path)
        file_size = self.format_file_size(os.path.getsize(file_path))
        self.file_info_label.config(text=f"✅ {file_name} ({file_size})")

        # 更新提示信息
        self.drag_hint_label.config(text=f"📦 已选择: {file_name}", foreground="#4CAF50")

        self.log_message(f"通过拖拽选择了压缩包: {file_name}")

    def format_file_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"

    def clear_log(self):
        """清空日志 - 已简化"""
        if hasattr(self, 'log_text'):
            self.log_text.delete(1.0, tk.END)

    def save_log(self):
        """保存日志到文件 - 已简化"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                title="保存日志",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if filename and hasattr(self, 'log_text'):
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("保存成功", f"日志已保存到:\n{filename}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存日志失败: {str(e)}")

    def select_archive(self):
        """选择压缩包"""
        # 获取上次使用的目录
        last_directory = self.config_manager.get("user_preferences.ui_settings.last_archive_directory", "")
        initial_dir = last_directory if last_directory and os.path.exists(last_directory) else None

        archive_path = filedialog.askopenfilename(
            title="选择压缩包",
            initialdir=initial_dir,
            filetypes=[
                ("压缩包文件", "*.zip;*.rar;*.7z"),
                ("ZIP文件", "*.zip"),
                ("RAR文件", "*.rar"),
                ("7Z文件", "*.7z"),
                ("所有文件", "*.*")
            ]
        )
        if archive_path:
            # 保存选择的目录到配置
            archive_directory = os.path.dirname(archive_path)
            self.config_manager.set("user_preferences.ui_settings.last_archive_directory", archive_directory)

            # 检查是否是新的压缩包
            old_archive = self.archive_var.get()
            if old_archive and old_archive != archive_path:
                # 导入新压缩包时自动清理
                from utils import auto_cleanup_on_new_archive
                try:
                    auto_cleanup_on_new_archive(archive_path, self.extracted_dir)
                    self.log_message("检测到新压缩包，已自动清理extracted_files目录")
                except Exception as e:
                    self.log_message(f"自动清理警告: {e}", "WARNING")

            self.archive_var.set(archive_path)

            # 更新文件信息显示
            file_name = os.path.basename(archive_path)
            file_size = self.format_file_size(os.path.getsize(archive_path))
            self.file_info_label.config(text=f"✅ {file_name} ({file_size})")

            # 更新提示信息
            self.drag_hint_label.config(text=f"📦 已选择: {file_name}", foreground="#4CAF50")

            self.log_message(f"已选择压缩包: {file_name}")

    def clear_inputs(self):
        """清空输入"""
        self.archive_var.set("")
        self.keyword_text.delete(1.0, tk.END)
        self.update_progress_status("就绪", "ready", "")

        # 清理界面状态
        self.file_info_label.config(text="")
        self.drag_hint_label.config(text="💡 提示：可以直接拖拽压缩包文件到上方输入框", foreground="gray")

        # 清理临时目录
        if self.temp_extract_dir:
            cleanup_temp_directory(self.temp_extract_dir)
            self.temp_extract_dir = None

    def get_keywords(self):
        """获取关键字列表"""
        keywords_text = self.keyword_text.get(1.0, tk.END).strip()
        if not keywords_text:
            return []

        # 按行分割关键字
        keywords = [line.strip() for line in keywords_text.split('\n') if line.strip()]
        return keywords

    def get_current_filters(self):
        """获取当前过滤器设置"""
        filters = self.advanced_filters.get_filters()

        # 添加文件类型过滤
        if self.file_type_selector.is_enabled():
            filters["file_types"] = self.file_type_selector.get_selected_types()
        else:
            filters["file_types"] = []

        return filters

    def validate_inputs(self):
        """验证输入"""
        archive_path = self.archive_var.get().strip()
        keywords = self.get_keywords()

        if not archive_path:
            messagebox.showwarning("输入错误", "请选择压缩包")
            return False

        if not keywords:
            messagebox.showwarning("输入错误", "请输入关键字")
            return False

        if not validate_archive(archive_path):
            messagebox.showerror("错误", "选择的压缩包无效或不支持的格式")
            return False

        # 验证正则表达式
        filters = self.get_current_filters()
        if filters.get("use_regex", False):
            valid, error = self.advanced_filters.validate_regex_keywords(keywords)
            if not valid:
                messagebox.showerror("正则表达式错误", error)
                return False

        return True

    def log_message(self, message, level="INFO"):
        """添加日志消息 - 仅记录到文件和内部日志"""
        # 记录到内部日志文本框（隐藏）
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)

        # 记录到日志文件
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "DEBUG":
            self.logger.debug(message)
        else:
            self.logger.info(message)

    def preview_files(self):
        """预览匹配的文件数量"""
        if not self.validate_inputs():
            return

        archive_path = self.archive_var.get().strip()
        keywords = self.get_keywords()

        try:
            self.update_progress_status("正在预览...", "search", "分析压缩包内容")
            self.progress_bar.start()

            # 在后台线程中执行预览
            thread = threading.Thread(target=self._preview_files_thread, args=(archive_path, keywords))
            thread.daemon = True
            thread.start()

        except Exception as e:
            self.progress_bar.stop()
            self.update_progress_status("预览失败", "error", f"错误: {str(e)}")
            messagebox.showerror("错误", f"预览失败: {str(e)}")

    def _preview_files_thread(self, archive_path, keywords):
        """在后台线程中预览文件"""
        try:
            # 获取过滤器设置
            filters = self.get_current_filters()

            matched_count, unmatched_count = count_matching_files_in_archive(archive_path, keywords, filters)
            self.root.after(0, self._preview_complete, matched_count, unmatched_count, None)
        except Exception as e:
            self.root.after(0, self._preview_complete, 0, 0, str(e))

    def _preview_complete(self, matched_count, unmatched_count, error):
        """预览完成回调"""
        self.progress_bar.stop()

        if error:
            self.update_progress_status("预览失败", "error", f"错误: {error}")
            self.log_message(f"预览失败: {error}", "ERROR")
            messagebox.showerror("预览失败", f"预览失败: {error}")
        else:
            total_count = matched_count + unmatched_count
            self.update_progress_status("预览完成", "success", f"总计 {total_count} 个文件，命中 {matched_count} 个")
            self.log_message(f"预览结果: 总文件 {total_count} 个，命中 {matched_count} 个，未命中 {unmatched_count} 个")
            messagebox.showinfo("预览结果",
                               f"预览完成！\n\n"
                               f"总文件数: {total_count}\n"
                               f"命中关键字: {matched_count} 个\n"
                               f"未命中关键字: {unmatched_count} 个")

    def start_processing(self):
        """开始处理文件"""
        if not self.validate_inputs():
            return

        archive_path = self.archive_var.get().strip()
        keywords = self.get_keywords()
        operation = self.operation_var.get()
        filters = self.get_current_filters()

        # 确认操作
        operation_text = {"move": "移动", "copy": "复制", "link": "创建链接"}[operation]
        filter_info = []

        if filters.get("use_regex"):
            filter_info.append("使用正则表达式")
        if filters.get("file_types"):
            filter_info.append(f"文件类型: {', '.join(filters['file_types'][:3])}...")

        confirm_msg = f"将要解压压缩包 '{os.path.basename(archive_path)}' 并搜索文件，"
        confirm_msg += f"然后{operation_text}到项目目录。\n\n"
        confirm_msg += f"关键字列表:\n{chr(10).join(keywords[:5])}"
        if len(keywords) > 5:
            confirm_msg += f"\n... 还有 {len(keywords) - 5} 个关键字"

        if filter_info:
            confirm_msg += f"\n\n过滤条件: {', '.join(filter_info)}"

        confirm_msg += "\n\n确定要继续吗？"

        result = messagebox.askyesno("确认操作", confirm_msg)
        if not result:
            return

        # 保存用户设置
        self.save_user_settings()

        # 在新线程中执行处理
        self.start_button.config(state='disabled')
        self.progress_bar.start()
        self.update_progress_status("正在处理...", "processing", "解压并分类文件")

        thread = threading.Thread(target=self.process_files, args=(archive_path, keywords, filters, operation))
        thread.daemon = True
        thread.start()

    def process_files(self, archive_path, keywords, filters, operation):
        """在后台线程中处理文件"""
        try:
            self.log_message(f"开始解压压缩包: {os.path.basename(archive_path)}")
            self.log_message(f"搜索关键字: {chr(10).join(keywords)}")
            self.log_message(f"操作模式: {operation}")

            if filters.get("use_regex"):
                self.log_message("使用正则表达式模式")
            if filters.get("file_types"):
                self.log_message(f"文件类型过滤: {', '.join(filters['file_types'])}")

            matched_files, unmatched_files, matched_dir, unmatched_dir = find_and_move_files_from_archive(
                archive_path, keywords, filters, operation, self.undo_manager, self.password_manager, self.config_manager
            )

            # 在主线程中更新UI
            self.root.after(0, self.processing_complete, matched_files, unmatched_files, matched_dir, unmatched_dir, operation, None)

        except Exception as e:
            self.root.after(0, self.processing_complete, [], [], "", "", operation, str(e))

    def processing_complete(self, matched_files, unmatched_files, matched_dir, unmatched_dir, operation, error):
        """处理完成后的回调"""
        self.progress_bar.stop()
        self.start_button.config(state='normal')

        if error:
            self.update_progress_status("处理失败", "error", f"错误: {error}")
            self.log_message(f"错误: {error}", "ERROR")
            messagebox.showerror("处理失败", f"操作失败: {error}")
        else:
            total_files = len(matched_files) + len(unmatched_files)
            operation_text = {"move": "移动", "copy": "复制", "link": "链接"}[operation]
            self.update_progress_status(f"处理完成", "done", f"总计 {total_files} 个文件已{operation_text}")

            # 记录详细结果
            self.log_message(f"文件处理完成 ({operation_text}):")
            self.log_message(f"  命中文件: {len(matched_files)} 个 -> {os.path.basename(matched_dir)}")
            self.log_message(f"  未命中文件: {len(unmatched_files)} 个 -> {os.path.basename(unmatched_dir)}")

            if matched_files:
                self.log_message(f"  命中文件列表: {', '.join(matched_files[:5])}")
                if len(matched_files) > 5:
                    self.log_message(f"    ... 还有 {len(matched_files) - 5} 个文件")

            if unmatched_files:
                self.log_message(f"  未命中文件列表: {', '.join(unmatched_files[:5])}")
                if len(unmatched_files) > 5:
                    self.log_message(f"    ... 还有 {len(unmatched_files) - 5} 个文件")

            # 显示结果对话框
            result_message = f"文件处理完成！\n\n"
            result_message += f"操作类型: {operation_text}\n"
            result_message += f"总文件数: {total_files}\n"
            result_message += f"命中关键字: {len(matched_files)} 个\n"
            result_message += f"未命中关键字: {len(unmatched_files)} 个\n\n"
            result_message += f"文件已分类保存到项目根目录下的 extracted_files 文件夹中：\n"
            result_message += f"• 命中文件 -> 命中文件/\n"
            result_message += f"• 未命中文件 -> 未命中文件/"

            messagebox.showinfo("处理完成", result_message)

            # 自动打开extracted_files文件夹
            auto_open = self.config_manager.get("user_preferences.ui_settings.auto_open_result_folder", True)
            if auto_open and os.path.exists(self.extracted_dir):
                from utils import open_folder_in_explorer
                if open_folder_in_explorer(self.extracted_dir):
                    self.log_message(f"已自动打开结果文件夹: {self.extracted_dir}")
                else:
                    self.log_message("自动打开文件夹失败", "WARNING")

            # 撤销管理功能已移除

    def open_settings(self):
        """打开设置对话框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)

        # 使设置窗口居中
        settings_window.transient(self.root)
        settings_window.grab_set()

        # 创建设置界面
        main_frame = ttk.Frame(settings_window, padding="10")
        main_frame.pack(fill="both", expand=True)

        # extracted_files文件夹位置设置
        location_frame = ttk.LabelFrame(main_frame, text="extracted_files文件夹位置", padding="5")
        location_frame.pack(fill="x", pady=(0, 10))

        location_var = tk.StringVar()
        current_location = self.config_manager.get("user_preferences.ui_settings.extracted_files_location", "current")
        location_var.set(current_location)

        ttk.Radiobutton(location_frame, text="当前程序目录", variable=location_var, value="current").pack(anchor="w")
        ttk.Radiobutton(location_frame, text="桌面", variable=location_var, value="desktop").pack(anchor="w")

        # 自动打开结果文件夹设置
        auto_open_frame = ttk.LabelFrame(main_frame, text="处理完成后", padding="5")
        auto_open_frame.pack(fill="x", pady=(0, 10))

        auto_open_var = tk.BooleanVar()
        auto_open_var.set(self.config_manager.get("user_preferences.ui_settings.auto_open_result_folder", True))

        ttk.Checkbutton(auto_open_frame, text="自动打开extracted_files文件夹", variable=auto_open_var).pack(anchor="w")

        # 记忆目录设置
        remember_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="5")
        remember_frame.pack(fill="x", pady=(0, 10))

        remember_var = tk.BooleanVar()
        remember_var.set(self.config_manager.get("user_preferences.ui_settings.remember_last_archive", True))

        ttk.Checkbutton(remember_frame, text="记忆上次选择压缩包的目录", variable=remember_var).pack(anchor="w")

        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        def save_settings():
            # 保存设置
            self.config_manager.set("user_preferences.ui_settings.extracted_files_location", location_var.get())
            self.config_manager.set("user_preferences.ui_settings.auto_open_result_folder", auto_open_var.get())
            self.config_manager.set("user_preferences.ui_settings.remember_last_archive", remember_var.get())

            # 如果位置发生变化，重新初始化目录
            if location_var.get() != current_location:
                try:
                    self.extracted_dir, self.matched_dir, self.unmatched_dir = initialize_project_directories(location_var.get())
                    self.log_message(f"extracted_files目录位置已更改为: {'桌面' if location_var.get() == 'desktop' else '当前程序目录'}")
                except Exception as e:
                    self.log_message(f"更改目录位置失败: {e}", "ERROR")
                    messagebox.showerror("错误", f"更改目录位置失败: {e}")
                    return

            self.config_manager.save_config()
            self.log_message("设置已保存")
            messagebox.showinfo("设置", "设置已保存！")
            settings_window.destroy()

        def cancel_settings():
            settings_window.destroy()

        ttk.Button(button_frame, text="保存", command=save_settings).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=cancel_settings).pack(side="right")

    def check_format_support(self):
        """检查压缩格式支持情况"""
        from utils import get_supported_formats, get_format_requirements

        supported = get_supported_formats()
        requirements = get_format_requirements()

        missing_formats = []
        for format_name, is_supported in supported.items():
            if not is_supported:
                missing_formats.append(f"{format_name}: {requirements[format_name]}")

        if missing_formats:
            self.logger.warning(f"部分压缩格式不支持: {', '.join([f.split(':')[0] for f in missing_formats])}")
            # 可以选择是否显示提示对话框
            # messagebox.showwarning("格式支持提示",
            #     f"以下格式需要安装额外依赖:\n\n" + "\n".join(missing_formats))
        else:
            self.logger.info("所有压缩格式都已支持")

    def __del__(self):
        """析构函数，清理临时目录"""
        if hasattr(self, 'temp_extract_dir') and self.temp_extract_dir:
            cleanup_temp_directory(self.temp_extract_dir)
        if hasattr(self, 'logger'):
            self.logger.info("程序结束")


def main():
    root = tk.Tk()
    app = FileFilterApp(root)

    # 添加窗口关闭事件处理
    def on_closing():
        if hasattr(app, 'temp_extract_dir') and app.temp_extract_dir:
            cleanup_temp_directory(app.temp_extract_dir)
        if hasattr(app, 'save_user_settings'):
            app.save_user_settings()
        if hasattr(app, 'logger'):
            app.logger.info("用户关闭程序")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
