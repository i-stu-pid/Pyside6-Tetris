@echo off
setlocal enabledelayedexpansion

:: ��ȡbat�ļ�����Ŀ¼���Զ�����·���еĿո�
set "current_dir=%~dp0"
if "%current_dir:~-1%"=="\" set "current_dir=%current_dir:~0,-1%"
echo ���ڴ���Ŀ¼��%current_dir%

:: ɾ������ __pycache__ �ļ���
echo �������� __pycache__ �ļ�...
for /r "%current_dir%" /d %%d in (__pycache__) do (
    if exist "%%d" (
        echo ɾ���ļ���: %%d
        rd /s /q "%%d"
    )
)

:: ɾ������ .pyc �ļ�
echo �������� .pyc �ļ�...
for /r "%current_dir%" %%f in (*.pyc) do (
    if exist "%%f" (
        echo ɾ���ļ�: %%f
        del /q "%%f"
    )
)

:: ��鲢���� build �ļ���
set "build_path=%current_dir%\build"
if exist "%build_path%" (
    echo ��⵽ build �ļ���: %build_path%
    choice /c YN /m "�Ƿ�ɾ�� build �ļ��У� ȷ���밴 Y, ���밴 N"
    if errorlevel 1 (
        echo ����ɾ�� build �ļ���...
        rd /s /q "%build_path%"
        echo ��ɾ�� build �ļ���
    ) else (
        echo ������ɾ�� build �ļ���
    )
) else (
    echo δ�ҵ� build �ļ���
)

echo ������ɣ�
pause
