#데이터 수집
import pygsheets
import re
import pandas
import numpy as np
from telegram import *
from telegram.ext import *
from telegram.ext import filters
from states import STATES

from config import *
from instance.config import *
from definition import *
import logging

from io import BytesIO
from telefuction import tele_manage

dir_now = os.path.dirname(os.path.abspath(__file__))
GET_NAME,GET_IMG = range(2)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

function_list = ['NFT 등록','등록한 NFT 확인']

class NFTmanager():
    def __init__(self,update_token) -> None:

        self.photoname =0
        self.gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_KEY)
        self.sh = self.gc.open(GOOGLE_SPREAD_SHEET)
        self.updater = Updater(update_token)
        self.dispatcher = self.updater.dispatcher
        self.userwks = self.sh.worksheet('title','userManage')
        #기본 기능
        self.quiz_m= tele_manage()
        #구글시트 연동기능

    def start(self,update:Update,context:CallbackContext)->str:

        text = "If you want to upload a photo, click(enter) the /register "
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        
    def startPhoto(self,update,context):
        text = "Enter the photo name to upload"
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        
        return GET_NAME

    def getname(self,update,context):
        


        self.photoname = update.message.text
        context.bot.send_message(chat_id = update.message.chat_id,text = "upload your photo")
        return GET_IMG

    def imageget(self, update, context):
        print("get")
        print(update.message.photo)
        file_path = os.path.join(dir_now, f'file_/{self.photoname}from_telegram.png')
        photo_id = update.message.photo[-1].file_id  # photo 번호가 높을수록 화질이 좋음
        photo_file = context.bot.getFile(photo_id)
        photo_file.download(file_path)

        text = "Upload success"
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        self.photoname =0 
        return ConversationHandler.END
        
    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Display the gathered info and end the conversation."""
        
        context.user_data.clear()
        update.message.reply_text("취소 되었습니다.")
        self.photoname =0
        return ConversationHandler.END

    def main(self)->None:
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler('register',self.startPhoto)],
            states={
                GET_NAME : [MessageHandler(Filters.text & ~Filters.command,self.getname)],
                GET_IMG : [MessageHandler(Filters.photo, self.imageget)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        ))

        dispatcher.add_handler(CommandHandler('start',self.start))
        self.updater.start_polling()

