import subprocess

class SubprocessCommands:
    def __init__(self,filename):
        self.command = ''
        if filename == 'settings': # I don't really need to open settings again.
            self.command = ["python", "-c",
           "from src.Gui.Exercise_setting_Gui import SettingGuiStandalone; SettingGuiStandalone().start_gui().run()"]
        elif filename == 'schedule':
            self.command = ["python", "-c",'from src.Schedule import Scheduler; Scheduler().start_scheduling().run()']
        

        self._run_subprocess()
        
    def _run_subprocess(self):
        try:
            subprocess.run(self.command, shell=True)
            print('runngig self.command')


        # print("Running tray from different file")
        except subprocess.CalledProcessError as e:
        # Handle any errors or exceptions that may occur
            print(f"Error running the external script: {e}")

if __name__ == "__main__":
    SubprocessCommands('settings')