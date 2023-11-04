import subprocess

class SubprocessCommands:
    def __init__(self,filename):
        self.command = ''
        if filename == 'settings': # I don't really need to open settings again.
            self.command = ["python", "-c",
           "from src.Gui.Exercise_setting_Gui import SettingGuiStandalone; SettingGuiStandalone().start_gui()"]
        elif filename == 'schedule':
            self.command = ["python", "-c",'from src.Schedule import Scheduler; Scheduler().start_scheduling()']
        elif filename == 'initialise':
            self.command = ["python", "-c", 'from src.config.initialise import update_initialise; update_initialise()']
        

        self._run_subprocess()
        
    def _run_subprocess(self):
        try:
            subprocess.run(self.command, shell=True)

        # print("Running tray from different file")
        except subprocess.CalledProcessError as e:
        # Handle any errors or exceptions that may occur
            print(f"Error running the external script: {e}")

if __name__ == "__main__":
    SubprocessCommands('settings')