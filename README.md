# FileMover v4.0 - 现代化文件筛选工具

<div align="center">

![Version](https://img.shields.io/badge/version-4.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

**现代化的文件筛选与移动工具，支持从压缩包中智能筛选和分类文件**

</div>

## ✨ 主要特性

- 🎨 **现代化UI设计** - 深色主题，圆角按钮，卡片式布局
- 📦 **压缩包支持** - ZIP、RAR、7Z等多种格式
- 🔍 **智能筛选** - 关键字匹配、正则表达式支持
- ⚡ **多种操作** - 移动、复制、创建链接
- 🚀 **处理完成自动打开文件夹**
- 🌐 **跨平台支持** - Windows、macOS、Linux
- 🛡️ **稳定可靠** - 彻底解决运行时错误问题

## 📦 下载使用

### 直接下载可执行文件

在 [Releases](https://github.com/mazongYY/FileMover/releases) 页面下载最新版本：

- **FileMover_Modern_v2.exe** ⭐⭐⭐⭐ 现代化UI v2（推荐）

### 从源码运行

```bash
# 克隆仓库
git clone https://github.com/mazongYY/FileMover.git
cd FileMover

# 安装依赖（可选，仅需要RAR/7Z支持时）
pip install rarfile py7zr

# 运行程序
python main_modern_v2.py
```

## 💻 系统要求

- **操作系统**: Windows 7/8/10/11、macOS 10.12+、Linux
- **Python**: 3.8+ （仅源码运行需要）
- **内存**: 建议4GB以上
- **磁盘空间**: 至少50MB可用空间

## 🚀 快速开始

1. **选择压缩包文件**
   - 点击"浏览文件"按钮选择ZIP/RAR/7Z文件
   - 或直接拖拽文件到程序界面

2. **输入关键字**
   - 在关键字输入框中输入搜索关键字
   - 每行一个关键字，支持中文、英文

3. **选择操作模式**
   - 移动文件：将匹配文件移动到目标文件夹
   - 复制文件：将匹配文件复制到目标文件夹
   - 创建链接：为匹配文件创建快捷方式

4. **开始处理**
   - 点击"预览匹配文件"查看将要处理的文件
   - 点击"开始处理"执行操作
   - 处理完成后可选择打开输出文件夹

## 🔧 高级功能

- **正则表达式匹配** - 支持复杂的文件名匹配规则
- **文件类型过滤** - 按文件扩展名筛选
- **批量处理** - 一次处理大量文件
- **操作历史** - 记录所有操作，支持撤销
- **密码保护** - 支持加密压缩包
- **多线程处理** - 提高大文件处理速度

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目主页：https://github.com/mazongYY/FileMover
- 问题反馈：https://github.com/mazongYY/FileMover/issues

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！



## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

```
MIT License

Copyright (c) 2024 GuoDong (m6773)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给它一个星标！**

[报告Bug](https://gitee.com/m6773/FileMover/issues) • [请求功能](https://gitee.com/m6773/FileMover/issues) • [贡献代码](https://gitee.com/m6773/FileMover/pulls)

Made with ❤️ by [GuoDong](https://gitee.com/m6773)

</div>
