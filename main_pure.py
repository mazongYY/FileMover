#!/usr/bin/env python3
"""
FileMover v4.0 - 纯净版本
只使用Python标准库，避免pkg_resources问题
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import zipfile
import shutil
import threading
import tempfile


class PureFileMover:
    def __init__(self, root):
        self.root = root
        self.root.title("FileMover v4.0 - Pure Edition")
        self.root.geometry("900x600")
        self.root.configure(bg='#2D2D2D')
        
        # 变量
        self.archive_path = tk.StringVar()
        self.operation_mode = tk.StringVar(value="move")
        
        # 创建界面
        self.create_interface()
        
        # 居中窗口
        self.center_window()
    
    def create_interface(self):
        """创建用户界面"""
        # 主标题
        title = tk.Label(self.root, 
                        text="📦 FileMover v4.0", 
                        font=('Arial', 18, 'bold'),
                        fg='#1976D2', 
                        bg='#2D2D2D')
        title.pack(pady=20)
        
        # 文件选择区域
        file_frame = tk.LabelFrame(self.root, 
                                  text="文件选择", 
                                  font=('Arial', 12, 'bold'),
                                  fg='white', 
                                  bg='#3D3D3D')
        file_frame.pack(fill='x', padx=20, pady=10)
        
        # 文件路径
        path_frame = tk.Frame(file_frame, bg='#3D3D3D')
        path_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(path_frame, text="压缩包路径:", 
                fg='white', bg='#3D3D3D', 
                font=('Arial', 10)).pack(anchor='w')
        
        entry_frame = tk.Frame(path_frame, bg='#3D3D3D')
        entry_frame.pack(fill='x', pady=(5,0))
        
        self.path_entry = tk.Entry(entry_frame, 
                                  textvariable=self.archive_path,
                                  font=('Arial', 10))
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0,10))
        
        browse_btn = tk.Button(entry_frame, 
                              text="浏览", 
                              command=self.browse_file,
                              bg='#1976D2', 
                              fg='white', 
                              font=('Arial', 10, 'bold'))
        browse_btn.pack(side='right')
        
        # 关键字区域
        keyword_frame = tk.LabelFrame(self.root, 
                                     text="关键字设置", 
                                     font=('Arial', 12, 'bold'),
                                     fg='white', 
                                     bg='#3D3D3D')
        keyword_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(keyword_frame, 
                text="输入搜索关键字，每行一个:", 
                fg='white', bg='#3D3D3D', 
                font=('Arial', 10)).pack(anchor='w', padx=15, pady=(15,5))
        
        text_frame = tk.Frame(keyword_frame, bg='#3D3D3D')
        text_frame.pack(fill='both', expand=True, padx=15, pady=(0,15))
        
        self.keyword_text = tk.Text(text_frame, 
                                   height=8, 
                                   font=('Arial', 10))
        scrollbar = tk.Scrollbar(text_frame, command=self.keyword_text.yview)
        self.keyword_text.configure(yscrollcommand=scrollbar.set)
        
        self.keyword_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 操作模式
        mode_frame = tk.LabelFrame(self.root, 
                                  text="操作模式", 
                                  font=('Arial', 12, 'bold'),
                                  fg='white', 
                                  bg='#3D3D3D')
        mode_frame.pack(fill='x', padx=20, pady=10)
        
        radio_frame = tk.Frame(mode_frame, bg='#3D3D3D')
        radio_frame.pack(padx=15, pady=15)
        
        tk.Radiobutton(radio_frame, text="移动文件", 
                      variable=self.operation_mode, value="move",
                      fg='white', bg='#3D3D3D', 
                      font=('Arial', 10)).pack(side='left', padx=(0,30))
        
        tk.Radiobutton(radio_frame, text="复制文件", 
                      variable=self.operation_mode, value="copy",
                      fg='white', bg='#3D3D3D', 
                      font=('Arial', 10)).pack(side='left', padx=(0,30))
        
        # 按钮区域
        button_frame = tk.Frame(self.root, bg='#2D2D2D')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Button(button_frame, text="预览文件", 
                 command=self.preview_files,
                 bg='#1976D2', fg='white', 
                 font=('Arial', 11, 'bold'),
                 padx=20, pady=8).pack(side='left', padx=(0,15))
        
        tk.Button(button_frame, text="开始处理", 
                 command=self.start_processing,
                 bg='#4CAF50', fg='white', 
                 font=('Arial', 11, 'bold'),
                 padx=20, pady=8).pack(side='left', padx=(0,15))
        
        tk.Button(button_frame, text="清空关键字", 
                 command=self.clear_keywords,
                 bg='#FF9800', fg='white', 
                 font=('Arial', 11, 'bold'),
                 padx=20, pady=8).pack(side='right')
        
        # 状态栏
        self.status_label = tk.Label(self.root, 
                                    text="就绪", 
                                    fg='#4CAF50', 
                                    bg='#2D2D2D', 
                                    font=('Arial', 10))
        self.status_label.pack(pady=(0,10))
    
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
            title="选择压缩包文件",
            filetypes=[
                ("ZIP文件", "*.zip"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.archive_path.set(file_path)
            self.status_label.config(text=f"已选择: {os.path.basename(file_path)}")
    
    def clear_keywords(self):
        """清空关键字"""
        self.keyword_text.delete(1.0, tk.END)
        self.status_label.config(text="关键字已清空")
    
    def preview_files(self):
        """预览匹配的文件"""
        archive_path = self.archive_path.get().strip()
        if not archive_path:
            messagebox.showerror("错误", "请先选择压缩包文件")
            return
        
        if not os.path.exists(archive_path):
            messagebox.showerror("错误", "文件不存在")
            return
        
        keywords_text = self.keyword_text.get(1.0, tk.END).strip()
        if not keywords_text:
            messagebox.showerror("错误", "请输入关键字")
            return
        
        keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        
        try:
            matched_files = []
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                for file_info in zip_file.filelist:
                    filename = file_info.filename
                    for keyword in keywords:
                        if keyword.lower() in filename.lower():
                            matched_files.append(filename)
                            break
            
            if matched_files:
                result = f"找到 {len(matched_files)} 个匹配文件:\n\n"
                result += "\n".join(matched_files[:20])  # 只显示前20个
                if len(matched_files) > 20:
                    result += f"\n\n... 还有 {len(matched_files) - 20} 个文件"
            else:
                result = "没有找到匹配的文件"
            
            messagebox.showinfo("预览结果", result)
            
        except Exception as e:
            messagebox.showerror("错误", f"预览失败: {str(e)}")
    
    def start_processing(self):
        """开始处理文件"""
        archive_path = self.archive_path.get().strip()
        if not archive_path:
            messagebox.showerror("错误", "请先选择压缩包文件")
            return
        
        keywords_text = self.keyword_text.get(1.0, tk.END).strip()
        if not keywords_text:
            messagebox.showerror("错误", "请输入关键字")
            return
        
        # 在新线程中处理
        thread = threading.Thread(target=self.process_files, 
                                 args=(archive_path, keywords_text))
        thread.daemon = True
        thread.start()
    
    def process_files(self, archive_path, keywords_text):
        """处理文件的实际逻辑"""
        try:
            self.status_label.config(text="正在处理...")
            
            keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
            
            # 创建输出目录
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_dir = os.path.join(desktop, "FileMover_Output")
            matched_dir = os.path.join(output_dir, "匹配文件")
            unmatched_dir = os.path.join(output_dir, "未匹配文件")
            
            os.makedirs(matched_dir, exist_ok=True)
            os.makedirs(unmatched_dir, exist_ok=True)
            
            matched_count = 0
            total_count = 0
            
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                for file_info in zip_file.filelist:
                    if file_info.is_dir():
                        continue
                    
                    total_count += 1
                    filename = file_info.filename
                    
                    # 检查是否匹配关键字
                    is_matched = False
                    for keyword in keywords:
                        if keyword.lower() in filename.lower():
                            is_matched = True
                            break
                    
                    # 提取文件
                    try:
                        zip_file.extract(file_info, output_dir)
                        source_path = os.path.join(output_dir, filename)
                        
                        if is_matched:
                            target_dir = matched_dir
                            matched_count += 1
                        else:
                            target_dir = unmatched_dir
                        
                        # 移动文件
                        target_path = os.path.join(target_dir, os.path.basename(filename))
                        
                        # 处理重名文件
                        counter = 1
                        original_target = target_path
                        while os.path.exists(target_path):
                            name, ext = os.path.splitext(original_target)
                            target_path = f"{name}_{counter}{ext}"
                            counter += 1
                        
                        shutil.move(source_path, target_path)
                        
                    except Exception as e:
                        print(f"处理文件 {filename} 时出错: {e}")
            
            # 清理临时目录
            for root, dirs, files in os.walk(output_dir):
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    if dir_path not in [matched_dir, unmatched_dir]:
                        try:
                            shutil.rmtree(dir_path)
                        except:
                            pass
            
            self.status_label.config(text=f"完成! 匹配: {matched_count}, 总计: {total_count}")
            messagebox.showinfo("处理完成", 
                              f"处理完成!\n"
                              f"匹配文件: {matched_count}\n"
                              f"总文件数: {total_count}\n"
                              f"输出目录: {output_dir}")
            
        except Exception as e:
            self.status_label.config(text="处理失败")
            messagebox.showerror("错误", f"处理失败: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PureFileMover(root)
    root.mainloop()
