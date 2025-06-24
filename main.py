#!/usr/bin/env python3
"""
FileMover
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import subprocess
import platform
import zipfile
import shutil
import tempfile
import json


class SimpleConfigManager:
    """简化的配置管理器"""
    def __init__(self):
        self.config_file = "config.json"
        self.config = {}
        self.load()
    
    def load(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
        except:
            self.config = {}
    
    def save(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key, value):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value


class ModernFileFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileMover")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # 设置现代化深色主题
        self.setup_modern_theme()
        
        # 初始化配置管理器
        self.config_manager = SimpleConfigManager()
        
        # 创建现代化界面
        self.setup_ui()
        
        # 居中窗口
        self.center_window()

    def setup_modern_theme(self):
        """设置现代化深色主题"""
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
            'text_primary': '#ffffff',    # 主要文字
            'text_secondary': '#b3b3b3',  # 次要文字
            'text_muted': '#6c757d',      # 静音文字
            'border': '#4a4a4a',          # 边框色
            'input_bg': '#404040',        # 输入框背景
        }
        
        # 设置根窗口背景
        self.root.configure(bg=self.colors['bg_primary'])

    def create_modern_button(self, parent, text, command=None, style="primary", width=None):
        """创建现代化圆角按钮"""
        if style == "primary":
            bg_color = self.colors['accent']
            hover_color = self.colors['accent_hover']
        elif style == "success":
            bg_color = self.colors['success']
            hover_color = self.colors['success_hover']
        elif style == "warning":
            bg_color = self.colors['warning']
            hover_color = self.colors['warning_hover']
        else:
            bg_color = self.colors['bg_card']
            hover_color = self.colors['border']
        
        button_frame = tk.Frame(parent, bg=bg_color, relief='flat', bd=0)
        
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
        card_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        card_container.pack(fill='x', pady=(0, 20))
        
        card = tk.Frame(card_container,
                       bg=self.colors['bg_card'],
                       relief='flat',
                       bd=0,
                       padx=20,
                       pady=20)
        card.pack(fill='x', padx=10)
        
        if title:
            title_frame = tk.Frame(card, bg=self.colors['bg_card'])
            title_frame.pack(fill='x', pady=(0, 15))
            
            title_label = tk.Label(title_frame,
                                  text=f"{icon} {title}" if icon else title,
                                  font=('Microsoft YaHei UI', 14, 'bold'),
                                  fg=self.colors['text_primary'],
                                  bg=self.colors['bg_card'])
            title_label.pack(anchor='w')
        
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
        
        # 简化的占位符处理
        if placeholder:
            entry.placeholder = placeholder
            entry.insert(0, placeholder)
            entry.config(fg=self.colors['text_muted'])
            
            def on_focus_in(event):
                if entry.get() == entry.placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=self.colors['text_primary'])
            
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, entry.placeholder)
                    entry.config(fg=self.colors['text_muted'])
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        return input_frame, entry

    def setup_ui(self):
        """设置现代化用户界面"""
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_header(main_container)

        content_container = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_container.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        left_panel = tk.Frame(content_container, bg=self.colors['bg_primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_panel = tk.Frame(content_container, bg=self.colors['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_header(self, parent):
        """创建顶部标题区域"""
        header = tk.Frame(parent, bg=self.colors['bg_secondary'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg=self.colors['bg_secondary'])
        header_content.pack(fill='both', expand=True, padx=30, pady=20)

        title_label = tk.Label(header_content,
                              text="📦 FileMover",
                              font=('Microsoft YaHei UI', 20, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(side='left')

        button_container = tk.Frame(header_content, bg=self.colors['bg_secondary'])
        button_container.pack(side='right')

        preview_frame, self.preview_btn = self.create_modern_button(
            button_container, "👁️ 预览匹配文件", self.preview_files, "primary")
        preview_frame.pack(side='right', padx=(0, 10))

        process_frame, self.process_btn = self.create_modern_button(
            button_container, "🚀 开始处理", self.start_processing, "success")
        process_frame.pack(side='right')

    def setup_left_panel(self, parent):
        """设置左侧面板"""
        file_content = self.create_modern_card(parent, "文件选择", "📁")
        self.setup_file_selection(file_content)

        keyword_content = self.create_modern_card(parent, "关键字设置", "🔍")
        self.setup_keyword_input(keyword_content)

    def setup_right_panel(self, parent):
        """设置右侧面板"""
        mode_content = self.create_modern_card(parent, "操作模式", "⚙️")
        self.setup_operation_mode(mode_content)

        status_content = self.create_modern_card(parent, "处理状态", "📊")
        self.setup_status_display(status_content)

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
        desc_label = tk.Label(parent,
                            text="输入搜索关键字，每行一个：",
                            font=('Microsoft YaHei UI', 11),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['bg_card'])
        desc_label.pack(anchor='w', pady=(0, 10))

        text_container = tk.Frame(parent,
                                bg=self.colors['input_bg'],
                                relief='flat',
                                bd=1,
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        text_container.pack(fill='both', expand=True, pady=(0, 15))

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

        scrollbar = tk.Scrollbar(text_container,
                               orient=tk.VERTICAL,
                               command=self.keyword_text.yview,
                               bg=self.colors['bg_card'],
                               troughcolor=self.colors['input_bg'],
                               activebackground=self.colors['accent'])
        self.keyword_text.configure(yscrollcommand=scrollbar.set)

        self.keyword_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        button_container = tk.Frame(parent, bg=self.colors['bg_card'])
        button_container.pack(fill='x')

        clear_frame, clear_btn = self.create_modern_button(
            button_container, "🗑️ 清空", self.clear_keywords, "warning", width=10)
        clear_frame.pack(side='left')

    def setup_operation_mode(self, parent):
        """设置操作模式区域"""
        self.operation_var = tk.StringVar(value="move")

        modes = [
            ("move", "📁 移动文件", "将匹配的文件移动到目标文件夹"),
            ("copy", "📋 复制文件", "将匹配的文件复制到目标文件夹"),
            ("link", "🔗 创建链接", "为匹配的文件创建快捷方式")
        ]

        for value, text, desc in modes:
            mode_container = tk.Frame(parent,
                                    bg=self.colors['bg_secondary'],
                                    relief='flat',
                                    bd=0,
                                    padx=15,
                                    pady=12)
            mode_container.pack(fill='x', pady=(0, 10))

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

            content_frame = tk.Frame(mode_container, bg=self.colors['bg_secondary'])
            content_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))

            title_label = tk.Label(content_frame,
                                 text=text,
                                 font=('Microsoft YaHei UI', 11, 'bold'),
                                 fg=self.colors['text_primary'],
                                 bg=self.colors['bg_secondary'])
            title_label.pack(anchor='w')

            desc_label = tk.Label(content_frame,
                                text=desc,
                                font=('Microsoft YaHei UI', 9),
                                fg=self.colors['text_secondary'],
                                bg=self.colors['bg_secondary'])
            desc_label.pack(anchor='w')

            def make_click_handler(v):
                return lambda e: self.operation_var.set(v)

            for widget in [mode_container, content_frame, title_label, desc_label]:
                widget.bind("<Button-1>", make_click_handler(value))

    def setup_status_display(self, parent):
        """设置状态显示区域"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        status_frame.pack(fill='x', pady=(0, 20))

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

        progress_container = tk.Frame(parent,
                                    bg=self.colors['bg_secondary'],
                                    relief='flat',
                                    bd=0,
                                    height=8)
        progress_container.pack(fill='x', pady=(0, 20))
        progress_container.pack_propagate(False)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Frame(progress_container,
                                   bg=self.colors['accent'],
                                   height=8)

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
        # 获取上次选择的目录
        last_dir = self.config_manager.get("user_preferences.last_browse_directory", os.path.expanduser("~"))

        file_path = filedialog.askopenfilename(
            title="选择压缩包文件",
            initialdir=last_dir,
            filetypes=[
                ("压缩包文件", "*.zip;*.rar;*.7z"),
                ("ZIP文件", "*.zip"),
                ("RAR文件", "*.rar"),
                ("7Z文件", "*.7z"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            # 保存当前选择的目录
            current_dir = os.path.dirname(file_path)
            self.config_manager.set("user_preferences.last_browse_directory", current_dir)
            self.config_manager.save()

            # 清除输入框内容并设置新路径
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

    def preview_files(self):
        """预览文件"""
        archive_path = self.archive_entry.get().strip()
        if not archive_path or archive_path == "请选择压缩包文件...":
            messagebox.showerror("错误", "请选择压缩包文件")
            return

        if not os.path.exists(archive_path):
            messagebox.showerror("错误", "压缩包文件不存在")
            return

        keywords_text = self.keyword_text.get(1.0, tk.END).strip()
        if not keywords_text:
            messagebox.showerror("错误", "请输入关键字")
            return

        try:
            keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]

            matched_count = 0
            total_count = 0

            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                file_list = [f for f in zip_file.filelist if not f.is_dir()]
                total_count = len(file_list)

                for file_info in file_list:
                    filename = file_info.filename
                    for keyword in keywords:
                        if keyword.lower() in filename.lower():
                            matched_count += 1
                            break

            messagebox.showinfo("预览结果",
                              f"预览完成！\n\n"
                              f"总文件数: {total_count}\n"
                              f"匹配文件: {matched_count}\n"
                              f"未匹配文件: {total_count - matched_count}")

        except Exception as e:
            messagebox.showerror("错误", f"预览失败: {str(e)}")

    def start_processing(self):
        """开始处理"""
        archive_path = self.archive_entry.get().strip()
        if not archive_path or archive_path == "请选择压缩包文件...":
            messagebox.showerror("错误", "请选择压缩包文件")
            return

        if not os.path.exists(archive_path):
            messagebox.showerror("错误", "压缩包文件不存在")
            return

        keywords_text = self.keyword_text.get(1.0, tk.END).strip()
        if not keywords_text:
            messagebox.showerror("错误", "请输入关键字")
            return

        thread = threading.Thread(target=self.process_files_thread,
                                 args=(archive_path, keywords_text))
        thread.daemon = True
        thread.start()

    def process_files_thread(self, archive_path, keywords_text):
        """在线程中处理文件"""
        try:
            self.update_status("正在处理...", "解压和筛选文件中", "🔄")
            self.update_progress(0)

            keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
            operation_mode = self.operation_var.get()

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_dir = os.path.join(desktop, "FileMover_Output")
            matched_dir = os.path.join(output_dir, "匹配文件")
            unmatched_dir = os.path.join(output_dir, "未匹配文件")

            for d in [output_dir, matched_dir, unmatched_dir]:
                os.makedirs(d, exist_ok=True)

            matched_count, total_count = self.process_archive_files(
                archive_path, keywords, matched_dir, unmatched_dir, operation_mode)

            self.update_status("处理完成", f"匹配: {matched_count}/{total_count}", "✅")
            self.update_progress(100)

            self.root.after(0, lambda: self.show_completion_dialog(output_dir, matched_count, total_count))

        except Exception as e:
            self.update_status("处理失败", str(e), "❌")
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {str(e)}"))

    def process_archive_files(self, archive_path, keywords, matched_dir, unmatched_dir, operation_mode):
        """处理压缩包文件"""
        matched_count = 0
        total_count = 0

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(archive_path, 'r') as zip_file:
                    file_list = [f for f in zip_file.filelist if not f.is_dir()]
                    total_count = len(file_list)

                    for i, file_info in enumerate(file_list):
                        progress = (i + 1) / total_count * 100
                        self.update_progress(progress)

                        filename = file_info.filename

                        is_matched = False
                        for keyword in keywords:
                            if keyword.lower() in filename.lower():
                                is_matched = True
                                break

                        try:
                            zip_file.extract(file_info, temp_dir)
                            source_path = os.path.join(temp_dir, filename)

                            target_dir = matched_dir if is_matched else unmatched_dir
                            target_path = os.path.join(target_dir, os.path.basename(filename))

                            counter = 1
                            original_target = target_path
                            while os.path.exists(target_path):
                                name, ext = os.path.splitext(original_target)
                                target_path = f"{name}_{counter}{ext}"
                                counter += 1

                            if operation_mode == "move":
                                shutil.move(source_path, target_path)
                            elif operation_mode == "copy":
                                shutil.copy2(source_path, target_path)
                            elif operation_mode == "link":
                                if platform.system() == "Windows":
                                    shutil.copy2(source_path, target_path)
                                else:
                                    os.symlink(source_path, target_path)

                            if is_matched:
                                matched_count += 1

                        except Exception as e:
                            continue

            except Exception as e:
                raise Exception(f"无法处理压缩包: {e}")

        return matched_count, total_count

    def show_completion_dialog(self, output_dir, matched_count, total_count):
        """处理完成后直接打开文件夹"""
        self.open_folder(output_dir)

    def open_folder(self, folder_path):
        """跨平台打开文件夹"""
        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", folder_path])
            else:
                subprocess.run(["xdg-open", folder_path])
            return True
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件夹: {e}")
            return False

    def on_closing(self):
        """窗口关闭事件"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFileFilterApp(root)
    root.mainloop()
