#!/usr/bin/env python3
"""
现代化UI设计模块
实现Material Design风格的卡片式布局
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from icon_manager import icon_manager


class ModernCard:
    """现代化卡片组件"""
    
    def __init__(self, parent, title, icon="", colors=None):
        self.parent = parent
        self.title = title
        self.icon = icon
        self.colors = colors or self.get_default_colors()
        
        self.create_card()
    
    def get_default_colors(self):
        """获取默认颜色方案"""
        return {
            'surface': '#FFFFFF',
            'background': '#FAFAFA',
            'text_primary': '#212121',
            'text_secondary': '#757575',
            'divider': '#E0E0E0',
            'shadow': '#00000020'
        }
    
    def create_card(self):
        """创建卡片"""
        # 卡片容器
        self.container = tk.Frame(self.parent, bg=self.colors['background'])
        self.container.pack(fill="x", padx=16, pady=8)
        
        # 阴影效果
        shadow = tk.Frame(self.container, bg=self.colors['shadow'], height=2)
        shadow.pack(fill="x", padx=2, pady=(2, 0))
        
        # 卡片主体
        self.card = tk.Frame(self.container, 
                           bg=self.colors['surface'],
                           relief='flat',
                           bd=0)
        self.card.pack(fill="x")
        
        # 卡片头部
        self.header = tk.Frame(self.card, bg=self.colors['surface'], height=56)
        self.header.pack(fill="x", padx=16, pady=(16, 0))
        self.header.pack_propagate(False)
        
        # 标题
        title_text = f"{self.icon} {self.title}" if self.icon else self.title
        self.title_label = tk.Label(self.header,
                                  text=title_text,
                                  font=('Microsoft YaHei UI', 14, 'bold'),
                                  fg=self.colors['text_primary'],
                                  bg=self.colors['surface'])
        self.title_label.pack(side="left", anchor="w")
        
        # 卡片内容区域
        self.content = tk.Frame(self.card, bg=self.colors['surface'])
        self.content.pack(fill="both", expand=True, padx=16, pady=(8, 16))
        
        return self.content


class ModernButton:
    """现代化按钮组件"""
    
    def __init__(self, parent, text, command=None, style="primary", icon="", colors=None):
        self.parent = parent
        self.text = text
        self.command = command
        self.style = style
        self.icon = icon
        self.colors = colors or self.get_default_colors()
        
        self.create_button()
    
    def get_default_colors(self):
        """获取默认颜色方案"""
        return {
            'primary': '#1976D2',
            'primary_variant': '#1565C0',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'surface': '#FFFFFF',
            'text_primary': '#212121'
        }
    
    def create_button(self):
        """创建按钮"""
        # 按钮容器
        self.container = tk.Frame(self.parent, bg=self.colors['surface'])
        
        # 根据样式设置颜色
        if self.style == "primary":
            bg_color = self.colors['primary']
            fg_color = '#FFFFFF'
        elif self.style == "success":
            bg_color = self.colors['success']
            fg_color = '#FFFFFF'
        elif self.style == "warning":
            bg_color = self.colors['warning']
            fg_color = '#FFFFFF'
        else:  # outlined
            bg_color = self.colors['surface']
            fg_color = self.colors['primary']
        
        # 按钮文本
        button_text = f"{self.icon} {self.text}" if self.icon else self.text
        
        # 创建按钮
        self.button = tk.Button(self.container,
                              text=button_text,
                              command=self.command,
                              bg=bg_color,
                              fg=fg_color,
                              font=('Microsoft YaHei UI', 10, 'bold'),
                              relief='flat',
                              bd=0,
                              padx=24,
                              pady=12,
                              cursor='hand2')
        self.button.pack()
        
        # 绑定悬停效果
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)
        
        return self.container
    
    def on_enter(self, event):
        """鼠标悬停效果"""
        if self.style == "primary":
            self.button.config(bg=self.colors['primary_variant'])
        elif self.style == "outlined":
            self.button.config(bg='#E3F2FD')
    
    def on_leave(self, event):
        """鼠标离开效果"""
        if self.style == "primary":
            self.button.config(bg=self.colors['primary'])
        elif self.style == "outlined":
            self.button.config(bg=self.colors['surface'])


class ModernInput:
    """现代化输入框组件"""
    
    def __init__(self, parent, label="", placeholder="", colors=None):
        self.parent = parent
        self.label = label
        self.placeholder = placeholder
        self.colors = colors or self.get_default_colors()
        
        self.create_input()
    
    def get_default_colors(self):
        """获取默认颜色方案"""
        return {
            'surface': '#FFFFFF',
            'primary': '#1976D2',
            'text_primary': '#212121',
            'text_secondary': '#757575',
            'border': '#E0E0E0'
        }
    
    def create_input(self):
        """创建输入框"""
        # 输入框容器
        self.container = tk.Frame(self.parent, bg=self.colors['surface'])
        
        # 标签
        if self.label:
            self.label_widget = tk.Label(self.container,
                                       text=self.label,
                                       font=('Microsoft YaHei UI', 10, 'bold'),
                                       fg=self.colors['text_primary'],
                                       bg=self.colors['surface'])
            self.label_widget.pack(anchor="w", pady=(0, 4))
        
        # 输入框边框
        self.input_frame = tk.Frame(self.container,
                                  bg=self.colors['border'],
                                  relief='solid',
                                  bd=1)
        self.input_frame.pack(fill="x", pady=(0, 8))
        
        # 输入框
        self.entry = tk.Entry(self.input_frame,
                            font=('Microsoft YaHei UI', 11),
                            bg=self.colors['surface'],
                            fg=self.colors['text_primary'],
                            relief='flat',
                            bd=0)
        self.entry.pack(fill="x", padx=12, pady=8)
        
        # 绑定焦点事件
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        
        # 设置占位符
        if self.placeholder:
            self.set_placeholder()
        
        return self.container
    
    def set_placeholder(self):
        """设置占位符"""
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=self.colors['text_secondary'])
        
        def on_click(event):
            if self.entry.get() == self.placeholder:
                self.entry.delete(0, tk.END)
                self.entry.config(fg=self.colors['text_primary'])
        
        def on_leave(event):
            if not self.entry.get():
                self.entry.insert(0, self.placeholder)
                self.entry.config(fg=self.colors['text_secondary'])
        
        self.entry.bind("<Button-1>", on_click)
        self.entry.bind("<FocusOut>", on_leave)
    
    def on_focus_in(self, event):
        """获得焦点"""
        self.input_frame.config(bg=self.colors['primary'], bd=2)
    
    def on_focus_out(self, event):
        """失去焦点"""
        self.input_frame.config(bg=self.colors['border'], bd=1)
    
    def get(self):
        """获取输入值"""
        value = self.entry.get()
        return value if value != self.placeholder else ""
    
    def set(self, value):
        """设置输入值"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.entry.config(fg=self.colors['text_primary'])


class ModernProgressBar:
    """现代化进度条组件"""
    
    def __init__(self, parent, colors=None):
        self.parent = parent
        self.colors = colors or self.get_default_colors()
        self.progress_value = 0
        
        self.create_progress_bar()
    
    def get_default_colors(self):
        """获取默认颜色方案"""
        return {
            'primary': '#1976D2',
            'surface': '#FFFFFF',
            'background': '#E0E0E0'
        }
    
    def create_progress_bar(self):
        """创建进度条"""
        # 进度条容器
        self.container = tk.Frame(self.parent, bg=self.colors['surface'])
        
        # 进度条背景
        self.bg_frame = tk.Frame(self.container,
                               bg=self.colors['background'],
                               height=4)
        self.bg_frame.pack(fill="x", pady=4)
        
        # 进度条前景
        self.fg_frame = tk.Frame(self.bg_frame,
                               bg=self.colors['primary'],
                               height=4)
        
        return self.container
    
    def set_progress(self, value):
        """设置进度值 (0-100)"""
        self.progress_value = max(0, min(100, value))
        
        # 计算宽度
        total_width = self.bg_frame.winfo_width()
        if total_width > 1:
            progress_width = int(total_width * self.progress_value / 100)
            self.fg_frame.place(x=0, y=0, width=progress_width, height=4)
    
    def start_indeterminate(self):
        """开始不确定进度动画"""
        self.animate_progress()
    
    def animate_progress(self):
        """动画效果"""
        # 简单的左右移动动画
        pass  # 后续实现
