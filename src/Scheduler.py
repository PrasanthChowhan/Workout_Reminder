import schedule
import time
from src.Gui.Gui_Main import NotificationGui
from src.DbManager import DbManager,ConfigReader
from src.utils.constants import DatabaseConstants

# NOTE: Run Gui on main thread or else it will throw errors
def schedule_gui():
    exercise = DbManager().give_me_a_exercise()
    # print('exercise in scheduling gui: \t', exercise, '\n')
    root = NotificationGui(exercise_dict=exercise)
    root.mainloop()


if __name__ == '__main__':

    schedule.every().second.do(schedule_gui)
    configuration = ConfigReader(DatabaseConstants.SETTINGS_YAML_PATH).read_config_file()
    schedule_after = int(configuration['schedule'])*60 # sleep is in seconds and interval is in min
    while True:
        schedule.run_pending()
        time.sleep(schedule_after)
