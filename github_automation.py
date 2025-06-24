#!/usr/bin/env python3
"""
GitHub自动化管理脚本
用于FileMover项目的自动化管理
"""

import os
import sys
import requests
import json
from datetime import datetime

class GitHubAutomation:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.owner = 'mazongYY'
        self.repo = 'FileMover'
        self.base_url = 'https://api.github.com'
        
        if not self.token:
            print("❌ GITHUB_TOKEN环境变量未设置")
            sys.exit(1)
            
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'FileMover-Automation'
        }
    
    def create_labels(self):
        """创建项目标签"""
        labels = [
            {'name': 'bug', 'color': 'd73a4a', 'description': '错误修复'},
            {'name': 'enhancement', 'color': 'a2eeef', 'description': '功能增强'},
            {'name': 'documentation', 'color': '0075ca', 'description': '文档更新'},
            {'name': 'ci/cd', 'color': 'f9d0c4', 'description': '持续集成相关'},
            {'name': 'ui/ux', 'color': 'e4e669', 'description': '用户界面改进'},
            {'name': 'performance', 'color': 'c5def5', 'description': '性能优化'},
            {'name': 'security', 'color': 'b60205', 'description': '安全相关'},
            {'name': 'good first issue', 'color': '7057ff', 'description': '适合新手的问题'},
            {'name': 'help wanted', 'color': '008672', 'description': '需要帮助'},
            {'name': 'priority: high', 'color': 'b60205', 'description': '高优先级'},
            {'name': 'priority: medium', 'color': 'fbca04', 'description': '中优先级'},
            {'name': 'priority: low', 'color': '0e8a16', 'description': '低优先级'}
        ]
        
        for label in labels:
            try:
                response = requests.post(
                    f'{self.base_url}/repos/{self.owner}/{self.repo}/labels',
                    headers=self.headers,
                    json=label
                )
                if response.status_code == 201:
                    print(f"✅ 创建标签: {label['name']}")
                elif response.status_code == 422:
                    print(f"ℹ️ 标签已存在: {label['name']}")
                else:
                    print(f"❌ 创建标签失败: {label['name']} - {response.status_code}")
            except Exception as e:
                print(f"❌ 创建标签异常: {label['name']} - {e}")
    
    def create_milestones(self):
        """创建项目里程碑"""
        milestones = [
            {
                'title': 'v1.0.0 - 基础功能完善',
                'description': '完善基础功能，修复已知问题，优化用户体验',
                'due_on': '2025-07-31T23:59:59Z'
            },
            {
                'title': 'v1.1.0 - 多格式支持',
                'description': '添加RAR、7Z等多种压缩格式支持',
                'due_on': '2025-08-31T23:59:59Z'
            },
            {
                'title': 'v1.2.0 - 高级筛选功能',
                'description': '实现正则表达式筛选、文件大小过滤等高级功能',
                'due_on': '2025-09-30T23:59:59Z'
            },
            {
                'title': 'v2.0.0 - 重大功能更新',
                'description': '重大架构改进和新功能添加',
                'due_on': '2025-12-31T23:59:59Z'
            }
        ]
        
        for milestone in milestones:
            try:
                response = requests.post(
                    f'{self.base_url}/repos/{self.owner}/{self.repo}/milestones',
                    headers=self.headers,
                    json=milestone
                )
                if response.status_code == 201:
                    print(f"✅ 创建里程碑: {milestone['title']}")
                else:
                    print(f"❌ 创建里程碑失败: {milestone['title']} - {response.status_code}")
            except Exception as e:
                print(f"❌ 创建里程碑异常: {milestone['title']} - {e}")
    
    def create_project_management_issue(self):
        """创建项目管理主Issue"""
        issue_body = """## 📋 项目概述

FileMover是一个现代化的文件筛选工具，支持从压缩包中智能筛选和处理文件。

## 🎯 当前状态

### ✅ 已完成功能
- [x] 现代化深色主题UI设计
- [x] ZIP压缩包支持
- [x] 关键字匹配筛选
- [x] 多种操作模式（移动/复制/链接）
- [x] 自动化构建流程
- [x] GitHub API集成测试
- [x] GitHub Actions CI/CD修复

### 🔧 技术栈
- **前端**: Python Tkinter (现代化深色主题)
- **后端**: Python标准库
- **构建**: PyInstaller
- **CI/CD**: GitHub Actions
- **API**: GitHub REST API

## 📊 项目管理

### 🏷️ 标签系统
- `bug` - 错误修复
- `enhancement` - 功能增强
- `documentation` - 文档更新
- `ci/cd` - 持续集成相关
- `ui/ux` - 用户界面改进
- `performance` - 性能优化
- `security` - 安全相关

### 🎯 里程碑规划
- **v1.0.0** - 基础功能完善
- **v1.1.0** - 多格式支持
- **v1.2.0** - 高级筛选功能
- **v2.0.0** - 重大功能更新

## 🔄 自动化工作流程

### GitHub Actions
1. **CI Pipeline** - 代码质量检查和构建测试
2. **Release Pipeline** - 自动化发布和打包
3. **Issue Management** - 自动标签和分配

### 开发流程
1. 创建Issue描述需求或问题
2. 创建功能分支进行开发
3. 提交Pull Request进行代码审查
4. 合并后自动触发CI/CD流程
5. 发布新版本时自动创建Release

## 📈 项目指标

- **代码质量**: 通过CI检查
- **构建状态**: [![CI Pipeline](https://github.com/mazongYY/FileMover/actions/workflows/ci.yml/badge.svg)](https://github.com/mazongYY/FileMover/actions/workflows/ci.yml)
- **最新版本**: 查看 [Releases](https://github.com/mazongYY/FileMover/releases)

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request
5. 等待代码审查

---

**📝 注意**: 此Issue用于项目整体管理和跟踪，具体功能请求和错误报告请创建单独的Issue。"""

        issue_data = {
            'title': '🚀 FileMover项目自动化管理系统',
            'body': issue_body,
            'labels': ['documentation', 'enhancement']
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/repos/{self.owner}/{self.repo}/issues',
                headers=self.headers,
                json=issue_data
            )
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ 创建项目管理Issue: #{issue['number']}")
                return issue['number']
            else:
                print(f"❌ 创建Issue失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 创建Issue异常: {e}")
            return None
    
    def setup_automation(self):
        """设置完整的自动化系统"""
        print("🚀 开始设置FileMover项目自动化管理系统")
        print("=" * 60)
        
        print("\n📋 1. 创建项目标签...")
        self.create_labels()
        
        print("\n🎯 2. 创建项目里程碑...")
        self.create_milestones()
        
        print("\n📝 3. 创建项目管理Issue...")
        issue_number = self.create_project_management_issue()
        
        print("\n" + "=" * 60)
        print("✅ 自动化管理系统设置完成！")
        
        if issue_number:
            print(f"📋 项目管理Issue: #{issue_number}")
            print(f"🔗 查看: https://github.com/{self.owner}/{self.repo}/issues/{issue_number}")

def main():
    """主函数"""
    automation = GitHubAutomation()
    automation.setup_automation()

if __name__ == "__main__":
    main()
