#!/usr/bin/env python3
"""
Windows 文件筛选与移动工具 v4.0 - 现代化UI版本
主程序入口
"""

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
from advanced_gui import FileTypeSelector, AdvancedFilters, ArchivePreview, UndoPanel
from undo_manager import UndoManager
from password_manager import PasswordManager
from ui_theme import UIStyler, ModernComponents, IconManager


class ModernFileFilterApp:
    """现代化文件筛选应用"""

    def __init__(self, root):
        self.root = root
        self.root.title("🗂️ 文件筛选与移动工具 v4.0 - 现代版")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)

        # 设置窗口图标
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 初始化UI主题
        self.ui_styler = UIStyler(self.root)
        self.components = ModernComponents(self.ui_styler)

        # 初始化管理器
        self.config_manager = ConfigManager()
        self.undo_manager = UndoManager()
        self.password_manager = PasswordManager()

        # 初始化日志系统
        self.logger = setup_logging()
        self.logger.info("现代化UI程序启动 v4.0")

        # 初始化项目目录
        try:
            self.extracted_dir, self.matched_dir, self.unmatched_dir = initialize_project_directories()
            self.logger.info("项目目录初始化完成")
        except Exception as e:
            self.logger.error(f"项目目录初始化失败: {e}")
            messagebox.showerror("初始化错误", f"无法初始化项目目录: {e}")

        # 添加临时目录跟踪
        self.temp_extract_dir = None

        # 加载用户配置
        self.load_user_settings()

        # 设置界面
        self.setup_modern_ui()

        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_modern_ui(self):
        """设置现代化界面"""
        # 主容器
        main_container = tk.Frame(self.root, bg=self.ui_styler.theme.COLORS['bg_primary'])
        main_container.pack(fill='both', expand=True)

        # 创建工具栏
        self.toolbar = self.components.create_toolbar(main_container)
        self.toolbar.pack(fill='x', side='top')

        # 创建主要内容区域
        content_area = tk.Frame(main_container, bg=self.ui_styler.theme.COLORS['bg_primary'])
        content_area.pack(fill='both', expand=True, padx=10, pady=10)

        # 创建左右分割的主面板
        main_paned = tk.PanedWindow(content_area,
                                   orient=tk.HORIZONTAL,
                                   bg=self.ui_styler.theme.COLORS['bg_primary'],
                                   sashwidth=8,
                                   sashrelief='flat')
        main_paned.pack(fill='both', expand=True)

        # 左侧面板
        left_panel = self.create_left_panel(main_paned)
        main_paned.add(left_panel, width=500, minsize=400)

        # 右侧面板
        right_panel = self.create_right_panel(main_paned)
        main_paned.add(right_panel, width=800, minsize=600)

        # 创建状态栏
        self.status_bar = self.components.create_status_bar(main_container)
        self.status_bar.pack(fill='x', side='bottom')

        # 创建通知区域
        self.notification_area = tk.Frame(main_container, bg=self.ui_styler.theme.COLORS['bg_primary'])
        self.notification_area.pack(fill='x', side='bottom', before=self.status_bar)

    def create_left_panel(self, parent):
        """创建左侧控制面板"""
        # 左侧主框架
        left_frame = tk.Frame(parent, bg=self.ui_styler.theme.COLORS['bg_primary'])

        # 创建滚动区域
        canvas = tk.Canvas(left_frame, bg=self.ui_styler.theme.COLORS['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview, style='Modern.Vertical.TScrollbar')
        scrollable_frame = tk.Frame(canvas, bg=self.ui_styler.theme.COLORS['bg_primary'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 1. 文件选择区域
        file_section = self.ui_styler.create_section_frame(scrollable_frame, "📁 文件选择")
        file_section.pack(fill='x', pady=(0, 15))

        # 拖拽区域
        self.drop_zone = self.components.create_file_drop_zone(file_section, self.on_archive_dropped)
        self.drop_zone.pack(fill='x', padx=15, pady=15)

        # 传统选择
        select_frame = tk.Frame(file_section, bg=self.ui_styler.theme.COLORS['bg_primary'])
        select_frame.pack(fill='x', padx=15, pady=(0, 15))

        self.archive_var = tk.StringVar()
        self.archive_entry = self.ui_styler.create_modern_entry(select_frame, textvariable=self.archive_var)
        self.archive_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        browse_btn = self.ui_styler.create_secondary_button(select_frame, "📂 浏览", command=self.select_archive)
        browse_btn.pack(side='right')

        # 2. 关键字设置区域
        keyword_section = self.ui_styler.create_section_frame(scrollable_frame, "🔍 关键字设置")
        keyword_section.pack(fill='x', pady=(0, 15))

        # 历史记录
        history_frame = tk.Frame(keyword_section, bg=self.ui_styler.theme.COLORS['bg_primary'])
        history_frame.pack(fill='x', padx=15, pady=(15, 10))

        history_label = self.ui_styler.create_caption_label(history_frame, "历史记录:")
        history_label.pack(side='left')

        self.history_var = tk.StringVar()
        history_combo = self.ui_styler.create_modern_combobox(history_frame, textvariable=self.history_var, state="readonly", width=25)
        history_combo.pack(side='right')
        history_combo.bind('<<ComboboxSelected>>', self.on_history_selected)

        # 加载历史
        history = self.config_manager.get("user_preferences.keywords_history", [])
        history_combo['values'] = history

        # 关键字输入
        keyword_input_frame = tk.Frame(keyword_section, bg=self.ui_styler.theme.COLORS['bg_primary'])
        keyword_input_frame.pack(fill='x', padx=15, pady=(0, 15))

        keyword_label = self.ui_styler.create_caption_label(keyword_input_frame, "输入关键字 (每行一个):")
        keyword_label.pack(anchor='w', pady=(0, 5))

        # 文本框容器
        text_container = tk.Frame(keyword_input_frame, bg=self.ui_styler.theme.COLORS['bg_primary'])
        text_container.pack(fill='x')

        self.keyword_text = tk.Text(text_container,
                                   height=4,
                                   wrap=tk.WORD,
                                   bg=self.ui_styler.theme.COLORS['input_bg'],
                                   fg=self.ui_styler.theme.COLORS['text_primary'],
                                   font=self.ui_styler.theme.FONTS['body'],
                                   relief='solid',
                                   bd=1,
                                   highlightthickness=1,
                                   highlightcolor=self.ui_styler.theme.COLORS['input_focus'])

        keyword_scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.keyword_text.yview, style='Modern.Vertical.TScrollbar')
        self.keyword_text.configure(yscrollcommand=keyword_scrollbar.set)

        self.keyword_text.pack(side='left', fill='both', expand=True)
        keyword_scrollbar.pack(side='right', fill='y')

        # 3. 操作模式区域
        operation_section = self.ui_styler.create_section_frame(scrollable_frame, "⚙️ 操作模式")
        operation_section.pack(fill='x', pady=(0, 15))

        operation_frame = tk.Frame(operation_section, bg=self.ui_styler.theme.COLORS['bg_primary'])
        operation_frame.pack(fill='x', padx=15, pady=15)

        self.operation_var = tk.StringVar(value=self.config_manager.get("user_preferences.operation_mode", "move"))

        move_rb = ttk.Radiobutton(operation_frame, text="📤 移动文件", variable=self.operation_var, value="move", style='Modern.TRadiobutton')
        move_rb.pack(side='left', padx=(0, 20))

        copy_rb = ttk.Radiobutton(operation_frame, text="📋 复制文件", variable=self.operation_var, value="copy", style='Modern.TRadiobutton')
        copy_rb.pack(side='left', padx=(0, 20))

        link_rb = ttk.Radiobutton(operation_frame, text="🔗 创建链接", variable=self.operation_var, value="link", style='Modern.TRadiobutton')
        link_rb.pack(side='left')

        # 4. 高级过滤器
        self.advanced_filters = AdvancedFilters(scrollable_frame)
        self.advanced_filters.frame.pack(fill='x', pady=(0, 15))

        # 5. 文件类型选择器
        file_type_presets = self.config_manager.get_file_type_presets()
        self.file_type_selector = FileTypeSelector(scrollable_frame, file_type_presets, self.on_filter_changed)
        self.file_type_selector.frame.pack(fill='x', pady=(0, 15))

        # 6. 操作按钮区域
        button_section = self.ui_styler.create_section_frame(scrollable_frame, "🎯 操作控制")
        button_section.pack(fill='x', pady=(0, 15))

        button_frame = tk.Frame(button_section, bg=self.ui_styler.theme.COLORS['bg_primary'])
        button_frame.pack(fill='x', padx=15, pady=15)

        # 按钮行1
        btn_row1 = tk.Frame(button_frame, bg=self.ui_styler.theme.COLORS['bg_primary'])
        btn_row1.pack(fill='x', pady=(0, 10))

        self.preview_btn = self.ui_styler.create_secondary_button(btn_row1, "👁️ 预览匹配", command=self.preview_files)
        self.preview_btn.pack(side='left', padx=(0, 10))

        self.start_btn = self.ui_styler.create_primary_button(btn_row1, "▶️ 开始处理", command=self.start_processing)
        self.start_btn.pack(side='left', padx=(0, 10))

        # 按钮行2
        btn_row2 = tk.Frame(button_frame, bg=self.ui_styler.theme.COLORS['bg_primary'])
        btn_row2.pack(fill='x')

        clear_btn = self.ui_styler.create_secondary_button(btn_row2, "🗑️ 清空", command=self.clear_inputs)
        clear_btn.pack(side='left', padx=(0, 10))

        settings_btn = self.ui_styler.create_secondary_button(btn_row2, "⚙️ 设置", command=self.show_settings)
        settings_btn.pack(side='left')

        # 7. 进度卡片
        self.progress_card = self.components.create_progress_card(scrollable_frame)
        self.progress_card.pack(fill='x', pady=(0, 15))

        # 配置滚动
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return left_frame

    def create_right_panel(self, parent):
        """创建右侧预览面板"""
        right_frame = tk.Frame(parent, bg=self.ui_styler.theme.COLORS['bg_primary'])

        # 创建现代化标签页
        self.notebook = self.ui_styler.create_modern_notebook(right_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # 1. 压缩包预览标签页
        preview_frame = tk.Frame(self.notebook, bg=self.ui_styler.theme.COLORS['bg_primary'])
        self.notebook.add(preview_frame, text="📦 压缩包预览")

        self.archive_preview = ArchivePreview(preview_frame)
        self.archive_preview.frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 2. 操作日志标签页
        log_frame = tk.Frame(self.notebook, bg=self.ui_styler.theme.COLORS['bg_primary'])
        self.notebook.add(log_frame, text="📋 操作日志")

        # 日志控制区域
        log_control_frame = tk.Frame(log_frame, bg=self.ui_styler.theme.COLORS['bg_primary'])
        log_control_frame.pack(fill='x', padx=10, pady=(10, 5))

        log_clear_btn = self.ui_styler.create_secondary_button(log_control_frame, "🗑️ 清空日志", command=self.clear_log)
        log_clear_btn.pack(side='left', padx=(0, 10))

        log_save_btn = self.ui_styler.create_secondary_button(log_control_frame, "💾 保存日志", command=self.save_log)
        log_save_btn.pack(side='left')

        # 日志显示区域
        log_text_frame = tk.Frame(log_frame, bg=self.ui_styler.theme.COLORS['bg_primary'])
        log_text_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.log_text = tk.Text(log_text_frame,
                               wrap=tk.WORD,
                               bg=self.ui_styler.theme.COLORS['bg_secondary'],
                               fg=self.ui_styler.theme.COLORS['text_primary'],
                               font=self.ui_styler.theme.FONTS['code'],
                               relief='solid',
                               bd=1)

        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview, style='Modern.Vertical.TScrollbar')
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')

        # 3. 撤销管理标签页
        undo_frame = tk.Frame(self.notebook, bg=self.ui_styler.theme.COLORS['bg_primary'])
        self.notebook.add(undo_frame, text="↩️ 撤销管理")

        self.undo_panel = UndoPanel(undo_frame, self.undo_manager)
        self.undo_panel.frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 4. 统计信息标签页
        stats_frame = tk.Frame(self.notebook, bg=self.ui_styler.theme.COLORS['bg_primary'])
        self.notebook.add(stats_frame, text="📊 统计信息")

        # 统计卡片容器
        stats_container = tk.Frame(stats_frame, bg=self.ui_styler.theme.COLORS['bg_primary'])
        stats_container.pack(fill='both', expand=True, padx=10, pady=10)

        # 统计卡片网格
        stats_grid = tk.Frame(stats_container, bg=self.ui_styler.theme.COLORS['bg_primary'])
        stats_grid.pack(fill='x', pady=(0, 20))

        # 创建统计卡片
        self.total_files_card = self.components.create_stats_card(stats_grid, "总文件数", "0", "📄")
        self.total_files_card.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky='ew')

        self.matched_files_card = self.components.create_stats_card(stats_grid, "匹配文件", "0", "✅")
        self.matched_files_card.grid(row=0, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')

        self.unmatched_files_card = self.components.create_stats_card(stats_grid, "未匹配文件", "0", "❌")
        self.unmatched_files_card.grid(row=0, column=2, pady=(0, 10), sticky='ew')

        self.operations_card = self.components.create_stats_card(stats_grid, "操作次数", "0", "🔄")
        self.operations_card.grid(row=1, column=0, padx=(0, 10), sticky='ew')

        self.success_rate_card = self.components.create_stats_card(stats_grid, "成功率", "0%", "📈")
        self.success_rate_card.grid(row=1, column=1, padx=(0, 10), sticky='ew')

        self.total_size_card = self.components.create_stats_card(stats_grid, "处理大小", "0 MB", "💾")
        self.total_size_card.grid(row=1, column=2, sticky='ew')

        # 配置网格权重
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        stats_grid.columnconfigure(2, weight=1)

        return right_frame

    def load_user_settings(self):
        """加载用户设置"""
        try:
            geometry = self.config_manager.get("user_preferences.ui_settings.window_geometry", "1400x900")
            self.root.geometry(geometry)
            self.logger.info("用户设置加载完成")
        except Exception as e:
            self.logger.error(f"加载用户设置失败: {e}")

    def save_user_settings(self):
        """保存用户设置"""
        try:
            self.config_manager.set("user_preferences.ui_settings.window_geometry", self.root.geometry())

            if hasattr(self, 'operation_var'):
                self.config_manager.set("user_preferences.operation_mode", self.operation_var.get())

            if hasattr(self, 'advanced_filters'):
                filters = self.advanced_filters.get_filters()
                self.config_manager.set("user_preferences.regex_mode", filters.get("use_regex", False))

            keywords = self.get_keywords()
            if keywords:
                self.config_manager.add_keyword_to_history(keywords)

            self.config_manager.save_config()
            self.logger.info("用户设置保存完成")
        except Exception as e:
            self.logger.error(f"保存用户设置失败: {e}")

    def on_archive_dropped(self, file_path: str):
        """处理拖拽的压缩包文件"""
        # 检查是否是新的压缩包
        old_archive = self.archive_var.get()
        if old_archive and old_archive != file_path:
            # 导入新压缩包时自动清理
            from utils import auto_cleanup_on_new_archive
            try:
                auto_cleanup_on_new_archive(file_path, self.extracted_dir)
                self.log_message("检测到新压缩包，已自动清理extracted_files目录")
                self.show_notification("已自动清理旧文件", "info")
            except Exception as e:
                self.log_message(f"自动清理警告: {e}", "WARNING")

        self.archive_var.set(file_path)
        if hasattr(self.drop_zone, 'drop_status'):
            self.drop_zone.drop_status.set(f"✅ 已选择: {os.path.basename(file_path)}")
        self.archive_preview.set_archive(file_path)
        self.log_message(f"通过拖拽选择了压缩包: {os.path.basename(file_path)}")
        self.show_notification("文件选择成功", "success")

    def select_archive(self):
        """选择压缩包"""
        archive_path = filedialog.askopenfilename(
            title="选择压缩包",
            filetypes=[
                ("压缩包文件", "*.zip;*.rar;*.7z"),
                ("ZIP文件", "*.zip"),
                ("RAR文件", "*.rar"),
                ("7Z文件", "*.7z"),
                ("所有文件", "*.*")
            ]
        )
        if archive_path:
            # 检查是否是新的压缩包
            old_archive = self.archive_var.get()
            if old_archive and old_archive != archive_path:
                # 导入新压缩包时自动清理
                from utils import auto_cleanup_on_new_archive
                try:
                    auto_cleanup_on_new_archive(archive_path, self.extracted_dir)
                    self.log_message("检测到新压缩包，已自动清理extracted_files目录")
                    self.show_notification("已自动清理旧文件", "info")
                except Exception as e:
                    self.log_message(f"自动清理警告: {e}", "WARNING")

            self.archive_var.set(archive_path)
            if hasattr(self.drop_zone, 'drop_status'):
                self.drop_zone.drop_status.set(f"✅ 已选择: {os.path.basename(archive_path)}")
            self.archive_preview.set_archive(archive_path)
            self.log_message(f"已选择压缩包: {os.path.basename(archive_path)}")
            self.show_notification("文件选择成功", "success")

    def on_history_selected(self, event):
        """历史记录选择事件"""
        selected = self.history_var.get()
        if selected:
            self.keyword_text.delete(1.0, tk.END)
            self.keyword_text.insert(1.0, selected)

    def on_filter_changed(self):
        """过滤器改变事件"""
        pass

    def get_keywords(self):
        """获取关键字列表"""
        keywords_text = self.keyword_text.get(1.0, tk.END).strip()
        if not keywords_text:
            return []
        keywords = [line.strip() for line in keywords_text.split('\n') if line.strip()]
        return keywords

    def get_current_filters(self):
        """获取当前过滤器设置"""
        filters = self.advanced_filters.get_filters()

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
            self.show_notification("请选择压缩包", "warning")
            return False

        if not keywords:
            self.show_notification("请输入关键字", "warning")
            return False

        if not validate_archive(archive_path):
            self.show_notification("选择的压缩包无效或不支持的格式", "error")
            return False

        filters = self.get_current_filters()
        if filters.get("use_regex", False):
            valid, error = self.advanced_filters.validate_regex_keywords(keywords)
            if not valid:
                self.show_notification(f"正则表达式错误: {error}", "error")
                return False

        return True

    def preview_files(self):
        """预览匹配的文件数量"""
        if not self.validate_inputs():
            return

        archive_path = self.archive_var.get().strip()
        keywords = self.get_keywords()
        filters = self.get_current_filters()

        try:
            self.components.update_progress("正在预览...", start=True)
            self.components.update_status("预览中...")

            thread = threading.Thread(target=self._preview_files_thread, args=(archive_path, keywords, filters))
            thread.daemon = True
            thread.start()

        except Exception as e:
            self.components.update_progress("预览失败", stop=True)
            self.components.update_status("预览失败")
            self.show_notification(f"预览失败: {str(e)}", "error")

    def _preview_files_thread(self, archive_path, keywords, filters):
        """在后台线程中预览文件"""
        try:
            matched_count, unmatched_count = count_matching_files_in_archive(archive_path, keywords, filters)
            self.root.after(0, self._preview_complete, matched_count, unmatched_count, None)
        except Exception as e:
            self.root.after(0, self._preview_complete, 0, 0, str(e))

    def _preview_complete(self, matched_count, unmatched_count, error):
        """预览完成回调"""
        self.components.update_progress("预览完成", stop=True)

        if error:
            self.components.update_status("预览失败")
            self.show_notification(f"预览失败: {error}", "error")
        else:
            total_count = matched_count + unmatched_count
            self.components.update_status(f"预览完成 - 总计 {total_count} 个文件")

            # 更新统计卡片
            self.update_stats_cards(total_count, matched_count, unmatched_count)

            message = f"预览完成！\n总文件数: {total_count}\n匹配文件: {matched_count}\n未匹配文件: {unmatched_count}"
            self.show_notification(message, "info")

            self.log_message(f"预览结果 - 总计: {total_count}, 匹配: {matched_count}, 未匹配: {unmatched_count}")

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
        self.start_btn.config(state='disabled')
        self.components.update_progress("正在处理...", start=True)
        self.components.update_status("处理中...")

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
                archive_path, keywords, filters, operation, self.undo_manager, self.password_manager
            )

            self.root.after(0, self.processing_complete, matched_files, unmatched_files, matched_dir, unmatched_dir, operation, None)

        except Exception as e:
            self.root.after(0, self.processing_complete, [], [], "", "", operation, str(e))

    def processing_complete(self, matched_files, unmatched_files, matched_dir, unmatched_dir, operation, error):
        """处理完成后的回调"""
        self.components.update_progress("处理完成", stop=True)
        self.start_btn.config(state='normal')

        if error:
            self.components.update_status("处理失败")
            self.log_message(f"错误: {error}", "ERROR")
            self.show_notification(f"操作失败: {error}", "error")
        else:
            total_files = len(matched_files) + len(unmatched_files)
            operation_text = {"move": "移动", "copy": "复制", "link": "链接"}[operation]
            self.components.update_status(f"处理完成 - 总计 {total_files} 个文件")

            # 更新统计卡片
            self.update_stats_cards(total_files, len(matched_files), len(unmatched_files))

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

            # 显示成功通知
            success_msg = f"处理完成！{operation_text}了 {total_files} 个文件"
            self.show_notification(success_msg, "success")

            # 刷新撤销面板
            if hasattr(self, 'undo_panel'):
                self.undo_panel.refresh_operations()

    def update_stats_cards(self, total, matched, unmatched):
        """更新统计卡片"""
        if hasattr(self, 'total_files_card'):
            self.total_files_card.value_var.set(str(total))
        if hasattr(self, 'matched_files_card'):
            self.matched_files_card.value_var.set(str(matched))
        if hasattr(self, 'unmatched_files_card'):
            self.unmatched_files_card.value_var.set(str(unmatched))

        # 计算成功率
        if total > 0:
            success_rate = (matched / total) * 100
            if hasattr(self, 'success_rate_card'):
                self.success_rate_card.value_var.set(f"{success_rate:.1f}%")

    def clear_inputs(self):
        """清空输入"""
        self.archive_var.set("")
        self.keyword_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.components.update_status("就绪")

        # 清理界面状态
        if hasattr(self.drop_zone, 'drop_status'):
            self.drop_zone.drop_status.set("")
        self.archive_preview.set_archive("")

        # 重置统计卡片
        self.update_stats_cards(0, 0, 0)

        # 清理临时目录
        if self.temp_extract_dir:
            cleanup_temp_directory(self.temp_extract_dir)
            self.temp_extract_dir = None

        self.show_notification("已清空所有输入", "info")

    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        self.show_notification("日志已清空", "info")

    def save_log(self):
        """保存日志到文件"""
        try:
            filename = filedialog.asksaveasfilename(
                title="保存日志",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message(f"日志已保存到: {filename}")
                self.show_notification(f"日志已保存到: {os.path.basename(filename)}", "success")
        except Exception as e:
            self.show_notification(f"保存日志失败: {str(e)}", "error")

    def show_settings(self):
        """显示设置对话框"""
        self.show_notification("设置功能开发中...", "info")

    def log_message(self, message: str, level: str = "INFO"):
        """记录日志消息"""
        timestamp = __import__('datetime').datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"

        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

        # 同时记录到文件
        if hasattr(self, 'logger'):
            if level == "ERROR":
                self.logger.error(message)
            elif level == "WARNING":
                self.logger.warning(message)
            else:
                self.logger.info(message)

    def show_notification(self, message: str, type: str = "info"):
        """显示通知"""
        notification = self.components.show_notification(self.notification_area, message, type)
        return notification

    def on_closing(self):
        """窗口关闭事件处理"""
        if hasattr(self, 'temp_extract_dir') and self.temp_extract_dir:
            cleanup_temp_directory(self.temp_extract_dir)
        if hasattr(self, 'save_user_settings'):
            self.save_user_settings()
        if hasattr(self, 'logger'):
            self.logger.info("用户关闭程序")
        self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()
    app = ModernFileFilterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
