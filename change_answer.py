import secinfo
import funcion_bot_General
from slackclient import SlackClient
import new_command_create_request
token = secinfo.API_Token
sc = SlackClient(token)

def request(string):
    num_start = string.find('change') + 18
    return string[num_start:len(string)]

def new_request(string):
    num_start = string.find('rechange') + 11
    return string[num_start:len(string)]

def all_strings(i):
    return_string = ''
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
    return_string = f[i][0:90]
    f[i] = ''
    fw = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt','w')
    fw.writelines(f)
    return return_string

def change_request():
    message = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
    num = 0
    oldpart = ''
    if "change my request:" in message:
        text = message
        chan = funcion_bot_General.define_chan()
        fl = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
        ask_len = len(fl)
        num = message.find("request:") + 8
        num_rechange = text[num:len(message)]
        try:
            if((int(num_rechange)-1) > 0) or ((int(num_rechange)-1) <= ask_len):
                oldpart = all_strings(int(num_rechange)-1)
                fl[int(num_rechange)-1] = ''
                fr = open('ask.txt','w')
                fr.writelines(fl)
            if oldpart != '':
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Write new request.\n\
    Use `jean rechange to a survey` + YOUR REQUEST')
                num = 1
            else :
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='So request isn`t found')
                num = 3
        except ValueError:
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='So request isn`t found')
        funcion_bot_General.clear_text()
    while(num == 1):
        num = 2
    while(num == 2):
        new_message = open('lol.txt').read()
        if ('rechange' in new_message) and (chan == funcion_bot_General.define_chan()) :
            info = new_command_create_request.survevy_info(new_message)
            if(new_command_create_request.questions_list(info[2]) != 0):
                textwrite = oldpart + chan + info[0] + ' ' + info[1] + info[2] + info[3] + '\n'
                f = open('ask.txt', 'a')
                f.write(str(textwrite))
                num = 3
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='I change it')
                funcion_bot_General.clear_text()
            else:
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Sorry but you wrote incorrect parameters')
