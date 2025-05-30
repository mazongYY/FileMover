import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import logging
from utils import (find_and_move_files, validate_directory, count_matching_files,
                   find_and_move_files_from_archive, validate_archive,
                   count_matching_files_in_archive, cleanup_temp_directory,
                   setup_logging, initialize_project_directories)


class FileFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件筛选与移动工具 - 支持压缩包 v2.0")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 初始化日志系统
        self.logger = setup_logging()
        self.logger.info("程序启动")

        # 初始化项目目录
        try:
            self.extracted_dir, self.matched_dir, self.unmatched_dir = initialize_project_directories()
            self.logger.info("项目目录初始化完成")
        except Exception as e:
            self.logger.error(f"项目目录初始化失败: {e}")
            messagebox.showerror("初始化错误", f"无法初始化项目目录: {e}")

        # 添加临时目录跟踪
        self.temp_extract_dir = None

        self.setup_ui()

    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 压缩包选择区域
        ttk.Label(main_frame, text="选择压缩包 (支持 .zip, .rar, .7z):").grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))

        self.archive_var = tk.StringVar()
        self.archive_entry = ttk.Entry(main_frame, textvariable=self.archive_var, width=50)
        self.archive_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 5))

        ttk.Button(main_frame, text="浏览", command=self.select_archive).grid(row=1, column=2, sticky=tk.W)

        # 关键字输入区域
        ttk.Label(main_frame, text="输入关键字 (每行一个关键字):").grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(20, 5))

        # 创建多行文本框
        keyword_frame = ttk.Frame(main_frame)
        keyword_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        keyword_frame.columnconfigure(0, weight=1)

        self.keyword_text = tk.Text(keyword_frame, height=4, wrap=tk.WORD)
        keyword_scrollbar = ttk.Scrollbar(keyword_frame, orient=tk.VERTICAL, command=self.keyword_text.yview)
        self.keyword_text.configure(yscrollcommand=keyword_scrollbar.set)

        self.keyword_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        keyword_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 预览按钮
        ttk.Button(main_frame, text="预览匹配文件数", command=self.preview_files).grid(row=4, column=0, sticky=tk.W, pady=(0, 10))

        # 操作按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))

        self.start_button = ttk.Button(button_frame, text="开始处理", command=self.start_processing)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(button_frame, text="清空", command=self.clear_inputs).pack(side=tk.LEFT)

        # 进度条
        self.progress_var = tk.StringVar(value="就绪")
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=(20, 5))

        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # 结果显示区域
        ttk.Label(main_frame, text="操作日志:").grid(row=8, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))

        # 创建文本框和滚动条
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(text_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 配置主框架的行权重
        main_frame.rowconfigure(9, weight=1)

        # 绑定Ctrl+Enter快捷键
        self.keyword_text.bind('<Control-Return>', lambda e: self.start_processing())

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
            self.archive_var.set(archive_path)
            self.log_message(f"已选择压缩包: {archive_path}")

    def clear_inputs(self):
        """清空输入"""
        self.archive_var.set("")
        self.keyword_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set("就绪")

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
        archive_path = self.archive_var.get().strip()
        keywords = self.get_keywords()

        if not archive_path or not keywords:
            messagebox.showwarning("输入错误", "请先选择压缩包并输入关键字")
            return

        if not validate_archive(archive_path):
            messagebox.showerror("错误", "选择的压缩包无效或不支持的格式")
            return

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
            matched_count, unmatched_count = count_matching_files_in_archive(archive_path, keywords)
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
        archive_path = self.archive_var.get().strip()
        keywords = self.get_keywords()

        if not archive_path or not keywords:
            messagebox.showwarning("输入错误", "请选择压缩包并输入关键字")
            return

        if not validate_archive(archive_path):
            messagebox.showerror("错误", "选择的压缩包无效或不支持的格式")
            return

        # 确认操作
        result = messagebox.askyesno("确认操作",
                                   f"将要解压压缩包 '{os.path.basename(archive_path)}' 并搜索包含关键字的文件，"
                                   f"然后移动到桌面。\n\n关键字列表:\n{chr(10).join(keywords)}\n\n确定要继续吗？")
        if not result:
            return

        # 在新线程中执行处理
        self.start_button.config(state='disabled')
        self.progress_bar.start()
        self.progress_var.set("正在处理...")

        thread = threading.Thread(target=self.process_files, args=(archive_path, keywords))
        thread.daemon = True
        thread.start()

    def process_files(self, archive_path, keywords):
        """在后台线程中处理文件"""
        try:
            self.log_message(f"开始解压压缩包: {os.path.basename(archive_path)}")
            self.log_message(f"搜索关键字: {chr(10).join(keywords)}")

            matched_files, unmatched_files, matched_dir, unmatched_dir = find_and_move_files_from_archive(archive_path, keywords)

            # 在主线程中更新UI
            self.root.after(0, self.processing_complete, matched_files, unmatched_files, matched_dir, unmatched_dir, None)

        except Exception as e:
            self.root.after(0, self.processing_complete, [], [], "", "", str(e))

    def processing_complete(self, matched_files, unmatched_files, matched_dir, unmatched_dir, error):
        """处理完成后的回调"""
        self.progress_bar.stop()
        self.start_button.config(state='normal')

        if error:
            self.progress_var.set("处理失败")
            self.log_message(f"错误: {error}", "ERROR")
            messagebox.showerror("处理失败", f"操作失败: {error}")
        else:
            total_files = len(matched_files) + len(unmatched_files)
            self.progress_var.set(f"处理完成 - 总计 {total_files} 个文件")

            # 记录详细结果
            self.log_message(f"文件处理完成:")
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
            result_message += f"总文件数: {total_files}\n"
            result_message += f"命中关键字: {len(matched_files)} 个\n"
            result_message += f"未命中关键字: {len(unmatched_files)} 个\n\n"
            result_message += f"文件已分类保存到项目根目录下的 extracted_files 文件夹中：\n"
            result_message += f"• 命中文件 -> 命中文件/\n"
            result_message += f"• 未命中文件 -> 未命中文件/"

            messagebox.showinfo("处理完成", result_message)

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
        if hasattr(app, 'logger'):
            app.logger.info("用户关闭程序")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
