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
from advanced_gui import FileTypeSelector, AdvancedFilters, DragDropFrame, ArchivePreview, UndoPanel
from undo_manager import UndoManager
from password_manager import PasswordManager


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
            self.extracted_dir, self.matched_dir, self.unmatched_dir = initialize_project_directories()
            self.logger.info("项目目录初始化完成")
        except Exception as e:
            self.logger.error(f"项目目录初始化失败: {e}")
            messagebox.showerror("初始化错误", f"无法初始化项目目录: {e}")

        # 添加临时目录跟踪
        self.temp_extract_dir = None

        # 加载用户配置
        self.load_user_settings()

        self.setup_ui()

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

            self.config_manager.save_config()
            self.logger.info("用户设置保存完成")
        except Exception as e:
            self.logger.error(f"保存用户设置失败: {e}")

    def setup_ui(self):
        """设置用户界面"""
        # 创建主要的PanedWindow来分割左右区域
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧面板（控制区域）
        left_frame = ttk.Frame(main_paned, padding="5")
        main_paned.add(left_frame, weight=1)

        # 右侧面板（预览区域）
        right_frame = ttk.Frame(main_paned, padding="5")
        main_paned.add(right_frame, weight=1)

        # 设置左侧面板内容
        self.setup_left_panel(left_frame)

        # 设置右侧面板内容
        self.setup_right_panel(right_frame)

    def setup_left_panel(self, parent):
        """设置左侧控制面板"""
        # 使用滚动框架
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 拖拽区域
        self.drag_drop_frame = DragDropFrame(scrollable_frame, self.on_archive_dropped)
        self.drag_drop_frame.frame.pack(fill="x", pady=(0, 10))

        # 传统文件选择
        file_select_frame = ttk.LabelFrame(scrollable_frame, text="或选择压缩包文件", padding="5")
        file_select_frame.pack(fill="x", pady=(0, 10))

        self.archive_var = tk.StringVar()
        self.archive_entry = ttk.Entry(file_select_frame, textvariable=self.archive_var, width=40)
        self.archive_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ttk.Button(file_select_frame, text="浏览", command=self.select_archive).pack(side="right")

        # 关键字输入区域
        keyword_frame = ttk.LabelFrame(scrollable_frame, text="关键字设置", padding="5")
        keyword_frame.pack(fill="x", pady=(0, 10))

        # 关键字历史
        history_frame = ttk.Frame(keyword_frame)
        history_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(history_frame, text="历史记录:").pack(side="left")
        self.history_var = tk.StringVar()
        history_combo = ttk.Combobox(history_frame, textvariable=self.history_var, width=25, state="readonly")
        history_combo.pack(side="right")
        history_combo.bind('<<ComboboxSelected>>', self.on_history_selected)

        # 加载关键字历史
        history = self.config_manager.get("user_preferences.keywords_history", [])
        history_combo['values'] = history

        # 多行关键字输入
        ttk.Label(keyword_frame, text="输入关键字 (每行一个):").pack(anchor="w", pady=(5, 2))

        text_frame = ttk.Frame(keyword_frame)
        text_frame.pack(fill="x", pady=(0, 5))

        self.keyword_text = tk.Text(text_frame, height=4, wrap=tk.WORD)
        keyword_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.keyword_text.yview)
        self.keyword_text.configure(yscrollcommand=keyword_scrollbar.set)

        self.keyword_text.pack(side="left", fill="both", expand=True)
        keyword_scrollbar.pack(side="right", fill="y")

        # 操作模式选择
        operation_frame = ttk.LabelFrame(scrollable_frame, text="操作模式", padding="5")
        operation_frame.pack(fill="x", pady=(0, 10))

        self.operation_var = tk.StringVar(value=self.config_manager.get("user_preferences.operation_mode", "move"))

        ttk.Radiobutton(operation_frame, text="移动文件", variable=self.operation_var, value="move").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(operation_frame, text="复制文件", variable=self.operation_var, value="copy").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(operation_frame, text="创建链接", variable=self.operation_var, value="link").pack(side=tk.LEFT)

        # 高级过滤器
        self.advanced_filters = AdvancedFilters(scrollable_frame)
        self.advanced_filters.frame.pack(fill="x", pady=(0, 10))

        # 文件类型选择器
        file_type_presets = self.config_manager.get_file_type_presets()
        self.file_type_selector = FileTypeSelector(scrollable_frame, file_type_presets, self.on_filter_changed)
        self.file_type_selector.frame.pack(fill="x", pady=(0, 10))

        # 控制按钮
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        self.preview_button = ttk.Button(button_frame, text="预览匹配文件", command=self.preview_files)
        self.preview_button.pack(side="left", padx=(0, 5))

        self.start_button = ttk.Button(button_frame, text="开始处理", command=self.start_processing)
        self.start_button.pack(side="left", padx=(0, 5))

        ttk.Button(button_frame, text="清空", command=self.clear_inputs).pack(side="left")

        # 进度显示
        progress_frame = ttk.Frame(scrollable_frame)
        progress_frame.pack(fill="x", pady=(10, 0))

        self.progress_var = tk.StringVar(value="就绪")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(anchor="w")

        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill="x", pady=(5, 0))

        # 绑定Ctrl+Enter快捷键
        self.keyword_text.bind('<Control-Return>', lambda e: self.start_processing())

        # 加载用户偏好设置
        self.load_user_preferences()

    def setup_right_panel(self, parent):
        """设置右侧预览面板"""
        # 创建Notebook来组织不同的预览功能
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        # 压缩包预览标签页
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="压缩包预览")

        self.archive_preview = ArchivePreview(preview_frame)
        self.archive_preview.frame.pack(fill="both", expand=True)

        # 操作日志标签页
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="操作日志")

        # 日志显示区域
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.log_text = tk.Text(log_text_frame, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")

        # 日志控制按钮
        log_button_frame = ttk.Frame(log_frame)
        log_button_frame.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Button(log_button_frame, text="清空日志", command=self.clear_log).pack(side="left")
        ttk.Button(log_button_frame, text="保存日志", command=self.save_log).pack(side="left", padx=(5, 0))

        # 撤销管理标签页
        undo_frame = ttk.Frame(notebook)
        notebook.add(undo_frame, text="撤销管理")

        self.undo_panel = UndoPanel(undo_frame, self.undo_manager)
        self.undo_panel.frame.pack(fill="both", expand=True, padx=5, pady=5)

    def load_user_preferences(self):
        """加载用户偏好设置"""
        try:
            # 设置正则表达式模式
            regex_mode = self.config_manager.get("user_preferences.regex_mode", False)
            if hasattr(self.advanced_filters, 'regex_var'):
                self.advanced_filters.regex_var.set(regex_mode)
        except Exception as e:
            self.logger.error(f"加载用户偏好失败: {e}")

    def on_history_selected(self, event):
        """历史记录选择事件"""
        selected = self.history_var.get()
        if selected:
            self.keyword_text.delete(1.0, tk.END)
            self.keyword_text.insert(1.0, selected)

    def on_filter_changed(self):
        """过滤器改变事件"""
        # 可以在这里添加实时预览等功能
        pass

    def on_archive_dropped(self, file_path: str):
        """处理拖拽的压缩包文件"""
        self.archive_var.set(file_path)
        self.drag_drop_frame.set_file(file_path)
        self.archive_preview.set_archive(file_path)
        self.log_message(f"通过拖拽选择了压缩包: {os.path.basename(file_path)}")

    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)

    def save_log(self):
        """保存日志到文件"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                title="保存日志",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message(f"日志已保存到: {filename}")
                messagebox.showinfo("保存成功", f"日志已保存到:\n{filename}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存日志失败: {str(e)}")

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
                except Exception as e:
                    self.log_message(f"自动清理警告: {e}", "WARNING")

            self.archive_var.set(archive_path)
            self.drag_drop_frame.set_file(archive_path)
            self.archive_preview.set_archive(archive_path)
            self.log_message(f"已选择压缩包: {os.path.basename(archive_path)}")

    def clear_inputs(self):
        """清空输入"""
        self.archive_var.set("")
        self.keyword_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set("就绪")

        # 清理界面状态
        self.drag_drop_frame.set_file("")
        self.archive_preview.set_archive("")

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
        """添加日志消息"""
        # 在GUI中显示
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

        # 同时记录到日志文件
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
            self.progress_var.set("正在预览...")
            self.progress_bar.start()

            # 在后台线程中执行预览
            thread = threading.Thread(target=self._preview_files_thread, args=(archive_path, keywords))
            thread.daemon = True
            thread.start()

        except Exception as e:
            self.progress_bar.stop()
            self.progress_var.set("预览失败")
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
            self.progress_var.set("预览失败")
            self.log_message(f"预览失败: {error}", "ERROR")
            messagebox.showerror("预览失败", f"预览失败: {error}")
        else:
            total_count = matched_count + unmatched_count
            self.progress_var.set("预览完成")
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
        self.progress_var.set("正在处理...")

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

            # 在主线程中更新UI
            self.root.after(0, self.processing_complete, matched_files, unmatched_files, matched_dir, unmatched_dir, operation, None)

        except Exception as e:
            self.root.after(0, self.processing_complete, [], [], "", "", operation, str(e))

    def processing_complete(self, matched_files, unmatched_files, matched_dir, unmatched_dir, operation, error):
        """处理完成后的回调"""
        self.progress_bar.stop()
        self.start_button.config(state='normal')

        if error:
            self.progress_var.set("处理失败")
            self.log_message(f"错误: {error}", "ERROR")
            messagebox.showerror("处理失败", f"操作失败: {error}")
        else:
            total_files = len(matched_files) + len(unmatched_files)
            operation_text = {"move": "移动", "copy": "复制", "link": "链接"}[operation]
            self.progress_var.set(f"处理完成 - 总计 {total_files} 个文件")

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

            # 刷新撤销面板
            if hasattr(self, 'undo_panel'):
                self.undo_panel.refresh_operations()

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
