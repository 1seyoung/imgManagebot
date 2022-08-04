
from definition import *
from telegram import *
from telegram.ext import *
from datetime import datetime

class tele_manage():

    def __init__(self):

        pass

    def alarm_data(self, update:Update, context:CallbackContext)->str:
        print("alarm_data")
        text = f'사용자 정보가 없습니다.\n 사용자 정보를 입력해주세요.\n 이름을 입력해주세요.'
        context.bot.send_message(context.user_data[ID],text)
       
        return INSERT

    def insert_user_name(self, update:Update, context:CallbackContext)->str:

        print("insert_name")
        insert_name = update.message.text

        context.user_data[NAME] = insert_name
            
        print(insert_name)

        return BACK
