import pystray
import threading
from pystray import Menu, MenuItem, Icon
from PIL import Image
from src.Gui.Exercise_setting_Gui import SettingGuiStandalone
# setter concept is used


class WorkoutTray:
    def __init__(self, next_exercise_time=None, ):
        self.next_exercise_time = next_exercise_time


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

    def start_tray(self):
        icon = self._tray_icon()
        # not auto updating if I don't setup i.e callable in icon.run_detached
        threading.Thread(target=icon.run_detached,args=(self._new_tray,)).start() #to avoid any errors with gui mainloop

    def _new_tray(self, icon):
        icon.visible = True
        icon.title = self._title()
        # icon.menu = self._menu() 
    def _open_settings(self, icon, item):
        threading.Thread(target=SettingGuiStandalone).start()

    def _exit(self, icon, item):
        icon.stop()
   

if __name__ == "__main__":
    tray = WorkoutTray(next_exercise_time='sunday')
    tray.start_tray()
    # tray.next_exercise_time = 'monday'
