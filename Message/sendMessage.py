import requests
import json

from Status.logList import log


def send_message(message):
    try:
        URL = "http://192.168.1.68:2333/v1/LuaApiCaller"
        params = {
            'qq': 2782594859,  #bot的QQ
            'funcname':'SendMsgV2', #调用方法类型
            }
        body = {
            "ToUserUid":1462648167,
            "SendToType":1,
            "SendMsgType":"TextMsg",
            "Content":message
            }

        r = requests.post(URL, params = params, data=json.dumps(body))
        log.update("（Message）：{}".format(message.replace("\n", " ")))
        return True
        # print(r.request.url)
        # r.raise_for_status()
        # print(r.text)
    except:
        log.update("（Message）：ERROR 数据发送失败")
        return False

