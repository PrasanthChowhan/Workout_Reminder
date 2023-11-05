import subprocess

class SubprocessCommands:
    @staticmethod  
    def run_subprocess(filename):
        command = ''
        if filename == 'settings': # I don't really need to open settings again.
            command= ["python", "-c",
           "from src.Gui.Exercise_setting_Gui import SettingGuiStandalone; SettingGuiStandalone().start_gui()"]
        elif filename == 'schedule':
            command= ["python", "-c",'from src.Schedule import Scheduler; Scheduler().start_scheduling()']
        elif filename == 'initialise':
            command= ["python", "-c", 'from src.config.initialise import update_initialise; update_initialise()']
        try:
            result = subprocess.run(self.command, shell=True)
            if result.returncode == 0:
                print(f'{command} subprocess executed successfully')

        # print("Running tray from different file")
        except subprocess.CalledProcessError as e:
        # Handle any errors or exceptions that may occur
            print(f"Error running the external script: {e}")

if __name__ == "__main__":
    SubprocessCommands('settings')