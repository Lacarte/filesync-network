@echo off
pushd %~dp0

:: Check if venv exists
IF EXIST .venv (
    :: Change to the venv's Scripts directory
    echo .venv found...
    pushd .venv\Scripts
    
    :: Run your script using this venv's python.exe
    python.exe ../../filesync-network.py
    popd
) ELSE (
    echo .venv not found...
    :: Run your script using the system's python
    python filesync-network.py
)

pause
