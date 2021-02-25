# -*- coding:utf-8 -*-
import time
import datetime


def time_guard(target_time, time_delta=5):
    """
    按照给定时间等待
    :param target_time: 目标等待时间 "%Y-%m-%d %H:%M:%S" 或者 时间间隔 s
    :param time_delta: 时间误差容忍， 默认5秒
    :return:
    """
    if isinstance(target_time, int):
        time.sleep(target_time)
        return
    else:
        tuple_time = time.strptime(target_time, "%Y-%m-%d %H:%M:%S")
        target_timestamp = time.mktime(tuple_time)
        while True:
            current_timestamp = time.time()
            if target_timestamp - current_timestamp > 0:
                time.sleep(target_timestamp - current_timestamp)
            elif current_timestamp - target_timestamp > time_delta:
                raise TimeoutError
            else:
                return


def format_dayrange(start_day=datetime.datetime.now(), day_diff=7, start_fmt="%m月%d日", end_fmt="%m月%d日", sep=" - "):

    end_day = start_day + datetime.timedelta(days=day_diff)
    text_fmt = "{start}{sep}{end}"

    return text_fmt.format(start=start_day.strftime(start_fmt), sep=sep, end=end_day.strftime(end_fmt))


def get_next_month_and_itself_year(obj):

    year = obj.year
    month = obj.month + 1
    if month > datetime.datetime.max.month:
        year = year + 1
        month = month - datetime.datetime.max.month
    return (year, month)
