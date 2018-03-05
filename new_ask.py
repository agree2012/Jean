import requests
import secinfo
import json

def all_user_list(userlist):
    users = {}
    text_end = ''
    num_start = 0
    g = 0
    for i in range(0,len(userlist)):
        if userlist[i] == ',':
            users[g] = userlist[num_start:i]
            g = g + 1
            num_start = i
            text_end = userlist[i+1:len(userlist)]
    users[g] = text_end
    return users


def user_from_channels(botchannel,url):
    number = 1
    url = url + '/api/channels.list?token=' + secinfo.API_Token
    r = requests.get(url)
    new_text = r.text
    num_start = new_text.find(botchannel)
    num_stop = new_text[num_start:len(new_text)].find('}') + 2
    text_start = new_text[num_start:num_stop]
    start_members = text_start.rfind('members":["')
    all_members = new_text[start_members:num_stop]
    start_members = all_members.find(':[') + 2
    all_members = all_members[start_members:len(all_members)]
    for i in range(0,len(all_members)):
        if all_members[i] == ',':
            number = number + 1
    users = all_user_list(all_members)
    return users


def get_channals(botchannel,url):
    string = user_from_channels(botchannel, url)
    text = {}
    url = url + '/api/im.list?token=' + secinfo.API_Token
    r = requests.get(url)
    new_text = r.json()
    for i in range(1, len(new_text['ims'])):
        for j in range(0,len(string)):
            if str(new_text['ims'][i]['user']) in string[j] :
                text[i] = str(new_text['ims'][i]['user']) + ' ' + str(new_text['ims'][i]['id'])
                text[i] = str(text[i])
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt','w')
    f.write(str(text))
    f.close()
    format_text()


def write_user_list(url):
    url = url+'/api/im.list?token='+secinfo.API_Token
    r = requests.get(url)
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.json','a')
    text = f.writelines(r.text.encode('cp1251'))
    text = open('list_and_channel.txt').read()
    text = text.replace('{', '\n')
    textwrite = open('list_and_channel.txt', 'w')
    textwrite = textwrite.writelines(text)

def write_in_json(url):
    text = open('list_and_channel.json', 'w')
    url = url + '/api/im.list?token=' + secinfo.API_Token
    r = requests.get(url)
    f = open('list_and_channel.json', 'a')
    text = f.writelines(r.text.encode('cp1251'))

def rewrite_json():
    text = open('list_and_channel.json').read()
    text = text.replace('{', '{\n')
    textwrite = open('list_and_channel.json', 'w')
    textwrite = textwrite.writelines(text)

def count_users(userlist):
    num = 0
    text ={}
    for i in range(1,len(userlist['ims'])):
        if((userlist['ims'][i]['is_user_deleted']) is False):
            text[i] =str(userlist['ims'][i]['user']) + ' ' + str(userlist['ims'][i]['id'])
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt','w')
    f=f.write(str(text))

def format_text():
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt').read()
    f = f.replace('1:',' 1:')
    f = f.replace(',','\n')
    f = f.replace('}','')
    f = f.replace('{','')
    fw = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt','w')
    fw.write(f)


#format_text()
def user_count():
    user_channals_info()
    f = open('list_and_channel.txt').readlines()
    return (len(f))

get_channals('bot_jean','https://testjenkinsslack.slack.com')

def user_channals_info():
    #write_in_json('https://testjenkinsslack.slack.com')
    #f = open("list_and_channel.json","r")
    #s=f.read()
    #userlist = json.loads(s)
    #count_users(userlist)
    #format_text()
    get_channals('bot_jean','https://testjenkinsslack.slack.com')

def get_users(i):
    f = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/list_and_channel.txt').readlines()
    username = ''
    for j in range(0,8):
        username = username + f[i][j]
    return username


def change_channel_id(channel_id):
    url = 'https://testjenkinsslack.slack.com/'
    url = url + 'api/im.list?token=' + secinfo.API_Token
    r = requests.get(url)
    id = ''
    text = r.text.encode('cp1251')
    num_start = text.find(channel_id)
    num__username_start = text[num_start:len(text)].find('user') + 7
    num_username_stop = text[num_start:len(text)].find('is_user_deleted') - 3
    for i in range(num__username_start,num_username_stop):
        id = id + text[num_start:len(text)][i]
    return id

def change_username_id(user_id):
    url = 'https://testjenkinsslack.slack.com/'
    url = url + 'api/users.list?token=' + secinfo.API_Token
    r = requests.get(url)
    username = ''
    text = r.text.encode('cp1251')
    num_start = text.find(user_id)
    num__username_start = text[num_start:len(text)].find('real_name') +12
    num_username_stop = text[num_start:len(text)].find('tz') -3
    for i in range(num__username_start,num_username_stop):
        username = username + text[num_start:len(text)][i]
    return username
