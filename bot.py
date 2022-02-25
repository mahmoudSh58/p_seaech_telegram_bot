token = "5077037030:AAGzMcx_QR_nnuhc-gqzDb81yYFtmLyMsMU"

import logging
from telegram import *
from telegram.ext import *
import datetime
from urllib.request import urlopen
from admin import *
from start_p import start
from add_order import *
import os
import psycopg2
import sys

url = 'postgres://wrhuzcmmpkdwsu:de85b41caa04428d064c150cffa270e3bcbaf368d7e06ff01c1a3a394e86f480@ec2-79-125-93-182.eu-west-1.compute.amazonaws.com:5432/dc3gdvkjqoqslh'
connect = psycopg2.connect(url, sslmode='require')
cursor = connect.cursor()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger=logging.getLogger(__name__)


ad , entr ,nam ,date_b , countr ,desc , m_fel, w_f_1 , w_f_2 , fel ,c_fel,link_w , phone ,social_w ,kyc , finsh ,send= map(chr,range(17))

prof , edit , back_p  = map(chr,range(17,20))
cont ,US,OW,BC,BO,BA ,ord ,back_m,w_ord,a_ord,r_ord,back_o ,back_a= map(chr,range(20,33))
data_f =[]
ch_f =''
END = ConversationHandler.END
bot = Bot(token=token)

# profile programer

def profile(update : Update , context: CallbackContext) -> str:
    return END

#---------------------





def main() -> None:
    updater = Updater(token,use_context=True)
    dispatcher = updater.dispatcher

    ord_con = ConversationHandler(
        entry_points=[CallbackQueryHandler(name,pattern='^'+str(ad)+'$')],
        states={
            nam: [MessageHandler(Filters.text & ~ Filters.command, country)],
            countr: [CallbackQueryHandler(date_of_birth, pattern='^C')],
            desc: [MessageHandler(Filters.text & ~ Filters.command, description)],
            m_fel: [MessageHandler(Filters.text & ~ Filters.command, main_f)],
            w_f_1: [CallbackQueryHandler(wrok_from_1, pattern='^F'), CallbackQueryHandler(con_f, pattern='^E')],
            w_f_2: [MessageHandler(Filters.text & ~ Filters.command, wrok_from_2)],
            fel: [MessageHandler(Filters.text & ~ Filters.command, field)],
            link_w: [CallbackQueryHandler(con_ch_f, pattern='^FF'),
                     CallbackQueryHandler(link_work, pattern='^(done)$')],
            phone: [MessageHandler(Filters.text & ~ Filters.command, phone_f)],
            social_w: [MessageHandler(Filters.contact, social_LINK)],
            kyc: [MessageHandler(Filters.text & ~ Filters.command, kyc_f)],
            finsh: [MessageHandler(Filters.photo, finsh_f)],
            send: [CallbackQueryHandler(send_f, pattern='^(send)$'), CallbackQueryHandler(name, pattern='^(re)$')],
        },
        fallbacks = [CommandHandler('cancel', cancel)],
        map_to_parent={
            entr : entr
        }
    )

    control_tool = ConversationHandler (
        entry_points=[CallbackQueryHandler(control,pattern='^'+str(cont)+'$')],
        states= {
            ord : [CallbackQueryHandler(orders,pattern='^(O)$'),
                   CallbackQueryHandler(adman_f,pattern='^(A)$')],

            w_ord: [CallbackQueryHandler(select_ord,pattern='^(WOR)'),
                    CallbackQueryHandler(orders,pattern='^(re)$'),
                    CallbackQueryHandler(control,pattern='^(b_c)$')],

            a_ord: [CallbackQueryHandler(accept_ord,pattern='^(A)$'),
                    CallbackQueryHandler(reject_ord,pattern='^(X)$'),
                    CallbackQueryHandler(back_s_o,pattern='^'+back_o+'$')],

            r_ord: [MessageHandler(Filters.text & ~ Filters.command, send_reason)],

            cont : [CallbackQueryHandler(adman_f,pattern='^(A)$'),
                    CallbackQueryHandler(control,pattern='^'+back_a+'$')]

        },
        fallbacks=[]
    )

    st_con = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            entr : [ord_con,control_tool],
            prof : [CallbackQueryHandler(profile,pattern='^'+str(prof)+'$')],
        },
        fallbacks=[]
    )

    dispatcher.add_handler(st_con)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()