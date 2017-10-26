# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
from slackclient import SlackClient
import secinfo
import jenkins
import jean_ask
import funcion_bot_General
import time
from multiprocessing import Process
import threading
import re
import schedule
import sched, time
import remind_function
funcion_bot_General.clear_text()
remind_function.shed_date_final()
jean_ask.shedule_clear_dolist()
jean_ask.shedule_write()
jean_ask.ask_about_work()
while(1) :
    funcion_bot_General.connect('lol.txt')
    t1 = threading.Thread(target = funcion_bot_General.build_project)
    funcion_bot_General.command_hello()
    funcion_bot_General.command_help()
    funcion_bot_General.command_stop_watching()
    funcion_bot_General.status_project()
    funcion_bot_General.list_of_reminds()
    t1.start()
    t2 = threading.Thread(target = funcion_bot_General.eye_on_server)
    t2.start()
    t3 = threading.Thread(target=funcion_bot_General.command_change_answer)
    t3.start()
    funcion_bot_General.write_remindlist()
    funcion_bot_General.delete_remind()
    schedule.run_pending()
