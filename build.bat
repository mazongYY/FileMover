@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo    FileMover v4.0 自动打包脚本
echo ==========================================
echo.

echo 🔍 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)

echo.
echo 🔍 检查依赖包...
python -c "import pyinstaller; print('✅ PyInstaller已安装')" 2>nul || (
    echo ❌ PyInstaller未安装，正在安装...
    pip install pyinstaller
)

python -c "import rarfile; print('✅ rarfile已安装')" 2>nul || (
    echo ❌ rarfile未安装，正在安装...
    pip install rarfile
)

python -c "import py7zr; print('✅ py7zr已安装')" 2>nul || (
    echo ❌ py7zr未安装，正在安装...
    pip install py7zr
)

echo.
echo 🧹 清理旧的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "portable_release" rmdir /s /q "portable_release"

echo.
echo 🔨 开始打包...
python -m PyInstaller --clean --noconfirm file_filter_tool.spec

if errorlevel 1 (
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo 📦 创建便携版...
mkdir "portable_release" 2>nul

if exist "dist\FileMover_v4.0.exe" (
    copy "dist\FileMover_v4.0.exe" "portable_release\FileMover.exe"
    echo ✅ 复制可执行文件
) else (
    echo ❌ 找不到可执行文件
    pause
    exit /b 1
)

if exist "README.md" copy "README.md" "portable_release\使用说明.md"
if exist "CHANGELOG.md" copy "CHANGELOG.md" "portable_release\更新日志.md"
if exist "LICENSE" copy "LICENSE" "portable_release\许可证.txt"

echo.
echo 📝 创建快速开始指南...
(
echo FileMover v4.0 - 快速开始指南
echo.
echo 🚀 使用步骤：
echo 1. 双击运行 FileMover.exe
echo 2. 选择要处理的压缩包文件
echo 3. 输入筛选关键字（每行一个）
echo 4. 配置高级过滤选项（可选）
echo 5. 点击"预览匹配文件"查看结果
echo 6. 点击"开始处理"执行文件操作
echo.
echo 📁 输出目录：
echo - 默认在桌面创建 extracted_files 文件夹
echo - 命中文件：extracted_files/命中文件/
echo - 未命中文件：extracted_files/未命中文件/
echo.
echo ⚙️ 主要功能：
echo - 支持ZIP、RAR、7Z压缩包
echo - 智能关键字搜索
echo - 多种操作模式（移动/复制/链接）
echo - 高级过滤选项
echo - 自动主题适配
echo.
echo 📞 技术支持：
echo - 项目地址：https://gitee.com/m6773/FileMover
echo - 问题反馈：请在项目页面提交Issue
echo.
echo 构建时间：%date% %time%
) > "portable_release\快速开始.txt"

echo.
echo 📊 打包完成统计：
echo ==========================================
for %%f in (portable_release\*) do (
    echo 📄 %%~nxf
)

echo.
echo 🎉 FileMover v4.0 打包完成！
echo 📁 便携版位置: portable_release\
echo 🚀 可以开始分发了！
echo.
pause
