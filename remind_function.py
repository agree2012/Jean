from slackclient import SlackClient
import os
import secinfo
import jenkins
from multiprocessing import Process
import threading
import schedule
from datetime import datetime, date, time
import cgi, re
import time
import datetime
import ast
import sys
import sched, time
import select_date_time
from select_date_time import selection_username, selection_eventname, int_date, int_time, selection_chan
from onetime_remind import  timer_sched, now_and_need_time
import everyday_remind
import verify
import jean_ask

token = secinfo.API_Token
sc = SlackClient(token)
s = sched.scheduler(time.time, time.sleep)

def event_sched_print(event):
    event = int(event)
    print(selection_chan(event))
    if(selection_username(event) != 'Void') and (selection_eventname(event) != 'Void') and (selection_chan(event) != 'Void'):
            if 'channel' in selection_username(event) :
                text = '<!channel>, you asked to remind about ' +  selection_eventname(event)
                sc.api_call('chat.postMessage', as_user='true:', channel=selection_chan(event), text=(text))
            elif '@' in selection_username(event) :
                text = '<' + selection_username(event) + '>, you asked to remind about ' +  selection_eventname(event)
                sc.api_call('chat.postMessage', as_user='true:', channel=selection_chan(event), text=(text))
            else :
                text = selection_username(event) + ', you asked to remind about ' +  selection_eventname(event)
                sc.api_call('chat.postMessage', as_user='true:', channel=selection_chan(event), text=(text))

def clear_shedule():
    schedule.clear()

def refresh_remind():
    clear_shedule()
    text = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
    for i in range(0,len(text)):
        if (len(text[i]) != 1) and (len(text[i]) != 2):
            everyday_remind.every_remind(i)

def datetime_now():
    date_now = str(datetime.datetime.now().date())
    date_now = date_now[0:10]
    (year_now,month_now, day_now) = date_now.split('-')
    date_now = [int(year_now),int(month_now),int(day_now)]
    time_now = str(datetime.datetime.now().time())
    time_now = time_now[0:8]
    (hour_now, minute_now,seconds_now) = time_now.split(':')
    time_now = [int(hour_now),int(minute_now),int(seconds_now)]
    return date_now, time_now

def delete_last_remind():
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
    for i in range(0,len(f)):
        if not 'every' in f[i]:
            if (len(f[i])!= 1) and (len(f[i])!=2):
                if datetime_now()[0][0] > int_date(i)[0]:
                    f[i] = ''+'\n'
                elif (datetime_now()[0][1] >int_date(i)[1]) and (datetime_now()[0][0] == int_date(i)[0]):
                    f[i] = ''+'\n'
                elif (datetime_now()[0][2] > int_date(i)[2]) and (datetime_now()[0][1] == int_date(i)[1]) and (datetime_now()[0][0] == int_date(i)[0]):
                    f[i] = ''+'\n'
                elif (datetime_now()[1][0] > int_time(i)[0]) and (datetime_now()[0][2] == int_date(i)[2]) \
                    and (datetime_now()[0][1] == int_date(i)[1]) and (datetime_now()[0][0] == int_date(i)[0]):
                    f[i] = ''+'\n'
                elif (datetime_now()[1][1] > int_time(i)[1]) and (datetime_now()[1][0] == int_time(i)[0]) and (datetime_now()[0][2] == int_date(i)[2])\
                    and (datetime_now()[0][1] == int_date(i)[1]) and (datetime_now()[0][0] == int_date(i)[0]):
                    f[i] = ''+'\n'
    fw = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt','w')
    fw = fw.writelines(f)

def remind_new():
    delete_last_remind()
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
    for i in range(0,len(f)):
        if  not 'every' in f[i]:
            if len(f[i]) > 2:
                if (datetime_now()[0][2] == int_date(i)[2]) and (datetime_now()[0][1] == int_date(i)[1]) \
                    and (datetime_now()[0][0] == int_date(i)[0]) and (datetime_now()[1][1] == int_time(i)[1]) \
                    and (datetime_now()[1][0] == int_time(i)[0]):
                    event_sched_print(i)
        else:
            refresh_remind()
            shed_date_final()

def shed_date_final():
    schedule.every(60).seconds.do(remind_new)
