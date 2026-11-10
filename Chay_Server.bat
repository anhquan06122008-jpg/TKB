@echo off
chcp 65001 >nul
title QLHT 3.9.0 - Khởi Động Máy Chủ Đồng Bộ
echo ======================================================================
echo           🚀 KHỞI ĐỘNG HỆ THỐNG QUẢN LÝ HỌC TẬP (QLHT) 3.9.0
echo ======================================================================
echo.

set PYTHON_BIN=

:: 1. Kiem tra MSYS2 UCRT64 Python
if exist "C:\msys64\ucrt64\bin\python.exe" (
    set "PYTHON_BIN=C:\msys64\ucrt64\bin\python.exe"
    goto :run_app
)

:: 2. Kiem tra MSYS2 MINGW64 Python
if exist "C:\msys64\mingw64\bin\python.exe" (
    set "PYTHON_BIN=C:\msys64\mingw64\bin\python.exe"
    goto :run_app
)

:: 3. Kiem tra py launcher
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PYTHON_BIN=py -3"
    goto :run_app
)

:: 4. Kiem tra python trong PATH
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python -c "import sys; print(sys.version)" >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_BIN=python"
        goto :run_app
    )
)

:: 5. Kiem tra LocalAppData
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        set "PYTHON_BIN=%%D\python.exe"
        goto :run_app
    )
)

:: 6. Kiem tra ProgramFiles
for /d %%D in ("%ProgramFiles%\Python*") do (
    if exist "%%D\python.exe" (
        set "PYTHON_BIN=%%D\python.exe"
        goto :run_app
    )
)

echo [!] Khong tim thay trinh thuc thi Python tren may tinh.
echo Vui long cai dat Python hoac kiem tra thu muc MSYS2.
pause
exit /b 1

:run_app
cd /d "%~dp0"
echo [*] Tim thay Python tai: %PYTHON_BIN%
echo [*] Dang khoi dong QLHT Backend Server...
echo.

:: Tu dong mo trinh duyet sau 1 giay
start "" cmd /c "timeout /t 1 /nobreak >nul & start http://localhost:8080"

:: Khoi dong server.py
%PYTHON_BIN% server.py 8080

pause
