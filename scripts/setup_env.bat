@echo off
setlocal enabledelayedexpansion

set ENV_NAME=tp_project_env
set PYTHON_VERSION=3.11

echo [INFO] Looking for conda...

if defined CONDA_EXE (
    set "CONDA_BAT=%CONDA_EXE%"
) else (
    call conda --version >nul 2>nul
    if errorlevel 1 (
        echo [ERROR] Conda not found in PATH. Please install Anaconda or Miniconda, or run this script from Anaconda Prompt.
        pause
        exit /b 1
    )
    for /f "delims=" %%i in ('where conda') do set "CONDA_EXE_PATH=%%i"
    set "CONDA_BAT=%CONDA_EXE_PATH%"
)

echo [INFO] Conda found: %CONDA_BAT%

call "%CONDA_BAT%" --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Failed to run conda.
    pause
    exit /b 1
)

echo [INFO] Checking if environment exists...
call "%CONDA_BAT%" env list | findstr /r /c:"^%ENV_NAME% " >nul
if errorlevel 1 (
    echo [INFO] Creating environment %ENV_NAME% with Python %PYTHON_VERSION%...
    call "%CONDA_BAT%" create -y -n %ENV_NAME% python=%PYTHON_VERSION%
    if errorlevel 1 (
        echo [ERROR] Failed to create environment.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Environment %ENV_NAME% already exists.
)

if not exist requirements.txt (
    echo [ERROR] requirements.txt not found in the project root.
    pause
    exit /b 1
)

if not exist broken_env.py (
    echo [ERROR] broken_env.py not found in the project root.
    pause
    exit /b 1
)

echo [INFO] Upgrading pip...
call "%CONDA_BAT%" run -n %ENV_NAME% python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip.
    pause
    exit /b 1
)

echo [INFO] Installing dependencies from requirements.txt...
call "%CONDA_BAT%" run -n %ENV_NAME% python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [INFO] Running smoke test...
call "%CONDA_BAT%" run -n %ENV_NAME% python broken_env.py
if errorlevel 1 (
    echo [ERROR] Smoke test failed.
    pause
    exit /b 1
)

echo [OK] Environment is ready.
pause
exit /b 0
