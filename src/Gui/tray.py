import pystray,sys
import threading,time,tkinter as tk
from pystray import Menu, MenuItem, Icon
from PIL import Image
from src.Gui.Exercise_setting_Gui import SettingGuiStandalone

# setter concept is used to auto update tray 


class WorkoutTray:
    
    def __init__(self, next_exercise_time=None,stop_scheduling_callabck = None ):
        self._next_exercise_time = next_exercise_time
        self.stop_scheduling_callabck = stop_scheduling_callabck

    @property
    def next_exercise_time(self):
        return self._next_exercise_time
    
    @next_exercise_time.setter
    def next_exercise_time(self,value):
        self._next_exercise_time = value
        self.update_tray()


    def _title(self) -> str:
        return "💪🏻Workout Reminder\n" + "next exercise on: " + self.next_exercise_time

    def _menu(self)-> Menu:
        return Menu(MenuItem("Settings", self._open_settings),
                    MenuItem("Exit", self._exit) # If you want to exit, then why use in the first place?
                    )

    def _image(self, ):    
        return Image.open(r"resources\icons\gui icon\fire.png")

   
    def _open_settings(self, icon, item):
        self.setting_gui = SettingGuiStandalone(self.stop_scheduling_callabck)
        # threading.Thread(target=SubprocessCommands, args=('settings', )).start()
        threading.Thread(target=self.setting_gui.start_gui,name='SettingGui',).start() #name of thread is important for scheulder

        while not self.setting_gui.get_close_gui_var(): # wait for tk.var is set
            pass

        self.close_var =self.setting_gui.get_close_gui_var()
        
    def _exit(self, *args):
        self.icon.stop()
    def close_setting_gui(self):
        self.close_var.set(True) # check _open_settings
    
    def update_tray(self):
        self.icon.title = self._title()

    def start_tray(self):
        self.icon = pystray.Icon(name='Workout-Reminder',
                            icon=self._image(),
                            menu=self._menu(),
                            title=self._title())
        self.icon.run_detached() # run_detached is imp



        

   

if __name__ == "__main__":
    tray = WorkoutTray(next_exercise_time='sunday')
    tray.start_tray()
    print('starting')

    tray.next_exercise_time = 'friday'
