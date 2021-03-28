import datetime
import requests
import json
import tushare as ts
from Status.logList import log


def getCurrentData_torxiong(code):
    URL = "https://api.doctorxiong.club/v1/stock/min"
    params = {
        'code': code
    }
    try:
        res = requests.get(URL, params=params)
        data = json.loads(res.text)
        # log.update('（Update）: 当前{}价格为{}元'.format(data["data"]["name"], data["data"]["price"]))
        return data["data"]
    except:
        log.update('（Update）: 数据获取失败 {}'.format(URL))
        return False
    # print(res.request.url)
    # res.raise_for_status()
    # print(res.text)
    # return res.text


def getCurrentData_sina(stock_id_list):
    # 上证指数： http://hq.sinajs.cn/list=s_sh000001
    # 深圳成指： http://hq.sinajs.cn/list=s_sz399001
    # http://hq.sinajs.cn/list=sz002307,sh600928
    URL = "http://hq.sinajs.cn/list=sz002307,sh600928"
    r = requests.post(URL)
    print(r.request.url)
    r.raise_for_status()
    print(r.text)


def getMonthData_tushare(stock_id):
    sh = ts.get_hist_data(stock_id)  # 一次性获取全部日k线数据

    i = 0
    dataList = []

    for item in sh.itertuples():
        # print(item)
        dataList.append(item)
        i += 1
        if i > 30:
            break

    jsonData = []

    for data in dataList:
        midDict = {}
        midDict['date'] = data[0]
        midDict['open'] = data[1]
        midDict['high'] = data[2]
        midDict['close'] = data[3]
        midDict['low'] = data[4]
        midDict['volume'] = data[5]
        midDict['price_change'] = data[6]
        midDict['p_change'] = data[7]
        midDict['ma5'] = data[8]
        midDict['ma10'] = data[9]
        midDict['ma20'] = data[10]
        midDict['v_ma5'] = data[11]
        midDict['v_ma10'] = data[12]
        midDict['v_ma20'] = data[13]
        jsonData.append(midDict)

    TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #log()
    return jsonData
