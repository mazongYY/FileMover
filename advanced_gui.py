#!/usr/bin/env python3
"""
高级GUI组件模块
包含文件类型选择、过滤器设置等高级界面组件
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import re


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
    def validate_regex(pattern: str) -> tuple[bool, str]:
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
        
        # 初始状态
        self.on_regex_changed()
    
    def on_regex_changed(self):
        """正则表达式选项改变"""
        if self.regex_var.get():
            self.regex_help.config(foreground="blue")
        else:
            self.regex_help.config(foreground="gray")
    
    def get_filters(self) -> Dict[str, Any]:
        """获取过滤器设置"""
        filters = {
            "use_regex": self.regex_var.get(),
            "size_filter": {
                "enabled": self.size_enabled_var.get(),
                "min_size": 0,
                "max_size": 0
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
        
        return filters
    
    def validate_regex_keywords(self, keywords: List[str]) -> tuple[bool, str]:
        """验证正则表达式关键字"""
        if not self.regex_var.get():
            return True, ""
        
        for keyword in keywords:
            if keyword.strip():
                valid, error = RegexValidator.validate_regex(keyword.strip())
                if not valid:
                    return False, f"关键字 '{keyword}' {error}"
        
        return True, ""
