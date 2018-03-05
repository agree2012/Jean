# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import funcion_bot_General
import threading
import jean_ask
import change_answer
import schedule
import new_ask
import new_command_create_request
import remind_function
import create_table_for_parse
funcion_bot_General.clear_text()
#jean_ask.start_all_event()
remind_function.shed_date_final()
while(1) :
    funcion_bot_General.connect('lol.txt')
    t1 = threading.Thread(target = funcion_bot_General.build_project)
    t4 = threading.Thread(target=change_answer.change_request)
    t4.start()
    funcion_bot_General.command_hello()
    funcion_bot_General.command_help()
    jean_ask.list_of_survey()
    funcion_bot_General.command_stop_watching()
    funcion_bot_General.status_project()
    funcion_bot_General.list_of_reminds()
    t1.start()
    t2 = threading.Thread(target = funcion_bot_General.eye_on_server)
    t2.start()
    #t3 = threading.Thread(target=funcion_bot_General.command_change_answer)
    #t3.start()
    jean_ask.start_all_event()
    #jean_ask.create_sheet()
    jean_ask.delete_askquestion()
  #  jean_ask.change_string()
    #t3 = threading.Thread(target = jean_ask.get_count_string_change)
    #t3.start()
    #jean_ask.get_count_string_change()
    new_command_create_request.create_survevy()
    funcion_bot_General.write_remindlist()
    funcion_bot_General.delete_remind()
    schedule.run_pending()
