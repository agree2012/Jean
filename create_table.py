import datetime
import secinfo
import new_command_create_request
def get_username(number_string):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    username = ''
    for i in range(0,9):
        username = username + f[number_string][i]
    for i in range(0,len(secinfo.channel_list)):
        if username in secinfo.channel_list[i]:
            username = secinfo.user_list[i]
    return username



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
    f = open('ask.txt').readlines()
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
    return new_command_create_request.count_of_ignore(get_ignore_text(i))
def ret_num_question(i):
    return new_command_create_request.count_of_question(get_text_questions(i))
