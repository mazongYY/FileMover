#!/usr/bin/env python3
"""
高级GUI组件模块
包含文件类型选择、过滤器设置等高级界面组件
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Optional, Callable, Tuple
from datetime import datetime, date
import re
import os


class FileTypeSelector:
    """文件类型选择器"""

    def __init__(self, parent, presets: Dict[str, List[str]], callback: Optional[Callable] = None):
        self.parent = parent
        self.presets = presets
        self.callback = callback
        self.selected_types = []

        self.frame = ttk.LabelFrame(parent, text="文件类型筛选", padding="5")
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 启用/禁用复选框
        self.enabled_var = tk.BooleanVar()
        self.enabled_check = ttk.Checkbutton(
            self.frame,
            text="启用文件类型筛选",
            variable=self.enabled_var,
            command=self.on_enabled_changed
        )
        self.enabled_check.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))

        # 预设类型选择
        self.preset_frame = ttk.Frame(self.frame)
        self.preset_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))

        self.preset_vars = {}
        row = 0
        col = 0
        for preset_name in self.presets.keys():
            var = tk.BooleanVar()
            check = ttk.Checkbutton(
                self.preset_frame,
                text=preset_name,
                variable=var,
                command=self.on_preset_changed
            )
            check.grid(row=row, column=col, sticky=tk.W, padx=(0, 10))
            self.preset_vars[preset_name] = var

            col += 1
            if col >= 3:  # 每行3个
                col = 0
                row += 1

        # 自定义扩展名
        ttk.Label(self.frame, text="自定义扩展名:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.custom_entry = ttk.Entry(self.frame, width=30)
        self.custom_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(10, 0), padx=(5, 0))
        ttk.Button(self.frame, text="添加", command=self.add_custom_type).grid(row=2, column=2, pady=(10, 0), padx=(5, 0))

        # 当前选择显示
        ttk.Label(self.frame, text="当前选择:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.selection_label = ttk.Label(self.frame, text="无", foreground="gray")
        self.selection_label.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=(10, 0), padx=(5, 0))

        # 初始状态
        self.on_enabled_changed()

    def on_enabled_changed(self):
        """启用状态改变"""
        enabled = self.enabled_var.get()

        # 启用/禁用所有子控件
        for widget in self.preset_frame.winfo_children():
            widget.configure(state='normal' if enabled else 'disabled')

        self.custom_entry.configure(state='normal' if enabled else 'disabled')

        self.update_selection()

        if self.callback:
            self.callback()

    def on_preset_changed(self):
        """预设选择改变"""
        self.update_selection()
        if self.callback:
            self.callback()

    def add_custom_type(self):
        """添加自定义类型"""
        custom_text = self.custom_entry.get().strip()
        if not custom_text:
            return

        # 解析扩展名
        extensions = [ext.strip() for ext in custom_text.replace(',', ' ').split() if ext.strip()]

        # 确保以点开头
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]

        if extensions:
            self.selected_types.extend(extensions)
            self.custom_entry.delete(0, tk.END)
            self.update_selection()

            if self.callback:
                self.callback()

    def update_selection(self):
        """更新选择显示"""
        if not self.enabled_var.get():
            self.selection_label.config(text="已禁用", foreground="gray")
            return

        selected_types = []

        # 添加预设类型
        for preset_name, var in self.preset_vars.items():
            if var.get():
                selected_types.extend(self.presets[preset_name])

        # 添加自定义类型
        selected_types.extend(self.selected_types)

        # 去重
        selected_types = list(set(selected_types))

        if selected_types:
            display_text = ', '.join(selected_types[:5])
            if len(selected_types) > 5:
                display_text += f" ... (共{len(selected_types)}个)"
            self.selection_label.config(text=display_text, foreground="black")
        else:
            self.selection_label.config(text="无选择", foreground="gray")

    def get_selected_types(self) -> List[str]:
        """获取选择的文件类型"""
        if not self.enabled_var.get():
            return []

        selected_types = []

        # 添加预设类型
        for preset_name, var in self.preset_vars.items():
            if var.get():
                selected_types.extend(self.presets[preset_name])

        # 添加自定义类型
        selected_types.extend(self.selected_types)

        return list(set(selected_types))

    def is_enabled(self) -> bool:
        """是否启用"""
        return self.enabled_var.get()


class RegexValidator:
    """正则表达式验证器"""

    @staticmethod
    def validate_regex(pattern: str) -> Tuple[bool, str]:
        """
        验证正则表达式

        Args:
            pattern: 正则表达式模式

        Returns:
            tuple[bool, str]: (是否有效, 错误信息)
        """
        if not pattern.strip():
            return True, ""

        try:
            re.compile(pattern)
            return True, ""
        except re.error as e:
            return False, f"正则表达式错误: {str(e)}"


class AdvancedFilters:
    """高级过滤器"""

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="高级过滤器", padding="5")
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 正则表达式选项
        self.regex_var = tk.BooleanVar()
        self.regex_check = ttk.Checkbutton(
            self.frame,
            text="使用正则表达式匹配",
            variable=self.regex_var,
            command=self.on_regex_changed
        )
        self.regex_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        # 正则表达式帮助
        self.regex_help = ttk.Label(
            self.frame,
            text="提示: 使用 .* 匹配任意字符，\\d+ 匹配数字",
            foreground="gray",
            font=("TkDefaultFont", 8)
        )
        self.regex_help.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # 文件大小过滤
        size_frame = ttk.LabelFrame(self.frame, text="文件大小过滤", padding="3")
        size_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))

        self.size_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(
            size_frame,
            text="启用大小过滤",
            variable=self.size_enabled_var
        ).grid(row=0, column=0, columnspan=4, sticky=tk.W)

        ttk.Label(size_frame, text="最小:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.min_size_entry = ttk.Entry(size_frame, width=10)
        self.min_size_entry.grid(row=1, column=1, padx=(0, 5))

        ttk.Label(size_frame, text="最大:").grid(row=1, column=2, sticky=tk.W, padx=(10, 5))
        self.max_size_entry = ttk.Entry(size_frame, width=10)
        self.max_size_entry.grid(row=1, column=3, padx=(0, 5))

        ttk.Label(size_frame, text="(单位: KB)", foreground="gray").grid(row=2, column=0, columnspan=4, sticky=tk.W)

        # 文件时间过滤
        date_frame = ttk.LabelFrame(self.frame, text="文件时间过滤", padding="3")
        date_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

        self.date_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(
            date_frame,
            text="启用时间过滤",
            variable=self.date_enabled_var,
            command=self.on_date_filter_changed
        ).grid(row=0, column=0, columnspan=4, sticky=tk.W)

        # 开始日期
        ttk.Label(date_frame, text="开始日期:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.start_date_entry = ttk.Entry(date_frame, width=12)
        self.start_date_entry.grid(row=1, column=1, padx=(0, 5))
        self.start_date_entry.insert(0, "2024-01-01")

        # 结束日期
        ttk.Label(date_frame, text="结束日期:").grid(row=1, column=2, sticky=tk.W, padx=(10, 5))
        self.end_date_entry = ttk.Entry(date_frame, width=12)
        self.end_date_entry.grid(row=1, column=3, padx=(0, 5))
        self.end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(date_frame, text="(格式: YYYY-MM-DD)", foreground="gray").grid(row=2, column=0, columnspan=4, sticky=tk.W)

        # 初始状态
        self.on_regex_changed()
        self.on_date_filter_changed()

    def on_regex_changed(self):
        """正则表达式选项改变"""
        if self.regex_var.get():
            self.regex_help.config(foreground="blue")
        else:
            self.regex_help.config(foreground="gray")

    def on_date_filter_changed(self):
        """日期过滤器选项改变"""
        enabled = self.date_enabled_var.get()
        self.start_date_entry.configure(state='normal' if enabled else 'disabled')
        self.end_date_entry.configure(state='normal' if enabled else 'disabled')

    def get_filters(self) -> Dict[str, Any]:
        """获取过滤器设置"""
        filters = {
            "use_regex": self.regex_var.get(),
            "size_filter": {
                "enabled": self.size_enabled_var.get(),
                "min_size": 0,
                "max_size": 0
            },
            "date_filter": {
                "enabled": self.date_enabled_var.get(),
                "start_date": None,
                "end_date": None
            }
        }

        # 解析文件大小
        if self.size_enabled_var.get():
            try:
                min_size_text = self.min_size_entry.get().strip()
                if min_size_text:
                    filters["size_filter"]["min_size"] = int(float(min_size_text) * 1024)  # KB to bytes

                max_size_text = self.max_size_entry.get().strip()
                if max_size_text:
                    filters["size_filter"]["max_size"] = int(float(max_size_text) * 1024)  # KB to bytes
            except ValueError:
                pass  # 忽略无效输入

        # 解析日期
        if self.date_enabled_var.get():
            try:
                start_date_text = self.start_date_entry.get().strip()
                if start_date_text:
                    start_date = datetime.strptime(start_date_text, "%Y-%m-%d")
                    filters["date_filter"]["start_date"] = start_date.isoformat()

                end_date_text = self.end_date_entry.get().strip()
                if end_date_text:
                    end_date = datetime.strptime(end_date_text, "%Y-%m-%d")
                    # 设置为当天的23:59:59
                    end_date = end_date.replace(hour=23, minute=59, second=59)
                    filters["date_filter"]["end_date"] = end_date.isoformat()
            except ValueError:
                pass  # 忽略无效输入

        return filters

    def validate_regex_keywords(self, keywords: List[str]) -> Tuple[bool, str]:
        """验证正则表达式关键字"""
        if not self.regex_var.get():
            return True, ""

        for keyword in keywords:
            if keyword.strip():
                valid, error = RegexValidator.validate_regex(keyword.strip())
                if not valid:
                    return False, f"关键字 '{keyword}' {error}"

        return True, ""


class DragDropFrame:
    """文件选择提示框架（简化版）"""

    def __init__(self, parent, callback: Optional[Callable] = None):
        self.parent = parent
        self.callback = callback

        self.frame = ttk.LabelFrame(parent, text="压缩包选择提示", padding="10")
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 提示区域
        self.drop_label = ttk.Label(
            self.frame,
            text="📦 请使用下方按钮选择压缩包文件\n支持格式: .zip, .rar, .7z",
            font=("TkDefaultFont", 10),
            foreground="gray",
            anchor="center"
        )
        self.drop_label.pack(expand=True, fill="both", pady=10)

        # 状态标签
        self.status_label = ttk.Label(self.frame, text="", foreground="blue")
        self.status_label.pack(pady=(0, 5))

        # 提示信息
        tip_label = ttk.Label(
            self.frame,
            text="💡 提示: 选择压缩包后可在右侧预览内容",
            font=("TkDefaultFont", 8),
            foreground="gray"
        )
        tip_label.pack()

    def set_file(self, file_path: str):
        """设置文件路径"""
        if file_path:
            self.status_label.config(
                text=f"✅ 已选择: {os.path.basename(file_path)}",
                foreground="green"
            )
        else:
            self.status_label.config(text="", foreground="blue")


class ArchivePreview:
    """压缩包内容预览"""

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="压缩包内容预览", padding="5")
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 控制按钮
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", pady=(0, 5))

        self.preview_button = ttk.Button(
            button_frame,
            text="预览内容",
            command=self.preview_content
        )
        self.preview_button.pack(side=tk.LEFT)

        self.refresh_button = ttk.Button(
            button_frame,
            text="刷新",
            command=self.refresh_preview
        )
        self.refresh_button.pack(side=tk.LEFT, padx=(5, 0))

        # 统计信息
        self.stats_label = ttk.Label(self.frame, text="", foreground="gray")
        self.stats_label.pack(anchor="w", pady=(0, 5))

        # 文件列表
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill="both", expand=True)

        # 创建Treeview
        self.tree = ttk.Treeview(
            list_frame,
            columns=("size", "type", "modified"),
            show="tree headings",
            height=8
        )

        # 设置列
        self.tree.heading("#0", text="文件名")
        self.tree.heading("size", text="大小")
        self.tree.heading("type", text="类型")
        self.tree.heading("modified", text="修改时间")

        self.tree.column("#0", width=200)
        self.tree.column("size", width=80)
        self.tree.column("type", width=60)
        self.tree.column("modified", width=120)

        # 滚动条
        scrollbar_v = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        # 布局
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # 初始状态
        self.archive_path = None
        self.preview_button.configure(state="disabled")
        self.refresh_button.configure(state="disabled")

    def set_archive(self, archive_path: str):
        """设置压缩包路径"""
        self.archive_path = archive_path
        if archive_path and os.path.exists(archive_path):
            self.preview_button.configure(state="normal")
            self.refresh_button.configure(state="normal")
            self.stats_label.config(text=f"压缩包: {os.path.basename(archive_path)}")
        else:
            self.preview_button.configure(state="disabled")
            self.refresh_button.configure(state="disabled")
            self.stats_label.config(text="")
            self.clear_preview()

    def preview_content(self):
        """预览压缩包内容"""
        if not self.archive_path:
            return

        try:
            from utils import get_archive_file_list
            files_info = get_archive_file_list(self.archive_path)
            self.display_files(files_info)
        except Exception as e:
            messagebox.showerror("预览失败", f"无法预览压缩包内容: {str(e)}")

    def refresh_preview(self):
        """刷新预览"""
        self.preview_content()

    def display_files(self, files_info: List[Dict[str, Any]]):
        """显示文件列表"""
        # 清空现有内容
        self.clear_preview()

        # 统计信息
        total_files = len(files_info)
        total_size = sum(info.get('size', 0) for info in files_info)
        size_text = self.format_size(total_size)

        self.stats_label.config(
            text=f"文件总数: {total_files}, 总大小: {size_text}",
            foreground="black"
        )

        # 添加文件到树形视图
        for info in files_info:
            name = info.get('name', '')
            size = self.format_size(info.get('size', 0))
            file_type = info.get('type', '')
            modified = info.get('modified', '')

            self.tree.insert("", "end", text=name, values=(size, file_type, modified))

    def clear_preview(self):
        """清空预览"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"

        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024

        return f"{size_bytes:.1f} TB"


class UndoPanel:
    """撤销功能面板"""

    def __init__(self, parent, undo_manager):
        self.parent = parent
        self.undo_manager = undo_manager
        self.frame = ttk.LabelFrame(parent, text="撤销管理", padding="5")
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 控制按钮
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", pady=(0, 5))

        self.refresh_button = ttk.Button(
            button_frame,
            text="刷新",
            command=self.refresh_operations
        )
        self.refresh_button.pack(side="left")

        self.undo_selected_button = ttk.Button(
            button_frame,
            text="撤销选中",
            command=self.undo_selected,
            state="disabled"
        )
        self.undo_selected_button.pack(side="left", padx=(5, 0))

        self.clear_history_button = ttk.Button(
            button_frame,
            text="清空历史",
            command=self.clear_history
        )
        self.clear_history_button.pack(side="right")

        # 统计信息
        self.stats_label = ttk.Label(self.frame, text="", foreground="gray")
        self.stats_label.pack(anchor="w", pady=(0, 5))

        # 操作列表
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill="both", expand=True)

        # 创建Treeview
        self.tree = ttk.Treeview(
            list_frame,
            columns=("type", "source", "target", "time", "size"),
            show="tree headings",
            height=6
        )

        # 设置列
        self.tree.heading("#0", text="操作ID")
        self.tree.heading("type", text="类型")
        self.tree.heading("source", text="源文件")
        self.tree.heading("target", text="目标文件")
        self.tree.heading("time", text="时间")
        self.tree.heading("size", text="大小")

        self.tree.column("#0", width=100)
        self.tree.column("type", width=60)
        self.tree.column("source", width=150)
        self.tree.column("target", width=150)
        self.tree.column("time", width=120)
        self.tree.column("size", width=80)

        # 滚动条
        scrollbar_v = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        # 布局
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # 绑定选择事件
        self.tree.bind('<<TreeviewSelect>>', self.on_selection_changed)

        # 初始加载
        self.refresh_operations()

    def refresh_operations(self):
        """刷新操作列表"""
        # 清空现有内容
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 获取最近操作
        operations = self.undo_manager.get_recent_operations(50)

        # 添加到树形视图
        for op in reversed(operations):  # 最新的在前
            operation_id = op.operation_id[-8:]  # 显示ID后8位
            op_type = {"move": "移动", "copy": "复制", "link": "链接"}.get(op.operation_type, op.operation_type)
            source = os.path.basename(op.source_path)
            target = os.path.basename(op.target_path)
            time_str = op.timestamp.split('T')[1][:8] if 'T' in op.timestamp else op.timestamp[-8:]
            size = self.format_size(op.file_size)

            # 检查是否可以撤销
            can_undo = self.undo_manager.can_undo(op.operation_id)
            tags = ("can_undo",) if can_undo else ("cannot_undo",)

            self.tree.insert("", "end", text=operation_id,
                           values=(op_type, source, target, time_str, size),
                           tags=tags)

        # 设置标签样式
        self.tree.tag_configure("can_undo", foreground="black")
        self.tree.tag_configure("cannot_undo", foreground="gray")

        # 更新统计信息
        self.update_statistics()

    def update_statistics(self):
        """更新统计信息"""
        stats = self.undo_manager.get_statistics()
        total = stats.get("total", 0)
        by_type = stats.get("by_type", {})

        type_text = ", ".join([f"{k}:{v}" for k, v in by_type.items()])
        self.stats_label.config(
            text=f"总操作数: {total} ({type_text})",
            foreground="black"
        )

    def on_selection_changed(self, event):
        """选择改变事件"""
        selected = self.tree.selection()
        if selected:
            self.undo_selected_button.config(state="normal")
        else:
            self.undo_selected_button.config(state="disabled")

    def undo_selected(self):
        """撤销选中的操作"""
        selected = self.tree.selection()
        if not selected:
            return

        # 获取选中的操作ID
        operation_ids = []
        for item in selected:
            operation_id_short = self.tree.item(item, "text")
            # 找到完整的操作ID
            for op in self.undo_manager.operations:
                if op.operation_id.endswith(operation_id_short):
                    operation_ids.append(op.operation_id)
                    break

        if not operation_ids:
            messagebox.showwarning("撤销失败", "未找到有效的操作记录")
            return

        # 确认撤销
        count = len(operation_ids)
        result = messagebox.askyesno(
            "确认撤销",
            f"确定要撤销 {count} 个操作吗？\n\n注意：撤销操作不可逆！"
        )

        if result:
            success_count = 0
            for op_id in operation_ids:
                if self.undo_manager.undo_operation(op_id):
                    success_count += 1

            messagebox.showinfo(
                "撤销完成",
                f"成功撤销 {success_count}/{count} 个操作"
            )

            self.refresh_operations()

    def clear_history(self):
        """清空撤销历史"""
        result = messagebox.askyesno(
            "确认清空",
            "确定要清空所有撤销历史吗？\n\n这将删除所有备份文件，操作不可逆！"
        )

        if result:
            self.undo_manager.clear_history()
            self.refresh_operations()
            messagebox.showinfo("清空完成", "撤销历史已清空")

    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"

        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024

        return f"{size_bytes:.1f} TB"