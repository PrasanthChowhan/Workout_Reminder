import schedule
import time, threading,sys
from src.Gui.Gui_Main import NotificationGui
from src.DbManager import DbManager,ConfigReader
from src.utils.constants import DatabaseConstants
from src.Gui.tray import WorkoutTray
from datetime import datetime, timedelta
import sys


class Scheduler:
    def __init__(self):
        self.continue_scheduling_var = True
    def _add_minutes_to_current_time(self,minutes_to_add):
        # Get the current time
        current_time = datetime.now()

        # Calculate the new time by adding the minutes
        new_time = current_time + timedelta(minutes=minutes_to_add)

        # Format and return the new time in "H:M" format
        formatted_time = new_time.strftime("%H:%M")
        
        return formatted_time

    def _is_thread_exists(self,thread_name):    
        for thread in threading.enumerate():            
            if thread.name == thread_name:            
                return True
    
    def _schedule_gui(self,):
        exercise = DbManager().give_me_a_exercise()
        # print('exercise in scheduling gui: \t', exercise, '\n')    
        self.root = NotificationGui(exercise_dict=exercise,stop_scheduling_callabck=self.stop_scheduling)
        self.root.mainloop()
    # NOTE: Run Gui on main thread or else it will throw errors

    def start_scheduling(self):
        schedule.every().second.do(self._schedule_gui)
        self.tray = WorkoutTray(next_exercise_time='',stop_scheduling_callabck=self.stop_scheduling)
        self.tray.start_tray()
        
        
        while self.continue_scheduling_var:
            try:
                configuration = ConfigReader.read_config_file(DatabaseConstants.SETTINGS_YAML_PATH,default_file=DatabaseConstants.DEFUALT_SETTINGS_YAML_PATH)
                schedule_after = int(configuration['schedule'])
                self.tray.next_exercise_time = self._add_minutes_to_current_time(schedule_after)
                
                time.sleep(10) 
                # time.sleep(schedule_after*60) # sleep is in seconds and interval is in min)


                if self._is_thread_exists('SettingGui'): 
                    ## If a thread with SettingGui is running close it as it has its own mainloop which is causing issues
                    self.tray.close_setting_gui() 
                
                if self.continue_scheduling_var:                                   
                    schedule.run_pending()
                
            except Exception as e:
                print('error occured in scheduler', e)             

                break
        print('progamme has quit')
            
    def stop_scheduling(self):
        self.tray._exit()
        self.continue_scheduling_var = False
        


if __name__ == '__main__':
    print('starting scheduler')
    Scheduler().start_scheduling()