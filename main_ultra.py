#!/usr/bin/env python3
"""
FileMover v4.0 - 超级简化版本
最小依赖，专门解决运行时错误
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
import shutil


class UltraFileMover:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FileMover v4.0 - Ultra Edition")
        self.root.geometry("800x500")
        self.root.configure(bg='#2B2B2B')
        
        self.archive_path = ""
        self.create_ui()
        self.center_window()
    
    def create_ui(self):
        """创建界面"""
        # 标题
        title = tk.Label(self.root, 
                        text="📦 FileMover v4.0 Ultra", 
                        font=('Arial', 16, 'bold'),
                        fg='#4A90E2', 
                        bg='#2B2B2B')
        title.pack(pady=20)
        
        # 文件选择
        file_frame = tk.Frame(self.root, bg='#3A3A3A', relief='raised', bd=2)
        file_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(file_frame, 
                text="选择ZIP压缩包:", 
                font=('Arial', 12, 'bold'),
                fg='white', 
                bg='#3A3A3A').pack(pady=10)
        
        btn_frame = tk.Frame(file_frame, bg='#3A3A3A')
        btn_frame.pack(pady=10)
        
        self.file_label = tk.Label(btn_frame, 
                                  text="未选择文件", 
                                  font=('Arial', 10),
                                  fg='#CCCCCC', 
                                  bg='#3A3A3A')
        self.file_label.pack(pady=5)
        
        tk.Button(btn_frame, 
                 text="📂 选择文件", 
                 command=self.select_file,
                 font=('Arial', 11, 'bold'),
                 bg='#4A90E2', 
                 fg='white',
                 padx=20, 
                 pady=5).pack()
        
        # 关键字输入
        keyword_frame = tk.Frame(self.root, bg='#3A3A3A', relief='raised', bd=2)
        keyword_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(keyword_frame, 
                text="输入关键字 (每行一个):", 
                font=('Arial', 12, 'bold'),
                fg='white', 
                bg='#3A3A3A').pack(pady=(10,5))
        
        self.text_area = tk.Text(keyword_frame, 
                               height=10, 
                               font=('Arial', 10),
                               bg='white', 
                               fg='black')
        self.text_area.pack(fill='both', expand=True, padx=10, pady=(0,10))
        
        # 按钮区域
        button_frame = tk.Frame(self.root, bg='#2B2B2B')
        button_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(button_frame, 
                 text="🔍 预览", 
                 command=self.preview,
                 font=('Arial', 11, 'bold'),
                 bg='#5CB85C', 
                 fg='white',
                 padx=15, 
                 pady=8).pack(side='left', padx=(0,10))
        
        tk.Button(button_frame, 
                 text="🚀 开始处理", 
                 command=self.process,
                 font=('Arial', 11, 'bold'),
                 bg='#D9534F', 
                 fg='white',
                 padx=15, 
                 pady=8).pack(side='left', padx=(0,10))
        
        tk.Button(button_frame, 
                 text="🗑️ 清空", 
                 command=self.clear,
                 font=('Arial', 11, 'bold'),
                 bg='#F0AD4E', 
                 fg='white',
                 padx=15, 
                 pady=8).pack(side='right')
        
        # 状态栏
        self.status = tk.Label(self.root, 
                              text="就绪", 
                              font=('Arial', 10),
                              fg='#5CB85C', 
                              bg='#2B2B2B')
        self.status.pack(pady=5)
    
    def center_window(self):
        """居中窗口"""
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
    
    def select_file(self):
        """选择文件"""
        file_path = filedialog.askopenfilename(
            title="选择ZIP文件",
            filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")]
        )
        if file_path:
            self.archive_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"已选择: {filename}")
            self.status.config(text=f"文件已选择: {filename}")
    
    def clear(self):
        """清空"""
        self.text_area.delete(1.0, tk.END)
        self.status.config(text="关键字已清空")
    
    def preview(self):
        """预览"""
        if not self.archive_path:
            messagebox.showerror("错误", "请先选择ZIP文件")
            return
        
        keywords_text = self.text_area.get(1.0, tk.END).strip()
        if not keywords_text:
            messagebox.showerror("错误", "请输入关键字")
            return
        
        keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        
        try:
            matched = []
            with zipfile.ZipFile(self.archive_path, 'r') as zf:
                for info in zf.filelist:
                    if info.is_dir():
                        continue
                    filename = info.filename
                    for keyword in keywords:
                        if keyword.lower() in filename.lower():
                            matched.append(filename)
                            break
            
            if matched:
                result = f"找到 {len(matched)} 个匹配文件:\n\n"
                result += "\n".join(matched[:15])
                if len(matched) > 15:
                    result += f"\n\n... 还有 {len(matched) - 15} 个文件"
            else:
                result = "没有找到匹配的文件"
            
            messagebox.showinfo("预览结果", result)
            
        except Exception as e:
            messagebox.showerror("错误", f"预览失败: {str(e)}")
    
    def process(self):
        """处理文件"""
        if not self.archive_path:
            messagebox.showerror("错误", "请先选择ZIP文件")
            return
        
        keywords_text = self.text_area.get(1.0, tk.END).strip()
        if not keywords_text:
            messagebox.showerror("错误", "请输入关键字")
            return
        
        try:
            self.status.config(text="正在处理...")
            self.root.update()
            
            keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
            
            # 创建输出目录
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_dir = os.path.join(desktop, "FileMover_Output")
            matched_dir = os.path.join(output_dir, "匹配文件")
            unmatched_dir = os.path.join(output_dir, "未匹配文件")
            
            for d in [output_dir, matched_dir, unmatched_dir]:
                if not os.path.exists(d):
                    os.makedirs(d)
            
            matched_count = 0
            total_count = 0
            
            with zipfile.ZipFile(self.archive_path, 'r') as zf:
                for info in zf.filelist:
                    if info.is_dir():
                        continue
                    
                    total_count += 1
                    filename = info.filename
                    
                    # 检查匹配
                    is_matched = False
                    for keyword in keywords:
                        if keyword.lower() in filename.lower():
                            is_matched = True
                            break
                    
                    # 提取文件
                    try:
                        zf.extract(info, output_dir)
                        source = os.path.join(output_dir, filename)
                        
                        target_dir = matched_dir if is_matched else unmatched_dir
                        target = os.path.join(target_dir, os.path.basename(filename))
                        
                        # 处理重名
                        counter = 1
                        original_target = target
                        while os.path.exists(target):
                            name, ext = os.path.splitext(original_target)
                            target = f"{name}_{counter}{ext}"
                            counter += 1
                        
                        shutil.move(source, target)
                        
                        if is_matched:
                            matched_count += 1
                            
                    except Exception as e:
                        print(f"处理文件 {filename} 出错: {e}")
            
            # 清理空目录
            for root, dirs, files in os.walk(output_dir, topdown=False):
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    if dir_path not in [matched_dir, unmatched_dir]:
                        try:
                            if not os.listdir(dir_path):
                                os.rmdir(dir_path)
                        except:
                            pass
            
            self.status.config(text=f"完成! 匹配: {matched_count}/{total_count}")
            messagebox.showinfo("处理完成", 
                              f"处理完成!\n匹配文件: {matched_count}\n总文件: {total_count}\n输出目录: {output_dir}")
            
        except Exception as e:
            self.status.config(text="处理失败")
            messagebox.showerror("错误", f"处理失败: {str(e)}")
    
    def run(self):
        """运行程序"""
        self.root.mainloop()


if __name__ == "__main__":
    app = UltraFileMover()
    app.run()
