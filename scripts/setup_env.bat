@echo off
setlocal

set "ENV_NAME=tp_project_env"
set "PYTHON_VERSION=3.11"
set "PROJECT_ROOT=%~dp0.."
set "PROJECT_ROOT=%PROJECT_ROOT:\=/%"
set "CONDA_EXE=C:\Users\IDD23\anaconda3\Scripts\conda.exe"

echo [INFO] Looking for conda...

if not exist "%CONDA_EXE%" (
    echo [ERROR] Conda was not found at:
    echo %CONDA_EXE%
    echo Please update CONDA_EXE in this script.
    pause
    exit /b 1
)

echo [INFO] Conda found: %CONDA_EXE%

"%CONDA_EXE%" --version
if errorlevel 1 (
    echo [ERROR] Failed to run conda.
    pause
    exit /b 1
)

cd /d "%~dp0.."

echo [INFO] Checking if environment exists...
"%CONDA_EXE%" env list | findstr /r /c:"%ENV_NAME%" >nul

if errorlevel 1 (
    echo [INFO] Creating environment %ENV_NAME% with Python %PYTHON_VERSION%...
    "%CONDA_EXE%" create -y -n %ENV_NAME% python=%PYTHON_VERSION%
    if errorlevel 1 (
        echo [ERROR] Failed to create environment.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Environment %ENV_NAME% already exists.
)

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt was not found.
    pause
    exit /b 1
)

if not exist "broken_env.py" (
    echo [ERROR] broken_env.py was not found.
    pause
    exit /b 1
)

echo [INFO] Installing dependencies from requirements.txt...
"%CONDA_EXE%" run -n %ENV_NAME% python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip.
    pause
    exit /b 1
)

"%CONDA_EXE%" run -n %ENV_NAME% python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [INFO] Running smoke test...
"%CONDA_EXE%" run -n %ENV_NAME% python broken_env.py
if errorlevel 1 (
    echo [ERROR] Smoke test failed.
    pause
    exit /b 1
)

echo [OK] Environment is ready.
pause
exit /b 0
if errorlevel 1 (
    echo [ERROR] Smoke test failed.
    pause
    exit /b 1
)

echo [OK] Environment is ready.
pause
exit /b 0
