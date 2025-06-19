#!/usr/bin/env python3
"""
图标管理器模块
提供Material Design风格的SVG图标
"""

import tkinter as tk
from tkinter import ttk
import base64
from io import BytesIO

class IconManager:
    """Material Design图标管理器"""
    
    def __init__(self):
        self.icons = {}
        self.load_icons()
    
    def load_icons(self):
        """加载Material Design图标"""
        # 文件夹图标
        self.icons['folder'] = "📁"
        
        # 搜索图标
        self.icons['search'] = "🔍"
        
        # 设置图标
        self.icons['settings'] = "⚙️"
        
        # 预览图标
        self.icons['preview'] = "👁️"
        
        # 开始/播放图标
        self.icons['play'] = "▶️"
        
        # 成功图标
        self.icons['success'] = "✅"
        
        # 警告图标
        self.icons['warning'] = "⚠️"
        
        # 错误图标
        self.icons['error'] = "❌"
        
        # 信息图标
        self.icons['info'] = "ℹ️"
        
        # 删除图标
        self.icons['delete'] = "🗑️"
        
        # 主题切换图标
        self.icons['theme'] = "🌓"
        
        # 火箭图标
        self.icons['rocket'] = "🚀"
        
        # 包裹图标
        self.icons['package'] = "📦"
        
        # 复制图标
        self.icons['copy'] = "📋"
        
        # 链接图标
        self.icons['link'] = "🔗"
        
        # 移动图标
        self.icons['move'] = "📁"
        
        # 帮助图标
        self.icons['help'] = "❓"
        
        # 关于图标
        self.icons['about'] = "ℹ️"
        
        # 刷新图标
        self.icons['refresh'] = "🔄"
        
        # 清空图标
        self.icons['clear'] = "🗑️"
        
        # 统计图标
        self.icons['stats'] = "📊"
        
        # 时间图标
        self.icons['time'] = "⏱️"
        
        # 文件图标
        self.icons['file'] = "📄"
        
        # 完成图标
        self.icons['done'] = "🎉"
        
        # 处理中图标
        self.icons['processing'] = "⚙️"
        
        # 就绪图标
        self.icons['ready'] = "⚪"
        
        # 失败图标
        self.icons['failed'] = "❌"
    
    def get_icon(self, name, fallback=""):
        """获取图标"""
        return self.icons.get(name, fallback)
    
    def get_button_text(self, icon_name, text):
        """获取带图标的按钮文本"""
        icon = self.get_icon(icon_name)
        return f"{icon} {text}" if icon else text
    
    def create_icon_label(self, parent, icon_name, size=16, **kwargs):
        """创建图标标签"""
        icon = self.get_icon(icon_name)
        return tk.Label(parent, text=icon, font=('Segoe UI Emoji', size), **kwargs)

# 全局图标管理器实例
icon_manager = IconManager()
