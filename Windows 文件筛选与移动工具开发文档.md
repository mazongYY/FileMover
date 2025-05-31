# Windows 文件筛选与移动工具开发文档

## 项目概述

本项目旨在开发一个简单的 Windows 应用程序，允许用户通过图形界面选择文件夹，并输入关键字来筛选该文件夹中的文件。随后，应用程序会将匹配关键字的文件移动到用户的桌面。

该应用程序使用 Python 编写，结合 Tkinter 进行 GUI 开发，并利用标准库进行文件操作。适用于 Windows 系统环境。

---

## 技术选型

- **编程语言**：Python 3.x
- **GUI 框架**：Tkinter
- **文件系统操作**：`os`, `shutil`
- **打包工具（可选）**：PyInstaller

---

## 功能需求

1. 用户可以选择一个文件夹。
2. 用户可以输入一个或多个关键字用于筛选文件名。
3. 程序扫描所选文件夹及其子目录中的所有文件。
4. 匹配关键字的文件被复制或移动到桌面。
5. 提供日志反馈，显示操作结果。

---

## 开发环境准备

### 安装 Python

请确保已安装 Python 3.x 并配置好环境变量。可以从 [Python官网](https://www.python.org/downloads/) 下载安装包。

### 安装依赖

无需额外依赖库，仅需使用标准库即可完成功能。

```bash
pip install pyinstaller  # 可选：用于打包为exe
```

---

## 项目结构

```
file_mover/
│
├── main.py               # 主程序入口
├── utils.py              # 工具函数（如文件筛选、移动）
├── README.md             # 说明文档
└── dist/                 # 打包后的可执行文件输出目录（可选）
```

---

## 核心代码实现

### `main.py` - GUI 主界面

```python
import tkinter as tk
from tkinter import filedialog, messagebox
from utils import find_and_move_files

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(tk.END, folder_path)

def start_processing():
    folder = folder_entry.get()
    keywords = keyword_entry.get().split(',')
    if not folder or not keywords:
        messagebox.showwarning("输入错误", "请输入有效的路径和关键字")
        return
    try:
        moved_files = find_and_move_files(folder, keywords)
        if moved_files:
            messagebox.showinfo("成功", f"共移动 {len(moved_files)} 个文件:\n{', '.join(moved_files)}")
        else:
            messagebox.showinfo("提示", "未找到匹配的文件")
    except Exception as e:
        messagebox.showerror("错误", str(e))

# 创建主窗口
root = tk.Tk()
root.title("文件筛选与移动工具")

# 文件夹选择
tk.Label(root, text="选择文件夹:").pack(pady=5)
folder_entry = tk.Entry(root, width=50)
folder_entry.pack(pady=5)
tk.Button(root, text="浏览", command=select_folder).pack(pady=5)

# 关键字输入
tk.Label(root, text="输入关键字 (逗号分隔):").pack(pady=5)
keyword_entry = tk.Entry(root, width=50)
keyword_entry.pack(pady=5)

# 开始按钮
tk.Button(root, text="开始处理", command=start_processing).pack(pady=20)

# 启动事件循环
root.mainloop()
```

---

### `utils.py` - 文件处理逻辑

```python
import os
import shutil
import time

def find_and_move_files(root_dir, keywords):
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop", f"筛选文件_{time.strftime('%Y%m%d')}")
    os.makedirs(desktop, exist_ok=True)
    
    matched_files = []
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(keyword.strip().lower() in filename.lower() for keyword in keywords):
                src_file = os.path.join(dirpath, filename)
                dst_file = os.path.join(desktop, filename)
                
                # 防止重名覆盖
                counter = 1
                while os.path.exists(dst_file):
                    name, ext = os.path.splitext(filename)
                    dst_file = os.path.join(desktop, f"{name}_{counter}{ext}")
                    counter += 1
                
                shutil.move(src_file, dst_file)
                matched_files.append(filename)
    
    return matched_files
```

---

## 使用说明

1. 运行程序后，点击“浏览”按钮选择目标文件夹。
2. 在文本框中输入关键字，多个关键字之间用英文逗号分隔。
3. 点击“开始处理”，程序会自动筛选并移动文件到桌面新建的文件夹中。
4. 操作完成后会弹出提示框显示结果。

---

## 打包为 EXE（可选）

使用 PyInstaller 将程序打包为独立的 `.exe` 文件：

```bash
pyinstaller --onefile --windowed main.py
```

生成的可执行文件位于 `dist/main.exe`。

---

## 注意事项

- 确保运行程序的用户有权限读取源文件夹和写入桌面。
- 若文件数量较多，建议在后台线程中执行操作以避免 UI 卡顿。
- 可扩展支持正则表达式、模糊搜索等功能。

---

## 后续改进方向

- 支持多选关键字模式（AND / OR）
- 增加进度条和日志窗口
- 添加撤销功能（恢复原位置）
- 支持拖放文件夹
- 支持配置保存常用关键字组合

---

## 结语

本项目提供了一个简单但实用的文件管理工具，适合初学者学习 GUI 和文件操作相关知识。后续可根据实际需求不断扩展功能模块。

--- 

如需完整项目模板，请告知我，我可以为你生成 ZIP 或 GitHub 仓库结构。