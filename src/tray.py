import pystray
import threading,time,tkinter as tk
from pystray import Menu, MenuItem, Icon
from PIL import Image
from src.Gui.Exercise_setting_Gui import SettingGuiStandalone




class WorkoutTray:
    
    def __init__(self, next_exercise_time=None, ):
        self.next_exercise_time = next_exercise_time
        # add any var here and in _new_tray to update when the var is changed 

    def _title(self) -> str:
        return "Workout Reminder\n" + "next exercise on: " + self.next_exercise_time

    def _menu(self)-> Menu:
        return Menu(MenuItem("Settings", self._open_settings),
                    # MenuItem("Exit", self._exit) # If you want to exit, then why use in the first place?
                    )

    def _image(self, ):    
        return Image.open("resources\icons\gui icon\pawn with balance.png")

    def _tray_icon(self):

        return pystray.Icon(name='Workout-Reminder',
                            icon=self._image(),
                            menu=self._menu(),
                            title=self._title())


        

    def _new_tray(self, icon):
        icon.visible = True
        icon.title = self._title()
        # icon.menu = self._menu()
        # 
    def _open_settings(self, icon, item):

        self.setting_gui = SettingGuiStandalone()
        threading.Thread(target=self.setting_gui.start_gui,name='SettingGui',).start() #name of thread is important for scheulder

        while not self.setting_gui.get_close_gui_var(): # wait for tk.var is set
            pass

        self.close_var =self.setting_gui.get_close_gui_var()
        
    def _exit(self, icon, item):
        icon.stop()
    
    def start_tray(self):
        icon = self._tray_icon()
        # not auto updating if I don't setup i.e callable in icon.run_detached
        # icon.run_detached(setup=self._new_tray)
        threading.Thread(target=icon.run_detached,args=(self._new_tray,)).start() #to avoid any errors with gui mainloop
    def close_setting_gui(self):
        self.close_var.set(True)


        

   

if __name__ == "__main__":
    tray = WorkoutTray(next_exercise_time='sunday')
    tray.start_tray()
    print('starting')
    
    tray.next_exercise_time = 'monday'
