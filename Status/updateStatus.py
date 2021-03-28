import json # 导入json头文件
from Status.logList import log

class Status:

    def __init__(self):
        self.status = {}
        self.json_path = 'Status/status.json'  # json原文件
        log.update('（Status）: Status.updateStatus')

    def load(self): # 获取json里面数据
        with open(self.json_path,'rb')as state_json_file: # 定义为只读模型，并定义名称为f
            self.status= json.load(state_json_file) # 加载json文件中的内容,保存在dict中
            state_json_file.close() # 关闭json读模式
        log.update('（Status）: JSON数据读取成功')
        return self.status # 返回dict字典内容

    def save(self): # 写入json文件
        with open(self.json_path,'w')as state_json_file: # 定义为写模式，名称定义为r
            json.dump(self.status, state_json_file,indent = 2)  #indent控制间隔, 将dict写入名称为r的文件中
            state_json_file.close() # 关闭json写模式
        log.update('（Status）: JSON数据写入成功')
        return 'Save Done'

DataState = Status()
state_json_data = DataState.load()
log.update("（主进程）：Settings配置导入完成")