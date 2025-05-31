#!/usr/bin/env python3
"""
密码管理器模块
处理密码保护的压缩包
"""

import os
import zipfile
import logging
from typing import Optional, List, Dict, Any
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    import rarfile
    RARFILE_AVAILABLE = True
except ImportError:
    RARFILE_AVAILABLE = False

try:
    import py7zr
    PY7ZR_AVAILABLE = True
except ImportError:
    PY7ZR_AVAILABLE = False


class PasswordManager:
    """密码管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger("FileFilterTool.Password")
        self.password_cache = {}  # 缓存已验证的密码
        
    def is_password_protected(self, archive_path: str) -> bool:
        """检查压缩包是否有密码保护"""
        try:
            _, ext = os.path.splitext(archive_path.lower())
            
            if ext == '.zip':
                return self._is_zip_password_protected(archive_path)
            elif ext == '.rar' and RARFILE_AVAILABLE:
                return self._is_rar_password_protected(archive_path)
            elif ext == '.7z' and PY7ZR_AVAILABLE:
                return self._is_7z_password_protected(archive_path)
            
            return False
        except Exception as e:
            self.logger.error(f"检查密码保护失败: {e}")
            return False
    
    def _is_zip_password_protected(self, archive_path: str) -> bool:
        """检查ZIP文件是否有密码保护"""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                for info in zip_ref.infolist():
                    if info.flag_bits & 0x1:  # 检查加密标志
                        return True
                # 尝试读取第一个文件
                if zip_ref.namelist():
                    try:
                        zip_ref.read(zip_ref.namelist()[0])
                        return False
                    except RuntimeError as e:
                        if "Bad password" in str(e) or "password required" in str(e).lower():
                            return True
            return False
        except Exception:
            return False
    
    def _is_rar_password_protected(self, archive_path: str) -> bool:
        """检查RAR文件是否有密码保护"""
        try:
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                return rar_ref.needs_password()
        except Exception:
            return False
    
    def _is_7z_password_protected(self, archive_path: str) -> bool:
        """检查7Z文件是否有密码保护"""
        try:
            with py7zr.SevenZipFile(archive_path, mode='r') as archive:
                return archive.needs_password()
        except Exception:
            return False
    
    def get_password(self, archive_path: str, parent_window=None) -> Optional[str]:
        """获取压缩包密码"""
        # 检查缓存
        if archive_path in self.password_cache:
            return self.password_cache[archive_path]
        
        # 弹出密码输入对话框
        password = self._show_password_dialog(archive_path, parent_window)
        
        if password and self.verify_password(archive_path, password):
            self.password_cache[archive_path] = password
            return password
        
        return None
    
    def _show_password_dialog(self, archive_path: str, parent_window=None) -> Optional[str]:
        """显示密码输入对话框"""
        filename = os.path.basename(archive_path)
        
        # 创建密码输入对话框
        dialog = PasswordDialog(parent_window, filename)
        return dialog.get_password()
    
    def verify_password(self, archive_path: str, password: str) -> bool:
        """验证密码是否正确"""
        try:
            _, ext = os.path.splitext(archive_path.lower())
            
            if ext == '.zip':
                return self._verify_zip_password(archive_path, password)
            elif ext == '.rar' and RARFILE_AVAILABLE:
                return self._verify_rar_password(archive_path, password)
            elif ext == '.7z' and PY7ZR_AVAILABLE:
                return self._verify_7z_password(archive_path, password)
            
            return False
        except Exception as e:
            self.logger.error(f"验证密码失败: {e}")
            return False
    
    def _verify_zip_password(self, archive_path: str, password: str) -> bool:
        """验证ZIP文件密码"""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.setpassword(password.encode('utf-8'))
                # 尝试读取第一个文件
                if zip_ref.namelist():
                    zip_ref.read(zip_ref.namelist()[0])
            return True
        except Exception:
            return False
    
    def _verify_rar_password(self, archive_path: str, password: str) -> bool:
        """验证RAR文件密码"""
        try:
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                rar_ref.setpassword(password)
                # 尝试读取第一个文件
                if rar_ref.namelist():
                    rar_ref.read(rar_ref.namelist()[0])
            return True
        except Exception:
            return False
    
    def _verify_7z_password(self, archive_path: str, password: str) -> bool:
        """验证7Z文件密码"""
        try:
            with py7zr.SevenZipFile(archive_path, mode='r', password=password) as archive:
                # 尝试列出文件
                archive.list()
            return True
        except Exception:
            return False
    
    def extract_with_password(self, archive_path: str, extract_path: str, password: str) -> bool:
        """使用密码解压文件"""
        try:
            _, ext = os.path.splitext(archive_path.lower())
            
            if ext == '.zip':
                return self._extract_zip_with_password(archive_path, extract_path, password)
            elif ext == '.rar' and RARFILE_AVAILABLE:
                return self._extract_rar_with_password(archive_path, extract_path, password)
            elif ext == '.7z' and PY7ZR_AVAILABLE:
                return self._extract_7z_with_password(archive_path, extract_path, password)
            
            return False
        except Exception as e:
            self.logger.error(f"密码解压失败: {e}")
            return False
    
    def _extract_zip_with_password(self, archive_path: str, extract_path: str, password: str) -> bool:
        """使用密码解压ZIP文件"""
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.setpassword(password.encode('utf-8'))
            zip_ref.extractall(extract_path)
        return True
    
    def _extract_rar_with_password(self, archive_path: str, extract_path: str, password: str) -> bool:
        """使用密码解压RAR文件"""
        with rarfile.RarFile(archive_path, 'r') as rar_ref:
            rar_ref.setpassword(password)
            rar_ref.extractall(extract_path)
        return True
    
    def _extract_7z_with_password(self, archive_path: str, extract_path: str, password: str) -> bool:
        """使用密码解压7Z文件"""
        with py7zr.SevenZipFile(archive_path, mode='r', password=password) as archive:
            archive.extractall(extract_path)
        return True
    
    def clear_password_cache(self):
        """清空密码缓存"""
        self.password_cache.clear()
        self.logger.info("密码缓存已清空")


class PasswordDialog:
    """密码输入对话框"""
    
    def __init__(self, parent, filename):
        self.parent = parent
        self.filename = filename
        self.password = None
        self.dialog = None
        
    def get_password(self) -> Optional[str]:
        """显示对话框并获取密码"""
        self.dialog = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.dialog.title("输入密码")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        
        # 设置为模态对话框
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        self._create_widgets()
        
        # 等待对话框关闭
        self.dialog.wait_window()
        
        return self.password
    
    def _create_widgets(self):
        """创建对话框组件"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # 图标和标题
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(title_frame, text="🔒", font=("TkDefaultFont", 24)).pack(side="left")
        ttk.Label(title_frame, text="密码保护的压缩包", font=("TkDefaultFont", 12, "bold")).pack(side="left", padx=(10, 0))
        
        # 文件名
        ttk.Label(main_frame, text=f"文件: {self.filename}").pack(anchor="w", pady=(0, 10))
        ttk.Label(main_frame, text="请输入解压密码:").pack(anchor="w", pady=(0, 5))
        
        # 密码输入
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=40)
        self.password_entry.pack(fill="x", pady=(0, 10))
        self.password_entry.focus()
        
        # 显示密码选项
        self.show_password_var = tk.BooleanVar()
        show_check = ttk.Checkbutton(
            main_frame,
            text="显示密码",
            variable=self.show_password_var,
            command=self._toggle_password_visibility
        )
        show_check.pack(anchor="w", pady=(0, 20))
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="确定", command=self._on_ok).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self._on_cancel).pack(side="right")
        
        # 绑定回车键
        self.dialog.bind('<Return>', lambda e: self._on_ok())
        self.dialog.bind('<Escape>', lambda e: self._on_cancel())
    
    def _toggle_password_visibility(self):
        """切换密码显示/隐藏"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def _on_ok(self):
        """确定按钮处理"""
        password = self.password_var.get().strip()
        if password:
            self.password = password
            self.dialog.destroy()
        else:
            messagebox.showwarning("输入错误", "请输入密码", parent=self.dialog)
    
    def _on_cancel(self):
        """取消按钮处理"""
        self.password = None
        self.dialog.destroy()
