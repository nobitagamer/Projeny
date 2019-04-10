@echo off
rem Run this script as admin once.

NET SESSION > NUL
IF NOT %ERRORLEVEL% EQU 0 (
    ECHO You are NOT Administrator. Exiting...
    PING 127.0.0.1 > NUL 2>&1
    EXIT /B 1
)

cinst -y python3 -ForceX86 --version 3.6.8

choco pin add -n=python3

cinst -y nsis
call refreshenv

pip3 install pyyaml pywin32

REM For Python 3.7 only, see https://stackoverflow.com/questions/50686243/cant-install-cx-freeze-or-scipy-python-3-7-64-bit
pip install wheel cx_Freeze
rem pip install cx_Freeze-5.1.1-cp36-cp36m-win32.whl
rem pip install cx_Freeze-5.1.1-cp37-cp37m-win_amd64.whl
