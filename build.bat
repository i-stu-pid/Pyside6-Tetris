@echo off
setlocal enabledelayedexpansion


:: ============================= ��Ҫ����������Ϣ ============================= 

:: miniconda ��װ·��
set conda_path=C:\Users\stu--\miniconda3

:: miniconda ����ű�·��
set conda_activate_script_path=%conda_path%\Scripts\activate.bat

:: ���⻷������
set env_name=env_pyside6

:: �����ļ���
set build_file_name=main.py

:: ���ɵĴ���ļ���
set package_name=tetris_game

:: ���ɵĴ���ļ����� [D �����ļ���; F ����exe�ļ�]
set package_type=D

:: ִ���ļ���ʾ���� [c ����̨; w ����]
set display_type=w

:: pyinstaller�����չ����
set pyinstaller_extend_config=--hidden-import PySide6.QtSvg --paths shiboken6.abi3.dll

:: ȷ������
echo conda ��װ·�� : %conda_path%
echo conda ����ű�·�� : %conda_activate_script_path%
echo ���⻷�� : %env_name%
echo �����ļ��� : %build_file_name%
echo ���ɵĴ���ļ��� : %package_name%
choice /c YN /m "������������ ȷ���밴 Y, ���밴 N"
if errorlevel 2 (
    echo ��� build.bat �ļ��޸�����
    pause
    exit /b 1
)

:: ============================= ��ʽִ�� ============================= 

:: ��ȡbat�ļ�����Ŀ¼���Զ�����·���еĿո�
set "current_dir=%~dp0"
if "%current_dir:~-1%"=="\" set "current_dir=%current_dir:~0,-1%"
echo ���ڴ���Ŀ¼��%current_dir%

:: ��ʼ��Conda������·�������ʵ�ʰ�װλ���޸ģ�
echo ��ʼ�� conda ����
call %conda_activate_script_path% %conda_path%
if errorlevel 1 (
    echo �����޷���ʼ�� conda ����
    pause
    exit /b 1
)

:: ����bat�ļ�����Ŀ¼
echo ����Ŀ¼ : %current_dir%
cd /d %current_dir%
if errorlevel 1 (
    echo ���󣺽���bat�ļ�����Ŀ¼ %current_dir%
    pause
    exit /b 1
)

:: ����Ŀ�껷��
echo ���� conda ���� [%env_name%]
call conda activate %env_name%
if errorlevel 1 (
    echo �����޷����� conda ���� [%env_name%]
    pause
    exit /b 1
)

:: ��������������������
set pip_requirements_file=requirements.txt
set conda_environment_file=environment.yml
echo ��������������������
pip freeze > %pip_requirements_file%
if errorlevel 1 (
    echo �������� %pip_requirements_file% ʧ��
    pause
    exit /b 1
)
call conda env export > %conda_environment_file%
if errorlevel 1 (
    echo ���󣺵��� %conda_environment_file% ʧ��
    pause
    exit /b 1
)

:: ����ļ��Ƿ����
if not exist "%pip_requirements_file%" (
    echo ����δ���� %pip_requirements_file%
    pause
    exit /b 1
)
if not exist "%conda_environment_file%" (
    echo ����δ���� %conda_environment_file%
    pause
    exit /b 1
)

:: ת��Ϊ UTF-8 �� BOM ��ʽ
echo ����ת��Ϊ UTF-8 �� BOM ��ʽ...
powershell -Command "$content = [System.IO.File]::ReadAllText('%pip_requirements_file%', [System.Text.Encoding]::Default); [System.IO.File]::WriteAllText('%pip_requirements_file%', $content, [System.Text.Encoding]::UTF8)"
powershell -Command "$content = [System.IO.File]::ReadAllText('%conda_environment_file%', [System.Text.Encoding]::Default); [System.IO.File]::WriteAllText('%conda_environment_file%', $content, [System.Text.Encoding]::UTF8)"

:: ʹ�� PyInstaller ���
echo PyInstaller ���
pyinstaller --clean -y -%package_type% -%display_type% %build_file_name% -n %package_name% %pyinstaller_extend_config%
if errorlevel 1 (
    echo ����PyInstaller ���ʧ��
    pause
    exit /b 1
)

echo ���в�������ɣ�
pause
