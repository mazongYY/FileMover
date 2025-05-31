@echo off
chcp 65001 >nul
echo ========================================
echo Windows 文件筛选与移动工具 - 打包脚本
echo ========================================
echo.

echo [1/6] 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境
    pause
    exit /b 1
)

echo.
echo [2/6] 检查依赖包...
python -c "import tkinter, rarfile, py7zr; print('所有依赖包检查通过')"
if %errorlevel% neq 0 (
    echo 错误: 缺少必要的依赖包
    echo 请运行: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo [3/6] 创建应用图标...
if not exist app_icon.ico (
    echo 创建默认图标...
    python -c "
from PIL import Image
img = Image.new('RGB', (256, 256), (52, 152, 219))
img.save('app_icon.ico')
print('图标创建完成')
    "
    if %errorlevel% neq 0 (
        echo 警告: 无法创建图标，将使用默认图标
    )
)

echo.
echo [4/6] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "文件筛选与移动工具.exe" del "文件筛选与移动工具.exe"

echo.
echo [5/6] 开始打包程序...
echo 这可能需要几分钟时间，请耐心等待...
pyinstaller file_filter_tool.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo 错误: 打包失败
    pause
    exit /b 1
)

echo.
echo [6/6] 复制可执行文件...
if exist "dist\文件筛选与移动工具.exe" (
    copy "dist\文件筛选与移动工具.exe" "文件筛选与移动工具.exe"
    echo.
    echo ========================================
    echo 打包完成！
    echo ========================================
    echo 可执行文件: 文件筛选与移动工具.exe
    echo 分发目录: dist\文件筛选与移动工具_分发版\
    echo.
    echo 您可以直接运行 "文件筛选与移动工具.exe"
    echo 或者分发整个 "dist\文件筛选与移动工具_分发版" 目录
    echo.
) else (
    echo 错误: 未找到生成的可执行文件
    exit /b 1
)

echo 按任意键退出...
pause >nul
