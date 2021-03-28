import datetime

from Status.logList import log
from Status.updateStatus import state_json_data


def analysis(stock):
    '''torxiong Form Data Analysis'''

    result = ''
    email_title = ''
    email_html = ''
    TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json_status = state_json_data["optional_list"]
    # "ID": 600352,
    # "cost_price": 17.61,
    # "loss_limit": 0.05,
    # "profit_limit": 0.05,
    # "volume": 2000000,
    # "time_out": 90
    profit_limit = float(json_status["profit_limit"])
    loss_limit = float(json_status["loss_limit"])
    volume_limit = float(json_status["volume"])

    # 'code': 'sh600352',
    # 'name': '浙江龙盛',
    # 'type': 'GP-A',
    # 'priceChange': '1.60',
    # 'changePercent': '9.99',
    # 'open': '15.85',
    # 'close': '16.01',
    # 'price': '17.61',
    # 'high': '17.61',
    # 'low': '15.79',
    # 'volume': '1992987',
    # 'turnover': '337149',
    # 'turnoverRate': '6.13',
    # 'totalWorth': '572.91',
    # 'circulationWorth': '572.91',
    # 'date': '2021-02-10 15:40:55',
    # 'buy': [ ··· ]
    # 'sell': [ ··· ]
    # 'minData': [ [ ··· ], [ ··· ], [ ··· ] ]

    name = stock["name"]
    changePercent = float(stock["changePercent"])
    volume = float(stock["volume"])

    # TODO 上涨到止盈位警告
    if changePercent > profit_limit and profit_limit:
        result = "告警\n当前{}上涨{}%\n{}".format(name, changePercent, TIME)

    # TODO 下跌到止损位警告
    elif changePercent < loss_limit and loss_limit:
        result = "告警\n当前{}下跌{}%\n{}".format(name, changePercent, TIME)

    # TODO 成交量突破
    elif volume > volume_limit and volume_limit:
        result = "当前{}成交额\n已达到{}股\n{}".format(name, volume, TIME)
        # email_title = "{}成交额{}股".format(name, volume)
        # email_html = "<h2>{}</h2>已达交易预警" \
        #              "<h1>当前成交额{}股</h1>" \
        #              "<p>{}</p>".format(name, volume, TIME)

    return result