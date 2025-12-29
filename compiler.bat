@echo off
title AutoClicker Compiler

:: Step 0 - Instructions
echo ============================================================
echo   INSTRUCTIONS:
echo   1. Create a new folder anywhere on your PC.
echo   2. Copy this batch file into that folder.
echo   3. Place your autoclicker.py file in the same folder.
echo   4. Once ready, press any key to continue.
echo ============================================================
pause

:: Step 1 - Install pynput
echo Installing pynput...
python -m pip install pynput

:: Step 2 - Install pyinstaller
echo Installing pyinstaller...
python -m pip install pyinstaller

:: Step 3 - Ask user for autoclicker.py path
set /p filepath=Enter full path to autoclicker.py: 

:: Step 4 - Compile Python file to EXE
echo Compiling %filepath% to EXE...
python -m PyInstaller --onefile "%filepath%"

:: Step 5 - Check for success or failure
IF ERRORLEVEL 1 (
    echo.
    echo ❌ Compilation failed! Please check:
    echo   - Is Python installed and added to PATH?
    echo   - Is autoclicker.py path correct?
    echo   - Do you have write permissions in this folder?
) ELSE (
    echo.
    echo ✅ Compilation complete! Check the "dist" folder for your EXE.
)

pause