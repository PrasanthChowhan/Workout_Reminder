import threading,tkinter as tk
import schedule
import time
from tk_Vertical_notification import VerticalGui
# NOTE: Run Gui on main thread or else it will throw an errors
def show():
    a=VerticalGui()
    
def schedule_gui():
    root = VerticalGui()
    print(time.ctime())
    # new_thread = threading.Thread(target=show)

    # new_thread.start()
    root.mainloop()

# new_thread.start()
# new_thread.join()
# print('Gui just exited')

if __name__ == '__main__':

    schedule.every().second.do(schedule_gui)
    while True:
        schedule.run_pending()
        time.sleep(10)

# def my_scheduled_task():
#     print("Scheduled task executed: ", time.ctime())
#     # NotificationGui()

# def run_scheduled_task():
#     while True:
#         schedule.run_pending()
#         time.sleep(5)  # Adjust the sleep interval as needed (e.g., longer for lower CPU usage)

# # Create a thread for running the scheduled task
# scheduled_task_thread = threading.Thread(target=run_scheduled_task)

# # Set the thread as a daemon (so it exits when the main program finishes)
# scheduled_task_thread.daemon = True

# # Start the thread
# scheduled_task_thread.start()

# schedule.every().second.do(my_scheduled_task)

# try:
#     # Continue running the main program concurrently with scheduled tasks
#     while True:
#         # Your main program logic here
#         time.sleep(1)  # Adjust the sleep interval for main program as needed

# except KeyboardInterrupt:
#     # Gracefully handle program exit (cleanup and stopping threads if necessary)
#     pass

# # Optionally, wait for the scheduled task thread to finish (if it needs cleanup)
# scheduled_task_thread.join()