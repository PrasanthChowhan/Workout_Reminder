
import tkinter as tk
import schedule
import time
from tk_notification_gui import NotificationGui
from DbManager import DbManager
# NOTE: Run Gui on main thread or else it will throw errors


def schedule_gui():
    exercise = DbManager().give_me_a_exercise()
    root = NotificationGui(exercise_dict=exercise)
    root.mainloop()


if __name__ == '__main__':

    schedule.every().second.do(schedule_gui)
    while True:
        schedule.run_pending()
        time.sleep(1)
