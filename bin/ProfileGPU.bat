@echo off
REM Check if the user provided an argument
if "%~1"=="" (
    echo Please provide the name of the executable as an argument.
    exit /b 1
)

REM Start the executable with the -x argument
start "" "%~1" -trace=cpu,gpu,frame,log,bookmark,RHICommands,RenderCommands -statnamedevents -ExecCmds="r.DynamicRes.OperationMode 0, r.RHISetGPUCaptureOptions 1"