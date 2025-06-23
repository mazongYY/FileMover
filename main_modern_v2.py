#!/usr/bin/env python3
"""
FileMover v4.0 - 现代化UI v2
基于用户提供的设计风格重新设计
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import logging
import subprocess
import platform
from utils import (find_and_move_files, validate_directory, count_matching_files,
                   find_and_move_files_from_archive, validate_archive,
                   count_matching_files_in_archive, cleanup_temp_directory,
                   setup_logging, initialize_project_directories)
from config_manager import ConfigManager
from advanced_gui import FileTypeSelector, AdvancedFilters
from undo_manager import UndoManager
from password_manager import PasswordManager
from icon_manager import icon_manager


class ModernFileFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileMover v4.0 - Modern Edition v2")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # 设置现代化深色主题
        self.setup_modern_theme()
        
        # 初始化组件
        self.config_manager = ConfigManager()
        self.undo_manager = UndoManager()
        self.password_manager = PasswordManager()
        
        # 初始化日志
        self.logger = setup_logging()
        self.logger.info("程序启动 v4.0 - 现代化UI v2")

        # 初始化项目目录
        try:
            location = self.config_manager.get("user_preferences.ui_settings.extracted_files_location", "current")
            self.extracted_dir, self.matched_dir, self.unmatched_dir = initialize_project_directories(location)
            self.logger.info(f"项目目录初始化完成，位置: {location}")
        except Exception as e:
            self.logger.error(f"项目目录初始化失败: {e}")
            messagebox.showerror("初始化错误", f"无法初始化项目目录: {e}")

        # 检查压缩格式支持
        self.check_format_support()
        
        # 临时目录跟踪
        self.temp_extract_dir = None

        # 创建现代化界面
        self.setup_ui()
        
        # 居中窗口
        self.center_window()

    def setup_modern_theme(self):
        """设置现代化深色主题"""
        # 现代化配色方案
        self.colors = {
            'bg_primary': '#1a1a1a',      # 主背景色
            'bg_secondary': '#2d2d2d',    # 次要背景色
            'bg_card': '#3a3a3a',         # 卡片背景色
            'accent': '#007acc',          # 主色调（蓝色）
            'accent_hover': '#005a9e',    # 主色调悬停
            'success': '#28a745',         # 成功色（绿色）
            'success_hover': '#218838',   # 成功色悬停
            'warning': '#ffc107',         # 警告色（黄色）
            'warning_hover': '#e0a800',   # 警告色悬停
            'danger': '#dc3545',          # 危险色（红色）
            'danger_hover': '#c82333',    # 危险色悬停
            'text_primary': '#ffffff',    # 主要文字
            'text_secondary': '#b3b3b3',  # 次要文字
            'text_muted': '#6c757d',      # 静音文字
            'border': '#4a4a4a',          # 边框色
            'input_bg': '#404040',        # 输入框背景
            'button_radius': 8,           # 按钮圆角
        }
        
        # 设置根窗口背景
        self.root.configure(bg=self.colors['bg_primary'])

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

    def create_modern_button(self, parent, text, command=None, style="primary", width=None):
        """创建现代化圆角按钮"""
        # 根据样式选择颜色
        if style == "primary":
            bg_color = self.colors['accent']
            hover_color = self.colors['accent_hover']
        elif style == "success":
            bg_color = self.colors['success']
            hover_color = self.colors['success_hover']
        elif style == "warning":
            bg_color = self.colors['warning']
            hover_color = self.colors['warning_hover']
        elif style == "danger":
            bg_color = self.colors['danger']
            hover_color = self.colors['danger_hover']
        else:
            bg_color = self.colors['bg_card']
            hover_color = self.colors['border']
        
        # 创建按钮框架（用于圆角效果）
        button_frame = tk.Frame(parent, bg=bg_color, relief='flat', bd=0)
        
        # 创建按钮
        button = tk.Button(button_frame,
                          text=text,
                          command=command,
                          font=('Microsoft YaHei UI', 10, 'bold'),
                          fg=self.colors['text_primary'],
                          bg=bg_color,
                          activebackground=hover_color,
                          activeforeground=self.colors['text_primary'],
                          relief='flat',
                          bd=0,
                          padx=20,
                          pady=10,
                          cursor='hand2')
        
        if width:
            button.config(width=width)
        
        button.pack(fill='both', expand=True, padx=2, pady=2)
        
        # 绑定悬停效果
        def on_enter(e):
            button.config(bg=hover_color)
            button_frame.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=bg_color)
            button_frame.config(bg=bg_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button_frame, button

    def create_modern_card(self, parent, title, icon=""):
        """创建现代化卡片"""
        # 卡片主容器
        card_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        card_container.pack(fill='x', pady=(0, 20))
        
        # 卡片主体
        card = tk.Frame(card_container,
                       bg=self.colors['bg_card'],
                       relief='flat',
                       bd=0,
                       padx=20,
                       pady=20)
        card.pack(fill='x', padx=10)
        
        # 卡片标题
        if title:
            title_frame = tk.Frame(card, bg=self.colors['bg_card'])
            title_frame.pack(fill='x', pady=(0, 15))
            
            title_label = tk.Label(title_frame,
                                  text=f"{icon} {title}" if icon else title,
                                  font=('Microsoft YaHei UI', 14, 'bold'),
                                  fg=self.colors['text_primary'],
                                  bg=self.colors['bg_card'])
            title_label.pack(anchor='w')
        
        # 内容区域
        content = tk.Frame(card, bg=self.colors['bg_card'])
        content.pack(fill='both', expand=True)
        
        return content

    def create_modern_input(self, parent, placeholder="", width=None):
        """创建现代化输入框"""
        input_frame = tk.Frame(parent,
                              bg=self.colors['input_bg'],
                              relief='flat',
                              bd=1,
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        
        entry = tk.Entry(input_frame,
                        font=('Microsoft YaHei UI', 10),
                        bg=self.colors['input_bg'],
                        fg=self.colors['text_primary'],
                        relief='flat',
                        bd=0,
                        insertbackground=self.colors['text_primary'],
                        selectbackground=self.colors['accent'],
                        selectforeground=self.colors['text_primary'])
        
        if width:
            entry.config(width=width)
        
        entry.pack(fill='both', expand=True, padx=10, pady=8)
        
        # 占位符效果
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=self.colors['text_muted'])
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=self.colors['text_primary'])
            
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=self.colors['text_muted'])
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        return input_frame, entry

    def setup_ui(self):
        """设置现代化用户界面"""
        # 创建主容器
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 创建顶部标题区域
        self.create_header(main_container)

        # 创建主内容区域
        content_container = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_container.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # 创建左右分栏
        left_panel = tk.Frame(content_container, bg=self.colors['bg_primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_panel = tk.Frame(content_container, bg=self.colors['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # 设置左侧面板
        self.setup_left_panel(left_panel)

        # 设置右侧面板
        self.setup_right_panel(right_panel)

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_header(self, parent):
        """创建顶部标题区域"""
        header = tk.Frame(parent, bg=self.colors['bg_secondary'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)

        # 标题内容
        header_content = tk.Frame(header, bg=self.colors['bg_secondary'])
        header_content.pack(fill='both', expand=True, padx=30, pady=20)

        # 左侧：应用标题
        title_label = tk.Label(header_content,
                              text="📦 FileMover v4.0",
                              font=('Microsoft YaHei UI', 20, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(side='left')

        # 右侧：操作按钮
        button_container = tk.Frame(header_content, bg=self.colors['bg_secondary'])
        button_container.pack(side='right')

        # 预览按钮
        preview_frame, self.preview_btn = self.create_modern_button(
            button_container, "👁️ 预览匹配文件", self.preview_files, "primary")
        preview_frame.pack(side='right', padx=(0, 10))

        # 开始处理按钮
        process_frame, self.process_btn = self.create_modern_button(
            button_container, "🚀 开始处理", self.start_processing, "success")
        process_frame.pack(side='right')

    def setup_left_panel(self, parent):
        """设置左侧面板"""
        # 文件选择卡片
        file_content = self.create_modern_card(parent, "文件选择", "📁")
        self.setup_file_selection(file_content)

        # 关键字设置卡片
        keyword_content = self.create_modern_card(parent, "关键字设置", "🔍")
        self.setup_keyword_input(keyword_content)

    def setup_right_panel(self, parent):
        """设置右侧面板"""
        # 操作模式卡片
        mode_content = self.create_modern_card(parent, "操作模式", "⚙️")
        self.setup_operation_mode(mode_content)

        # 处理状态卡片
        status_content = self.create_modern_card(parent, "处理状态", "📊")
        self.setup_status_display(status_content)

    # 占位方法，后续实现
    def setup_file_selection(self, parent):
        """设置文件选择区域"""
        # 文件路径输入
        input_frame, self.archive_entry = self.create_modern_input(
            parent, "请选择压缩包文件...")
        input_frame.pack(fill='x', pady=(0, 15))

        # 浏览按钮
        browse_frame, browse_btn = self.create_modern_button(
            parent, "📂 浏览文件", self.browse_archive, "primary", width=15)
        browse_frame.pack(anchor='w')

        # 文件信息显示
        self.file_info_label = tk.Label(parent,
                                      text="",
                                      font=('Microsoft YaHei UI', 10),
                                      fg=self.colors['success'],
                                      bg=self.colors['bg_card'])
        self.file_info_label.pack(anchor='w', pady=(10, 0))

    def setup_keyword_input(self, parent):
        """设置关键字输入区域"""
        # 说明文字
        desc_label = tk.Label(parent,
                            text="输入搜索关键字，每行一个：",
                            font=('Microsoft YaHei UI', 11),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['bg_card'])
        desc_label.pack(anchor='w', pady=(0, 10))

        # 关键字输入区域
        text_container = tk.Frame(parent,
                                bg=self.colors['input_bg'],
                                relief='flat',
                                bd=1,
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        text_container.pack(fill='both', expand=True, pady=(0, 15))

        # 文本框
        self.keyword_text = tk.Text(text_container,
                                  height=8,
                                  wrap=tk.WORD,
                                  font=('Microsoft YaHei UI', 10),
                                  bg=self.colors['input_bg'],
                                  fg=self.colors['text_primary'],
                                  relief='flat',
                                  bd=0,
                                  padx=10,
                                  pady=10,
                                  insertbackground=self.colors['text_primary'],
                                  selectbackground=self.colors['accent'],
                                  selectforeground=self.colors['text_primary'])

        # 滚动条
        scrollbar = tk.Scrollbar(text_container,
                               orient=tk.VERTICAL,
                               command=self.keyword_text.yview,
                               bg=self.colors['bg_card'],
                               troughcolor=self.colors['input_bg'],
                               activebackground=self.colors['accent'])
        self.keyword_text.configure(yscrollcommand=scrollbar.set)

        # 布局
        self.keyword_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # 操作按钮
        button_container = tk.Frame(parent, bg=self.colors['bg_card'])
        button_container.pack(fill='x')

        # 清空按钮
        clear_frame, clear_btn = self.create_modern_button(
            button_container, "🗑️ 清空", self.clear_keywords, "warning", width=10)
        clear_frame.pack(side='left', padx=(0, 10))

        # 示例按钮
        example_frame, example_btn = self.create_modern_button(
            button_container, "💡 示例", self.load_example_keywords, "primary", width=10)
        example_frame.pack(side='left')

    def setup_operation_mode(self, parent):
        """设置操作模式区域"""
        # 操作模式变量
        self.operation_var = tk.StringVar(value="move")

        # 模式选项
        modes = [
            ("move", "📁 移动文件", "将匹配的文件移动到目标文件夹"),
            ("copy", "📋 复制文件", "将匹配的文件复制到目标文件夹"),
            ("link", "🔗 创建链接", "为匹配的文件创建快捷方式")
        ]

        for value, text, desc in modes:
            # 模式选项容器
            mode_container = tk.Frame(parent,
                                    bg=self.colors['bg_secondary'],
                                    relief='flat',
                                    bd=0,
                                    padx=15,
                                    pady=12)
            mode_container.pack(fill='x', pady=(0, 10))

            # 单选按钮
            radio = tk.Radiobutton(mode_container,
                                 text="",
                                 variable=self.operation_var,
                                 value=value,
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['accent'],
                                 selectcolor=self.colors['accent'],
                                 activebackground=self.colors['bg_secondary'],
                                 font=('Microsoft YaHei UI', 12))
            radio.pack(side='left')

            # 文字内容
            content_frame = tk.Frame(mode_container, bg=self.colors['bg_secondary'])
            content_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))

            # 标题
            title_label = tk.Label(content_frame,
                                 text=text,
                                 font=('Microsoft YaHei UI', 11, 'bold'),
                                 fg=self.colors['text_primary'],
                                 bg=self.colors['bg_secondary'])
            title_label.pack(anchor='w')

            # 描述
            desc_label = tk.Label(content_frame,
                                text=desc,
                                font=('Microsoft YaHei UI', 9),
                                fg=self.colors['text_secondary'],
                                bg=self.colors['bg_secondary'])
            desc_label.pack(anchor='w')

            # 绑定点击事件
            def make_click_handler(v):
                return lambda e: self.operation_var.set(v)

            for widget in [mode_container, content_frame, title_label, desc_label]:
                widget.bind("<Button-1>", make_click_handler(value))

    def setup_status_display(self, parent):
        """设置状态显示区域"""
        # 当前状态
        status_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        status_frame.pack(fill='x', pady=(0, 20))

        # 状态图标和文字
        self.status_icon = tk.Label(status_frame,
                                  text="⚪",
                                  font=('Segoe UI Emoji', 16),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_card'])
        self.status_icon.pack(side='left', padx=(0, 10))

        status_text_frame = tk.Frame(status_frame, bg=self.colors['bg_card'])
        status_text_frame.pack(side='left', fill='x', expand=True)

        self.status_text = tk.Label(status_text_frame,
                                  text="就绪",
                                  font=('Microsoft YaHei UI', 12, 'bold'),
                                  fg=self.colors['text_primary'],
                                  bg=self.colors['bg_card'])
        self.status_text.pack(anchor='w')

        self.status_detail = tk.Label(status_text_frame,
                                    text="等待用户操作",
                                    font=('Microsoft YaHei UI', 9),
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['bg_card'])
        self.status_detail.pack(anchor='w')

        # 进度条容器
        progress_container = tk.Frame(parent,
                                    bg=self.colors['bg_secondary'],
                                    relief='flat',
                                    bd=0,
                                    height=8)
        progress_container.pack(fill='x', pady=(0, 20))
        progress_container.pack_propagate(False)

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Frame(progress_container,
                                   bg=self.colors['accent'],
                                   height=8)

        # 统计信息
        stats_container = tk.Frame(parent, bg=self.colors['bg_card'])
        stats_container.pack(fill='x')

        # 统计卡片
        self.create_stat_card(stats_container, "处理文件", "0", "📄")
        self.create_stat_card(stats_container, "匹配成功", "0", "✅")
        self.create_stat_card(stats_container, "处理时间", "0s", "⏱️")

    def create_stat_card(self, parent, label, value, icon):
        """创建统计卡片"""
        card = tk.Frame(parent,
                       bg=self.colors['bg_secondary'],
                       relief='flat',
                       bd=0,
                       padx=15,
                       pady=10)
        card.pack(side='left', fill='x', expand=True, padx=(0, 10))

        # 图标
        icon_label = tk.Label(card,
                            text=icon,
                            font=('Segoe UI Emoji', 14),
                            bg=self.colors['bg_secondary'])
        icon_label.pack()

        # 数值
        value_label = tk.Label(card,
                             text=value,
                             font=('Microsoft YaHei UI', 12, 'bold'),
                             fg=self.colors['text_primary'],
                             bg=self.colors['bg_secondary'])
        value_label.pack()

        # 标签
        label_widget = tk.Label(card,
                              text=label,
                              font=('Microsoft YaHei UI', 9),
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_secondary'])
        label_widget.pack()

        # 保存引用以便更新
        setattr(self, f"stat_{label.replace(' ', '_').lower()}_value", value_label)

    def center_window(self):
        """居中窗口"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def browse_archive(self):
        """浏览压缩包"""
        file_path = filedialog.askopenfilename(
            title="选择压缩包文件",
            filetypes=[
                ("压缩包文件", "*.zip;*.rar;*.7z"),
                ("ZIP文件", "*.zip"),
                ("RAR文件", "*.rar"),
                ("7Z文件", "*.7z"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            # 清除占位符效果
            self.archive_entry.delete(0, tk.END)
            self.archive_entry.insert(0, file_path)
            self.archive_entry.config(fg=self.colors['text_primary'])

            # 更新文件信息
            file_name = os.path.basename(file_path)
            try:
                file_size = self.format_file_size(os.path.getsize(file_path))
                self.file_info_label.config(text=f"✅ {file_name} ({file_size})")
            except:
                self.file_info_label.config(text=f"✅ {file_name}")

    def clear_keywords(self):
        """清空关键字"""
        self.keyword_text.delete(1.0, tk.END)

    def load_example_keywords(self):
        """加载示例关键字"""
        examples = ["图片", "文档", "视频", "音频", "压缩包"]
        self.keyword_text.delete(1.0, tk.END)
        self.keyword_text.insert(1.0, "\n".join(examples))

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

    def update_status(self, text, detail="", icon="⚪"):
        """更新状态显示"""
        self.status_text.config(text=text)
        self.status_detail.config(text=detail)
        self.status_icon.config(text=icon)

    def update_progress(self, value):
        """更新进度条"""
        self.progress_var.set(value)
        # 更新进度条显示
        progress_width = int((value / 100) * 300)  # 假设进度条宽度为300px
        self.progress_bar.config(width=progress_width)

    def preview_files(self):
        """预览文件"""
        messagebox.showinfo("预览", "预览功能开发中...")

    def start_processing(self):
        """开始处理"""
        messagebox.showinfo("处理", "处理功能开发中...")

    def on_closing(self):
        """窗口关闭事件"""
        if self.temp_extract_dir:
            cleanup_temp_directory(self.temp_extract_dir)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFileFilterApp(root)
    root.mainloop()
