@echo off
setlocal enabledelayedexpansion


:: ============================= 需要配置以下信息 ============================= 

:: miniconda 安装路径
set conda_path=C:\Users\stu--\miniconda3

:: miniconda 激活脚本路径
set conda_activate_script_path=%conda_path%\Scripts\activate.bat

:: 虚拟环境名称
set env_name=env_pyside6

:: 编译文件名
set build_file_name=main.py

:: 生成的打包文件名
set package_name=tetris_game

:: 生成的打包文件类型 [D 单个文件夹; F 单个exe文件]
set package_type=D

:: 执行文件显示类型 [c 控制台; w 窗口]
set display_type=w

:: pyinstaller打包拓展配置
set pyinstaller_extend_config=--hidden-import PySide6.QtSvg --paths shiboken6.abi3.dll

:: 确认配置
echo conda 安装路径 : %conda_path%
echo conda 激活脚本路径 : %conda_activate_script_path%
echo 虚拟环境 : %env_name%
echo 编译文件名 : %build_file_name%
echo 生成的打包文件名 : %package_name%
choice /c YN /m "上述配置无误？ 确认请按 Y, 否请按 N"
if errorlevel 2 (
    echo 请打开 build.bat 文件修改配置
    pause
    exit /b 1
)

:: ============================= 正式执行 ============================= 

:: 获取bat文件所在目录（自动处理路径中的空格）
set "current_dir=%~dp0"
if "%current_dir:~-1%"=="\" set "current_dir=%current_dir:~0,-1%"
echo 正在处理目录：%current_dir%

:: 初始化Conda环境（路径需根据实际安装位置修改）
echo 初始化 conda 环境
call %conda_activate_script_path% %conda_path%
if errorlevel 1 (
    echo 错误：无法初始化 conda 环境
    pause
    exit /b 1
)

:: 进入bat文件所在目录
echo 进入目录 : %current_dir%
cd /d %current_dir%
if errorlevel 1 (
    echo 错误：进入bat文件所在目录 %current_dir%
    pause
    exit /b 1
)

:: 激活目标环境
echo 激活 conda 环境 [%env_name%]
call conda activate %env_name%
if errorlevel 1 (
    echo 错误：无法激活 conda 环境 [%env_name%]
    pause
    exit /b 1
)

:: 导出环境、包需求配置
set pip_requirements_file=requirements.txt
set conda_environment_file=environment.yml
echo 导出环境、包需求配置
pip freeze > %pip_requirements_file%
if errorlevel 1 (
    echo 错误：生成 %pip_requirements_file% 失败
    pause
    exit /b 1
)
call conda env export > %conda_environment_file%
if errorlevel 1 (
    echo 错误：导出 %conda_environment_file% 失败
    pause
    exit /b 1
)

:: 检查文件是否存在
if not exist "%pip_requirements_file%" (
    echo 错误：未生成 %pip_requirements_file%
    pause
    exit /b 1
)
if not exist "%conda_environment_file%" (
    echo 错误：未生成 %conda_environment_file%
    pause
    exit /b 1
)

:: 转换为 UTF-8 无 BOM 格式
echo 正在转换为 UTF-8 无 BOM 格式...
powershell -Command "$content = [System.IO.File]::ReadAllText('%pip_requirements_file%', [System.Text.Encoding]::Default); [System.IO.File]::WriteAllText('%pip_requirements_file%', $content, [System.Text.Encoding]::UTF8)"
powershell -Command "$content = [System.IO.File]::ReadAllText('%conda_environment_file%', [System.Text.Encoding]::Default); [System.IO.File]::WriteAllText('%conda_environment_file%', $content, [System.Text.Encoding]::UTF8)"

:: 使用 PyInstaller 打包
echo PyInstaller 打包
pyinstaller --clean -y -%package_type% -%display_type% %build_file_name% -n %package_name% %pyinstaller_extend_config%
if errorlevel 1 (
    echo 错误：PyInstaller 打包失败
    pause
    exit /b 1
)

echo 所有操作已完成！
pause
