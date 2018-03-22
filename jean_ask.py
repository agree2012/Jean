from slackclient import SlackClient
import secinfo
import trainToGoogleDoc
import threading
import schedule
from datetime import datetime
import datetime
import sched, time
import funcion_bot_General
import new_ask
import create_table_for_parse
import new_command_create_request
token = secinfo.API_Token
sc = SlackClient(token)
s = sched.scheduler(time.time, time.sleep)

def define_chan():
    chan_string = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    if chan_string != '':
        chan = ''
        for i in range(0,9):
            chan = chan + chan_string[i]
        return chan

def connect(file):
    f = open(file, 'a')
    userlist = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/userslist.txt').readlines()
    sc.rtm_connect()
    input= sc.rtm_read()
    if input:
        for action in input:
            for i in range(0,len(userlist)):
                if 'user' in action:
                    if action['user'] != 'D643XUBNG':
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
                            f.close

def connecting():
    text = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    return text

def delete_user_ask(chan):
    fr=open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    for i in range(0,len(fr)):
        if chan in fr[i]:
            fr[i] =''
            fw = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt','w')
            fw = fw.writelines(fr)


def clear_dolist():
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt','w')
    f.close()

def call_about_results(request,chan):
    request = request['spreadsheetId']
    finalUrl = 'https://docs.google.com/spreadsheets/d/' + str(request)+'/edit#gid=0'
    sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=finalUrl + '. There you can see resault of ask.')

def parse_question(string):
    text = ''
    num_start = string.find('My answer is:') + 13
    for i in range(num_start,len(string)):
        text = text + string[i]
    return text

def get_answer(count_question):
    text={}
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    for j in range(0,len(f),count_question):
        for k in range(j,j+count_question):
            text[k] = parse_question(f[k])
    return text

def get_username_dolist(i):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    text = ''
    for j in range(0,9):
        text = text + f[i][j]
    return text

def write_in_form(k):
    counter = 0
    username = {}
    data = str(new_command_create_request.get_date()) + ' ' + str(get_time_requets(k)[0]) + str(get_time_requets(k)[1])
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    count_question = len(new_command_create_request.question_list_again(k))
    new_command_create_request.list_question(k,data)
    for j in range(1,(len(f)/count_question)+1):
        if j > 1:
            counter = counter + count_question
        for i in range(1,count_question+1):
            trainToGoogleDoc.write_his_answer(new_command_create_request.get_spreadsheetId(k),data,create_table_for_parse.get_range(i,j+1),[get_answer(count_question)[i+counter-1]])
    for j in range(1,((len(f)/count_question)+1)):
        username[j] = new_ask.change_username_id(new_ask.change_channel_id(get_username_dolist((j-1)*count_question)))
        response = trainToGoogleDoc.write_his_answer(new_command_create_request.get_spreadsheetId(k),
                                          data, create_table_for_parse.get_range(0,j+1),
                                          [username[j]])
        return response

def user_ignore(username,i):
    ignore  = new_command_create_request.ignore_list(i)
    num = 0
    for j in range(0,len(ignore)):
        if(ignore[j] == ((username))):
            num =  1
    if(num != 1):
        return 0
    else:
        return 1

def delete_uncorrect_request(i):
    text = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt','w')
    text[i] = ''
    f.writelines(text)
    f.close()

def ask_requsests(count_question,list_question,i):
    chan = define_chan()
    if(len(list_question) != 0):
        text = connecting()
        all_channels = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt').read()
        if ('Yes i ready' in text) and (chan in all_channels):
            username = '@' + new_ask.change_channel_id(define_chan())
            if ((user_ignore(username,i)) == 0):
                f=open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt','w')
                f.close()
                t4 = threading.Thread(target = ask_all_about_all_quetstion, args = (chan, count_question, list_question,i,))
                t4.start()
    else :
        delete_uncorrect_request(i)
        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text="Request was incorrect. He was deleted")


def assert_username(text):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt').readlines()
    username = text[0:8]
    num = 0
    for i in range(0,len(f)):
        if username in f[i]:
            f[i] = text
            num = 1
            delete_user_ask(username)

    fw = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/do_list.txt','a')
    fw.write(text)


def ask_all_about_all_quetstion(chan,count_question, list_question,i):
    try:
        if(len(list_question) != 0):
            text = connecting()
            answer = ''
            num1 = 1
            question = str(list_question[1]) + ' Use `My answer is:` + your answer '
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text = question)
            while(num1 <= count_question):
                    if(('My answer is:' in text ) and chan == define_chan()):
                        if((num1 + 1) <= count_question):
                            question = str(list_question[num1+1]) + ' Use `My answer is:` + your answer '
                            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=question)
                        answer = answer + text
                        f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt','w')
                        f = f.close()
                        num1 = num1 + 1
                        text = connecting()
                    else:
                        text = connecting()
            else :
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Thank you')
                assert_username(answer)
                return answer
        else :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text="Nuber of question was write incorrect")
            delete_uncorrect_request(i)
    except AttributeError :
        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text="Sorry but request" + list_question + "has incorrect parameter")
        delete_uncorrect_request(i)
    except TypeError:
        sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                    text="Sorry but request" + list_question + "was incorrect")
        delete_uncorrect_request(i)
    except KeyError:
        sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                    text="Sorry but request" + list_question + "was incorrect")

def get_time_requets(i):
    try:
        f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
        if(len(f) != 0):
            text = f[i]
            hour_minutes = {}
            start_num = 99
            end_num = text.find('every')-1
            text = text[start_num:end_num]
            hour_minutes[0] = int(text[0:text.find(':')])
            hour_minutes[1] = int(text[text.find(':')+1:len(text)])
            if(hour_minutes[0] < 25):
                if(hour_minutes[1] < 60):
                    return hour_minutes
                else :
                    chan = get_channel_request(i)
                    sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                                text='Your survey was incorrect. I delete it.')
                    delete_uncorrect_request(i)
            else :
                delete_uncorrect_request(i)
    except IndexError:
        pass
    except ValueError:
        chan = get_channel_request(i)
        sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                    text='Your survey:'+' at '+ str(f[i][99:len(f[i])]) + 'was incorrect. I delete it.')
        delete_uncorrect_request(i)

def get_channel_request(i):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    if (len(f) != 0):
        text = f[i]
        return text[90:99]

def get_time_now():
    time_now = str(datetime.datetime.now().time())
    time_now = time_now[0:8]
    (hour_now, minute_now, seconds_now) = time_now.split(':')
    time_now = [int(hour_now), int(minute_now), int(seconds_now)]
    return time_now

def create_sheet():
    if(get_time_now()[0] == 11) and (get_time_now()[1] == 25) and (get_time_now()[2] == 0):
        new_command_create_request.add_new_sheet()
    if (get_time_now()[0] == 11) and (get_time_now()[1] == 26) and (get_time_now()[2] == 0):
        new_command_create_request.every_day_create_list_question()



def get_username_all(j):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt').readlines()
    username = ''
    for i in range(2,11):
        username = username + f[j][i]
    return username

def get_start_question_ask(i):
    ignore = new_command_create_request.ignore_list(i)
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt').readlines()
    for k in range(0,len(f)):
        num = 1
        for j in range(0,len(ignore)):
            if ignore[j] =='@' + get_username_all(k):
                num = 0
        if(num != 0):
            sc.api_call('chat.postMessage', as_user='true:', channel=get_channel(k), text='Are you ready to answer on a few question? Use `Yes i ready` when will be ready.')



def day_of_week_today(num,i):
    now = datetime.datetime.now()
    num_today = now.weekday()
    pagenumber = 0
    if (num == num_today) and (get_time_now()[0] == get_time_requets(i)[0]) and (get_time_now()[1] == get_time_requets(i)[1]) and  (get_time_now()[2] == 0):
        data = str(new_command_create_request.get_date()) + ' ' + str(get_time_requets(i)[0]) + str(
            get_time_requets(i)[1])
        new_command_create_request.new_sheet(i)
        new_command_create_request.list_question(i, data)
        get_start_question_ask(i)
    if(num == num_today) and (get_time_now()[0] == get_time_requets(i)[0]) and (get_time_now()[1] >= get_time_requets(i)[1]):
        if(new_command_create_request.question_list_again(i) != 0):
            ask_requsests(len(new_command_create_request.question_list_again(i)),new_command_create_request.question_list_again(i),i)
        else :
            sc.api_call('chat.postMessage', as_user='true:', channel=get_channel_request(i),
                        text="Incorrect question structure")
            delete_uncorrect_request(i)
    if(num == num_today) and  (get_time_now()[0] == get_time_requets(i)[0]) and (get_time_now()[1] == 59) and (get_time_now()[2] == 40):
        pagenumber =  write_in_form(i)
        clear_dolist()
        sc.api_call('chat.postMessage', as_user='true:', channel=get_channel_request(i),text = 'Result of ask there: https://docs.google.com/spreadsheets/d/' + str(new_command_create_request.get_spreadsheetId(i)) + '/edit#gid=' + str(pagenumber))



def start_all_event():
    try:
        f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
        day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i in range(0,len(f)):
            if(' day' in f[i]):
                if (get_time_now()[0] == get_time_requets(i)[0]-1) and (get_time_now()[1] == get_time_requets(i)[1]) and (get_time_now()[2] == 0):
                    new_command_create_request.new_sheet(i)
                    data = str(new_command_create_request.get_date()) + ' ' + str(get_time_requets(i)[0]) + str(get_time_requets(i)[1])
                    new_command_create_request.list_question(i,data)
                    get_start_question_ask(i)
                    clear_dolist()
                if(get_time_now()[0] == get_time_requets(i)[0]-1) and (get_time_now()[1] >= get_time_requets(i)[1]):
                    ask_requsests(len(new_command_create_request.question_list_again(i)),new_command_create_request.question_list_again(i),i)
                if(((get_time_now()[0] == (get_time_requets(i)[0]-1))) and (get_time_now()[1] == 59) and (get_time_now()[2] == 50)):
                    pagenumber = write_in_form(i)
                    clear_dolist()
                    sc.api_call('chat.postMessage', as_user='true:', channel=get_channel_request(i),text='Result of ask there: https://docs.google.com/spreadsheets/d/' + str(new_command_create_request.get_spreadsheetId(i)) + '/edit#gid='+str(pagenumber))
            for j in range(0,len(day_of_week)):
                if (day_of_week[j] in f[i]):
                    num = new_command_create_request.every_time_parse(f[i])
                    day_of_week_today(num,i)
    except TypeError:
        pass

def get_channel(j):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt').readlines()
    channel = ''
    for i in range(12,21):
        channel = channel + f[j][i]
    return channel

def what_text(text):
    num = text.find("ask:") + 3
    text = text[num:len(text)]
    return text

def delete_survey():
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').readlines()
    for i in range(0,len(f)):
        if('Jean delete survey:' in f[i]):
            chan = define_chan()
            num_start = f[i].find('Jean delete survey:') + 19
            text = f[i][num_start:len(f[i])]
            funcion_bot_General.clear_text()
            try:
                ask_list =open('ask.txt').readlines()
                if(int(text) > len(ask_list)):
                    sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                        text='Sorry but i can`t find this survey, maybe number line is incorrect')
                else:
                    num = int(text) - 1
                    if(num >= 0):
                        ask_list[num] = ''
                        fw = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt','w')
                        fw.writelines(ask_list)
                        sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                                text='Okay i delete it')
                    else:
                        sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                        text='Sorry but i can`t find this survey, maybe number line is incorrect')
            except ValueError:
                sc.api_call('chat.postMessage', as_user='true:', channel=chan,
                            text='Incorrect number of string')


def list_of_survey():
    text = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    if('show survey' in text) :
        chan = define_chan()
        funcion_bot_General.clear_text()
        survey = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
        if(len(survey) > 0):
            for i in range(0,len(survey)):
                sc.api_call('chat.postMessage', as_user='true:', channel=chan,text=str(i+1) + ': at '+ str(survey[i][99:len(survey[i])]))
        else:
            sc.api_call('chat.postMessage', as_user='true:', channel=chan,text='List is empty')
