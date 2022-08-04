#데이터 수집
from email.mime import image
from config import *
#from instance.config import *

import pygsheets
import re
import pandas
from telegram import *
from telegram.ext import *
from telegram.ext import filters
import logging
from io import BytesIO
import json
import datetime


dir_now = os.path.dirname(os.path.abspath(__file__))
GET_USER_NAME,GET_NAME,GET_IMG, GET_LIST,SEND_IMG= range(5)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

function_list = ['NFT 등록','등록한 NFT 확인']

class NFTmanager():
    def __init__(self,update_token) -> None:


        self.gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_KEY)
        self.sh = self.gc.open(GOOGLE_SPREAD_SHEET)
        self.updater = Updater(update_token)
        self.dispatcher = self.updater.dispatcher
        self.wks = self.sh.worksheet('title','Manage')
        #기본 기능
        
        #구글시트 연동기능

    def start(self,update:Update,context:CallbackContext)->str:

        text = "ヽ(･̑ᴗ･̑)ﾉ\n-> If you want to upload a work?\n-> click the /register !!\n\n->  If you want to check a upload work?\n-> click the /my_list !!\n\nClick /cancel to cancel registration"
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        
    def startPhoto(self,update,context):
        text = "(•̀ᴗ•́)و ̑̑\n-> Please enter the name of the work owner!!!\nClick /cancel to cancel registration"
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        
        return GET_USER_NAME

    def getuser(self,update,context):
        #작품 주인 이름 얻기
        context.user_data['owner'] = str(update.message.text)
        context.user_data['telid'] = update.effective_user.id
        
        

        text = "-( ᐛ )/\n-> Enter the title of the work to be uploaded!!!!\nClick /cancel to cancel registration"
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        return GET_NAME

    def getname(self,update,context):
        #작품 이름 얻기
        context.user_data['artwork'] = update.message.text


        context.bot.send_message(chat_id = update.message.chat_id,text = "¡¡¡( •̀ ᴗ •́ )و!!!\n->upload your work(JPG/JPEG/PNG etc.)!\nClick /cancel to cancel registration")
        return GET_IMG

    def imageget(self, update, context):

        text = "loading..."
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        a=context.user_data['artwork']
        b=context.user_data['owner']
        print("get")
        print(update.message.photo)
        file_path = os.path.join(dir_now, f'file_/{a}_from_{b}.png')
        photo_id = update.message.photo[-1].file_id  # photo 번호가 높을수록 화질이 좋음
        photo_file = context.bot.getFile(photo_id)
        photo_file.download(file_path)

        context.user_data['workpath'] = file_path
        context.user_data['uploadtime']= str(datetime.datetime.now())

        df = self.wks.get_as_df()
        list_= [context.user_data['telid'],context.user_data['owner'] ,context.user_data['artwork'],context.user_data['workpath'],context.user_data['uploadtime']]
        self.wks.update_row((len(df)+2),list_,col_offset=0)

        

        text = "✧*｡٩(ˊᗜˋ*)و✧*｡\n-> Upload success!\n\n->  If you want to check a upload work?\n-> click the /my_list !!"
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        print("DDDD")
        return ConversationHandler.END
        
    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Display the gathered info and end the conversation."""
        
        context.user_data.clear()
        update.message.reply_text("(´╹〽╹`)\n->Cancellation of work registration")
        self.photoname =0
        return ConversationHandler.END

    def get_info(self, update: Update, context: CallbackContext) -> int:
        df = self.wks.get_as_df()
        text = "✧*｡٩(ˊᗜˋ*)و✧*｡\n-> Select work to check!"
        context.bot.send_message(chat_id = update.message.chat_id,text = text)
        update.effective_user.id

        is_teldf = df['tel_id']== update.effective_user.id
        teldf =df[is_teldf]
        

        artdic = teldf.set_index('artwork').T.to_dict()

        #인덱스만 남음(artwork)
        art_data=list(artdic)
        context.user_data['list'] = artdic
        show_list= []
        for art in art_data:
            a=str(artdic[art]['owner'])
            show_list.append([InlineKeyboardButton(a+" : "+art,callback_data=art)])
        show_markup = InlineKeyboardMarkup(show_list)
        update.message.reply_text("Select the work you want to check",reply_markup=show_markup)
        
        return SEND_IMG
        

    def sendimg(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        info=context.user_data['list']
        infodic  = info[query.data]

        context.bot.send_photo(chat_id=update.effective_user.id,photo=open(infodic['filepath'],'rb'))
        text = f"Upload Time : {infodic['uploadtime']}\nOwner : {infodic['owner']}\nTitle of work : {query.data} "
        update.callback_query.message.edit_text(text)
        return ConversationHandler.END

    def main(self)->None:
        dispatcher = self.updater.dispatcher
        #사진 등록 핸들러
        dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler('register',self.startPhoto)],
            states={
                GET_USER_NAME : [MessageHandler(Filters.text & ~Filters.command,self.getuser)],
                GET_NAME : [MessageHandler(Filters.text & ~Filters.command,self.getname)],
                GET_IMG : [MessageHandler(Filters.photo, self.imageget)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        ))
        #리스트 확인 핸들러
        dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler('my_list',self.get_info)],
            states={
                #GET_LIST : [MessageHandler(Filters.text & ~Filters.command,self.getuser)],
                SEND_IMG : [CallbackQueryHandler(self.sendimg)]
                #GET_IMG : [MessageHandler(Filters.photo, self.imageget)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        ))

        dispatcher.add_handler(CommandHandler('start',self.start))
        self.updater.start_polling()

