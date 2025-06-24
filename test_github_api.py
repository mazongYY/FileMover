#!/usr/bin/env python3
"""
GitHub API连接测试脚本
用于验证GITHUB_TOKEN是否正确配置
"""

import os
import sys
import requests
import json
from datetime import datetime

def print_status(message, status="info"):
    """打印带状态的消息"""
    icons = {
        "success": "✅",
        "error": "❌", 
        "warning": "⚠️",
        "info": "ℹ️"
    }
    print(f"{icons.get(status, 'ℹ️')} {message}")

def test_github_token():
    """测试GitHub Token配置"""
    print("🔍 GitHub API连接测试")
    print("=" * 50)
    
    # 检查环境变量
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print_status("GITHUB_TOKEN环境变量未设置", "error")
        print("\n📋 设置方法：")
        print("Windows PowerShell:")
        print('[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_your_token", "User")')
        print("\nLinux/macOS:")
        print('export GITHUB_TOKEN="ghp_your_token"')
        return False
    
    print_status(f"GITHUB_TOKEN已设置，长度：{len(token)}", "success")
    
    # 验证Token格式
    if not token.startswith(('ghp_', 'github_pat_')):
        print_status("Token格式可能不正确，应以ghp_或github_pat_开头", "warning")
    
    # 设置请求头
    headers = {
        'Authorization': f'token {token}',
        'User-Agent': 'FileMover-Test-Script',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # 测试1：获取用户信息
        print("\n🔍 测试1：获取用户信息")
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print_status(f"用户：{user_data['login']}", "success")
            print_status(f"用户名：{user_data.get('name', 'N/A')}", "info")
            print_status(f"邮箱：{user_data.get('email', 'N/A')}", "info")
        elif response.status_code == 401:
            print_status("Token无效或已过期", "error")
            return False
        elif response.status_code == 403:
            print_status("Token权限不足", "error")
            return False
        else:
            print_status(f"API请求失败：{response.status_code}", "error")
            print(f"响应：{response.text}")
            return False
            
        # 测试2：检查Token权限
        print("\n🔍 测试2：检查Token权限")
        scopes = response.headers.get('X-OAuth-Scopes', '').split(', ')
        print_status(f"Token权限：{', '.join(scopes) if scopes[0] else '无'}", "info")
        
        required_scopes = ['repo', 'workflow']
        missing_scopes = [scope for scope in required_scopes if scope not in scopes]
        if missing_scopes:
            print_status(f"缺少必需权限：{', '.join(missing_scopes)}", "warning")
        else:
            print_status("Token权限充足", "success")
            
        # 测试3：访问FileMover仓库
        print("\n🔍 测试3：访问FileMover仓库")
        response = requests.get('https://api.github.com/repos/mazongYY/FileMover', headers=headers, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            print_status(f"仓库：{repo_data['full_name']}", "success")
            print_status(f"描述：{repo_data.get('description', 'N/A')}", "info")
            print_status(f"私有：{'是' if repo_data['private'] else '否'}", "info")
            print_status(f"权限：{repo_data.get('permissions', {})}", "info")
        elif response.status_code == 404:
            print_status("仓库不存在或无访问权限", "error")
            return False
        else:
            print_status(f"仓库访问失败：{response.status_code}", "error")
            return False
            
        # 测试4：测试Issues API
        print("\n🔍 测试4：测试Issues API")
        response = requests.get('https://api.github.com/repos/mazongYY/FileMover/issues', headers=headers, timeout=10)
        
        if response.status_code == 200:
            issues = response.json()
            print_status(f"Issues访问成功，共{len(issues)}个Issue", "success")
        else:
            print_status(f"Issues访问失败：{response.status_code}", "warning")
            
        # 测试5：测试Rate Limit
        print("\n🔍 测试5：检查API限制")
        response = requests.get('https://api.github.com/rate_limit', headers=headers, timeout=10)
        
        if response.status_code == 200:
            rate_data = response.json()
            core_limit = rate_data['resources']['core']
            print_status(f"API限制：{core_limit['remaining']}/{core_limit['limit']}", "info")
            reset_time = datetime.fromtimestamp(core_limit['reset'])
            print_status(f"重置时间：{reset_time}", "info")
        
        print("\n" + "=" * 50)
        print_status("所有测试通过！GitHub API连接正常", "success")
        return True
        
    except requests.exceptions.Timeout:
        print_status("请求超时，请检查网络连接", "error")
        return False
    except requests.exceptions.ConnectionError:
        print_status("网络连接错误", "error")
        return False
    except Exception as e:
        print_status(f"未知错误：{e}", "error")
        return False

def main():
    """主函数"""
    print("🚀 FileMover GitHub API测试工具")
    print(f"⏰ 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = test_github_token()
    
    if success:
        print("\n🎉 恭喜！GitHub MCP工具现在可以正常使用了")
        print("\n📋 可用功能：")
        print("- create_issue_GitHub")
        print("- create_pull_request_GitHub") 
        print("- get_file_contents_GitHub")
        print("- push_files_GitHub")
        print("- 等等...")
    else:
        print("\n❌ 请修复上述问题后重新测试")
        sys.exit(1)

if __name__ == "__main__":
    main()
