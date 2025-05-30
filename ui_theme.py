#!/usr/bin/env python3
"""
UI主题美化模块
提供现代化的界面主题和样式
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from typing import Dict, Any, Optional


class ModernTheme:
    """现代化主题配置"""

    # 颜色方案
    COLORS = {
        # 主色调 - 深蓝色系
        'primary': '#2563eb',           # 主要蓝色
        'primary_light': '#3b82f6',     # 浅蓝色
        'primary_dark': '#1d4ed8',      # 深蓝色

        # 背景色
        'bg_primary': '#ffffff',        # 主背景 - 白色
        'bg_secondary': '#f8fafc',      # 次背景 - 浅灰
        'bg_tertiary': '#f1f5f9',       # 第三背景
        'bg_dark': '#1e293b',           # 深色背景

        # 文字颜色
        'text_primary': '#1e293b',      # 主要文字
        'text_secondary': '#64748b',    # 次要文字
        'text_muted': '#94a3b8',        # 弱化文字
        'text_white': '#ffffff',        # 白色文字

        # 边框和分割线
        'border': '#e2e8f0',            # 边框色
        'border_focus': '#3b82f6',      # 焦点边框
        'divider': '#e2e8f0',           # 分割线

        # 状态颜色
        'success': '#10b981',           # 成功 - 绿色
        'warning': '#f59e0b',           # 警告 - 橙色
        'error': '#ef4444',             # 错误 - 红色
        'info': '#06b6d4',              # 信息 - 青色

        # 按钮颜色
        'btn_primary': '#2563eb',       # 主按钮
        'btn_primary_hover': '#1d4ed8', # 主按钮悬停
        'btn_secondary': '#6b7280',     # 次按钮
        'btn_secondary_hover': '#4b5563', # 次按钮悬停
        'btn_success': '#10b981',       # 成功按钮
        'btn_danger': '#ef4444',        # 危险按钮

        # 输入框颜色
        'input_bg': '#ffffff',          # 输入框背景
        'input_border': '#d1d5db',      # 输入框边框
        'input_focus': '#3b82f6',       # 输入框焦点

        # 选择和高亮
        'selection': '#dbeafe',         # 选择背景
        'highlight': '#fef3c7',         # 高亮背景
        'hover': '#f3f4f6',             # 悬停背景
    }

    # 字体配置
    FONTS = {
        'default': ('Segoe UI', 9),
        'heading_large': ('Segoe UI', 16, 'bold'),
        'heading_medium': ('Segoe UI', 14, 'bold'),
        'heading_small': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 9),
        'body_bold': ('Segoe UI', 9, 'bold'),
        'caption': ('Segoe UI', 8),
        'code': ('Consolas', 9),
        'button': ('Segoe UI', 9, 'bold'),
    }

    # 间距配置
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 24,
        'xxl': 32,
    }

    # 圆角配置
    RADIUS = {
        'sm': 4,
        'md': 6,
        'lg': 8,
        'xl': 12,
    }


class UIStyler:
    """UI样式管理器"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.theme = ModernTheme()
        self.style = ttk.Style()
        self.setup_theme()

    def setup_theme(self):
        """设置主题样式"""
        # 设置主题
        self.style.theme_use('clam')

        # 配置根窗口
        self.root.configure(bg=self.theme.COLORS['bg_primary'])

        # 配置ttk样式
        self.configure_ttk_styles()

        # 配置字体
        self.configure_fonts()

    def configure_ttk_styles(self):
        """配置ttk组件样式"""
        colors = self.theme.COLORS

        # Frame样式
        self.style.configure('Modern.TFrame',
                           background=colors['bg_primary'],
                           relief='flat',
                           borderwidth=0)

        self.style.configure('Card.TFrame',
                           background=colors['bg_secondary'],
                           relief='solid',
                           borderwidth=1,
                           bordercolor=colors['border'])

        # LabelFrame样式
        self.style.configure('Modern.TLabelframe',
                           background=colors['bg_primary'],
                           bordercolor=colors['border'],
                           borderwidth=1,
                           relief='solid')

        self.style.configure('Modern.TLabelframe.Label',
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'],
                           font=self.theme.FONTS['heading_small'])

        # Button样式
        self.style.configure('Primary.TButton',
                           background=colors['btn_primary'],
                           foreground=colors['text_white'],
                           borderwidth=0,
                           focuscolor='none',
                           font=self.theme.FONTS['button'])

        self.style.map('Primary.TButton',
                      background=[('active', colors['btn_primary_hover']),
                                ('pressed', colors['primary_dark'])])

        self.style.configure('Secondary.TButton',
                           background=colors['btn_secondary'],
                           foreground=colors['text_white'],
                           borderwidth=0,
                           focuscolor='none',
                           font=self.theme.FONTS['button'])

        self.style.map('Secondary.TButton',
                      background=[('active', colors['btn_secondary_hover'])])

        self.style.configure('Success.TButton',
                           background=colors['btn_success'],
                           foreground=colors['text_white'],
                           borderwidth=0,
                           focuscolor='none',
                           font=self.theme.FONTS['button'])

        self.style.configure('Danger.TButton',
                           background=colors['btn_danger'],
                           foreground=colors['text_white'],
                           borderwidth=0,
                           focuscolor='none',
                           font=self.theme.FONTS['button'])

        # Entry样式
        self.style.configure('Modern.TEntry',
                           fieldbackground=colors['input_bg'],
                           bordercolor=colors['input_border'],
                           borderwidth=1,
                           insertcolor=colors['text_primary'],
                           font=self.theme.FONTS['body'])

        self.style.map('Modern.TEntry',
                      bordercolor=[('focus', colors['input_focus'])])

        # Combobox样式
        self.style.configure('Modern.TCombobox',
                           fieldbackground=colors['input_bg'],
                           bordercolor=colors['input_border'],
                           borderwidth=1,
                           font=self.theme.FONTS['body'])

        # Checkbutton样式
        self.style.configure('Modern.TCheckbutton',
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'],
                           focuscolor='none',
                           font=self.theme.FONTS['body'])

        # Radiobutton样式
        self.style.configure('Modern.TRadiobutton',
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'],
                           focuscolor='none',
                           font=self.theme.FONTS['body'])

        # Label样式
        self.style.configure('Modern.TLabel',
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'],
                           font=self.theme.FONTS['body'])

        self.style.configure('Heading.TLabel',
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'],
                           font=self.theme.FONTS['heading_medium'])

        self.style.configure('Caption.TLabel',
                           background=colors['bg_primary'],
                           foreground=colors['text_secondary'],
                           font=self.theme.FONTS['caption'])

        # Notebook样式
        self.style.configure('Modern.TNotebook',
                           background=colors['bg_primary'],
                           borderwidth=0)

        self.style.configure('Modern.TNotebook.Tab',
                           background=colors['bg_tertiary'],
                           foreground=colors['text_secondary'],
                           padding=[12, 8],
                           font=self.theme.FONTS['body_bold'])

        self.style.map('Modern.TNotebook.Tab',
                      background=[('selected', colors['bg_primary']),
                                ('active', colors['hover'])],
                      foreground=[('selected', colors['text_primary'])])

        # Treeview样式
        self.style.configure('Modern.Treeview',
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'],
                           fieldbackground=colors['bg_primary'],
                           borderwidth=1,
                           bordercolor=colors['border'],
                           font=self.theme.FONTS['body'])

        self.style.configure('Modern.Treeview.Heading',
                           background=colors['bg_secondary'],
                           foreground=colors['text_primary'],
                           borderwidth=1,
                           bordercolor=colors['border'],
                           font=self.theme.FONTS['body_bold'])

        self.style.map('Modern.Treeview',
                      background=[('selected', colors['selection'])],
                      foreground=[('selected', colors['text_primary'])])

        # Progressbar样式
        self.style.configure('Modern.TProgressbar',
                           background=colors['primary'],
                           borderwidth=0,
                           lightcolor=colors['primary'],
                           darkcolor=colors['primary'])

        # Scrollbar样式
        self.style.configure('Modern.Vertical.TScrollbar',
                           background=colors['bg_tertiary'],
                           bordercolor=colors['border'],
                           arrowcolor=colors['text_secondary'],
                           darkcolor=colors['bg_tertiary'],
                           lightcolor=colors['bg_tertiary'])

        self.style.configure('Modern.Horizontal.TScrollbar',
                           background=colors['bg_tertiary'],
                           bordercolor=colors['border'],
                           arrowcolor=colors['text_secondary'],
                           darkcolor=colors['bg_tertiary'],
                           lightcolor=colors['bg_tertiary'])

    def configure_fonts(self):
        """配置字体"""
        # 设置默认字体
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=9)

        text_font = tkFont.nametofont("TkTextFont")
        text_font.configure(family="Segoe UI", size=9)

        fixed_font = tkFont.nametofont("TkFixedFont")
        fixed_font.configure(family="Consolas", size=9)

    def create_card_frame(self, parent, **kwargs) -> ttk.Frame:
        """创建卡片样式的框架"""
        frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return frame

    def create_section_frame(self, parent, title: str, **kwargs) -> ttk.LabelFrame:
        """创建带标题的区域框架"""
        frame = ttk.LabelFrame(parent, text=title, style='Modern.TLabelframe', **kwargs)
        return frame

    def create_primary_button(self, parent, text: str, **kwargs) -> ttk.Button:
        """创建主要按钮"""
        return ttk.Button(parent, text=text, style='Primary.TButton', **kwargs)

    def create_secondary_button(self, parent, text: str, **kwargs) -> ttk.Button:
        """创建次要按钮"""
        return ttk.Button(parent, text=text, style='Secondary.TButton', **kwargs)

    def create_success_button(self, parent, text: str, **kwargs) -> ttk.Button:
        """创建成功按钮"""
        return ttk.Button(parent, text=text, style='Success.TButton', **kwargs)

    def create_danger_button(self, parent, text: str, **kwargs) -> ttk.Button:
        """创建危险按钮"""
        return ttk.Button(parent, text=text, style='Danger.TButton', **kwargs)

    def create_modern_entry(self, parent, **kwargs) -> ttk.Entry:
        """创建现代化输入框"""
        return ttk.Entry(parent, style='Modern.TEntry', **kwargs)

    def create_modern_combobox(self, parent, **kwargs) -> ttk.Combobox:
        """创建现代化下拉框"""
        return ttk.Combobox(parent, style='Modern.TCombobox', **kwargs)

    def create_heading_label(self, parent, text: str, **kwargs) -> ttk.Label:
        """创建标题标签"""
        return ttk.Label(parent, text=text, style='Heading.TLabel', **kwargs)

    def create_caption_label(self, parent, text: str, **kwargs) -> ttk.Label:
        """创建说明标签"""
        return ttk.Label(parent, text=text, style='Caption.TLabel', **kwargs)

    def create_modern_treeview(self, parent, **kwargs) -> ttk.Treeview:
        """创建现代化树形视图"""
        return ttk.Treeview(parent, style='Modern.Treeview', **kwargs)

    def create_modern_notebook(self, parent, **kwargs) -> ttk.Notebook:
        """创建现代化标签页"""
        return ttk.Notebook(parent, style='Modern.TNotebook', **kwargs)

    def add_hover_effect(self, widget, hover_color: Optional[str] = None):
        """为组件添加悬停效果"""
        if hover_color is None:
            hover_color = self.theme.COLORS['hover']

        original_bg = widget.cget('background') if hasattr(widget, 'cget') else None

        def on_enter(event):
            if hasattr(widget, 'configure'):
                widget.configure(background=hover_color)

        def on_leave(event):
            if hasattr(widget, 'configure') and original_bg:
                widget.configure(background=original_bg)

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    def add_shadow_effect(self, widget):
        """为组件添加阴影效果（模拟）"""
        # 在tkinter中模拟阴影效果
        shadow_frame = tk.Frame(widget.master,
                               bg=self.theme.COLORS['text_muted'],
                               height=2, width=2)

        # 获取组件位置并放置阴影
        widget.update_idletasks()
        x = widget.winfo_x() + 2
        y = widget.winfo_y() + 2
        shadow_frame.place(x=x, y=y,
                          width=widget.winfo_width(),
                          height=widget.winfo_height())

        # 确保原组件在阴影之上
        widget.lift()


class IconManager:
    """图标管理器"""

    # Unicode图标字典
    ICONS = {
        'file': '📄',
        'folder': '📁',
        'archive': '📦',
        'search': '🔍',
        'filter': '🔽',
        'settings': '⚙️',
        'history': '📋',
        'undo': '↩️',
        'redo': '↪️',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌',
        'info': 'ℹ️',
        'lock': '🔒',
        'unlock': '🔓',
        'download': '⬇️',
        'upload': '⬆️',
        'refresh': '🔄',
        'clear': '🗑️',
        'save': '💾',
        'copy': '📋',
        'move': '➡️',
        'link': '🔗',
        'preview': '👁️',
        'close': '✖️',
        'minimize': '➖',
        'maximize': '⬜',
        'menu': '☰',
        'home': '🏠',
        'back': '⬅️',
        'forward': '➡️',
        'up': '⬆️',
        'down': '⬇️',
        'left': '⬅️',
        'right': '➡️',
        'plus': '➕',
        'minus': '➖',
        'check': '✓',
        'cross': '✗',
        'star': '⭐',
        'heart': '❤️',
        'thumbs_up': '👍',
        'thumbs_down': '👎',
    }

    @classmethod
    def get_icon(cls, name: str, fallback: str = '') -> str:
        """获取图标"""
        return cls.ICONS.get(name, fallback)

    @classmethod
    def create_icon_label(cls, parent, icon_name: str, text: str = '', **kwargs) -> ttk.Label:
        """创建带图标的标签"""
        icon = cls.get_icon(icon_name)
        display_text = f"{icon} {text}" if text else icon
        return ttk.Label(parent, text=display_text, **kwargs)


class ModernComponents:
    """现代化组件库"""

    def __init__(self, styler: UIStyler):
        self.styler = styler
        self.theme = styler.theme

    def create_status_bar(self, parent) -> tk.Frame:
        """创建状态栏"""
        status_frame = tk.Frame(parent,
                               bg=self.theme.COLORS['bg_secondary'],
                               height=30,
                               relief='flat',
                               bd=1)

        # 状态文本
        self.status_text = tk.StringVar(value="就绪")
        status_label = tk.Label(status_frame,
                               textvariable=self.status_text,
                               bg=self.theme.COLORS['bg_secondary'],
                               fg=self.theme.COLORS['text_secondary'],
                               font=self.theme.FONTS['caption'],
                               anchor='w')
        status_label.pack(side='left', padx=10, pady=5)

        # 版本信息
        version_label = tk.Label(status_frame,
                                text="v4.0 专业版",
                                bg=self.theme.COLORS['bg_secondary'],
                                fg=self.theme.COLORS['text_muted'],
                                font=self.theme.FONTS['caption'])
        version_label.pack(side='right', padx=10, pady=5)

        return status_frame

    def create_toolbar(self, parent) -> tk.Frame:
        """创建工具栏"""
        toolbar = tk.Frame(parent,
                          bg=self.theme.COLORS['bg_secondary'],
                          height=50,
                          relief='flat',
                          bd=1)

        # 工具栏按钮样式
        btn_style = {
            'bg': self.theme.COLORS['bg_secondary'],
            'fg': self.theme.COLORS['text_primary'],
            'font': self.theme.FONTS['body'],
            'relief': 'flat',
            'bd': 0,
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2'
        }

        # 添加工具栏按钮
        buttons = [
            ('📁 打开', None),
            ('🔍 预览', None),
            ('▶️ 开始', None),
            ('↩️ 撤销', None),
            ('⚙️ 设置', None),
        ]

        for text, command in buttons:
            btn = tk.Button(toolbar, text=text, command=command, **btn_style)
            btn.pack(side='left', padx=2)

            # 添加悬停效果
            self.add_button_hover_effect(btn)

        return toolbar

    def add_button_hover_effect(self, button):
        """为按钮添加悬停效果"""
        original_bg = button.cget('bg')
        hover_bg = self.theme.COLORS['hover']

        def on_enter(event):
            button.configure(bg=hover_bg)

        def on_leave(event):
            button.configure(bg=original_bg)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    def create_progress_card(self, parent) -> tk.Frame:
        """创建进度卡片"""
        card = tk.Frame(parent,
                       bg=self.theme.COLORS['bg_primary'],
                       relief='solid',
                       bd=1,
                       highlightbackground=self.theme.COLORS['border'])

        # 标题
        title_label = tk.Label(card,
                              text="处理进度",
                              bg=self.theme.COLORS['bg_primary'],
                              fg=self.theme.COLORS['text_primary'],
                              font=self.theme.FONTS['heading_small'])
        title_label.pack(anchor='w', padx=15, pady=(15, 5))

        # 进度条容器
        progress_frame = tk.Frame(card, bg=self.theme.COLORS['bg_primary'])
        progress_frame.pack(fill='x', padx=15, pady=(0, 10))

        # 进度条
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           mode='indeterminate')
        self.progress_bar.pack(fill='x', pady=5)

        # 状态文本
        self.progress_text = tk.StringVar(value="等待开始...")
        status_label = tk.Label(progress_frame,
                               textvariable=self.progress_text,
                               bg=self.theme.COLORS['bg_primary'],
                               fg=self.theme.COLORS['text_secondary'],
                               font=self.theme.FONTS['caption'])
        status_label.pack(anchor='w', pady=(5, 0))

        return card

    def create_stats_card(self, parent, title: str, value: str = "0", icon: str = "📊") -> tk.Frame:
        """创建统计卡片"""
        card = tk.Frame(parent,
                       bg=self.theme.COLORS['bg_primary'],
                       relief='solid',
                       bd=1,
                       highlightbackground=self.theme.COLORS['border'])

        # 图标和标题
        header_frame = tk.Frame(card, bg=self.theme.COLORS['bg_primary'])
        header_frame.pack(fill='x', padx=15, pady=(15, 5))

        icon_label = tk.Label(header_frame,
                             text=icon,
                             bg=self.theme.COLORS['bg_primary'],
                             font=('Segoe UI', 16))
        icon_label.pack(side='left')

        title_label = tk.Label(header_frame,
                              text=title,
                              bg=self.theme.COLORS['bg_primary'],
                              fg=self.theme.COLORS['text_secondary'],
                              font=self.theme.FONTS['caption'])
        title_label.pack(side='left', padx=(10, 0))

        # 数值
        self.value_var = tk.StringVar(value=value)
        value_label = tk.Label(card,
                              textvariable=self.value_var,
                              bg=self.theme.COLORS['bg_primary'],
                              fg=self.theme.COLORS['text_primary'],
                              font=self.theme.FONTS['heading_large'])
        value_label.pack(anchor='w', padx=15, pady=(0, 15))

        return card

    def create_notification(self, parent, message: str, type: str = "info") -> tk.Frame:
        """创建通知组件"""
        # 颜色映射
        color_map = {
            'info': self.theme.COLORS['info'],
            'success': self.theme.COLORS['success'],
            'warning': self.theme.COLORS['warning'],
            'error': self.theme.COLORS['error']
        }

        icon_map = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }

        color = color_map.get(type, self.theme.COLORS['info'])
        icon = icon_map.get(type, 'ℹ️')

        notification = tk.Frame(parent,
                               bg=color,
                               relief='flat',
                               bd=0)

        # 内容框架
        content_frame = tk.Frame(notification,
                                bg=self.theme.COLORS['bg_primary'],
                                relief='flat',
                                bd=0)
        content_frame.pack(fill='both', expand=True, padx=1, pady=1)

        # 图标
        icon_label = tk.Label(content_frame,
                             text=icon,
                             bg=self.theme.COLORS['bg_primary'],
                             font=('Segoe UI', 12))
        icon_label.pack(side='left', padx=(15, 10), pady=10)

        # 消息文本
        message_label = tk.Label(content_frame,
                                text=message,
                                bg=self.theme.COLORS['bg_primary'],
                                fg=self.theme.COLORS['text_primary'],
                                font=self.theme.FONTS['body'],
                                wraplength=400,
                                justify='left')
        message_label.pack(side='left', fill='both', expand=True, pady=10)

        # 关闭按钮
        close_btn = tk.Button(content_frame,
                             text='✖',
                             bg=self.theme.COLORS['bg_primary'],
                             fg=self.theme.COLORS['text_muted'],
                             font=('Segoe UI', 8),
                             relief='flat',
                             bd=0,
                             cursor='hand2',
                             command=lambda: notification.destroy())
        close_btn.pack(side='right', padx=(10, 15), pady=10)

        # 自动消失
        parent.after(5000, lambda: notification.destroy() if notification.winfo_exists() else None)

        return notification

    def create_file_drop_zone(self, parent, callback=None) -> tk.Frame:
        """创建文件拖拽区域"""
        drop_zone = tk.Frame(parent,
                            bg=self.theme.COLORS['bg_tertiary'],
                            relief='ridge',
                            bd=2,
                            highlightbackground=self.theme.COLORS['border'])

        # 内容
        content_frame = tk.Frame(drop_zone, bg=self.theme.COLORS['bg_tertiary'])
        content_frame.pack(expand=True, fill='both')

        # 图标
        icon_label = tk.Label(content_frame,
                             text='📦',
                             bg=self.theme.COLORS['bg_tertiary'],
                             font=('Segoe UI', 32))
        icon_label.pack(pady=(30, 10))

        # 主要文本
        main_text = tk.Label(content_frame,
                            text='拖拽压缩包到此处',
                            bg=self.theme.COLORS['bg_tertiary'],
                            fg=self.theme.COLORS['text_primary'],
                            font=self.theme.FONTS['heading_medium'])
        main_text.pack()

        # 次要文本
        sub_text = tk.Label(content_frame,
                           text='支持 .zip, .rar, .7z 格式',
                           bg=self.theme.COLORS['bg_tertiary'],
                           fg=self.theme.COLORS['text_secondary'],
                           font=self.theme.FONTS['caption'])
        sub_text.pack(pady=(5, 30))

        # 状态标签
        self.drop_status = tk.StringVar(value="")
        status_label = tk.Label(content_frame,
                               textvariable=self.drop_status,
                               bg=self.theme.COLORS['bg_tertiary'],
                               fg=self.theme.COLORS['success'],
                               font=self.theme.FONTS['body_bold'])
        status_label.pack()

        return drop_zone

    def update_status(self, message: str):
        """更新状态栏"""
        if hasattr(self, 'status_text'):
            self.status_text.set(message)

    def update_progress(self, message: str, start: bool = False, stop: bool = False):
        """更新进度"""
        if hasattr(self, 'progress_text'):
            self.progress_text.set(message)

        if hasattr(self, 'progress_bar'):
            if start:
                self.progress_bar.start()
            elif stop:
                self.progress_bar.stop()

    def show_notification(self, parent, message: str, type: str = "info"):
        """显示通知"""
        notification = self.create_notification(parent, message, type)
        notification.pack(fill='x', padx=10, pady=5)
        return notification
