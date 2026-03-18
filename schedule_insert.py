"""
提供排程的方式固定在 9:00 ~ 13:30 分執行 , 每30秒執行一次
第二 單次執行( 13:31 分) 執行一次
套件: schedule
pip install schedule
"""
import schedule 
import time
from datetime import datetime

def run_every_5seconds():
    now = datetime.now().strftime("%H:%M:%S")
    print(f"每 5秒執行一次, 觸發時間: {now}")

# 隨機在 5~15 秒之間執行一次，直到 15:59 結束
schedule.every(5).to(15).seconds.do(run_every_5seconds).until("15:59")

while True:
    schedule.run_pending()
    time.sleep(1)
