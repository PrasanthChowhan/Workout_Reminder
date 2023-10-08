
import tkinter as tk
import schedule,threading
import time
from src.Gui.Gui_Main import NotificationGui
from DbManager import DbManager
# NOTE: Run Gui on main thread or else it will throw errors




   
   
    

def schedule_gui():
    exercise = DbManager().give_me_a_exercise()
    print('exercise in scheduling gui: \t',exercise, '\n')
    root = NotificationGui(exercise_dict=exercise)
    root.mainloop()
    print('rooot is exited')

if __name__ == '__main__':

    schedule.every().second.do(schedule_gui)
    while True:
        schedule.run_pending()
        time.sleep(1)


