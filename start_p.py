token = "5077037030:AAGzMcx_QR_nnuhc-gqzDb81yYFtmLyMsMU"

import logging
from telegram import *
from telegram.ext import *
import datetime
from urllib.request import urlopen
from admin import *
from add_order import *
import os
import psycopg2

url = 'postgres://wrhuzcmmpkdwsu:de85b41caa04428d064c150cffa270e3bcbaf368d7e06ff01c1a3a394e86f480@ec2-79-125-93-182.eu-west-1.compute.amazonaws.com:5432/dc3gdvkjqoqslh'
connect= psycopg2.connect(url, sslmode='require')
cursor = connect.cursor()


ad , entr ,nam ,date_b , countr ,desc , m_fel, w_f_1 , w_f_2 , fel ,c_fel,link_w , phone ,social_w ,kyc , finsh ,send= map(chr,range(17))

prof , edit , back_p  = map(chr,range(17,20))
cont ,US,OW,BC,BO,BA ,ord ,back_m,w_ord,a_ord,r_ord,back_o ,back_a= map(chr,range(20,33))
data_f =[]
ch_f =''
END = ConversationHandler.END
bot = Bot(token=token)

def start(update : Update , context: CallbackContext) -> str:
    user = update.effective_user
    ch_id = update.effective_chat['id']
    cursor.execute(f'''SELECT * FROM "PERSON" WHERE "ID" = '{str(user['id'])}' ''')
    connect.commit()
    data_p = cursor.fetchall()

    cursor.execute(f'''SELECT * FROM "ORDERS" WHERE "C_ID" = '{str(user['id'])}' AND  "STATE" != 'X' ''')
    connect.commit()
    ords = cursor.fetchall()

    cursor.execute(f'''SELECT "A_ID" FROM "ADMIN" WHERE "A_ID" = '{str(user['id'])}' ;''')
    connect.commit()
    admins =cursor.fetchall()
    btt_a_text = 'انضم لفريق المبرمجين'
    bott = [[InlineKeyboardButton(text=btt_a_text, callback_data=str(ad))]]
    text = '''👋 اهلا بك في P_Search
    افضل مكان لإجاد افضل المصممين والمبرمجين العرب
    '''

    if not data_p :
        date = datetime.datetime.now().replace(microsecond=0)
        cursor.execute(f'''INSERT INTO "PERSON" VALUES ('{user['id']}','C','{str(date)}','0') ''')
        cursor.execute(f'''INSERT INTO "CLIENT" VALUES ('{user['id']}','{str(date)}')''')
        connect.commit()
    elif admins :
        text = '''اهلا بك 👋 Admin'''
        bott = [[InlineKeyboardButton(text='Enter Control Tools', callback_data=str(cont))]]
    elif ords :
        bott = [[InlineKeyboardButton(text='Profile', callback_data=str(prof))]]


    keybo = InlineKeyboardMarkup(bott)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return entr
