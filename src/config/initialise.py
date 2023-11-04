import os,subprocess,shutil,platform
from pathlib import Path
from src.Gui.Exercise_setting_Gui import SettingGuiStandalone


## INSTALL REQUIREMENTS ##
def install_requiremnts(file_path):
    # Define the pip command to install requirements
    pip_command = ['pip', 'install', '-r', file_path]

    try:
        # Run the pip command
        subprocess.run(pip_command, check=True)
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")

## CREATE USER DIRECTORY AS EMPTY DIRECTORY NOT SAVED IN GIT
def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")


def install_fonts(fonts_dir, target_dir=None):
    if target_dir is None:
        # target_dir = get_font_directory()
        target_dir = get_user_font_directory()

    for font_file in Path(fonts_dir).glob("*.otf"):
        target_path = target_dir / font_file.name
        shutil.copy(font_file, target_path)
        print(f"Installed font: {font_file.name} to {target_path}")

def get_font_directory():
    system = platform.system()
    if system == "Windows":
        return Path(os.environ["SystemRoot"]) / "Fonts"
    elif system == "Darwin":
        return Path.home() / "Library" / "Fonts"
    elif system == "Linux":
        font_dirs = [
            Path.home() / ".fonts",
            Path("/usr/local/share/fonts"),
            Path("/usr/share/fonts"),
        ]
        for font_dir in font_dirs:
            if font_dir.exists():
                return font_dir
    return None

def get_user_font_directory(): # for current user doesn't need admin permission
    system = platform.system()
    if system == "Windows":
        return Path.home() / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts"
    elif system == "Darwin":
        return Path.home() / "Library" / "Fonts"
    elif system == "Linux":
        return Path.home() / ".fonts"
    return None

def update_initialise():
    install_requiremnts('requirements.txt')
    create_directory_if_not_exists("data/user")

if __name__ == "__main__":
    install_requiremnts('requirements.txt')
    create_directory_if_not_exists("data/user")
    SettingGuiStandalone().start_gui()
    # install_fonts('resources/fonts')
    

