import time
import datetime

from Status.logList import log
from Message.sendEmail import send_email
from Message.sendMessage import send_message
from Scheduler.dataAnalysis import analysis
from Update.getData import getCurrentData_torxiong


def getTime():
    # time.localtime(time.time())
    # int tm_sec; /* 秒 – 取值区间为[0,59] */
    # int tm_min; /* 分 - 取值区间为[0,59] */
    # int tm_hour; /* 时 - 取值区间为[0,23] */
    # int tm_mday; /* 一个月中的日期 - 取值区间为[1,31] */
    # int tm_mon; /* 月份（从一月开始，0代表一月） - 取值区间为[0,11] */
    # int tm_year; /* 年份，其值等于实际年份减去1900 */
    # int tm_wday; /* 星期 – 取值区间为[0,6]，其中0代表星期一，1代表星期二，以此类推 */
    # int tm_yday; /* 从每年的1月1日开始的天数 – 取值区间为[0,365]，其中0代表1月1日，1代表1月2日，以此类推 */
    # int tm_isdst; /* 夏令时标识符，实行夏令时的时候，tm_isdst为正。不实行夏令时的时候，tm_isdst为0；不了解情况时，tm_isdst()为负。
    return time.localtime(time.time())

def dormancy(to_time):
    pass

def min_sleep(startTime, endTime):
    '''计算两个时间点之间的分钟数'''
    # 处理格式,加上秒位
    startTime1 = startTime + ':00'
    endTime1 = endTime + ':00'
    # 计算分钟数
    startTime2 = datetime.datetime.strptime(startTime1, "%Y-%m-%d %H:%M:%S")
    endTime2 = datetime.datetime.strptime(endTime1, "%Y-%m-%d %H:%M:%S")
    seconds = (endTime2 - startTime2).seconds
    # 来获取时间差中的秒数。注意，seconds获得的秒只是时间差中的小时、分钟和秒部分的和，并没有包含时间差的天数（既是两个时间点不是同一天，失效）
    total_seconds = (endTime2 - startTime2).total_seconds()
    # 来获取准确的时间差，并将时间差转换为秒
    # print(total_seconds)
    # mins = total_seconds / 60
    log.update("（子线程：巡航模块）：即将休眠，将于{}重新工作".format(endTime2))
    time.sleep(total_seconds)
    return True
    # return int(mins)

    # if __name__ == "__main__":
    #     startTime_1 = '2019-07-28 00:00'
    #     endTime_1 = '2019-07-29 00:00'
    #     fenNum = minNums(startTime_1, endTime_1)
    #     print(fenNum)

def time_in_work():
    '''判断当前时间是否开市'''
    # 范围时间
    morning_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
    morning_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')
    afternoon_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:00', '%Y-%m-%d%H:%M')
    afternoon_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    # 当前时间
    now_time = datetime.datetime.now()

    # 判断当前时间是否在范围时间内
    if morning_end_time > now_time > morning_start_time:
        return True
    elif afternoon_end_time > now_time > afternoon_start_time:
        return True
    elif afternoon_start_time > now_time > morning_end_time:
        return "REST"
    else:
        return False


def daily_tracking(stock_code, mins): # 股票代码与获取数据频率
    now = time.localtime(time.time())
    log.update("（子线程：巡航模块）：今日任务初始化成功")
    if now.tm_wday - 1 < 5: # 如果是工作日
        log.update("（子线程：巡航模块）：当前为工作日")
        if time_in_work() == "REST": # 午休时间
            log.update("（子线程：巡航模块）：当前已到午休时间")
            now_str_time = "{}-{}-{} {}:{}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            end_time = "{}-{}-{} 13:00".format(now.tm_year, now.tm_mon, now.tm_mday)
            min_sleep(now_str_time, end_time)
        elif time_in_work(): # 开市时间
            log.update("（子线程：巡航模块）：当前为正常交易时间")
            log.update("（子线程：巡航模块）：启用数据获取模块Update.getData与数据分析模块Scheduler.dataAnalyse")
            log.update("（子线程：巡航模块）：当前持续监测中，数据获取频率：{}分钟/次".format(mins))
            while time_in_work():
                data = getCurrentData_torxiong(stock_code)
                analysis_result = analysis(data)
                if analysis_result:
                    send_message(analysis_result)
                # if email_title:
                #     send_email(email_title, email_html)
                time.sleep(60 * mins) # 暂时休眠5分钟
        elif now.tm_hour > 15: # 午休未开市
            log.update("（子线程：巡航模块）：结束休眠，正在等待开盘")
            time.sleep(60 * 5) 
        elif now.tm_hour < 9: # 今天未开市
            log.update("（子线程：巡航模块）：等待开市")
            now_str_time = "{}-{}-{} {}:{}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            end_time = "{}-{}-{} 9:30".format(now.tm_year, now.tm_mon, now.tm_mday)
            min_sleep(now_str_time, end_time)
        else: # 今天已休市
            log.update("（子线程：巡航模块）：已休市")
            now_str_time = "{}-{}-{} {}:{}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            end_time = "{}-{}-{} 9:30".format(now.tm_year, now.tm_mon, now.tm_mday+1)
            min_sleep(now_str_time, end_time)
    else: # 周末
        log.update("（子线程：巡航模块）：今日为周六")
        if now.tm_wday == 5: # 周六
            now_str_time = "{}-{}-{} {}:{}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            end_time = "{}-{}-{} 9:30".format(now.tm_year, now.tm_mon, now.tm_mday+2)
            min_sleep(now_str_time, end_time)
        if now.tm_wday == 6: # 周日
            log.update("（子线程：巡航模块）：今日为周五")
            now_str_time = "{}-{}-{} {}:{}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            end_time = "{}-{}-{} 9:30".format(now.tm_year, now.tm_mon, now.tm_mday+1)
            min_sleep(now_str_time, end_time)




def timing(stock_code):
    while True:
        daily_tracking(stock_code, 5)
