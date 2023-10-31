import schedule
import time,threading,logging

from src.Gui.Gui_Main import NotificationGui
from src.DbManager import DbManager,ConfigReader
from src.utils.constants import DatabaseConstants
from tray import WorkoutTray
from datetime import datetime, timedelta

def schedule_gui():
    exercise = DbManager().give_me_a_exercise()
    # print('exercise in scheduling gui: \t', exercise, '\n')    
    root = NotificationGui(exercise_dict=exercise)
    root.mainloop()
# NOTE: Run Gui on main thread or else it will throw errors





def add_minutes_to_current_time(minutes_to_add):
    # Get the current time
    current_time = datetime.now()

    # Calculate the new time by adding the minutes
    new_time = current_time + timedelta(minutes=minutes_to_add)

    # Format and return the new time in "H:M" format
    formatted_time = new_time.strftime("%H:%M")
    
    return formatted_time

def is_thread_exists(thread_name):    
    for thread in threading.enumerate():
        
        if thread.name == thread_name:            
            return True

# Configure the logging settings
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':

    schedule.every().second.do(schedule_gui)
    tray = WorkoutTray(next_exercise_time='')
    tray.start_tray()

    
    while True:
        try:
            configuration = ConfigReader(DatabaseConstants.SETTINGS_YAML_PATH).read_config_file()
            schedule_after = int(configuration['schedule'])
            tray.next_exercise_time = add_minutes_to_current_time(schedule_after)
            print(add_minutes_to_current_time(schedule_after))
            # time.sleep(5)
            time.sleep(schedule_after*60) # sleep is in seconds and interval is in min)


            if is_thread_exists('SettingGui'): 
                ## If a thread with SettingGui is running close it as it has its own mainloop which is causing issues
                tray.close_setting_gui()
            
            schedule.run_pending()
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            print('error occured in scheduler')
            break
