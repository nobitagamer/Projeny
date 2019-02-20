@echo off

cinst -y python3 -ForceX86 --version 3.6.8
call refreshenv

pip3 install pyyaml pywin32

REM For Python 3.7 only, see https://stackoverflow.com/questions/50686243/cant-install-cx-freeze-or-scipy-python-3-7-64-bit
pip install wheel cx_Freeze
rem pip install cx_Freeze-5.1.1-cp36-cp36m-win32.whl
rem pip install cx_Freeze-5.1.1-cp37-cp37m-win_amd64.whl

pushd "%~dp0Source"

call PackageBuild.bat"

popd
pause