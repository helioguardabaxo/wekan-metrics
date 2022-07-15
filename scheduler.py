import cumulativeflowdiagram
import schedule
import datetime
import time   

# Schedules
boardId = 'fC64YwSb7Ry4YrvNt'
schedule.every(60).seconds.do(cumulativeflowdiagram.job)
# schedule.every().day.at("00:10").do(job)

# schedule.every(70).seconds.do(plot_cfd)
# schedule.every().day.at("00:12").do(plot_cfd)


while True:
    schedule.run_pending()
    time.sleep(1)