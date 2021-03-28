from threading import Thread
from Scheduler.dailyMission import timing
from Status.logList import log
from Status.updateStatus import state_json_data
import time

start_time = time.time()
log.update("（主进程）：交易系统初始化成功")

tracking_stock_code = state_json_data['optional_list']['ID']
log.update("（主进程）：ID:{} 加入跟踪池".format(tracking_stock_code))

# 创建 Thread 实例
log.update("（主进程）：预挂载 --> 巡航模块Scheduler.dailyMission")
thread_daily = Thread(target=timing(tracking_stock_code))

# 启动线程运行
log.update("（主进程）：挂载巡航模块 --> 子线程 （成功：用时{}s）".format(time.time() - start_time))
thread_daily.start()

# 等待所有线程执行完毕
thread_daily.join()  # join() 等待线程终止，要不然一直挂起