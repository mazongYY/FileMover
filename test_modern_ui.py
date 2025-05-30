#!/usr/bin/env python3
"""
现代化UI测试脚本
"""

import tkinter as tk
from tkinter import ttk
import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui_theme import UIStyler, ModernComponents, IconManager, ModernTheme
    print("✅ UI主题模块导入成功")
except ImportError as e:
    print(f"❌ UI主题模块导入失败: {e}")
    sys.exit(1)


def test_theme_colors():
    """测试主题颜色"""
    print("\n🎨 测试主题颜色...")
    theme = ModernTheme()
    
    print(f"主色调: {theme.COLORS['primary']}")
    print(f"背景色: {theme.COLORS['bg_primary']}")
    print(f"文字色: {theme.COLORS['text_primary']}")
    print(f"成功色: {theme.COLORS['success']}")
    print(f"错误色: {theme.COLORS['error']}")
    
    print("✅ 主题颜色测试完成")


def test_icon_manager():
    """测试图标管理器"""
    print("\n🔍 测试图标管理器...")
    
    icons_to_test = ['file', 'folder', 'search', 'settings', 'success', 'error']
    
    for icon_name in icons_to_test:
        icon = IconManager.get_icon(icon_name)
        print(f"{icon_name}: {icon}")
    
    print("✅ 图标管理器测试完成")


def create_demo_window():
    """创建演示窗口"""
    print("\n🖼️ 创建UI演示窗口...")
    
    root = tk.Tk()
    root.title("🎨 现代化UI演示 - 文件筛选工具v4.0")
    root.geometry("1200x800")
    
    # 初始化UI样式
    styler = UIStyler(root)
    components = ModernComponents(styler)
    
    # 主容器
    main_container = tk.Frame(root, bg=styler.theme.COLORS['bg_primary'])
    main_container.pack(fill='both', expand=True)
    
    # 工具栏
    toolbar = components.create_toolbar(main_container)
    toolbar.pack(fill='x', side='top')
    
    # 内容区域
    content_area = tk.Frame(main_container, bg=styler.theme.COLORS['bg_primary'])
    content_area.pack(fill='both', expand=True, padx=20, pady=20)
    
    # 左右分割
    paned = tk.PanedWindow(content_area, orient=tk.HORIZONTAL, bg=styler.theme.COLORS['bg_primary'])
    paned.pack(fill='both', expand=True)
    
    # 左侧面板
    left_panel = create_left_demo_panel(paned, styler, components)
    paned.add(left_panel, width=500)
    
    # 右侧面板
    right_panel = create_right_demo_panel(paned, styler, components)
    paned.add(right_panel, width=600)
    
    # 状态栏
    status_bar = components.create_status_bar(main_container)
    status_bar.pack(fill='x', side='bottom')
    
    # 通知区域
    notification_area = tk.Frame(main_container, bg=styler.theme.COLORS['bg_primary'])
    notification_area.pack(fill='x', side='bottom', before=status_bar)
    
    # 显示一些演示通知
    def show_demo_notifications():
        components.show_notification(notification_area, "这是一个信息通知", "info")
        root.after(2000, lambda: components.show_notification(notification_area, "这是一个成功通知", "success"))
        root.after(4000, lambda: components.show_notification(notification_area, "这是一个警告通知", "warning"))
    
    root.after(1000, show_demo_notifications)
    
    print("✅ UI演示窗口创建完成")
    return root


def create_left_demo_panel(parent, styler, components):
    """创建左侧演示面板"""
    left_frame = tk.Frame(parent, bg=styler.theme.COLORS['bg_primary'])
    
    # 文件选择区域
    file_section = styler.create_section_frame(left_frame, "📁 文件选择演示")
    file_section.pack(fill='x', pady=(0, 15))
    
    # 拖拽区域
    drop_zone = components.create_file_drop_zone(file_section)
    drop_zone.pack(fill='x', padx=15, pady=15)
    
    # 输入框演示
    input_section = styler.create_section_frame(left_frame, "📝 输入控件演示")
    input_section.pack(fill='x', pady=(0, 15))
    
    input_frame = tk.Frame(input_section, bg=styler.theme.COLORS['bg_primary'])
    input_frame.pack(fill='x', padx=15, pady=15)
    
    # 现代化输入框
    entry_label = styler.create_caption_label(input_frame, "现代化输入框:")
    entry_label.pack(anchor='w', pady=(0, 5))
    
    demo_entry = styler.create_modern_entry(input_frame)
    demo_entry.pack(fill='x', pady=(0, 10))
    demo_entry.insert(0, "这是一个现代化的输入框")
    
    # 下拉框
    combo_label = styler.create_caption_label(input_frame, "现代化下拉框:")
    combo_label.pack(anchor='w', pady=(0, 5))
    
    demo_combo = styler.create_modern_combobox(input_frame, values=["选项1", "选项2", "选项3"])
    demo_combo.pack(fill='x', pady=(0, 10))
    demo_combo.set("选项1")
    
    # 按钮演示
    button_section = styler.create_section_frame(left_frame, "🔘 按钮演示")
    button_section.pack(fill='x', pady=(0, 15))
    
    button_frame = tk.Frame(button_section, bg=styler.theme.COLORS['bg_primary'])
    button_frame.pack(fill='x', padx=15, pady=15)
    
    # 不同类型的按钮
    btn_row1 = tk.Frame(button_frame, bg=styler.theme.COLORS['bg_primary'])
    btn_row1.pack(fill='x', pady=(0, 10))
    
    primary_btn = styler.create_primary_button(btn_row1, "主要按钮")
    primary_btn.pack(side='left', padx=(0, 10))
    
    secondary_btn = styler.create_secondary_button(btn_row1, "次要按钮")
    secondary_btn.pack(side='left', padx=(0, 10))
    
    btn_row2 = tk.Frame(button_frame, bg=styler.theme.COLORS['bg_primary'])
    btn_row2.pack(fill='x')
    
    success_btn = styler.create_success_button(btn_row2, "成功按钮")
    success_btn.pack(side='left', padx=(0, 10))
    
    danger_btn = styler.create_danger_button(btn_row2, "危险按钮")
    danger_btn.pack(side='left')
    
    # 进度卡片
    progress_card = components.create_progress_card(left_frame)
    progress_card.pack(fill='x', pady=(0, 15))
    
    # 启动进度演示
    def demo_progress():
        components.update_progress("演示进度中...", start=True)
        root.after(3000, lambda: components.update_progress("演示完成", stop=True))
    
    root = left_frame.winfo_toplevel()
    root.after(2000, demo_progress)
    
    return left_frame


def create_right_demo_panel(parent, styler, components):
    """创建右侧演示面板"""
    right_frame = tk.Frame(parent, bg=styler.theme.COLORS['bg_primary'])
    
    # 标签页演示
    notebook = styler.create_modern_notebook(right_frame)
    notebook.pack(fill='both', expand=True)
    
    # 统计卡片标签页
    stats_frame = tk.Frame(notebook, bg=styler.theme.COLORS['bg_primary'])
    notebook.add(stats_frame, text="📊 统计演示")
    
    # 统计卡片网格
    stats_container = tk.Frame(stats_frame, bg=styler.theme.COLORS['bg_primary'])
    stats_container.pack(fill='both', expand=True, padx=20, pady=20)
    
    stats_grid = tk.Frame(stats_container, bg=styler.theme.COLORS['bg_primary'])
    stats_grid.pack(fill='x')
    
    # 创建演示统计卡片
    card1 = components.create_stats_card(stats_grid, "总文件数", "1,234", "📄")
    card1.grid(row=0, column=0, padx=(0, 15), pady=(0, 15), sticky='ew')
    
    card2 = components.create_stats_card(stats_grid, "匹配文件", "567", "✅")
    card2.grid(row=0, column=1, padx=(0, 15), pady=(0, 15), sticky='ew')
    
    card3 = components.create_stats_card(stats_grid, "成功率", "89.2%", "📈")
    card3.grid(row=0, column=2, pady=(0, 15), sticky='ew')
    
    card4 = components.create_stats_card(stats_grid, "处理大小", "2.4 GB", "💾")
    card4.grid(row=1, column=0, padx=(0, 15), sticky='ew')
    
    card5 = components.create_stats_card(stats_grid, "操作次数", "42", "🔄")
    card5.grid(row=1, column=1, padx=(0, 15), sticky='ew')
    
    card6 = components.create_stats_card(stats_grid, "节省时间", "3.2h", "⏱️")
    card6.grid(row=1, column=2, sticky='ew')
    
    # 配置网格权重
    stats_grid.columnconfigure(0, weight=1)
    stats_grid.columnconfigure(1, weight=1)
    stats_grid.columnconfigure(2, weight=1)
    
    # 树形视图演示
    tree_frame = tk.Frame(notebook, bg=styler.theme.COLORS['bg_primary'])
    notebook.add(tree_frame, text="🌳 列表演示")
    
    tree_container = tk.Frame(tree_frame, bg=styler.theme.COLORS['bg_primary'])
    tree_container.pack(fill='both', expand=True, padx=20, pady=20)
    
    # 现代化树形视图
    tree = styler.create_modern_treeview(tree_container, columns=("size", "type", "date"), show="tree headings")
    
    tree.heading("#0", text="文件名")
    tree.heading("size", text="大小")
    tree.heading("type", text="类型")
    tree.heading("date", text="日期")
    
    tree.column("#0", width=200)
    tree.column("size", width=80)
    tree.column("type", width=60)
    tree.column("date", width=120)
    
    # 添加演示数据
    demo_files = [
        ("📄 document.txt", "2.3 KB", "文本", "2024-05-30"),
        ("📷 image.jpg", "1.2 MB", "图片", "2024-05-29"),
        ("📦 archive.zip", "15.6 MB", "压缩", "2024-05-28"),
        ("📊 data.xlsx", "456 KB", "表格", "2024-05-27"),
        ("🎵 music.mp3", "3.8 MB", "音频", "2024-05-26"),
    ]
    
    for i, (name, size, type_name, date) in enumerate(demo_files):
        tree.insert("", "end", text=name, values=(size, type_name, date))
    
    tree.pack(fill='both', expand=True)
    
    # 日志演示
    log_frame = tk.Frame(notebook, bg=styler.theme.COLORS['bg_primary'])
    notebook.add(log_frame, text="📋 日志演示")
    
    log_container = tk.Frame(log_frame, bg=styler.theme.COLORS['bg_primary'])
    log_container.pack(fill='both', expand=True, padx=20, pady=20)
    
    log_text = tk.Text(log_container,
                       bg=styler.theme.COLORS['bg_secondary'],
                       fg=styler.theme.COLORS['text_primary'],
                       font=styler.theme.FONTS['code'],
                       relief='solid',
                       bd=1)
    
    log_scrollbar = ttk.Scrollbar(log_container, orient=tk.VERTICAL, command=log_text.yview, style='Modern.Vertical.TScrollbar')
    log_text.configure(yscrollcommand=log_scrollbar.set)
    
    log_text.pack(side='left', fill='both', expand=True)
    log_scrollbar.pack(side='right', fill='y')
    
    # 添加演示日志
    demo_logs = [
        "[10:30:15] INFO: 程序启动",
        "[10:30:16] INFO: 加载配置文件",
        "[10:30:17] INFO: 初始化UI主题",
        "[10:30:18] SUCCESS: 压缩包选择成功",
        "[10:30:20] INFO: 开始预览文件",
        "[10:30:22] SUCCESS: 预览完成 - 找到 156 个文件",
        "[10:30:25] INFO: 开始处理文件",
        "[10:30:28] SUCCESS: 文件处理完成",
        "[10:30:30] INFO: 操作记录已保存",
    ]
    
    for log in demo_logs:
        log_text.insert(tk.END, log + "\n")
    
    return right_frame


def main():
    """主函数"""
    print("🚀 开始现代化UI测试...")
    
    # 测试基础功能
    test_theme_colors()
    test_icon_manager()
    
    # 创建演示窗口
    try:
        root = create_demo_window()
        
        print("\n🎉 现代化UI演示窗口已启动！")
        print("📝 功能特点:")
        print("  • 现代化配色方案")
        print("  • 美观的组件样式")
        print("  • 丰富的图标支持")
        print("  • 响应式布局设计")
        print("  • 专业级用户体验")
        print("\n👀 请查看演示窗口体验新的UI设计...")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ UI演示失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
