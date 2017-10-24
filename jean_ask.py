from slackclient import SlackClient
import os
import jenkins
import secinfo
import trainToGoogleDoc
from multiprocessing import Process
import threading
import schedule
from datetime import datetime, date, time
import cgi, re
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime
import create_table
import ast
import sys
import sched, time
import remind_function
import funcion_bot_General
import select_date_time
from select_date_time import weekday_today
from onetime_remind import count_day
import verify
import onetime_remind
import select_date_time
token = secinfo.API_Token
sc = SlackClient(token)
s = sched.scheduler(time.time, time.sleep)

def define_chan():
    chan_string = open('lol.txt').read()
    if chan_string != '':
        chan = ''
        for i in range(0,9):
            chan = chan + chan_string[i]
        return chan


def check_hi():
    word2 = 'hi, Yes i ready'
    verify = 0
    data = open('lol.txt').read()
    if word2 in data:
         funcion_bot_General.connect('2.txt')
         while(what_you_do() != 1):
             what_you_do()

def what_you_do():
    word2 = 'today i do'
    data = open('2.txt').read()
    if word2 in data:
        print('lol')
        return 1

def connect(file):
    f = open(file, 'a')
    userlist = open('userslist.txt').readlines()
    sc.rtm_connect()
    input= sc.rtm_read()
    if input:
        for action in input:
            for i in range(0,len(userlist)):
                if 'user' in action:
                    if action['user'] != 'U642G4JGJ':
                        if 'type' in action and action['type'] == "message" :
                            username = action['user']
                            report = action['text']
                            channel = action['channel']
                            report = str(channel) + ' ' + report
                            if '@me' in report:
                                report = report.replace('@me','<@'+ username + '>')
                            if ('@all' in report):
                                report = report.replace('@all','<!@channel>')
                            f.write(report + '\n')
                            #f.write(report.encode('utf-8') + '\n')
                            f.close

def connecting():
    #connect('lol.txt')
    text = open('lol.txt').read()
    return text

def dialog(chan):
    num = 0
    text = connecting()
    while(num == 0):
        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='You have a time to talk about god?')
        num = 1
    while(num == 1):
        if (('Yes i ready' in text) and (define_chan() == chan) and (num == 1)):
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='What you do today?')
            funcion_bot_General.clear_text()
            num = 2
        else :
            text = connecting()
    while(num == 2):
        text = connecting()
        if('Today i ' in text) and (num == 2)  and (define_chan() == chan):
            i_do = text
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='What you plain do tommorow')
            funcion_bot_General.clear_text()
            num =3
        else :
            text = connecting()
    while(num == 3):
        if('Tommorow i ' in text) and (num == 3)  and (define_chan() == chan):
            i_will_be_do = text
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Which more information you want to retrive')
            funcion_bot_General.clear_text()
            num = 4
        else :
            text = connecting()
    while(num == 4):
        text = connecting()
        if('Anything i' in text) and (num == 4) and (define_chan() == chan):
            anyting = text
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Okay thank you')
            funcion_bot_General.clear_text()
            num = 5
            fr = open('do_list.txt').read()
            fw = open('do_list.txt', 'a')
            if ((not i_do in fr) and (not i_will_be_do in fr) and (not anyting in fr)):
                fw = fw.write(i_do + i_will_be_do + anyting)
                return 1
            else:
                text = connecting()

def request_work(chan):
    while(dialog(chan) != 1):
        a=1

def delete_user_ask(chan):
    fr=open('do_list.txt').readlines()
    for i in range(0,len(fr)):
        if chan in fr[i]:
            fr[i] =''
            fw = open('do_list.txt','w')
            fw = fw.writelines(fr)





def change_my_answer(chan):
    time_now = str(datetime.datetime.now().time())
    time_now = time_now[0:8]
    (hour_now, minute_now, seconds_now) = time_now.split(':')
    time_now = [int(hour_now), int(minute_now), int(seconds_now)]
    if ((int(hour_now)) > 8) and ((int(hour_now)) < 11):
        delete_user_ask(chan)
        request_work(chan)
    else:
        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Sorry but result already send')


def ask_about_work():
    time_now = str(datetime.datetime.now().time())
    time_now = time_now[0:8]
    (hour_now, minute_now, seconds_now) = time_now.split(':')
    time_now = [int(hour_now), int(minute_now), int(seconds_now)]
    if(((int(hour_now)) == 12) and ((int(minute_now)) == 50) and ((int(seconds_now))==0)):
        for i in range(0,len(secinfo.channel_list)):
            t1 = threading.Thread(target=request_work, args=(secinfo.channel_list[i],))
            t1.start()


def clear_dolist():
    f = open('do_list.txt','w')
    f.close()

def shedule_clear_dolist():
    schedule.every().day.at("11:14").do(clear_dolist)

def call_about_results(request,chan):
    request = request['spreadsheetId']
    finalUrl = 'https://docs.google.com/spreadsheets/d/' + str(request)+'/edit#gid=0'
    sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=finalUrl + '. There you can see resault of ask.')

def write_in_form():
    request = trainToGoogleDoc.create_table(create_table.get_date(),create_table.get_row()/3+1)
    for i in range(2,create_table.get_row(),3):
           trainToGoogleDoc.write_his_answer(request,create_table.get_date(),create_table.get_range((i/3)+1),create_table.get_username(i),create_table.get_do_today(i),create_table.going_to_do_tommorow(i), create_table.get_anything(i))
    call_about_results(request,'D63CABG6L')

def shedule_write():
    schedule.every().day.at("12:22").do(write_in_form)
