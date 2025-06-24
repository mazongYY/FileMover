# 贡献指南

感谢您对FileMover项目的关注！我们欢迎所有形式的贡献。

## 🤝 如何贡献

### 报告Bug
1. 检查[现有Issues](https://github.com/mazongYY/FileMover/issues)确保bug未被报告
2. 使用[Bug报告模板](.github/ISSUE_TEMPLATE/bug_report.md)创建新Issue
3. 提供详细的重现步骤和环境信息

### 建议功能
1. 检查[现有Issues](https://github.com/mazongYY/FileMover/issues)确保功能未被建议
2. 使用[功能请求模板](.github/ISSUE_TEMPLATE/feature_request.md)创建新Issue
3. 详细描述功能需求和使用场景

### 提交代码
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📋 开发环境设置

### 环境要求
- Python 3.8+
- Git
- 代码编辑器 (推荐VSCode)

### 安装步骤
```bash
# 克隆仓库
git clone https://github.com/mazongYY/FileMover.git
cd FileMover

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 🎨 代码规范

### Python代码风格
- 遵循PEP 8规范
- 使用4个空格缩进
- 行长度不超过88字符
- 使用有意义的变量和函数名

### 注释规范
```python
def process_archive(file_path: str, keywords: list) -> tuple:
    """
    处理压缩包文件
    
    Args:
        file_path (str): 压缩包文件路径
        keywords (list): 关键字列表
    
    Returns:
        tuple: (匹配文件数, 总文件数)
    """
    pass
```

### 提交信息规范
使用[约定式提交](https://www.conventionalcommits.org/zh-hans/)格式：

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

**类型说明：**
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例：**
```
feat(ui): 添加拖拽文件功能

- 支持拖拽压缩包文件到程序界面
- 添加拖拽区域视觉提示
- 支持多文件同时拖拽

Closes #123
```

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
python -m pytest

# 运行特定测试
python -m pytest tests/test_archive.py

# 生成覆盖率报告
python -m pytest --cov=main
```

### 测试要求
- 新功能必须包含测试
- 测试覆盖率应保持在80%以上
- 所有测试必须通过

## 📚 文档

### 文档更新
- 新功能需要更新README.md
- API变更需要更新代码注释
- 重要变更需要更新使用说明

### 文档风格
- 使用清晰简洁的中文
- 提供代码示例
- 包含截图说明（如适用）

## 🔍 代码审查

### 审查标准
- 代码功能正确性
- 代码风格一致性
- 性能影响评估
- 安全性考虑
- 文档完整性

### 审查流程
1. 自动化检查通过
2. 至少一位维护者审查
3. 解决所有审查意见
4. 合并到主分支

## 🏷️ 版本发布

### 版本号规则
遵循[语义化版本](https://semver.org/lang/zh-CN/)：
- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 发布流程
1. 更新版本号
2. 更新CHANGELOG.md
3. 创建Release标签
4. 发布可执行文件

## 📞 联系方式

- 🐛 **Bug报告**: [创建Issue](https://github.com/mazongYY/FileMover/issues/new?template=bug_report.md)
- ✨ **功能建议**: [创建Issue](https://github.com/mazongYY/FileMover/issues/new?template=feature_request.md)
- ❓ **问题咨询**: [创建Issue](https://github.com/mazongYY/FileMover/issues/new?template=question.md)
- 💬 **讨论**: [GitHub Discussions](https://github.com/mazongYY/FileMover/discussions)

## 📄 许可证

通过贡献代码，您同意您的贡献将在[MIT许可证](LICENSE)下授权。

---

再次感谢您的贡献！🎉
