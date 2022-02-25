

token = "5077037030:AAGzMcx_QR_nnuhc-gqzDb81yYFtmLyMsMU"

import logging
from telegram import *
from telegram.ext import *
import datetime
from urllib.request import urlopen
import sys

from admin import *
from start_p import start

import os
import psycopg2

url = 'postgres://wrhuzcmmpkdwsu:de85b41caa04428d064c150cffa270e3bcbaf368d7e06ff01c1a3a394e86f480@ec2-79-125-93-182.eu-west-1.compute.amazonaws.com:5432/dc3gdvkjqoqslh'
connect = psycopg2.connect(url, sslmode='require')
cursor = connect.cursor()




ad , entr ,nam ,date_b , countr ,desc , m_fel, w_f_1 , w_f_2 , fel ,c_fel,link_w , phone ,social_w ,kyc , finsh ,send= map(chr,range(17))

prof , edit , back_p  = map(chr,range(17,20))
cont ,US,OW,BC,BO,BA ,ord ,back_m,w_ord,a_ord,r_ord,back_o ,back_a= map(chr,range(20,33))
data_f =[]
ch_f =''
END = ConversationHandler.END
bot = Bot(token=token)





def name(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    text = '''ما اسمك الثلاثي ؟

/cancel >> لإنهاء الطلب'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text)
    context.user_data['msg'] = msg.message_id
    return nam


def country(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['الأسم '] = update.message.text
    text = 'اختر بلدك :'
    cursor.execute(f'''SELECT * FROM "COUNTRY" ''')
    connect.commit()
    data_c = cursor.fetchall()
    butt = []
    for i in data_c:
        butt.append([InlineKeyboardButton(text=i[1], callback_data='C' + str(i[1]) + ' ' + str(i[0]))])
    keybo = InlineKeyboardMarkup(butt)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return countr


def date_of_birth(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    update.callback_query.answer()
    d = update.callback_query.data[1:].split(' ')
    context.user_data['البلد '] = d
    text = '''ما هو عام ميلادك ؟
ex : 2001 

/cancel >> لإنهاء الطلب'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text)
    context.user_data['msg'] = msg.message_id
    return desc


def description(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['تاريخ الميلاد '] = int(update.message.text)
    text = '''اخبرنا عن نفسك ...
ملحوظه ⚠️ : هذا الوصف سوف يظهر للعملاء

/cancel >> لإنهاء الطلب'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text)
    context.user_data['msg'] = msg.message_id
    return m_fel


def main_f(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['الوصف '] = update.message.text
    text = '''اختر مجالك الاساسي :'''
    li = ['ذكاء الاصطناعي', 'أمن الشبكات', 'علم البيانات', 'انترنت الأشياء', 'علم الروبوتات', 'نظم المعلومات الحاسوبية',
          'هندسة البرمجيات']
    butt = []
    for i in li:
        butt.append([InlineKeyboardButton(text=i, callback_data='F' + str(i))])
    i = 'مجال آخر'
    butt.append([InlineKeyboardButton(text=i, callback_data='E' + str(i))])
    keybo = InlineKeyboardMarkup(butt)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return w_f_1


def con_f(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    text = '''ما هو هذا المجال ؟

/cancel >> لإنهاء الطلب'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text)
    context.user_data['msg'] = msg.message_id
    return w_f_2


def wrok_from_1(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['المجال الرئسي '] = update.callback_query.data[1:]
    text = '''في اي عام بدأت العمل في هذا المجال ؟

/cancel >> لإنهاء الطلب'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id, message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id, text=text)
    context.user_data['msg'] = msg.message_id

    return fel


def wrok_from_2(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['المجال الرئسي '] = update.message.text
    text = '''في اي عام بدأت العمل في هذا المجال ؟

/cancel >> لإنهاء الطلب'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text)
    context.user_data['msg'] = msg.message_id
    return fel


def field(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['تعمل منذ '] = int(update.message.text)
    context.user_data['مجالات العمل '] = []
    global ch_f
    global data_f
    ch_f = ''
    text = '''/cancel >> لإنهاء الطلب

اختر المجالات الذي تعمل بيها :'''
    butt = []
    cursor.execute(f'''SELECT * FROM "FIELD" ''')
    connect.commit()
    data_f = cursor.fetchall()
    c = 0
    for i in data_f:
        butt.append(
            [InlineKeyboardButton(text=i[1], callback_data='FF' + ' ' + str(c) + ' ' + str(i[0]) + ' ' + str(i[1]))])
        c += 1
    keybo = InlineKeyboardMarkup(butt)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return link_w


def con_ch_f(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    update.callback_query.answer()
    n = update.callback_query.data
    n = n.split(' ')
    f = int(n[2])
    d = int(n[1])
    context.user_data['مجالات العمل '].append(f)
    global ch_f
    global data_f
    ch_f += f'\n- {data_f[d][1]}'
    data_f.remove(data_f[d])
    text = f'''ملحوظه ⚠️ : يسمح بأختيار اكثر من مجال

          اضغط "تم" عندما تنتهي من الأختيار

/cancel >> لإنهاء الطلب

لقد اخترت :
--------------------------------------------{ch_f}
--------------------------------------------
    اختر المجالات الذي تعمل بيها :'''
    butt = []
    c = 0
    butt.append([InlineKeyboardButton(text='✅ تم ✅', callback_data='done')])
    for i in data_f:
        butt.append(
            [InlineKeyboardButton(text=i[1], callback_data='FF' + ' ' + str(c) + ' ' + str(i[0]) + ' ' + str(i[1]))])
        c += 1

    keybo = InlineKeyboardMarkup(butt)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return link_w


def link_work(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    text = '''ارسل روابط لاعمالك ....

/cancel >> لإنهاء الطلب

ex :
https://github.com/ex1
https://github.com/ex2
https://github.com/ex3'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,disable_web_page_preview=True)
    context.user_data['msg'] = msg.message_id
    return phone


def phone_f(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['اعمالك '] = update.message.text
    text = '''اضغط *ارسال رقم المحمول* لإرسال رقم المحمول 

/cancel >> لإنهاء الطلب'''
    butt = [[KeyboardButton('ارسال رقم المحمول', request_contact=True)]]
    keybo = ReplyKeyboardMarkup(butt, one_time_keyboard=True, resize_keyboard=True)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return social_w


def social_LINK(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['رقم المحمول '] = update.message.contact.phone_number
    text = '''ارسل روابط حساباتك علي مواقع التواصل ....

/cancel >> لإنهاء الطلب

ex :
https://ar-ar.facebook.com/ex
https://www.linkedin.com/ex
https://twitter.com/ex'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text)
    context.user_data['msg'] = msg.message_id
    return kyc

def kyc_f(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    context.user_data['مواقع التواصل '] = update.message.text
    text = '''ارسل صوره لأي وثيقه تثبت هويتك ...

مثل :
البطاقة الوطنية , رخصة القياده , جواز سفر

/cancel >> لإنهاء الطلب

ملحوظه ⚠️ : هذه الصوره لن يتم مشراكتها مع العملاء
و لكن لتأكد من صحة بياناتك'''

    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id, message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id, text=text)
    context.user_data['msg'] = msg.message_id
    return finsh


def finsh_f(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    ch = ''
    for k, v in context.user_data.items():
        if k == 'msg':
            continue
        if k == 'البلد ':
            v = v[0]
        if k == 'مجالات العمل ':
            cursor.execute(f'''SELECT * FROM "FIELD" ''')
            connect.commit()
            data_f = cursor.fetchall()
            sf = ''

            for i in data_f:
                if i[0] in v:
                    sf += f'    - {i[1]}\n'

            ch += f'\n{k} : \n{sf}\n\n----------------------------------------\n'
            continue

        ch += f'\n{k} : \n{v}\n\n----------------------------------------\n'

    photo_file = update.message.photo[-1].get_file()
    photo_path = photo_file['file_path']
    img = urlopen(photo_path).read()
    img = bin(int.from_bytes(img,byteorder=sys.byteorder))[2:]
    context.user_data['KYC'] = img


    text = f'''بياناتك :
{ch}

اضغط *ارسال* لارسال الطلب
او اضغط *تصحيح البيانات* لاعادة ادخال البيانات مره اخري

/cancel >> لإنهاء الطلب
'''
    butt = [[InlineKeyboardButton(text='ارسال', callback_data='send')],
            [InlineKeyboardButton(text='تصحيح البيانات', callback_data='re')]]
    keybo = InlineKeyboardMarkup(butt)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo,disable_web_page_preview=True)
    context.user_data['msg'] = msg.message_id
    return send


def send_f(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    user = update.effective_user
    date = str(datetime.datetime.now().replace(microsecond=0))
    text = '''تم ارسال طلبك و سيتم مراجعته خلال 24 ساعه كحد اقصي'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    bot.send_message(chat_id=ch_id,text=text)
    b = list(context.user_data.values())
    cursor.execute(
        f'''INSERT INTO "ORDERS" ("STATE","C_ID","A_ID","USERNAME","DATE","NAME","DESC","LINK_WORK","M_FIELD", "KYC","Y_DATE_B","SOCIAL_LINK","PHONE","WORK_FROM","COUNTRY_ID")
        VALUES ('W','{str(user['id'])}',null,'{user['username']}','{date}','{b[1]}','{b[4]}','{b[8]}','{b[5]}', '{b[11]}','{b[3]}','{b[10]}','{b[9]}','{b[6]}',{b[2][1]})
        ''')
    connect.commit()
    cursor.execute('''SELECT currval(pg_get_serial_sequence('"ORDERS"','O_ID'));''')
    connect.commit()
    d = cursor.fetchall()
    for i in b[7]:
        cursor.execute(f'''INSERT INTO "FIELD_OR_LINE" VALUES ({d[0][0]},{i})''')
        connect.commit()

    text = f" @{user['username']} Send order number {d[0][0]}"
    cursor.execute('SELECT "A_ID" FROM "ADMIN" ;')
    connect.commit()
    admins = cursor.fetchall()
    for adm_id in admins:
        bot.send_message(chat_id=adm_id[0], text=text)

    return start(update, context)


def cancel(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id, message_id=msg_id)
    return start(update, context)
