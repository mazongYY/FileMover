# GitHub Wiki 设置指南

本指南将帮助您在GitHub上设置FileMover项目的Wiki文档。

## 📋 准备工作

### 1. 确认权限
- 确保您有仓库的管理员权限
- 或者是项目的维护者/协作者

### 2. 启用Wiki功能
1. 访问GitHub仓库页面
2. 点击"Settings"标签
3. 滚动到"Features"部分
4. 勾选"Wikis"选项
5. 点击"Save changes"

## 🚀 创建Wiki页面

### 1. 访问Wiki
1. 在仓库页面点击"Wiki"标签
2. 如果是第一次，会看到"Create the first page"

### 2. 创建首页
1. 点击"Create the first page"
2. 页面标题设为"Home"
3. 复制`wiki/Home.md`的内容到编辑器
4. 点击"Save Page"

### 3. 创建其他页面

#### 快速开始页面
1. 点击"New Page"
2. 页面标题: `Quick-Start`
3. 复制`wiki/Quick-Start.md`的内容
4. 保存页面

#### 用户指南页面
1. 点击"New Page"
2. 页面标题: `User-Guide`
3. 复制`wiki/User-Guide.md`的内容
4. 保存页面

#### 常见问题页面
1. 点击"New Page"
2. 页面标题: `FAQ`
3. 复制`wiki/FAQ.md`的内容
4. 保存页面

#### 开发文档页面
1. 点击"New Page"
2. 页面标题: `Development-Setup`
3. 复制`wiki/Development-Setup.md`的内容
4. 保存页面

### 4. 设置侧边栏
1. 创建新页面，标题为`_Sidebar`
2. 复制`wiki/_Sidebar.md`的内容
3. 保存页面
4. 侧边栏会自动显示在所有Wiki页面

## 📝 页面创建清单

### 用户文档
- [ ] **Home** - Wiki首页
- [ ] **Quick-Start** - 快速开始指南
- [ ] **User-Guide** - 完整用户指南
- [ ] **FAQ** - 常见问题解答
- [ ] **Troubleshooting** - 故障排除指南
- [ ] **Installation-Guide** - 安装指南

### 开发文档
- [ ] **Development-Setup** - 开发环境搭建
- [ ] **Code-Structure** - 代码结构说明
- [ ] **API-Documentation** - API接口文档
- [ ] **Contributing-Guide** - 贡献指南
- [ ] **Release-Process** - 发布流程

### 技术文档
- [ ] **Architecture** - 架构设计
- [ ] **Performance-Optimization** - 性能优化
- [ ] **Security-Considerations** - 安全考虑
- [ ] **Testing-Guide** - 测试指南

### 项目管理
- [ ] **Version-History** - 版本历史
- [ ] **Roadmap** - 项目路线图
- [ ] **Known-Issues** - 已知问题
- [ ] **Feature-Requests** - 功能请求

### 特殊页面
- [ ] **_Sidebar** - 侧边栏导航
- [ ] **_Footer** - 页脚信息（可选）

## 🎨 Wiki格式化技巧

### 1. 页面标题
```markdown
# 主标题
## 二级标题
### 三级标题
```

### 2. 链接
```markdown
# 内部链接（Wiki页面）
[快速开始](Quick-Start)
[用户指南](User-Guide)

# 外部链接
[GitHub仓库](https://github.com/mazongYY/FileMover)

# 锚点链接
[跳转到章节](#章节标题)
```

### 3. 代码块
```markdown
# 行内代码
使用 `python main.py` 运行程序

# 代码块
```bash
git clone https://github.com/mazongYY/FileMover.git
cd FileMover
python main.py
```
```

### 4. 表格
```markdown
| 格式 | 支持状态 | 说明 |
|------|----------|------|
| ZIP | ✅ 完全支持 | 最常用格式 |
| RAR | ✅ 完全支持 | 需要rarfile库 |
```

### 5. 提示框
```markdown
> **注意**: 这是一个重要提示

> **警告**: 这是一个警告信息

> **提示**: 这是一个使用技巧
```

## 🔧 Wiki管理

### 1. 编辑页面
1. 在Wiki页面点击"Edit"按钮
2. 修改内容
3. 在底部填写编辑说明
4. 点击"Save Page"

### 2. 删除页面
1. 在Wiki页面点击"Edit"按钮
2. 点击"Delete Page"按钮
3. 确认删除操作

### 3. 查看历史
1. 在Wiki页面点击"Page History"
2. 查看所有编辑记录
3. 可以比较不同版本的差异

### 4. 克隆Wiki
```bash
# Wiki有独立的Git仓库
git clone https://github.com/mazongYY/FileMover.wiki.git

# 编辑本地文件
# 提交更改
git add .
git commit -m "Update wiki content"
git push origin master
```

## 📊 Wiki维护

### 1. 定期更新
- 随着软件版本更新Wiki内容
- 添加新功能的使用说明
- 更新已知问题和解决方案

### 2. 内容审查
- 检查链接是否有效
- 确保信息准确性
- 修正拼写和语法错误

### 3. 用户反馈
- 关注用户在Issues中的文档相关问题
- 根据反馈改进文档内容
- 添加用户常问的问题到FAQ

## 🎯 最佳实践

### 1. 内容组织
- 使用清晰的层级结构
- 提供充足的交叉引用
- 保持导航的一致性

### 2. 写作风格
- 使用简洁明了的语言
- 提供具体的示例
- 包含必要的截图

### 3. 维护策略
- 建立定期更新计划
- 指定专人负责维护
- 建立内容审查流程

## 📞 获取帮助

如果在设置Wiki过程中遇到问题：

1. **GitHub文档**
   - [About wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis)
   - [Adding or editing wiki pages](https://docs.github.com/en/communities/documenting-your-project-with-wikis/adding-or-editing-wiki-pages)

2. **联系维护者**
   - 在仓库中创建Issue
   - 标记为`documentation`标签

3. **社区支持**
   - GitHub Community Forum
   - Stack Overflow

---

**完成Wiki设置后，记得在README.md中添加Wiki链接！**

```markdown
## 📚 文档

- [📖 Wiki文档](https://github.com/mazongYY/FileMover/wiki)
- [🚀 快速开始](https://github.com/mazongYY/FileMover/wiki/Quick-Start)
- [❓ 常见问题](https://github.com/mazongYY/FileMover/wiki/FAQ)
```
