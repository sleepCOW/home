@echo off
pushd "%~dp0"
if "%1"=="" (
    echo Usage: run_python script.py [args...]
    exit /b 1
)
set SCRIPT=%1
shift
python %SCRIPT% %1 %2 %3 %4 %5 %6 %7 %8 %9
popd