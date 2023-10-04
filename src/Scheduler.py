import threading,tkinter as tk
import schedule
import time
from tk_notification_gui import NotificationGui
from DbManager import DbManager
# NOTE: Run Gui on main thread or else it will throw errors

    
def schedule_gui():
    exercise = DbManager('data\settings.yaml', 'data\exercise_database.sqlite').give_me_a_exercise()
    print(exercise)
    root = NotificationGui(exercise_dict=exercise)
    print(time.ctime())
   
    root.mainloop()



if __name__ == '__main__':

    schedule.every().second.do(schedule_gui)
    while True:
        schedule.run_pending()
        time.sleep(1)
