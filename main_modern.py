#!/usr/bin/env python3
"""
FileMover v4.0 - 现代化UI版本
完全重新设计的Material Design风格界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
from modern_ui import ModernCard, ModernButton, ModernInput, ModernProgressBar


class ModernFileFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileMover v4.0 - Modern Edition")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # 设置最小窗口大小
        self.root.minsize(1200, 800)
        
        # 初始化配置管理器
        self.config_manager = ConfigManager()
        self.undo_manager = UndoManager()
        self.password_manager = PasswordManager()
        
        # 初始化日志系统
        self.logger = setup_logging()
        self.logger.info("现代化UI版本启动 v4.0")
        
        # 初始化项目目录
        try:
            location = self.config_manager.get("user_preferences.ui_settings.extracted_files_location", "current")
            self.extracted_dir, self.matched_dir, self.unmatched_dir = initialize_project_directories(location)
        except Exception as e:
            self.logger.error(f"项目目录初始化失败: {e}")
            messagebox.showerror("初始化错误", f"无法初始化项目目录: {e}")
        
        # 检测主题
        self.is_dark_theme = self.detect_system_theme()
        self.setup_colors()
        
        # 初始化变量
        self.archive_var = tk.StringVar()
        self.operation_var = tk.StringVar(value="move")
        
        # 设置UI
        self.setup_modern_ui()
        
        # 居中显示窗口
        self.center_window()
    
    def detect_system_theme(self):
        """检测系统主题"""
        user_theme = self.config_manager.get("user_preferences.ui_settings.theme_mode", "auto")
        
        if user_theme == "dark":
            return True
        elif user_theme == "light":
            return False
        
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0
        except:
            return False
    
    def setup_colors(self):
        """设置颜色方案"""
        if self.is_dark_theme:
            self.colors = {
                'primary': '#1976D2',
                'primary_variant': '#1565C0',
                'secondary': '#03DAC6',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336',
                'background': '#121212',
                'surface': '#1E1E1E',
                'surface_variant': '#2D2D2D',
                'text_primary': '#FFFFFF',
                'text_secondary': '#B3B3B3',
                'text_disabled': '#666666',
                'border': '#333333',
                'divider': '#2D2D2D',
                'shadow': '#00000040'
            }
        else:
            self.colors = {
                'primary': '#1976D2',
                'primary_variant': '#1565C0',
                'secondary': '#03DAC6',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336',
                'background': '#FAFAFA',
                'surface': '#FFFFFF',
                'surface_variant': '#F5F5F5',
                'text_primary': '#212121',
                'text_secondary': '#757575',
                'text_disabled': '#BDBDBD',
                'border': '#E0E0E0',
                'divider': '#E0E0E0',
                'shadow': '#00000020'
            }
    
    def setup_modern_ui(self):
        """设置现代化UI"""
        # 设置根窗口背景
        self.root.configure(bg=self.colors['background'])
        
        # 创建主容器
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建顶部导航栏
        self.create_top_navigation()
        
        # 创建主内容区域
        self.create_main_content()
        
        # 创建底部状态栏
        self.create_bottom_status()
    
    def create_top_navigation(self):
        """创建顶部导航栏"""
        # 导航栏容器
        nav_container = tk.Frame(self.main_container, 
                               bg=self.colors['surface'], 
                               height=80)
        nav_container.pack(fill="x", padx=0, pady=0)
        nav_container.pack_propagate(False)
        
        # 添加阴影
        shadow = tk.Frame(self.main_container, 
                        bg=self.colors['shadow'], 
                        height=2)
        shadow.pack(fill="x")
        
        # 导航内容
        nav_content = tk.Frame(nav_container, bg=self.colors['surface'])
        nav_content.pack(fill="both", expand=True, padx=24, pady=16)
        
        # 左侧：应用标题和图标
        left_section = tk.Frame(nav_content, bg=self.colors['surface'])
        left_section.pack(side="left", fill="y")
        
        # 应用图标
        app_icon = tk.Label(left_section,
                          text="📦",
                          font=('Segoe UI Emoji', 24),
                          fg=self.colors['primary'],
                          bg=self.colors['surface'])
        app_icon.pack(side="left", padx=(0, 12))
        
        # 应用标题
        title_frame = tk.Frame(left_section, bg=self.colors['surface'])
        title_frame.pack(side="left", fill="y")
        
        app_title = tk.Label(title_frame,
                           text="FileMover",
                           font=('Microsoft YaHei UI', 20, 'bold'),
                           fg=self.colors['text_primary'],
                           bg=self.colors['surface'])
        app_title.pack(anchor="w")
        
        app_subtitle = tk.Label(title_frame,
                              text="现代化文件筛选与移动工具",
                              font=('Microsoft YaHei UI', 11),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['surface'])
        app_subtitle.pack(anchor="w")
        
        # 右侧：操作按钮
        right_section = tk.Frame(nav_content, bg=self.colors['surface'])
        right_section.pack(side="right", fill="y")
        
        # 主题切换按钮
        theme_btn = ModernButton(right_section, 
                               "主题", 
                               command=self.toggle_theme,
                               style="outlined",
                               icon="🌓",
                               colors=self.colors)
        theme_btn.container.pack(side="right", padx=(0, 12))
        
        # 预览按钮
        self.preview_btn = ModernButton(right_section,
                                      "预览匹配文件",
                                      command=self.preview_files,
                                      style="outlined",
                                      icon="👁️",
                                      colors=self.colors)
        self.preview_btn.container.pack(side="right", padx=(0, 12))
        
        # 开始处理按钮
        self.start_btn = ModernButton(right_section,
                                    "开始处理",
                                    command=self.start_processing,
                                    style="success",
                                    icon="🚀",
                                    colors=self.colors)
        self.start_btn.container.pack(side="right")
    
    def create_main_content(self):
        """创建主内容区域"""
        # 主内容容器
        content_container = tk.Frame(self.main_container, bg=self.colors['background'])
        content_container.pack(fill="both", expand=True, padx=0, pady=16)
        
        # 创建左右分栏
        # 左侧：文件选择和关键字设置 (40%)
        left_panel = tk.Frame(content_container, bg=self.colors['background'])
        left_panel.pack(side="left", fill="both", expand=True, padx=(16, 8))
        
        # 右侧：高级设置和状态显示 (60%)
        right_panel = tk.Frame(content_container, bg=self.colors['background'])
        right_panel.pack(side="right", fill="both", expand=True, padx=(8, 16))
        
        # 设置左侧内容
        self.setup_left_panel(left_panel)
        
        # 设置右侧内容
        self.setup_right_panel(right_panel)
    
    def setup_left_panel(self, parent):
        """设置左侧面板"""
        # 文件选择卡片
        file_card = ModernCard(parent, "文件选择", "📁", self.colors)
        self.setup_file_selection(file_card.content)
        
        # 关键字设置卡片
        keyword_card = ModernCard(parent, "关键字设置", "🔍", self.colors)
        self.setup_keyword_input(keyword_card.content)
    
    def setup_right_panel(self, parent):
        """设置右侧面板"""
        # 操作模式卡片
        mode_card = ModernCard(parent, "操作模式", "⚙️", self.colors)
        self.setup_operation_mode(mode_card.content)
        
        # 高级过滤卡片
        filter_card = ModernCard(parent, "高级过滤", "🎯", self.colors)
        self.setup_advanced_filters(filter_card.content)
        
        # 处理状态卡片
        status_card = ModernCard(parent, "处理状态", "📊", self.colors)
        self.setup_status_display(status_card.content)
    
    def create_bottom_status(self):
        """创建底部状态栏"""
        # 状态栏容器
        status_container = tk.Frame(self.main_container,
                                  bg=self.colors['surface'],
                                  height=50)
        status_container.pack(fill="x", side="bottom")
        status_container.pack_propagate(False)
        
        # 添加顶部分割线
        divider = tk.Frame(self.main_container,
                         bg=self.colors['divider'],
                         height=1)
        divider.pack(fill="x", side="bottom")
        
        # 状态内容
        status_content = tk.Frame(status_container, bg=self.colors['surface'])
        status_content.pack(fill="both", expand=True, padx=24, pady=12)
        
        # 左侧：版权信息
        copyright_label = tk.Label(status_content,
                                 text="© 2024 FileMover v4.0 - Modern Edition",
                                 font=('Microsoft YaHei UI', 9),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['surface'])
        copyright_label.pack(side="left")
        
        # 右侧：状态指示
        self.status_indicator = tk.Label(status_content,
                                       text="🟢 就绪",
                                       font=('Microsoft YaHei UI', 9),
                                       fg=self.colors['success'],
                                       bg=self.colors['surface'])
        self.status_indicator.pack(side="right")
    
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 占位方法，后续实现
    def setup_file_selection(self, parent):
        """设置文件选择区域"""
        # 大型拖拽区域
        drop_zone = tk.Frame(parent,
                           bg=self.colors['surface_variant'],
                           relief='dashed',
                           bd=2,
                           height=120)
        drop_zone.pack(fill="x", pady=(0, 16))
        drop_zone.pack_propagate(False)

        # 拖拽区域内容
        drop_content = tk.Frame(drop_zone, bg=self.colors['surface_variant'])
        drop_content.pack(expand=True)

        # 拖拽图标
        drop_icon = tk.Label(drop_content,
                           text="📦",
                           font=('Segoe UI Emoji', 32),
                           fg=self.colors['text_secondary'],
                           bg=self.colors['surface_variant'])
        drop_icon.pack(pady=(16, 8))

        # 拖拽提示文字
        drop_text = tk.Label(drop_content,
                           text="拖拽压缩包文件到此处\n或点击下方按钮选择文件",
                           font=('Microsoft YaHei UI', 11),
                           fg=self.colors['text_secondary'],
                           bg=self.colors['surface_variant'],
                           justify="center")
        drop_text.pack()

        # 文件路径输入
        self.file_input = ModernInput(parent,
                                    label="压缩包路径",
                                    placeholder="请选择压缩包文件...",
                                    colors=self.colors)
        self.file_input.container.pack(fill="x", pady=(0, 16))

        # 浏览按钮
        browse_btn = ModernButton(parent,
                                "浏览文件",
                                command=self.select_archive,
                                style="primary",
                                icon="📂",
                                colors=self.colors)
        browse_btn.container.pack(anchor="w")

        # 文件信息显示
        self.file_info_frame = tk.Frame(parent, bg=self.colors['surface'])
        self.file_info_frame.pack(fill="x", pady=(16, 0))

        self.file_info_label = tk.Label(self.file_info_frame,
                                      text="",
                                      font=('Microsoft YaHei UI', 10),
                                      fg=self.colors['success'],
                                      bg=self.colors['surface'])
        self.file_info_label.pack(anchor="w")

        # 绑定拖拽事件
        self.setup_drag_drop(drop_zone)
    
    def setup_keyword_input(self, parent):
        """设置关键字输入区域"""
        # 说明文字
        desc_label = tk.Label(parent,
                            text="输入搜索关键字，每行一个：",
                            font=('Microsoft YaHei UI', 11, 'bold'),
                            fg=self.colors['text_primary'],
                            bg=self.colors['surface'])
        desc_label.pack(anchor="w", pady=(0, 12))

        # 关键字输入区域容器
        input_container = tk.Frame(parent,
                                 bg=self.colors['border'],
                                 relief='solid',
                                 bd=1)
        input_container.pack(fill="both", expand=True, pady=(0, 16))

        # 关键字文本框
        self.keyword_text = tk.Text(input_container,
                                  height=6,
                                  wrap=tk.WORD,
                                  font=('Microsoft YaHei UI', 11),
                                  bg=self.colors['surface'],
                                  fg=self.colors['text_primary'],
                                  relief='flat',
                                  bd=0,
                                  padx=12,
                                  pady=12,
                                  insertbackground=self.colors['text_primary'],
                                  selectbackground=self.colors['primary'],
                                  selectforeground='white')

        # 滚动条
        scrollbar = ttk.Scrollbar(input_container,
                                orient=tk.VERTICAL,
                                command=self.keyword_text.yview)
        self.keyword_text.configure(yscrollcommand=scrollbar.set)

        # 布局
        self.keyword_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 操作按钮区域
        button_frame = tk.Frame(parent, bg=self.colors['surface'])
        button_frame.pack(fill="x")

        # 清空按钮
        clear_btn = ModernButton(button_frame,
                               "清空",
                               command=self.clear_keywords,
                               style="warning",
                               icon="🗑️",
                               colors=self.colors)
        clear_btn.container.pack(side="left")

        # 示例按钮
        example_btn = ModernButton(button_frame,
                                 "插入示例",
                                 command=self.insert_example_keywords,
                                 style="outlined",
                                 icon="💡",
                                 colors=self.colors)
        example_btn.container.pack(side="left", padx=(12, 0))

        # 绑定快捷键
        self.keyword_text.bind('<Control-Return>', lambda e: self.start_processing())
    
    def setup_operation_mode(self, parent):
        """设置操作模式区域"""
        pass
    
    def setup_advanced_filters(self, parent):
        """设置高级过滤区域"""
        pass
    
    def setup_status_display(self, parent):
        """设置状态显示区域"""
        pass
    
    def toggle_theme(self):
        """切换主题"""
        pass
    
    def preview_files(self):
        """预览文件"""
        pass
    
    def start_processing(self):
        """开始处理"""
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFileFilterApp(root)
    root.mainloop()
