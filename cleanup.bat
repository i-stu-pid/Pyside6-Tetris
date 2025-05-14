@echo off
setlocal enabledelayedexpansion

:: 获取bat文件所在目录（自动处理路径中的空格）
set "current_dir=%~dp0"
if "%current_dir:~-1%"=="\" set "current_dir=%current_dir:~0,-1%"
echo 正在处理目录：%current_dir%

:: 删除所有 __pycache__ 文件夹
echo 正在清理 __pycache__ 文件...
for /r "%current_dir%" /d %%d in (__pycache__) do (
    if exist "%%d" (
        echo 删除文件夹: %%d
        rd /s /q "%%d"
    )
)

:: 删除所有 .pyc 文件
echo 正在清理 .pyc 文件...
for /r "%current_dir%" %%f in (*.pyc) do (
    if exist "%%f" (
        echo 删除文件: %%f
        del /q "%%f"
    )
)

:: 检查并处理 build 文件夹
set "build_path=%current_dir%\build"
if exist "%build_path%" (
    echo 检测到 build 文件夹: %build_path%
    choice /c YN /m "是否删除 build 文件夹？ 确认请按 Y, 否请按 N"
    if errorlevel 1 (
        echo 正在删除 build 文件夹...
        rd /s /q "%build_path%"
        echo 已删除 build 文件夹
    ) else (
        echo 已跳过删除 build 文件夹
    )
) else (
    echo 未找到 build 文件夹
)

echo 清理完成！
pause
