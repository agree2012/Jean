import trainToGoogleDoc
import datetime
import funcion_bot_General
from slackclient import SlackClient
import secinfo
import jean_ask
import schedule
import new_ask
import create_table_for_parse
token = secinfo.API_Token
sc = SlackClient(token)

def survevy_info(text):
    time = ''
    day = ''
    question = ''
    ignore = ''
    start = text.find('survey at') + 9
    every_start = text.find('every')
    every_stop = text.find('uestion')
    start_please_ignore = (text.rfind('?') + 2)
    for i in range(start,every_start-1):
        time = time + text[i]
    for i in range(every_start,every_stop-1):
        day = day + text[i]
    for i in range(every_stop-1,start_please_ignore-1):
        question = question + text[i]
    for i in range(start_please_ignore-1,len(text)-1):
        ignore = ignore + text[i]
    return [time, day, question, ignore]

def two_parts_time(string):
    time = {}
    start_num = string.find(':') - 2
    end_num = string.find(':') + 2
    time[0] = string[start_num:start_num+2]
    time[1] = string[start_num+2:end_num]
    return time

def count_of_question(text):
    count = 0
    for i in range(0,len(text)):
        if text[i] == '?':
            count = count + 1
    return count

def questions_list(question):
    num = {}
    textstring = ''
    text = {}
    final = count_of_question(question) + 1
    num[final]=len(question)
    question_list = {}
    for i in range(1,count_of_question(question)+1):
        num[i] = question.find(str(i)+ ')')
    for i in range(1,(count_of_question(question)+1)):
        for j in range(num[i],num[i+1]):
            textstring = textstring + question[j]
        text[i]=textstring
        if text[i] == '':
            text[i] = 'uncorrect question structure'
        if 'uncorrect question structure' in text[i]:
            return 0
        textstring = ''
    return text


def every_time_parse(every_regexp):
    num = 0
    day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if 'day' in every_regexp:
        num = 13
    for i in range(0,len(day_of_week)):
        if day_of_week[i] in every_regexp:
            num = i
    return num


def count_of_ignore(ignore_users):
    num = 0
    for i in range(0,len(ignore_users)):
        if (ignore_users[i] == '@') and (ignore_users[i-1] =='<'):
            num = num + 1
    return num


def nums_massive(text):
    start_nums = {}
    stop_nums = {}
    nums = {}
    j=0
    k=0
    for i in range(0,len(text)):
        if (text[i] == '@') and (text[i - 1] == '<'):
            start_nums[j] = i
            j=j+1
        if(text[i] == '>'):
            stop_nums[k] = i
            k=k+1
    for i in range(0,2*len(start_nums),2):
        nums[i] = start_nums[i/2]
    for i in range(1,2*len(stop_nums),2):
        nums[i] = stop_nums[i/2]
    return nums


def ignore_parse(ignore_users):
    ignoreuser={}
    text = ''
    count_nums = nums_massive(ignore_users)
    for i in range(0,2*count_of_ignore(ignore_users),2):
        for j in range(count_nums[i],count_nums[i+1]):
            text = text + ignore_users[j]
        ignoreuser[i/2] = text
        text = ''
    return ignoreuser

def create_survevy():
        number = 0
        chan = funcion_bot_General.define_chan()
        data = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
        try:
            if(data != ''):
                if 'Jean, can you please conduct a survey' in data:
                    text = data
                    info = survevy_info(text)
                    count_row = new_ask.user_count() - count_of_ignore(info[3]) + 1
                    count_column = count_of_question(info[2]) + 1
                    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
                    for i in range(0,len(f)):
                        if (info[0] in f[i]) and (info[1] in f[i]) and (info[2] in f[i]) and (info[3] in f[i]):
                            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text="This requset already create!")
                            number = 1
                            return number
                        if(int(two_parts_time(info[0])[0]) == jean_ask.get_time_requets(i)[0]):
                            if(info[1] in f[i]) or ('every day' in info[1]) or ('every day' in f[i]):
                                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text="Sorry but this time already busy!")
                                number = 1
                                return number
                    if(number != 1):
                        textwrite = info[0]+' '+info[1]+' '+info[2]+' '+ info[3]+' '
                        response = trainToGoogleDoc.create_table(get_date(),int(count_row),int(count_column))
                        spreadsheetId = response['spreadsheetId']
                        add_username_field(spreadsheetId,create_table_for_parse.get_date())
                        if(questions_list(info[2]) != 0):
                            add_questions(spreadsheetId,count_of_question(info[2]),questions_list(info[2]),create_table_for_parse.get_date())
                            textwrite = str(response) + ' ' + chan + textwrite + '\n'
                            fw = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt','a')
                            fw.write(textwrite)
                            time_end = int(two_parts_time(info[0])[0]) + 1
                            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text="Your tables is https://docs.google.com/spreadsheets/d/" + spreadsheetId + "/edit#gid=0 Result will be write at " + str(time_end) + ":00")
                        else:
                            sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                                        text="Sorry but you write incorrect time")
        except ValueError :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                    text="Sorry but parameter(s) request is't correct")



def add_username_field(spreadsheet,date):
    trainToGoogleDoc.write_his_answer(spreadsheet,date,'A1', ['Username'])

def write_range_header(i,j):
    text = ''
    num_start = 65
    num_stop = num_start + i
    text = chr(num_stop)+str(j)
    return text

def add_questions(spreadsheet,count_questions,question_list,date):
    for i in range(1,count_questions+1):
        trainToGoogleDoc.write_his_answer(spreadsheet, date, write_range_header(i,1), [question_list[i]])

def add_new_sheet():
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    for i in range(0,len(f)):
        row_count = int(ret_num_question(i)) + 1
        usercount = new_ask.user_count() - ret_num_ignore(i) + 1
        spreadsheet = get_spreadsheetId(i)
        trainToGoogleDoc.add_sheet(spreadsheet,usercount,row_count,get_date())

def new_sheet(i):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    date = str(get_date()) + ' ' + str(jean_ask.get_time_requets(i)[0]) + str(jean_ask.get_time_requets(i)[1])
    row_count = int(ret_num_question(i)) + 1
    usercount = new_ask.user_count() - ret_num_ignore(i) + 1 
    spreadsheet = get_spreadsheetId(i)
    return trainToGoogleDoc.add_sheet(spreadsheet, usercount, row_count, date)

def get_do_today(number_string):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    work_today = ''
    for i in range(10,len(f[number_string-2])):
        work_today = work_today + f[number_string-2][i]
    return work_today

def going_to_do_tommorow(number_string):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    work_tommorow = ''
    for i in range(10, len(f[number_string-1])):
        work_tommorow = work_tommorow + f[number_string-1][i]
    return work_tommorow

def get_anything(number_string):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    work_tommorow = ''
    for i in range(10, len(f[number_string])):
        work_tommorow = work_tommorow + f[number_string][i]
    if 'No thanks' in work_tommorow:
        work_tommorow = 'Not  more information'
    return work_tommorow

def get_range(number):
    number += 1
    range = 'A'+str(number)+':D'+str(number)
    return range

def get_date():
    now_date = str(datetime.datetime.now().date())
    now_date = now_date[0:10]
    return now_date

def get_row():
    f=open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    row = len(f)
    return row

def get_spreadsheetId(i):
    spreadsheetId = ''
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    for j in range(21,65):
        spreadsheetId = spreadsheetId + f[i][j]
    return spreadsheetId


def get_ignore_text(i):
    num = 0
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    text = f[i]
    num = text.find('nd please ignore')
    text_final = (text[num-1:len(text)])
    return text_final


def get_text_questions(i):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    text = f[i]
    num = text.find('1)')
    num_end = text.rfind('?') + 1
    text_final = text[num:num_end]
    return text_final

def ret_num_ignore(i):
    return count_of_ignore(get_ignore_text(i))

def ret_num_question(i):
    return count_of_question(get_text_questions(i))

def question_list_again(i):
    text = get_text_questions(i)
    return questions_list(text)

def ignore_list(i):
    text = get_ignore_text(i)
    return ignore_parse(text)

def every_day_create_list_question():
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    for i in range(0,len(f)):
        add_username_field(create_table_for_parse.get_spreadsheetId(i))
        add_questions(create_table_for_parse.get_spreadsheetId(i),len(question_list_again(i)),question_list_again(i))

def list_question(i,date):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    add_username_field(create_table_for_parse.get_spreadsheetId(i),date)
    add_questions(create_table_for_parse.get_spreadsheetId(i), len(question_list_again(i)), question_list_again(i),date)
