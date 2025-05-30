@echo off
chcp 65001 >nul
title 打包文件筛选与移动工具

echo ========================================
echo    打包文件筛选与移动工具为EXE
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python，请先安装Python 3.6或更高版本
    pause
    exit /b 1
)

echo 检查PyInstaller是否安装...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller未安装，正在安装...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo 安装PyInstaller失败，请检查网络连接
        pause
        exit /b 1
    )
)

echo.
echo 开始打包程序...
echo 这可能需要几分钟时间，请耐心等待...
echo.

REM 清理之前的构建文件
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

REM 使用PyInstaller打包
pyinstaller --onefile --windowed --name "文件筛选与移动工具" main.py

if %errorlevel% eq 0 (
    echo.
    echo ========================================
    echo 打包成功！
    echo ========================================
    echo.
    echo 可执行文件位置：dist\文件筛选与移动工具.exe
    echo.
    echo 您可以将exe文件复制到任何位置使用
    echo 无需安装Python环境
    echo.
    
    REM 询问是否打开dist文件夹
    set /p choice="是否打开dist文件夹？(y/n): "
    if /i "%choice%"=="y" (
        explorer dist
    )
) else (
    echo.
    echo 打包失败，请检查错误信息
    echo.
)

pause
