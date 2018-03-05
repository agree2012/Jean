# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
from slackclient import SlackClient
import os
import secinfo
import jenkins
from datetime import datetime, date, time
import  re
import datetime
import sched, time
import remind_function
import funcion_bot_General
from select_date_time import weekday_today
from onetime_remind import count_day
import verify
import onetime_remind
import select_date_time
token = secinfo.API_Token
sc = SlackClient(token)
s = sched.scheduler(time.time, time.sleep)

def define_username():
    string = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    if string != '':
        username = ''
        for i in range(9,18):
            username = username + string[i]
        return username

def define_chan():
    chan_string = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    if chan_string != '':
        chan = ''
        for i in range(0, 9):
            chan = chan + chan_string[i]
        return chan

def check_status_project(param):
    try:
      server = jenkins.Jenkins('http://jenkins.andersenlab.com', username=secinfo.username, password=secinfo.passowrd)
      next_build_number = server.get_job_info(param)['nextBuildNumber']
      build_number = next_build_number - 1
      build_info = server.get_build_info(param, build_number)
      status = build_info.get('result')
      if status == None:
          status = 'In process, wait the end of build'
      else:
	         status = status.lower() + ', number of build is ' + str(build_number)
    except jenkins.NotFoundException:
        status = 'Name of project is not right'
    return status



def slack_status_build_job(param):
    try:
        server = jenkins.Jenkins('http://jenkins.andersenlab.com', username=secinfo.username, password=secinfo.passowrd)
        next_build_number = server.get_job_info(param)['nextBuildNumber']
        build_number = next_build_number - 1
        build_info = server.get_build_info(param, build_number)
        status = build_info.get('result')
        message = ('final build number is ' + str(build_number)+ ', status this build ' + status)
    except jenkins.NotFoundException:
        message = 'Name of project is not right'
    return message

def slack_build_job_jenkins(param):
    try:
        server = jenkins.Jenkins('http://jenkins.andersenlab.com', username=secinfo.username, password=secinfo.passowrd)
        next_build_number = server.get_job_info(param)['nextBuildNumber']
        build_number = next_build_number - 1
        if(check_status_project(param) != 'In process, wait the end of build'):
            server.build_job(param, parameters=None, token = secinfo.API_Token)
            while(build_number==next_build_number-1):
                next_build_number = server.get_job_info(param)['nextBuildNumber']
        while(check_status_project(param) == 'In process, wait the end of build'):
            time.sleep(1)
        else :
            message = slack_status_build_job(param)
    except jenkins.NotFoundException:
        message = 'Name of project is not right'
    return message


def ping_the_server(hostname):
    if not(('@' in hostname) or (';' in hostname) or ('&' in hostname) or ('|' in hostname)):
        response = os.system("ping " + hostname)
        if response == 0:
            message = 'server is up!'
        else:
           message = 'server is down!'
        return message


def command(text):
    number = 0
    for count in range(0,(len(text))):
        if text[count] == '@' :
            number = count
            command = ''
    for count in range(0,number):
        command += text[count]
    return command

def job(text):
    job = ''
    number = 0
    for count in range(0,(len(text)-1)):
        if text[count] == '@' :
            number = count
            command = ''
    for count in range(number+1,len(text)-1):
        job +=text[count]
    return job

def site_and_job(text):
    job = ''
    site = ''
    p=[]
    num = 0
    number = text.find('it is')
    for i in range(0,number):
        site += text[i]
    for i in range(number+6, len(text)):
        job += text[i]
    p=[site,job]
    return p

def connect(file):
    f = open(file, 'a')
    sc.rtm_connect()
    input= sc.rtm_read()
    if input:
        for action in input:
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
                        #f.write(report + '\n')
                        f.write(report.encode('utf-8') + '\n')
                        f.close
                        return report

def clear_text():
        f=open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt', 'w')
        f.close()

def command_hello():
    word1 = 'hello jean'
    word2 = 'hi jean'
    data = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    if (word1 in data) or (word2 in data) :
        sc.api_call('chat.postMessage', as_user='true:', channel=define_chan(), text='Hello')
        clear_text()

def command_help():
    word = 'jean help'
    data = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    if word in data:
        sc.api_call('chat.postMessage', as_user='true:', channel=define_chan(), \
        text='Use: `Jean, what about status @Projectname` if you want to check status of project. \n\
Example: `Jean, what about status @DevopsTest/online-shopJSFinal` \n\
Use: `Jean, build please @Projectname` if you want to build project. \n\
Example: `Jean, build please @DevopsTest/online-shopJSFinal`       \n\
Use: `Jean, remind/stop_remind @name/me about "event" at time date or day of week` if you want to remind something.\n\
Example: `Jean, remind @me about "Call" at 17:00 tommorow`\n\
Use `Jean, can you please conduct a survey at TIME every DAY OR DAY OF WEEK. Questions is 1) Question? 2) Question? And please ignore: username`\n\
Examle `Jean, can you please conduct a survey at 7:08 every day. Questions is 1) What you doing now? 2) Do you have tasks? And please ignore @mike` \n\
Use `Jean can you please rechange my request a survey at TIME every DAY OR DAY OF WEEK. Questions is 1) Question? 2) Question?`\n\
Example `Jean change my request a survey at 15:57 every day. Questions is 1) What you doing now? 2) Do you have tasks?`\n\
Use `show survey` if you want watch list of survey\n\
Use `Jean delete request: a survey at at TIME every DAY OR DAY OF WEEK. Questions is 1) Question? 2) Question?`\n\
Example: `Jean delete request: a survey at 10:49 every day.  Questions is 1) What you doing now? 2) Do you have tasks? 3) What task will be next? 4) Lolaqq?`\n\
Use: `Jean, watching to @ip_addr it is Name_Project` if you want to watching on server. \n\
Example `Jean, watching to @google.com it is DevopsTest/online-shopJSFinal`')
        clear_text()

def status_project():
    text = ''
    chan = define_chan()
    file1 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').readlines()
    for i in range(0,len(file1)):
        if 'what about' in file1[i]:
            text = file1[i]
            clear_text()
            report = check_status_project(funcion_bot_General.job(text))
            if report != 'Name of project is not right':
                report= 'status is ' + report
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text= report)

def build_project():
    file1 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').readlines()
    text = ''
    chan = define_chan()
    for i in range(0,len(file1)):
        if 'build please' in file1[i]:
            text = file1[i]
            clear_text()
    if(text != ''):
        if check_status_project(job(text)) != 'In process, wait the end of build' :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Build started now!')
        else :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='build already start, please wait!')
        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=slack_build_job_jenkins(funcion_bot_General.job(text)))

def eye_on_server():
    text = ''
    chan = define_chan()
    param = 0
    file1 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').readlines()
    for i in range(0,len(file1)):
        if 'watching to' in file1[i]:
            text = file1[i]
            job = funcion_bot_General.job(text)
            clear_text()
            if (check_status_project(site_and_job(job)[1]) == 'Name of project is not right'):
                 sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Name of project is not right')
            else :
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Ok, i will keep an eye on it')
                while(ping_the_server(site_and_job(job)[0]) != 'server is down!'):
                    for i in range(0,600):
                        file2 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/stop.txt').read()
                        if(file2 != ''):
                            if 'stop it' in file2:
                                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Ok, i end watching on server')
                                #file3 = open('stop.txt', 'w')
                                return True
                        else:
                            time.sleep(0.1)
                else :
                    job_Name = site_and_job(job)[1]
                    build_or_nothing(job_Name,site_and_job(job)[0],chan)
                    clear_text()

#def command_change_answer():
    #word1 = 'Rechange my answer'
    #data = open('lol.txt').read()
    #if (word1 in data):
        #chan = define_chan()
      #  sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Okay rechange your answer')
      #  jean_ask.change_my_answer(chan)
       # clear_text()


def command_stop_watching():
    number = 0
    data = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    file_stop = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/stop.txt', 'w')
    if(data != ''):
        if 'stop watching' in data:
            text = 'stop it'
            file_stop = file_stop.write(text)
            clear_text()

def build_or_nothing(job, server,chan):
    if(check_status_project(job) != 'In process, wait the end of build') :
        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='I can`t reach ' + server + ', but it`s not building, maybe i need to rebuild it?')
        while(command_yes(job,chan) != 2):
            command_yes(job,chan)

def command_yes(job,chan):
    number = 0
    data = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    if(data != ''):
        if 'yes' in data:
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Build is started')
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=slack_build_job_jenkins(job))
            clear_text()
            number = 2
            return number
        elif 'no' in data :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Okay, then i finish work')
            number = 2
            clear_text()
            return number
    else :
        return number

def format_date(string):
    _time_now = str(datetime.datetime.now().date())
    _time_now = _time_now[0:10]
    (year_now, month_now, day_now) = _time_now.split('-')
    year_now = int(year_now)
    day_now = int(day_now)
    month_now = int(month_now)
    if 'p.m.' in string:
        time  = re.findall('(\d+)', string)
        time_replace = time[0] + ':'
        time_null = str(int(time[0])+12) + ':'
        string = string.replace(time_replace, time_null)
        string = string.replace(' p.m.', '')
    if 'a.m.' in string:
        string = string.replace(' a.m.', '')
    if 'at' in string:
        date_event = ''
        string = string.replace('at', date_event)
    if 'tommorow' in string:
        if day_now >= onetime_remind.count_day(month_now):
            month_now = str(int(month_now)+1)
            day_now = 1
        else :
            day_now = int(day_now) + 1
        date_event = str(day_now)+'.'+str(month_now)+'.'+str(year_now)
        string = string.replace('tommorow', date_event)
    elif 'today' in string:
        date_event = str(day_now)+'.'+str(month_now)+'.'+str(year_now)
        string = string.replace('today', date_event)
    elif ('monday' in string) or \
        ('tuesday' in string) or \
        ('wednesday' in string) or \
        ('thursday' in string) or \
        ('friday' in string) or \
        ('saturday' in string) or \
        ('sunday' in string):
        day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for j in range(0,7):
            if day_of_week[j] in string:
                name_day = day_of_week[j]
                if j >= weekday_today():
                    dweek = j - weekday_today()
                else:
                    dweek = j - weekday_today() + 7
        dweek = dweek + int(day_now)
        if count_day(int(month_now)) < dweek:
            day_now = dweek - count_day(int(day_now))
            date_event = str(day_now)+'.'+str(month_now + 1)+'.'+str(year_now)
            string = string.replace(name_day, date_event)
        else:
            day_now = dweek
            date_event = str(day_now)+'.'+str(month_now)+'.'+str(year_now)
            string = string.replace(name_day, date_event)
    return string

def find_quotes(file_text):
    number_quotes = file_text.find('"')
    text = select_date_time.selection_word(file_text,number_quotes,len(file_text))
    return text

def list_of_reminds():
    text = ''
    chan = define_chan()
    file1 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').readlines()
    for i in range(0,len(file1)):
        if 'jean list' in file1[i]:
            text = file1[i]
            clear_text()
            file2 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
            for i in range(0,len(file2)):
                text = find_quotes(file2[i])
        if text != '' :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text= text)

def write_remindlist():
    text = ''
    send = ''
    job = ''
    chan = define_chan()
    file3 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').read()
    file1 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').readlines()
    file2 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt','a')
    for i in range(0,len(file1)):
        try :
            if ' remind' in file1[i]:
                text = file1[i]
                job = funcion_bot_General.job(text)
                number_start = job.find('at') + 3
                number_end = len(job)
                noformat_job = job[0:number_start]
                format_job = job[number_start:number_end]
                if  not ':' in job:
                    time  = re.findall('(\d+)', format_job)
                    time_replace = time[0] + ':' + '00'
                    format_job = format_job.replace(time[0], time_replace)
                    job = noformat_job+format_job
                if ('every' in job):
                    if 'p.m.' in job :
                        time  = re.findall('(\d+)', format_job)
                        time_replace = time[0] + ':'
                        time_null = str(int(time[0])+12) + ':'
                        format_job = format_job.replace(time_replace, time_null)
                        format_job = format_job.replace('p.m.', '')
                        job = noformat_job+format_job
                    if 'a.m.' in job:
                        job = job.replace('a.m.', '')
                        job = '@' + job
                else:
                    format_job = format_date(format_job)
                    job = '@' + noformat_job+format_job
                if job in file3:
                    send = 'So remind already has in remindlist'
                    sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=send)
                else :
                    if(verify.verify_username(i) == 'Void') or \
                        (verify.verify_eventname(i) == 'Void') or (verify.verify_time_and_date(i) == 'Void'):
                        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Incorrect data')
                    else :
                        if 'channel' in verify.verify_username(i) :
                            send = 'Okay, i will remind '+ '<!channel>'
                        elif '@' in verify.verify_username(i) :
                            send = 'Okay, i will remind '+ '<' + verify.verify_username(i) + '>'
                        else :
                            send = 'Okay, i will remind '+ verify.verify_username(i)
                        file2 = file2.write(chan + ' ' + job + '\n')
                        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=send)
                clear_text()
        except IndexError:
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Incorrect time')
            clear_text()

def delete_remind():
    text = ''
    number = 0
    send = 'Sorry, i don`t remind you at that time'
    job = ''
    chan = define_chan()
    file1 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').readlines()
    file2 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
    clear_text()
    for i in range(0,len(file1)):
        if 'stop_remind' in file1[i]:
            number = 5
            text = file1[i]
            job = funcion_bot_General.job(text)
            if ('every' in job):
                if 'a.m.' in job:
                    job = job.replace('a.m.', '')
            else:
                number_start = job.find('at') + 3
                number_end = len(job)
                noformat_job = job[0:number_start]
                format_job = job[number_start:number_end]
                format_job = format_date(format_job)
                job = noformat_job+format_job
            for i in range(0,len(file2)):
                if job in file2[i]:
                    file3 = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt','w')
                    send = 'Okay, i stop to remind you about this'
                    text = file2[i]
                    text = text.replace(job, '')
                    file2[i] = text
                    file3 = file3.writelines(file2)
                    if 'every' in file2[i]:
                        remind_function.refresh_remind()
                        remind_function.shed_date_final()
        if (number == 5):
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=send)
