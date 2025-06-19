@echo off
echo FileMover Windows可执行文件编译
echo ================================

echo 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo 开始编译现代化版本...
pyinstaller --onefile --windowed --name=FileMover_Modern --clean main_modern.py

if exist dist\FileMover_Modern.exe (
    echo 编译成功！
    echo 可执行文件位置: dist\FileMover_Modern.exe
    
    echo 复制配置文件...
    if exist config.json copy config.json dist\
    if exist README.md copy README.md dist\
    
    echo 显示文件信息...
    dir dist\
) else (
    echo 编译失败！
)

pause
