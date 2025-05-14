@echo off
setlocal enabledelayedexpansion

:: ============================= ��Ҫ����������Ϣ ============================= 

:: miniconda ��װ·��
set conda_path=

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

:: ============================= ��ȡ conda ��װ·�� =============================
:: ���ֶ����ð�װ·��
if not "%conda_path%"=="" (
    :: ·������, �û�ȷ������
    if exist "%conda_path%" (
        goto confirm_configuration
    )
    echo �ֶ����õ� conda ��װ·�� [ %current_dir% ] ������, ���Զ�����
) else (
    echo conda ��װ·��Ϊ��, ���Զ�����
)

:: ���CONDA_EXE��������
echo ���CONDA_EXE�������� %CONDA_EXE%
if not "%CONDA_EXE%"=="" (
    if exist "%CONDA_EXE%" (
        set "conda_exe=%CONDA_EXE%"
        goto get_conda_path_pass
    )
)

:: ���PATH�е�conda.exe
echo ��黷������PATH�е�conda.exe
for %%p in ("%path:;=" "%") do (
    if exist "%%~p\conda.exe" (
        set "conda_exe=%%~p\conda.exe"
        goto get_conda_path_pass
    )
)

:: ���Ĭ�ϰ�װ·��
set default_paths=%USERPROFILE%\Miniconda3 C:\Miniconda3 C:\ProgramData\Miniconda3
echo ���Ĭ�ϰ�װ·�� : default_paths
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

:: ����ʧ��
echo ���� : δ�ҵ� conda ��װ·��, ���ֶ�����
pause
exit /b 1

:: ���ҳɹ� ��ȡ��װ·��
:get_conda_path_pass
for %%a in ("%conda_exe%") do set "dir1=%%~dpa"
set "dir1=!dir1:~0,-1!"
for %%b in ("!dir1!") do set "base_dir=%%~dpb"
set "base_dir=!base_dir:~0,-1!"
:: echo conda ��װ·�� : !base_dir!

:: miniconda ��װ·��
set conda_path=!base_dir!
:: miniconda ����ű�·��
set conda_activate_script_path=%conda_path%\Scripts\activate.bat

:: ============================= �û�ȷ������ ============================= 
:confirm_configuration
::����
echo.

:: ȷ������
echo ��ǰ��������
echo conda ��װ·�� : %conda_path%
echo conda ����ű�·�� : %conda_activate_script_path%
echo ���⻷�� : %env_name%
echo �����ļ��� : %build_file_name%
echo ���ɵĴ���ļ��� : %package_name%
choice /c YN /m "������������ ? ( ȷ���밴 Y, ���밴 N ) "
if errorlevel 2 (
    echo ��� build.bat �ļ��޸�����
    pause
    exit /b 1
)

:: ============================= ��ʽִ�� ============================= 
::����
echo.

:: ��ȡbat�ļ�����Ŀ¼���Զ�����·���еĿո�
set "current_dir=%~dp0"
if "%current_dir:~-1%"=="\" set "current_dir=%current_dir:~0,-1%"
echo ���ڴ���Ŀ¼ : %current_dir%

:: ��ʼ��Conda������·�������ʵ�ʰ�װλ���޸ģ�
echo ��ʼ�� conda ����
call %conda_activate_script_path% %conda_path%
if errorlevel 1 (
    echo ���� : �޷���ʼ�� conda ����
    pause
    exit /b 1
)

:: ����bat�ļ�����Ŀ¼
echo ����Ŀ¼ : %current_dir%
cd /d %current_dir%
if errorlevel 1 (
    echo ���� : ����bat�ļ�����Ŀ¼ %current_dir%
    pause
    exit /b 1
)

:: ����Ŀ�껷��
echo ���� conda ���� [%env_name%]
call conda activate %env_name%
if errorlevel 1 (
    echo ���� : �޷����� conda ���� [%env_name%]
    pause
    exit /b 1
)

:: ʹ�� PyInstaller ���
echo PyInstaller ���
pyinstaller --clean -y -%package_type% -%display_type% %build_file_name% -n %package_name% %pyinstaller_extend_config%
if errorlevel 1 (
    echo ���� : PyInstaller ���ʧ��
    pause
    exit /b 1
)
echo PyInstaller ����ɹ�

:: ============================= �������������������� ============================= 
::����
echo.

:: �����ļ�����
set pip_requirements_file=requirements.txt
set conda_environment_file=environment.yml

:: ��������������������
echo ��������������������
pip freeze > %pip_requirements_file%
if errorlevel 1 (
    echo ���� : ���� %pip_requirements_file% ʧ��
    pause
    exit /b 1
)
call conda env export > %conda_environment_file%
if errorlevel 1 (
    echo ���� : ���� %conda_environment_file% ʧ��
    pause
    exit /b 1
)

:: ����ļ��Ƿ����
if not exist "%pip_requirements_file%" (
    echo ���� : δ���� %pip_requirements_file%
    pause
    exit /b 1
)
if not exist "%conda_environment_file%" (
    echo ���� : δ���� %conda_environment_file%
    pause
    exit /b 1
)

:: ת��Ϊ UTF-8 �� BOM ��ʽ
echo ����ת��Ϊ UTF-8 �� BOM ��ʽ...
powershell -Command "$content = [System.IO.File]::ReadAllText('%pip_requirements_file%', [System.Text.Encoding]::Default); [System.IO.File]::WriteAllText('%pip_requirements_file%', $content, [System.Text.Encoding]::UTF8)"
powershell -Command "$content = [System.IO.File]::ReadAllText('%conda_environment_file%', [System.Text.Encoding]::Default); [System.IO.File]::WriteAllText('%conda_environment_file%', $content, [System.Text.Encoding]::UTF8)"
echo ת�����

:: ============================= ִ�гɹ� ============================= 
::����
echo.

echo ���в�����ִ�гɹ���
pause
