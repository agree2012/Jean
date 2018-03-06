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
    if "change my request" in message:
        text = message
        chan = funcion_bot_General.define_chan()
        fl = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt').readlines()
        info = new_command_create_request.survevy_info(text)
        for i in range(0, len(fl)):
            if ((info[0] in fl[i]) and (info[1] in fl[i]) and (info[2] in fl[i]) and (info[3] in fl[i])):
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Send the new request please')
                message = request(text)
                oldpart = all_strings(i)
        if oldpart != '':
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Write new request.\n\
    Use `jean rechange to YOUR REQUEST')
            num = 1
        else :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='So request isn`t found')
            num = 3
        funcion_bot_General.clear_text()
    while(num == 1):
        num = 2
    while(num == 2):
        new_message = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/lol.txt').read()
        if ('rechange' in new_message) and (chan == funcion_bot_General.define_chan()) :
            info = new_command_create_request.survevy_info(new_message)
            if(new_command_create_request.questions_list(info[2]) != 0):
                textwrite = oldpart + chan + info[0] + ' ' + info[1] + info[2] + info[3] + '\n'
                f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/ask.txt', 'a')
                f.write(str(textwrite))
                num = 3
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='I change it')
                funcion_bot_General.clear_text()
            else:
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Sorry but you wrote incorrect parameters')
