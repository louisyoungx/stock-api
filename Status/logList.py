import datetime

class Log():

    def __init__(self):
        self.log_data = []

    def update(self, log_message):
        TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = "[{}] {}".format(TIME, log_message)
        print(log_message)
        self.log_data.append(log_message)
        if len(self.log_data) > 30:
            self.log_data.pop()

log = Log()
log.update("（主进程）：Log模块加载完成")
