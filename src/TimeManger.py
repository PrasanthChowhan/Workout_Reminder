import time, threading,schedule
from NotificationGui import NotificationGui

class TimeManager:
    def __init__(self):
        pass

    def run_this(self,func):
        t1 = threading.Thread(target=func)
        t1.start()
        t1.join()
        while True:
            print(time.ctime())
            time.sleep(1)

if __name__ == "__main__":
    tm = TimeManager()
    tm.run_this(NotificationGui)


    