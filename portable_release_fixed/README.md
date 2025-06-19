# 🗂️ Windows 文件筛选与移动工具

<div align="center">

![Version](https://img.shields.io/badge/version-4.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**一个功能强大的Windows文件管理工具，支持从压缩包中智能筛选和分类文件**

[功能特点](#-功能特点) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [高级功能](#-高级功能) • [贡献指南](#-贡献指南)

</div>

---

## 📋 目录

- [功能特点](#-功能特点)
- [系统要求](#-系统要求)
- [快速开始](#-快速开始)
- [使用指南](#-使用指南)
- [高级功能](#-高级功能)
- [配置说明](#-配置说明)
- [故障排除](#-故障排除)
- [版本历史](#-版本历史)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

## ✨ 功能特点

### 🎯 核心功能
- **智能文件筛选**: 基于关键字快速筛选文件
- **多格式支持**: 支持ZIP、RAR、7Z等主流压缩格式
- **自动分类**: 自动将匹配和未匹配文件分类到不同目录
- **拖拽操作**: 支持拖拽压缩包到程序界面
- **自动清理**: 导入新压缩包时自动清理旧文件

### 🔧 高级功能
- **正则表达式**: 支持复杂的正则表达式匹配模式
- **文件类型过滤**: 按文件类型（图片、文档、视频等）筛选
- **多种操作模式**: 支持移动、复制、创建链接三种操作
- **撤销功能**: 完整的操作撤销和恢复机制
- **密码保护**: 支持密码保护的压缩包
- **压缩包预览**: 无需解压即可预览压缩包内容

### 🎨 用户体验
- **直观界面**: 现代化的图形用户界面
- **实时预览**: 处理前预览匹配文件数量
- **详细日志**: 完整的操作日志记录
- **配置保存**: 自动保存用户偏好设置
- **智能窗口**: 自适应屏幕大小的窗口布局

## 💻 系统要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 7/8/10/11 |
| **Python版本** | 3.6 或更高版本 |
| **内存** | 最少 512MB RAM |
| **存储空间** | 最少 50MB 可用空间 |
| **显示器** | 最小分辨率 1024x768 |

## 🚀 快速开始

### 方法一：直接运行Python脚本

1. **克隆仓库**
   ```bash
   git clone https://gitee.com/m6773/FileMover.git
   cd FileMover
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

### 方法二：使用可执行文件

1. 下载最新版本的可执行文件
2. 双击运行 `文件筛选与移动工具v4.0.exe`
3. 无需安装Python环境

## 📖 使用指南

### 基础使用流程

1. **选择压缩包**
   - 点击"浏览"按钮选择压缩包
   - 或直接拖拽压缩包到程序界面

2. **设置筛选条件**
   - 在关键字输入框中输入筛选关键字（每行一个）
   - 可选择启用正则表达式模式
   - 可设置文件类型过滤

3. **预览结果**
   - 点击"预览匹配文件"查看匹配数量
   - 在右侧面板查看压缩包内容

4. **执行操作**
   - 选择操作模式（移动/复制/创建链接）
   - 点击"开始处理"执行文件操作

### 界面说明

```
┌─────────────────────────────────────────────────────────────┐
│  🗂️ 文件筛选与移动工具 v4.0                                  │
├─────────────────────┬───────────────────────────────────────┤
│                     │                                       │
│  📁 文件选择        │  📦 压缩包预览                        │
│  🔍 关键字设置      │  📋 操作日志                          │
│  ⚙️ 操作模式        │  ↩️ 撤销管理                          │
│  🎯 高级过滤        │                                       │
│  🎮 操作控制        │                                       │
│                     │                                       │
└─────────────────────┴───────────────────────────────────────┘
```

## 🔧 高级功能

### 正则表达式支持

启用正则表达式模式后，可以使用复杂的匹配模式：

```regex
# 匹配特定格式的文件名
^report_\d{4}_\d{2}_\d{2}\.pdf$

# 匹配包含特定关键字的文件
.*(重要|urgent|important).*

# 匹配特定日期范围
.*202[3-4]-(0[1-9]|1[0-2]).*
```

### 文件类型预设

程序内置了常用的文件类型分类：

| 类型 | 扩展名 |
|------|--------|
| **图片文件** | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp |
| **文档文件** | .doc, .docx, .pdf, .txt, .rtf, .odt |
| **表格文件** | .xls, .xlsx, .csv, .ods |
| **演示文件** | .ppt, .pptx, .odp |
| **视频文件** | .mp4, .avi, .mkv, .mov, .wmv, .flv |
| **音频文件** | .mp3, .wav, .flac, .aac, .ogg |
| **压缩文件** | .zip, .rar, .7z, .tar, .gz |
| **代码文件** | .py, .js, .html, .css, .java, .cpp, .c |

### 撤销功能

- **完整记录**: 记录所有文件操作的详细信息
- **一键撤销**: 支持单个操作或批量撤销
- **安全备份**: 自动备份被移动的文件
- **状态恢复**: 完整恢复文件的原始位置

## ⚙️ 配置说明

### 配置文件位置

- **用户配置**: `config.json`
- **撤销历史**: `undo_history.json`
- **日志文件**: `logs/file_filter.log`

### 主要配置项

```json
{
  "user_preferences": {
    "keywords_history": [],           // 关键字历史记录
    "operation_mode": "move",         // 默认操作模式
    "regex_mode": false,              // 正则表达式模式
    "ui_settings": {
      "window_geometry": "1200x800",  // 窗口大小
      "remember_last_archive": true   // 记住上次选择的压缩包
    }
  }
}
```

## 🔍 故障排除

### 常见问题

<details>
<summary><strong>Q: 程序无法启动，提示缺少模块</strong></summary>

**A:** 请确保已安装所有依赖：
```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>Q: 无法处理RAR格式的压缩包</strong></summary>

**A:** 需要安装额外的RAR支持：
```bash
pip install rarfile
```
并确保系统中安装了WinRAR或UnRAR。
</details>

<details>
<summary><strong>Q: 处理大文件时程序卡顿</strong></summary>

**A:** 这是正常现象，程序在后台处理文件。可以通过以下方式优化：
- 关闭其他占用内存的程序
- 使用SSD硬盘提高I/O性能
- 分批处理大量文件
</details>

<details>
<summary><strong>Q: 撤销功能无法使用</strong></summary>

**A:** 检查以下项目：
- 确保有足够的磁盘空间用于备份
- 检查backup目录的写入权限
- 查看日志文件了解具体错误信息
</details>

### 获取帮助

如果遇到其他问题，请：

1. 查看 `logs/file_filter.log` 日志文件
2. 在 [Issues](https://gitee.com/m6773/FileMover/issues) 页面搜索相似问题
3. 创建新的Issue并提供详细信息

## 📚 版本历史

### v4.0 (2024-05-31)
- ✨ 新增自动清理功能
- 🎨 优化窗口大小和布局
- 🔧 改进错误处理机制
- 📝 完善文档和注释

### v3.0 (2024-05-30)
- ✨ 新增撤销功能
- 🔐 支持密码保护压缩包
- 🎯 增强用户界面
- 📊 添加文件大小和时间过滤

### v2.0 (2024-05-29)
- ✨ 新增正则表达式支持
- 📁 文件类型筛选功能
- ⚙️ 配置文件保存
- 🔄 多种移动模式

### v1.0 (2024-05-28)
- 🎉 初始版本发布
- 📦 基础压缩包处理
- 🔍 关键字筛选功能
- 🖥️ 图形用户界面

查看完整的 [更新日志](CHANGELOG.md)

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork** 这个仓库
2. **创建** 你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **打开** 一个Pull Request

### 贡献类型

- 🐛 **Bug修复**: 报告或修复程序错误
- ✨ **新功能**: 提出或实现新功能
- 📝 **文档**: 改进文档和注释
- 🎨 **界面**: 改进用户界面设计
- ⚡ **性能**: 优化程序性能
- 🧪 **测试**: 添加或改进测试用例

### 开发环境设置

```bash
# 克隆仓库
git clone https://gitee.com/m6773/FileMover.git
cd FileMover

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

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
