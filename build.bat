@echo off
setlocal enabledelayedexpansion

:: ============================= 需要配置以下信息 ============================= 

:: miniconda 安装路径
set conda_path=

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

:: ============================= 获取 conda 安装路径 =============================
:: 已手动配置安装路径
if not "%conda_path%"=="" (
    :: 路径存在, 用户确认配置
    if exist "%conda_path%" (
        goto confirm_configuration
    )
    echo 手动配置的 conda 安装路径 [ %current_dir% ] 不存在, 将自动搜索
) else (
    echo conda 安装路径为空, 将自动搜索
)

:: 检查CONDA_EXE环境变量
echo 检查CONDA_EXE环境变量 %CONDA_EXE%
if not "%CONDA_EXE%"=="" (
    if exist "%CONDA_EXE%" (
        set "conda_exe=%CONDA_EXE%"
        goto get_conda_path_pass
    )
)

:: 检查PATH中的conda.exe
echo 检查环境变量PATH中的conda.exe
for %%p in ("%path:;=" "%") do (
    if exist "%%~p\conda.exe" (
        set "conda_exe=%%~p\conda.exe"
        goto get_conda_path_pass
    )
)

:: 检查默认安装路径
set default_paths=%USERPROFILE%\Miniconda3 C:\Miniconda3 C:\ProgramData\Miniconda3
echo 检查默认安装路径 : default_paths
for %%d in (%default_paths%) do (
    if exist "%%d\Scripts\conda.exe" (
        set "conda_exe=%%d\Scripts\conda.exe"
        goto get_conda_path_pass
    )
    if exist "%%d\condabin\conda.exe" (
        set "conda_exe=%%d\condabin\conda.exe"
        goto get_conda_path_pass
    )
)

:: 查找失败
echo 错误 : 未找到 conda 安装路径, 请手动配置
pause
exit /b 1

:: 查找成功 提取安装路径
:get_conda_path_pass
for %%a in ("%conda_exe%") do set "dir1=%%~dpa"
set "dir1=!dir1:~0,-1!"
for %%b in ("!dir1!") do set "base_dir=%%~dpb"
set "base_dir=!base_dir:~0,-1!"
:: echo conda 安装路径 : !base_dir!

:: miniconda 安装路径
set conda_path=!base_dir!
:: miniconda 激活脚本路径
set conda_activate_script_path=%conda_path%\Scripts\activate.bat

:: ============================= 用户确认配置 ============================= 
:confirm_configuration
::空行
echo.

:: 确认配置
echo 当前配置如下
echo conda 安装路径 : %conda_path%
echo conda 激活脚本路径 : %conda_activate_script_path%
echo 虚拟环境 : %env_name%
echo 编译文件名 : %build_file_name%
echo 生成的打包文件名 : %package_name%
choice /c YN /m "上述配置无误 ? ( 确认请按 Y, 否请按 N ) "
if errorlevel 2 (
    echo 请打开 build.bat 文件修改配置
    pause
    exit /b 1
)

:: ============================= 正式执行 ============================= 
::空行
echo.

:: 获取bat文件所在目录（自动处理路径中的空格）
set "current_dir=%~dp0"
if "%current_dir:~-1%"=="\" set "current_dir=%current_dir:~0,-1%"
echo 正在处理目录 : %current_dir%

:: 初始化Conda环境（路径需根据实际安装位置修改）
echo 初始化 conda 环境
call %conda_activate_script_path% %conda_path%
if errorlevel 1 (
    echo 错误 : 无法初始化 conda 环境
    pause
    exit /b 1
)

:: 进入bat文件所在目录
echo 进入目录 : %current_dir%
cd /d %current_dir%
if errorlevel 1 (
    echo 错误 : 进入bat文件所在目录 %current_dir%
    pause
    exit /b 1
)

:: 激活目标环境
echo 激活 conda 环境 [%env_name%]
call conda activate %env_name%
if errorlevel 1 (
    echo 错误 : 无法激活 conda 环境 [%env_name%]
    pause
    exit /b 1
)

:: 使用 PyInstaller 打包
echo PyInstaller 打包
pyinstaller --clean -y -%package_type% -%display_type% %build_file_name% -n %package_name% %pyinstaller_extend_config%
if errorlevel 1 (
    echo 错误 : PyInstaller 打包失败
    pause
    exit /b 1
)
echo PyInstaller 打包成功

:: ============================= 导出环境、包需求配置 ============================= 
::空行
echo.

:: 配置文件名称
set pip_requirements_file=requirements.txt
set conda_environment_file=environment.yml

:: 导出环境、包需求配置
echo 导出环境、包需求配置
pip freeze > %pip_requirements_file%
if errorlevel 1 (
    echo 错误 : 生成 %pip_requirements_file% 失败
    pause
    exit /b 1
)
call conda env export > %conda_environment_file%
if errorlevel 1 (
    echo 错误 : 导出 %conda_environment_file% 失败
    pause
    exit /b 1
)

:: 检查文件是否存在
if not exist "%pip_requirements_file%" (
    echo 错误 : 未生成 %pip_requirements_file%
    pause
    exit /b 1
)
if not exist "%conda_environment_file%" (
    echo 错误 : 未生成 %conda_environment_file%
    pause
    exit /b 1
)

:: 转换为 UTF-8 无 BOM 格式
echo 正在转换为 UTF-8 无 BOM 格式...
powershell -Command "$content = [System.IO.File]::ReadAllText('%pip_requirements_file%', [System.Text.Encoding]::Default); [System.IO.File]::WriteAllText('%pip_requirements_file%', $content, [System.Text.Encoding]::UTF8)"
powershell -Command "$content = [System.IO.File]::ReadAllText('%conda_environment_file%', [System.Text.Encoding]::Default); [System.IO.File]::WriteAllText('%conda_environment_file%', $content, [System.Text.Encoding]::UTF8)"
echo 转换完成

:: ============================= 执行成功 ============================= 
::空行
echo.

echo 所有操作均执行成功！
pause
