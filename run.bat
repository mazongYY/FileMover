@echo off
chcp 65001 >nul
title 文件筛选与移动工具

echo ========================================
echo    Windows 文件筛选与移动工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python，请先安装Python 3.6或更高版本
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo 正在启动程序...
echo.

REM 运行主程序
python main.py

REM 如果程序异常退出，显示错误信息
if %errorlevel% neq 0 (
    echo.
    echo 程序运行出错，错误代码：%errorlevel%
    echo 请检查Python环境和文件完整性
    echo.
    pause
)
