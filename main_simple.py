#!/usr/bin/env python3
"""
FileMover v4.0 - 简化版本
专为Windows可执行文件优化的版本
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
import zipfile
import rarfile
import py7zr
import shutil
import re
import json
from pathlib import Path


class SimpleFileMover:
    def __init__(self, root):
        self.root = root
        self.root.title("FileMover v4.0 - Simple Edition")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 设置颜色主题
        self.setup_colors()
        
        # 初始化变量
        self.archive_var = tk.StringVar()
        self.operation_var = tk.StringVar(value="move")
        
        # 创建界面
        self.create_ui()
        
        # 居中显示
        self.center_window()
    
    def setup_colors(self):
        """设置颜色方案"""
        self.colors = {
            'bg': '#2D2D2D',
            'surface': '#3D3D3D',
            'primary': '#1976D2',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'text': '#FFFFFF',
            'text_secondary': '#CCCCCC'
        }
    
    def create_ui(self):
        """创建用户界面"""
        # 设置根窗口背景
        self.root.configure(bg=self.colors['bg'])
        
        # 主容器
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(main_frame,
                             text="📦 FileMover v4.0",
                             font=('Microsoft YaHei UI', 20, 'bold'),
                             fg=self.colors['primary'],
                             bg=self.colors['bg'])
        title_label.pack(pady=(0, 20))
        
        # 文件选择区域
        self.create_file_section(main_frame)
        
        # 关键字输入区域
        self.create_keyword_section(main_frame)
        
        # 操作模式区域
        self.create_mode_section(main_frame)
        
        # 按钮区域
        self.create_button_section(main_frame)
        
        # 状态区域
        self.create_status_section(main_frame)
    
    def create_file_section(self, parent):
        """创建文件选择区域"""
        # 文件选择框架
        file_frame = tk.LabelFrame(parent,
                                 text="📁 文件选择",
                                 font=('Microsoft YaHei UI', 12, 'bold'),
                                 fg=self.colors['text'],
                                 bg=self.colors['surface'],
                                 bd=2,
                                 relief='groove')
        file_frame.pack(fill="x", pady=(0, 15))
        
        # 文件路径输入
        path_frame = tk.Frame(file_frame, bg=self.colors['surface'])
        path_frame.pack(fill="x", padx=15, pady=15)
        
        tk.Label(path_frame,
               text="压缩包路径:",
               font=('Microsoft YaHei UI', 10),
               fg=self.colors['text'],
               bg=self.colors['surface']).pack(anchor="w")
        
        input_frame = tk.Frame(path_frame, bg=self.colors['surface'])
        input_frame.pack(fill="x", pady=(5, 0))
        
        self.path_entry = tk.Entry(input_frame,
                                 textvariable=self.archive_var,
                                 font=('Microsoft YaHei UI', 10),
                                 bg='white',
                                 fg='black')
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(input_frame,
                             text="📂 浏览",
                             command=self.browse_file,
                             font=('Microsoft YaHei UI', 10, 'bold'),
                             bg=self.colors['primary'],
                             fg='white',
                             relief='flat',
                             padx=20)
        browse_btn.pack(side="right")
    
    def create_keyword_section(self, parent):
        """创建关键字输入区域"""
        keyword_frame = tk.LabelFrame(parent,
                                    text="🔍 关键字设置",
                                    font=('Microsoft YaHei UI', 12, 'bold'),
                                    fg=self.colors['text'],
                                    bg=self.colors['surface'],
                                    bd=2,
                                    relief='groove')
        keyword_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # 说明
        tk.Label(keyword_frame,
               text="输入搜索关键字，每行一个：",
               font=('Microsoft YaHei UI', 10),
               fg=self.colors['text'],
               bg=self.colors['surface']).pack(anchor="w", padx=15, pady=(15, 5))
        
        # 文本输入区域
        text_frame = tk.Frame(keyword_frame, bg=self.colors['surface'])
        text_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.keyword_text = tk.Text(text_frame,
                                  height=8,
                                  font=('Microsoft YaHei UI', 10),
                                  bg='white',
                                  fg='black',
                                  wrap=tk.WORD)
        
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.keyword_text.yview)
        self.keyword_text.configure(yscrollcommand=scrollbar.set)
        
        self.keyword_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_mode_section(self, parent):
        """创建操作模式区域"""
        mode_frame = tk.LabelFrame(parent,
                                 text="⚙️ 操作模式",
                                 font=('Microsoft YaHei UI', 12, 'bold'),
                                 fg=self.colors['text'],
                                 bg=self.colors['surface'],
                                 bd=2,
                                 relief='groove')
        mode_frame.pack(fill="x", pady=(0, 15))
        
        radio_frame = tk.Frame(mode_frame, bg=self.colors['surface'])
        radio_frame.pack(fill="x", padx=15, pady=15)
        
        # 单选按钮
        modes = [
            ("move", "📁 移动文件"),
            ("copy", "📋 复制文件"),
            ("link", "🔗 创建链接")
        ]
        
        for value, text in modes:
            radio = tk.Radiobutton(radio_frame,
                                 text=text,
                                 variable=self.operation_var,
                                 value=value,
                                 font=('Microsoft YaHei UI', 10),
                                 fg=self.colors['text'],
                                 bg=self.colors['surface'],
                                 selectcolor=self.colors['primary'],
                                 activebackground=self.colors['surface'])
            radio.pack(side="left", padx=(0, 30))
    
    def create_button_section(self, parent):
        """创建按钮区域"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill="x", pady=(0, 15))
        
        # 预览按钮
        preview_btn = tk.Button(button_frame,
                              text="👁️ 预览匹配文件",
                              command=self.preview_files,
                              font=('Microsoft YaHei UI', 11, 'bold'),
                              bg=self.colors['primary'],
                              fg='white',
                              relief='flat',
                              padx=30,
                              pady=10)
        preview_btn.pack(side="left", padx=(0, 15))
        
        # 开始处理按钮
        start_btn = tk.Button(button_frame,
                            text="🚀 开始处理",
                            command=self.start_processing,
                            font=('Microsoft YaHei UI', 11, 'bold'),
                            bg=self.colors['success'],
                            fg='white',
                            relief='flat',
                            padx=30,
                            pady=10)
        start_btn.pack(side="left")
        
        # 清空按钮
        clear_btn = tk.Button(button_frame,
                            text="🗑️ 清空",
                            command=self.clear_keywords,
                            font=('Microsoft YaHei UI', 11, 'bold'),
                            bg=self.colors['warning'],
                            fg='white',
                            relief='flat',
                            padx=30,
                            pady=10)
        clear_btn.pack(side="right")
    
    def create_status_section(self, parent):
        """创建状态显示区域"""
        status_frame = tk.LabelFrame(parent,
                                   text="📊 处理状态",
                                   font=('Microsoft YaHei UI', 12, 'bold'),
                                   fg=self.colors['text'],
                                   bg=self.colors['surface'],
                                   bd=2,
                                   relief='groove')
        status_frame.pack(fill="x")
        
        self.status_label = tk.Label(status_frame,
                                   text="就绪",
                                   font=('Microsoft YaHei UI', 11),
                                   fg=self.colors['text'],
                                   bg=self.colors['surface'])
        self.status_label.pack(padx=15, pady=15)
    
    def center_window(self):
        """居中显示窗口"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def browse_file(self):
        """浏览文件"""
        file_path = filedialog.askopenfilename(
            title="选择压缩包",
            filetypes=[
                ("压缩包文件", "*.zip;*.rar;*.7z"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.archive_var.set(file_path)
    
    def clear_keywords(self):
        """清空关键字"""
        self.keyword_text.delete(1.0, tk.END)
    
    def preview_files(self):
        """预览文件"""
        messagebox.showinfo("预览", "预览功能开发中...")
    
    def start_processing(self):
        """开始处理"""
        archive_path = self.archive_var.get().strip()
        if not archive_path:
            messagebox.showerror("错误", "请选择压缩包文件")
            return
        
        keywords = self.keyword_text.get(1.0, tk.END).strip()
        if not keywords:
            messagebox.showerror("错误", "请输入关键字")
            return
        
        messagebox.showinfo("处理", "处理功能开发中...")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleFileMover(root)
    root.mainloop()
