# GitHub API连接测试脚本 (PowerShell版本)
# 用于验证GITHUB_TOKEN是否正确配置

function Write-Status {
    param(
        [string]$Message,
        [string]$Status = "Info"
    )
    
    $icons = @{
        "Success" = "✅"
        "Error" = "❌"
        "Warning" = "⚠️"
        "Info" = "ℹ️"
    }
    
    $icon = $icons[$Status]
    if (-not $icon) { $icon = "ℹ️" }
    
    Write-Host "$icon $Message"
}

function Test-GitHubToken {
    Write-Host "🔍 GitHub API连接测试" -ForegroundColor Cyan
    Write-Host ("=" * 50)
    
    # 检查环境变量
    $token = $env:GITHUB_TOKEN
    if (-not $token) {
        Write-Status "GITHUB_TOKEN环境变量未设置" "Error"
        Write-Host "`n📋 设置方法："
        Write-Host '[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_your_token", "User")' -ForegroundColor Yellow
        Write-Host "然后重启PowerShell" -ForegroundColor Yellow
        return $false
    }
    
    Write-Status "GITHUB_TOKEN已设置，长度：$($token.Length)" "Success"
    
    # 验证Token格式
    if (-not ($token.StartsWith("ghp_") -or $token.StartsWith("github_pat_"))) {
        Write-Status "Token格式可能不正确，应以ghp_或github_pat_开头" "Warning"
    }
    
    # 设置请求头
    $headers = @{
        "Authorization" = "token $token"
        "User-Agent" = "FileMover-Test-Script"
        "Accept" = "application/vnd.github.v3+json"
    }
    
    try {
        # 测试1：获取用户信息
        Write-Host "`n🔍 测试1：获取用户信息"
        $response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -TimeoutSec 10
        
        Write-Status "用户：$($response.login)" "Success"
        Write-Status "用户名：$($response.name)" "Info"
        Write-Status "邮箱：$($response.email)" "Info"
        
        # 测试2：访问FileMover仓库
        Write-Host "`n🔍 测试2：访问FileMover仓库"
        $repoResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/mazongYY/FileMover" -Headers $headers -TimeoutSec 10
        
        Write-Status "仓库：$($repoResponse.full_name)" "Success"
        Write-Status "描述：$($repoResponse.description)" "Info"
        Write-Status "私有：$(if($repoResponse.private) {'是'} else {'否'})" "Info"
        
        # 测试3：测试Issues API
        Write-Host "`n🔍 测试3：测试Issues API"
        $issuesResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/mazongYY/FileMover/issues" -Headers $headers -TimeoutSec 10
        
        Write-Status "Issues访问成功，共$($issuesResponse.Count)个Issue" "Success"
        
        # 测试4：检查API限制
        Write-Host "`n🔍 测试4：检查API限制"
        $rateLimitResponse = Invoke-RestMethod -Uri "https://api.github.com/rate_limit" -Headers $headers -TimeoutSec 10
        
        $coreLimit = $rateLimitResponse.resources.core
        Write-Status "API限制：$($coreLimit.remaining)/$($coreLimit.limit)" "Info"
        
        $resetTime = [DateTimeOffset]::FromUnixTimeSeconds($coreLimit.reset).DateTime
        Write-Status "重置时间：$resetTime" "Info"
        
        Write-Host "`n$("=" * 50)"
        Write-Status "所有测试通过！GitHub API连接正常" "Success"
        return $true
        
    } catch {
        $errorMessage = $_.Exception.Message
        if ($errorMessage -like "*401*") {
            Write-Status "Token无效或已过期" "Error"
        } elseif ($errorMessage -like "*403*") {
            Write-Status "Token权限不足" "Error"
        } elseif ($errorMessage -like "*404*") {
            Write-Status "仓库不存在或无访问权限" "Error"
        } else {
            Write-Status "API请求失败：$errorMessage" "Error"
        }
        return $false
    }
}

function Main {
    Write-Host "🚀 FileMover GitHub API测试工具" -ForegroundColor Green
    Write-Host "⏰ 测试时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    
    $success = Test-GitHubToken
    
    if ($success) {
        Write-Host "`n🎉 恭喜！GitHub MCP工具现在可以正常使用了" -ForegroundColor Green
        Write-Host "`n📋 可用功能："
        Write-Host "- create_issue_GitHub"
        Write-Host "- create_pull_request_GitHub"
        Write-Host "- get_file_contents_GitHub"
        Write-Host "- push_files_GitHub"
        Write-Host "- 等等..."
    } else {
        Write-Host "`n❌ 请修复上述问题后重新测试" -ForegroundColor Red
        exit 1
    }
}

# 运行主函数
Main
