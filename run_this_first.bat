@echo off

rem Check if pip is available
where pip > nul 2>&1
if %errorlevel% equ 0 (
    pip install -r requirements.txt
) else (
    echo Pip is not installed. Please install Python and pip.
    pause
)
rem Open the Python script
mkdir "data/user" 
python src/Gui/Exercise_setting_Gui.py