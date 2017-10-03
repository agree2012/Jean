
import os
from slackclient import SlackClient
from multiprocessing import Process
import schedule
from datetime import datetime, date, time
import time
import datetime
import ast
import sys
from select_date_time import str_date, str_time
import remind_function 
import secinfo
import  select_date_time
token = secinfo.API_Token
sc = SlackClient(token)
chan=secinfo.channel_id

def every_day_of_week(weekday_today,time,work,i):
    if weekday_today == 0:
        schedule.every().monday.at(time).do(work, i=i)
    elif weekday_today == 1:
        schedule.every().tuesday.at(time).do(work, i=i)
    elif weekday_today == 2:
        schedule.every().wednesday.at(time).do(work, i=i)
    elif weekday_today == 3:
        schedule.every().thursday.at(time).do(work, i=i)
    elif weekday_today == 4:
        schedule.every().friday.at(time).do(work, i=i)
    elif weekday_today == 5:
        schedule.every().saturday.at(time).do(work, i=i)
    elif weekday_today == 6:
        schedule.every().sunday.at(time).do(work, i=i)

def every_remind(i):
    day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    days_event = select_date_time.str_date(i)
    day = ''
    if 'every' in days_event:
        if 'day' in days_event:
            schedule.every().day.at(str_time(i)).do(remind_function.event_sched_print, i)
        else:
            for j in range(0,7):
                if day_of_week[j] in days_event:
                    every_day_of_week(j,str_time(i),remind_function.event_sched_print,i)
