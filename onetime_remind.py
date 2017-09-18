import os
from multiprocessing import Process
import schedule
from datetime import datetime, date, time
import cgi, re
import time
import datetime
import ast
import sys
import sched, time
from select_date_time import int_date, str_date, int_time, str_time

def count_day(month):
    if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        counts_day = 31;
    elif month == 2:
        counts_day = 28
    else:
        counts_day = 30
    return counts_day

def now_and_need_time(i):
    need_time = datetime.time(int_time(i)[0],int_time(i)[1])
    _time_now = str(datetime.datetime.now().time())
    _time_now = _time_now[0:8]
    (hour_now, minute_now, second_now) = _time_now.split(':')
    _time_need = str(need_time)
    (hour_need, minute_need, second_need) = _time_need.split(':')
    _time_need = [hour_need, minute_need, second_need]
    _time_now = [hour_now, minute_now, second_now]
    return _time_need, _time_now

def now_and_need_date(i):
    now_date = str(datetime.datetime.now().date())
    now_date = now_date[0:10]
    (year_now, month_now, day_now) = now_date.split('-')
    now_date = [int(year_now),int(month_now),int(day_now)]
    need_date = date(int_date(i)[0],int_date(i)[1],int_date(i)[2])
    need_date = str(need_date)
    need_date = need_date[0:10]
    (year_need, month_need, day_need) = need_date.split('-')
    need_date = [int(year_need),int(month_need),int(day_need)]
    return need_date, now_date

def seconds_today_and_need_day(i):
    seconds_now = int(now_and_need_time(i)[1][0]) * 3600 + int(now_and_need_time(i)[1][1]) \
                                                * 60 + int(now_and_need_time(i)[1][2])
    seconds_need = int(now_and_need_time(i)[0][0]) * 3600 + int(now_and_need_time(i)[0][1]) * 60
    return 86400 - seconds_now + seconds_need

def seconds_allday(i):
    month_now = now_and_need_date(i)[0][1]
    month_need = now_and_need_date(i)[1][1]
    day_now = now_and_need_date(i)[0][2]
    day_need = now_and_need_date(i)[1][2]
    m = month_need - month_now
    if m == 0:
        seconds_all = (day_need - day_now - 1) * 86400
    elif m == 1:
        seconds_all = (count_day(month_now) - day_now) * 86400 + day_need * 86400
    elif m < 0:
        print("ZNACHIT NAPOMINALKA USTARELA EE NADO UDALIT")
    else:
        counts_day = 0
        while (m != 1):
            counts_day = counts_day + count_day(month_now + 1)
            m = m - 1
        seconds_month = counts_day * 86400
        seconds_day = (count_day(month_now) - day_now * 86400) + day_need * 86400
        seconds_all = seconds_day + seconds_month
    return seconds_all


def timer_sched(i):
    return seconds_allday(i) + seconds_today_and_need_day(i)
