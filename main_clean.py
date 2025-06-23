#!/usr/bin/env python3
"""
FileMover v4.0 - 原始UI版本
去除深色适配，恢复传统Windows界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import logging
import subprocess
import platform
from utils import (find_and_move_files, validate_directory, count_matching_files,
                   find_and_move_files_from_archive, validate_archive,
                   count_matching_files_in_archive, cleanup_temp_directory,
                   setup_logging, initialize_project_directories)
from config_manager import ConfigManager
from advanced_gui import FileTypeSelector, AdvancedFilters
from undo_manager import UndoManager
from password_manager import PasswordManager
from icon_manager import icon_manager


class FileFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件筛选与移动工具 v4.0 - 原始UI")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # 设置窗口图标
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 初始化组件
        self.config_manager = ConfigManager()
        self.undo_manager = UndoManager()
        self.password_manager = PasswordManager()
        
        # 初始化日志
        self.logger = setup_logging()
        self.logger.info("程序启动 v4.0 - 原始UI版本")

        # 初始化项目目录
        try:
            location = self.config_manager.get("user_preferences.ui_settings.extracted_files_location", "current")
            self.extracted_dir, self.matched_dir, self.unmatched_dir = initialize_project_directories(location)
            self.logger.info(f"项目目录初始化完成，位置: {location}")
        except Exception as e:
            self.logger.error(f"项目目录初始化失败: {e}")
            messagebox.showerror("初始化错误", f"无法初始化项目目录: {e}")

        # 检查压缩格式支持
        self.check_format_support()
        
        # 临时目录跟踪
        self.temp_extract_dir = None

        # 设置原始样式
        self.setup_styles()
        
        # 创建界面
        self.setup_ui()

    def setup_styles(self):
        """设置原始样式"""
        self.style = ttk.Style()
        
        # 使用Windows原生主题
        try:
            self.style.theme_use('winnative')
        except:
            self.style.theme_use('default')

        # 配置按钮样式
        self.style.configure(
            "Primary.TButton",
            background='#0078D4',
            foreground='white',
            font=('Microsoft YaHei UI', 9)
        )

        self.style.configure(
            "Success.TButton",
            background='#107C10',
            foreground='white',
            font=('Microsoft YaHei UI', 9)
        )

        self.style.configure(
            "Warning.TButton",
            background='#FF8C00',
            foreground='white',
            font=('Microsoft YaHei UI', 9)
        )

    def check_format_support(self):
        """检查压缩格式支持"""
        try:
            import rarfile
            self.rar_support = True
            self.logger.info("RAR格式支持已启用")
        except ImportError:
            self.rar_support = False
            self.logger.warning("RAR格式支持未安装")

        try:
            import py7zr
            self.seven_zip_support = True
            self.logger.info("7Z格式支持已启用")
        except ImportError:
            self.seven_zip_support = False
            self.logger.warning("7Z格式支持未安装")

    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建顶部控制区域
        self.create_top_controls(main_frame)

        # 创建中间内容区域
        self.create_middle_content(main_frame)

        # 创建底部状态区域
        self.create_bottom_status(main_frame)

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_top_controls(self, parent):
        """创建顶部控制区域"""
        # 顶部控制框架
        top_frame = ttk.LabelFrame(parent, text="文件选择与操作", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # 第一行：文件选择
        file_frame = ttk.Frame(top_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(file_frame, text="压缩包路径:").pack(side=tk.LEFT)
        
        self.archive_var = tk.StringVar()
        self.archive_entry = ttk.Entry(file_frame, textvariable=self.archive_var, width=60)
        self.archive_entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)

        self.browse_button = ttk.Button(file_frame, text="浏览...", 
                                       command=self.browse_archive,
                                       style="Primary.TButton")
        self.browse_button.pack(side=tk.RIGHT)

        # 第二行：操作按钮
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(fill=tk.X)

        self.preview_button = ttk.Button(button_frame, text="预览匹配文件", 
                                        command=self.preview_files,
                                        style="Primary.TButton")
        self.preview_button.pack(side=tk.LEFT, padx=(0, 10))

        self.process_button = ttk.Button(button_frame, text="开始处理", 
                                        command=self.start_processing,
                                        style="Success.TButton")
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))

        self.undo_button = ttk.Button(button_frame, text="撤销上次操作", 
                                     command=self.undo_last_operation,
                                     style="Warning.TButton")
        self.undo_button.pack(side=tk.LEFT, padx=(0, 10))

        # 右侧：设置按钮
        self.settings_button = ttk.Button(button_frame, text="设置", 
                                         command=self.open_settings)
        self.settings_button.pack(side=tk.RIGHT)

    def create_middle_content(self, parent):
        """创建中间内容区域"""
        # 创建左右分栏
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧：关键字输入
        left_frame = ttk.LabelFrame(content_frame, text="关键字设置", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # 关键字输入说明
        ttk.Label(left_frame, text="请输入搜索关键字，每行一个:").pack(anchor=tk.W, pady=(0, 5))

        # 关键字文本框
        text_frame = ttk.Frame(left_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.keyword_text = tk.Text(text_frame, height=15, wrap=tk.WORD, 
                                   font=('Microsoft YaHei UI', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.keyword_text.yview)
        self.keyword_text.configure(yscrollcommand=scrollbar.set)

        self.keyword_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 关键字操作按钮
        keyword_button_frame = ttk.Frame(left_frame)
        keyword_button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(keyword_button_frame, text="清空", 
                  command=self.clear_keywords,
                  style="Warning.TButton").pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(keyword_button_frame, text="示例", 
                  command=self.load_example_keywords).pack(side=tk.LEFT)

        # 右侧：高级选项
        right_frame = ttk.LabelFrame(content_frame, text="高级选项", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # 操作模式选择
        mode_frame = ttk.LabelFrame(right_frame, text="操作模式", padding=5)
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        self.operation_var = tk.StringVar(value="move")
        ttk.Radiobutton(mode_frame, text="移动文件", variable=self.operation_var, 
                       value="move").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="复制文件", variable=self.operation_var, 
                       value="copy").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="创建链接", variable=self.operation_var, 
                       value="link").pack(anchor=tk.W)

        # 文件类型过滤
        try:
            self.file_type_selector = FileTypeSelector(right_frame)
        except:
            pass

        # 高级过滤选项
        try:
            self.advanced_filters = AdvancedFilters(right_frame)
        except:
            pass

    def create_bottom_status(self, parent):
        """创建底部状态区域"""
        # 状态框架
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding=5)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        # 状态标签
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT)

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          maximum=100, length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))

    # 占位方法
    def browse_archive(self):
        """浏览压缩包"""
        file_path = filedialog.askopenfilename(
            title="选择压缩包文件",
            filetypes=[
                ("压缩包文件", "*.zip;*.rar;*.7z"),
                ("ZIP文件", "*.zip"),
                ("RAR文件", "*.rar"),
                ("7Z文件", "*.7z"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.archive_var.set(file_path)

    def preview_files(self):
        """预览匹配文件"""
        messagebox.showinfo("预览", "预览功能开发中...")

    def start_processing(self):
        """开始处理"""
        # 验证输入
        archive_path = self.archive_var.get().strip()
        if not archive_path:
            messagebox.showerror("错误", "请选择压缩包文件")
            return

        if not os.path.exists(archive_path):
            messagebox.showerror("错误", "压缩包文件不存在")
            return

        keywords_text = self.keyword_text.get(1.0, tk.END).strip()
        if not keywords_text:
            messagebox.showerror("错误", "请输入关键字")
            return

        # 在新线程中处理
        thread = threading.Thread(target=self.process_files_thread,
                                 args=(archive_path, keywords_text))
        thread.daemon = True
        thread.start()

    def process_files_thread(self, archive_path, keywords_text):
        """在线程中处理文件"""
        try:
            # 更新状态
            self.status_label.config(text="正在处理...")
            self.progress_var.set(0)

            keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
            operation_mode = self.operation_var.get()

            # 创建输出目录
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_dir = os.path.join(desktop, "FileMover_Output")
            matched_dir = os.path.join(output_dir, "匹配文件")
            unmatched_dir = os.path.join(output_dir, "未匹配文件")

            for d in [output_dir, matched_dir, unmatched_dir]:
                os.makedirs(d, exist_ok=True)

            # 处理文件
            matched_count, total_count = self.process_archive_files(
                archive_path, keywords, matched_dir, unmatched_dir, operation_mode)

            # 更新状态
            self.status_label.config(text=f"完成! 匹配: {matched_count}/{total_count}")
            self.progress_var.set(100)

            # 显示完成对话框
            self.root.after(0, lambda: self.show_completion_dialog(output_dir, matched_count, total_count))

        except Exception as e:
            self.logger.error(f"处理失败: {e}")
            self.status_label.config(text="处理失败")
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {str(e)}"))

    def process_archive_files(self, archive_path, keywords, matched_dir, unmatched_dir, operation_mode):
        """处理压缩包文件"""
        import zipfile
        import shutil

        matched_count = 0
        total_count = 0

        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                file_list = [f for f in zip_file.filelist if not f.is_dir()]
                total_count = len(file_list)

                for i, file_info in enumerate(file_list):
                    # 更新进度
                    progress = (i + 1) / total_count * 100
                    self.progress_var.set(progress)

                    filename = file_info.filename

                    # 检查是否匹配关键字
                    is_matched = False
                    for keyword in keywords:
                        if keyword.lower() in filename.lower():
                            is_matched = True
                            break

                    # 提取文件
                    try:
                        zip_file.extract(file_info, self.extracted_dir)
                        source_path = os.path.join(self.extracted_dir, filename)

                        target_dir = matched_dir if is_matched else unmatched_dir
                        target_path = os.path.join(target_dir, os.path.basename(filename))

                        # 处理重名文件
                        counter = 1
                        original_target = target_path
                        while os.path.exists(target_path):
                            name, ext = os.path.splitext(original_target)
                            target_path = f"{name}_{counter}{ext}"
                            counter += 1

                        # 根据操作模式处理文件
                        if operation_mode == "move":
                            shutil.move(source_path, target_path)
                        elif operation_mode == "copy":
                            shutil.copy2(source_path, target_path)
                        elif operation_mode == "link":
                            # 创建快捷方式（Windows）
                            if platform.system() == "Windows":
                                import win32com.client
                                shell = win32com.client.Dispatch("WScript.Shell")
                                shortcut = shell.CreateShortCut(target_path + ".lnk")
                                shortcut.Targetpath = source_path
                                shortcut.save()
                            else:
                                # Unix系统创建符号链接
                                os.symlink(source_path, target_path)

                        if is_matched:
                            matched_count += 1

                    except Exception as e:
                        self.logger.error(f"处理文件 {filename} 时出错: {e}")
                        continue

        except Exception as e:
            raise Exception(f"无法处理压缩包: {e}")

        return matched_count, total_count

    def undo_last_operation(self):
        """撤销上次操作"""
        messagebox.showinfo("撤销", "撤销功能开发中...")

    def open_settings(self):
        """打开设置"""
        messagebox.showinfo("设置", "设置功能开发中...")

    def clear_keywords(self):
        """清空关键字"""
        self.keyword_text.delete(1.0, tk.END)

    def load_example_keywords(self):
        """加载示例关键字"""
        examples = ["图片", "文档", "视频", "音频", "压缩包"]
        self.keyword_text.delete(1.0, tk.END)
        self.keyword_text.insert(1.0, "\n".join(examples))

    def open_folder(self, folder_path):
        """跨平台打开文件夹"""
        try:
            if platform.system() == "Windows":
                # Windows系统
                os.startfile(folder_path)
            elif platform.system() == "Darwin":
                # macOS系统
                subprocess.run(["open", folder_path])
            else:
                # Linux系统
                subprocess.run(["xdg-open", folder_path])

            self.logger.info(f"已打开文件夹: {folder_path}")
            return True
        except Exception as e:
            self.logger.error(f"打开文件夹失败: {e}")
            return False

    def show_completion_dialog(self, output_dir, matched_count, total_count):
        """显示处理完成对话框"""
        # 创建自定义对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("处理完成")
        dialog.geometry("400x200")
        dialog.resizable(False, False)

        # 居中显示
        dialog.transient(self.root)
        dialog.grab_set()

        # 计算居中位置
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
        dialog.geometry(f"400x200+{x}+{y}")

        # 主框架
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 成功图标和标题
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(title_frame, text="✅", font=('Arial', 24)).pack(side=tk.LEFT)
        ttk.Label(title_frame, text="处理完成！",
                 font=('Microsoft YaHei UI', 14, 'bold')).pack(side=tk.LEFT, padx=(10, 0))

        # 统计信息
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(stats_frame, text=f"匹配文件: {matched_count} 个").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"总文件数: {total_count} 个").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"输出目录: {output_dir}").pack(anchor=tk.W)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))

        # 打开文件夹按钮
        open_btn = ttk.Button(button_frame, text="📂 打开文件夹",
                             command=lambda: self.open_folder_and_close(output_dir, dialog),
                             style="Primary.TButton")
        open_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 关闭按钮
        close_btn = ttk.Button(button_frame, text="关闭",
                              command=dialog.destroy)
        close_btn.pack(side=tk.RIGHT)

        # 设置默认按钮
        open_btn.focus_set()
        dialog.bind('<Return>', lambda e: self.open_folder_and_close(output_dir, dialog))
        dialog.bind('<Escape>', lambda e: dialog.destroy())

    def open_folder_and_close(self, folder_path, dialog):
        """打开文件夹并关闭对话框"""
        self.open_folder(folder_path)
        dialog.destroy()

    def on_closing(self):
        """窗口关闭事件"""
        # 清理临时目录
        if self.temp_extract_dir:
            cleanup_temp_directory(self.temp_extract_dir)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileFilterApp(root)
    root.mainloop()
