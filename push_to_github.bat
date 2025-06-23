@echo off
echo FileMover项目推送到GitHub脚本
echo ================================

echo 检查Git状态...
git status

echo.
echo 推送到GitHub仓库...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ 推送成功！
    echo 项目已成功推送到: https://github.com/mazongYY/FileMover
    echo.
    echo 📦 包含的可执行文件:
    echo - FileMover_Modern_v2.exe (现代化UI v2)
    echo - FileMover_Clean.exe (原始UI版本)
    echo - FileMover_Ultra_v2.exe (超级版本v2)
    echo - FileMover_Ultra.exe (超级版本)
    echo - FileMover_Pure.exe (纯净版本)
    echo - FileMover_Simple.exe (简化版本)
    echo.
    echo 🌐 访问项目主页: https://github.com/mazongYY/FileMover
    echo 📋 创建Release: https://github.com/mazongYY/FileMover/releases/new
) else (
    echo.
    echo ❌ 推送失败！
    echo 可能的原因:
    echo 1. 网络连接问题
    echo 2. 需要配置GitHub认证
    echo 3. 仓库权限问题
    echo.
    echo 解决方案:
    echo 1. 检查网络连接
    echo 2. 配置Git凭据: git config --global user.name "your-username"
    echo 3. 配置Git邮箱: git config --global user.email "your-email@example.com"
    echo 4. 使用GitHub Desktop或其他Git客户端
)

echo.
pause
