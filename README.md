# FileMover

<div align="center">

[![Version](https://img.shields.io/badge/version-4.0-blue.svg)](https://github.com/mazongYY/FileMover/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/mazongYY/FileMover)

**一个现代化的文件筛选与移动工具，支持从压缩包中智能筛选和分类文件**

*A modern file filtering and moving tool that intelligently filters and categorizes files from archives*

[中文](#中文) | [English](#english)

</div>

---

## 中文

### ✨ 主要特性

- 🎨 **现代化UI设计** - 深色主题，圆角按钮，卡片式布局
- 📦 **压缩包支持** - ZIP、RAR、7Z等多种格式
- 🔍 **智能筛选** - 关键字匹配，支持正则表达式
- ⚡ **多种操作** - 移动、复制、创建链接
- 🚀 **自动打开文件夹** - 处理完成后自动打开输出文件夹
- 🌐 **跨平台支持** - Windows、macOS、Linux
- 🛡️ **稳定可靠** - 彻底解决运行时错误问题

### 📦 下载安装

#### 方式一：下载可执行文件

从 [Releases](https://github.com/mazongYY/FileMover/releases) 下载最新版本：

- **FileMover.exe** - 推荐版本（约8MB）

#### 方式二：源码运行

```bash
# 克隆仓库
git clone https://github.com/mazongYY/FileMover.git
cd FileMover

# 安装可选依赖（RAR/7Z支持）
pip install rarfile py7zr

# 运行程序
python main.py
```

### � 系统要求

- **操作系统**: Windows 7/8/10/11、macOS 10.12+、Linux
- **Python**: 3.8+（仅源码运行需要）
- **内存**: 建议4GB以上
- **磁盘空间**: 至少50MB可用空间

### 🚀 快速开始

1. **选择压缩包文件**
   - 点击"浏览文件"选择ZIP/RAR/7Z文件
   - 或直接拖拽文件到程序界面

2. **输入关键字**
   - 在文本框中输入搜索关键字
   - 每行一个关键字，支持中英文

3. **选择操作模式**
   - 移动：将匹配文件移动到目标文件夹
   - 复制：将匹配文件复制到目标文件夹
   - 链接：为匹配文件创建快捷方式

4. **开始处理**
   - 点击"预览匹配文件"查看处理内容
   - 点击"开始处理"执行操作
   - 处理完成后自动打开输出文件夹

### 🔧 高级功能

- **正则表达式匹配** - 支持复杂的文件名匹配规则
- **文件类型过滤** - 按文件扩展名筛选
- **批量处理** - 一次处理大量文件
- **操作历史** - 记录所有操作，支持撤销
- **密码保护** - 支持加密压缩包
- **多线程处理** - 提高大文件处理速度

### 📚 版本历史

#### v4.0 (2024-12-19)
- ✅ 全新现代化UI设计
- 🚀 处理完成自动打开文件夹
- 🛡️ 完全解决运行时错误
- 🔧 优化性能和用户体验

### 🤝 贡献

欢迎贡献代码！请随时提交Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### � 联系方式

- 🏠 **项目主页**: https://github.com/mazongYY/FileMover
- 🐛 **问题反馈**: https://github.com/mazongYY/FileMover/issues
- 📧 **邮箱**: [创建Issue联系](https://github.com/mazongYY/FileMover/issues/new)

### 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## English

### 🚀 Features

- 🎨 **Modern UI Design** - Dark theme with rounded buttons and card-style layout
- 📦 **Archive Support** - ZIP, RAR, 7Z and other formats
- 🔍 **Smart Filtering** - Keyword matching with regex support
- ⚡ **Multiple Operations** - Move, copy, or create links
- 🚀 **Auto Open Folder** - Automatically opens output folder when complete
- 🌐 **Cross Platform** - Windows, macOS, Linux support
- 🛡️ **Stable & Reliable** - Completely resolved runtime errors

### 📦 Download & Installation

#### Option 1: Download Executable

Download the latest release from [Releases](https://github.com/mazongYY/FileMover/releases):

- **FileMover.exe** - Recommended version (~8MB)

#### Option 2: Run from Source

```bash
# Clone repository
git clone https://github.com/mazongYY/FileMover.git
cd FileMover

# Install optional dependencies (for RAR/7Z support)
pip install rarfile py7zr

# Run application
python main.py
```

### �️ System Requirements

- **OS**: Windows 7/8/10/11, macOS 10.12+, Linux
- **Python**: 3.8+ (source code only)
- **Memory**: 4GB+ recommended
- **Storage**: 50MB+ available space

### 🎯 Quick Start

1. **Select Archive File**
   - Click "Browse File" to select ZIP/RAR/7Z files
   - Or drag and drop files into the interface

2. **Enter Keywords**
   - Input search keywords in the text area
   - One keyword per line, supports Chinese and English

3. **Choose Operation Mode**
   - Move: Move matching files to target folder
   - Copy: Copy matching files to target folder
   - Link: Create shortcuts for matching files

4. **Start Processing**
   - Click "Preview Matching Files" to see what will be processed
   - Click "Start Processing" to execute
   - Output folder opens automatically when complete

### 🔧 Advanced Features

- **Regex Matching** - Complex filename pattern matching
- **File Type Filtering** - Filter by file extensions
- **Batch Processing** - Handle large numbers of files at once
- **Operation History** - Track all operations with undo support
- **Password Protection** - Support for encrypted archives
- **Multi-threading** - Improved performance for large files

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给个Star支持一下！**

Made with ❤️ by [mazongYY](https://github.com/mazongYY)

</div>
