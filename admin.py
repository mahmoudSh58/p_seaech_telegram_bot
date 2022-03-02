import logging
import io
from telegram import *
from telegram.ext import *
import datetime
from urllib.request import urlopen
from add_order import *
from start_p import start
import os
import psycopg2
import sys

url = str(os.environ['DATABASE_URL'])
token = str(os.environ['TOKEN'])
connect = psycopg2.connect(url, sslmode='require')
cursor = connect.cursor()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

ad , entr ,nam ,date_b , countr ,desc , m_fel, w_f_1 , w_f_2 , fel ,c_fel,link_w , phone ,social_w ,kyc , finsh ,send= map(chr,range(17))

prof , edit , back_p  = map(chr,range(17,20))
cont ,US,OW,BC,BO,BA ,ord ,back_m,w_ord,a_ord,r_ord,back_o ,back_a= map(chr,range(20,33))
data_f =[]
ch_f =''
END = ConversationHandler.END
bot = Bot(token=token)



# admin control tool

def admin_check(ac , id) -> bool :
    cursor.execute(f'''SELECT "A_TYPE" FROM "ADMIN" WHERE  "A_ID" = '{id}' ''')
    connect.commit()
    ad = cursor.fetchall()
    if ad[0][0] == ac :
        return True
    else:
        return False


def control(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    user_id = update.effective_user['id']
 
    if  not (admin_check('A',user_id) or admin_check('O',user_id) ):
        msg_id = context.user_data['msg']
        bot.delete_message(chat_id=ch_id, message_id=msg_id)
        bot.send_message(chat_id=ch_id,text='you not admin \n send ')
        return start(update,context)

    text = 'اختر :'
    butt =[[InlineKeyboardButton(text='ORDER',callback_data='O')]]


    if admin_check('O',user_id) :
        butt.append([InlineKeyboardButton(text='ADMIN',callback_data='A')])

    keybo = InlineKeyboardMarkup(butt)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return ord

def orders(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    user_id = update.effective_user['id']

    if not (admin_check('A',user_id) or admin_check('O',user_id) ):
        msg_id = context.user_data['msg']
        bot.delete_message(chat_id=ch_id, message_id=msg_id)
        bot.send_message(chat_id=ch_id, text='you not admin \n send /start')
        return start(update,context)


    text = '''wait order :'''
    cursor.execute(f'''SELECT * FROM "ORDERS" WHERE  "STATE" = 'W' ''')
    connect.commit()
    ords = cursor.fetchall()
    butt =[[InlineKeyboardButton(text='🔄 refresh 🔄',callback_data='re'),
           InlineKeyboardButton(text='➡ back ➡',callback_data='b_c')]]
    for i in ords :
        butt.append([InlineKeyboardButton(text=f'ORDER {i[0]} : @{i[11]}',callback_data='WOR'+ ' ' + str(i[0]))])
    keybo = InlineKeyboardMarkup(butt)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return w_ord

def select_ord(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    user_id = update.effective_user['id']

    if not (admin_check('A',user_id) or admin_check('O',user_id) ):
        msg_id = context.user_data['msg']
        bot.delete_message(chat_id=ch_id, message_id=msg_id)
        bot.send_message(chat_id=ch_id, text='you not admin \n send /start')
        return start(update,context)


    A_ID = update.effective_user['id']
    a= update.callback_query.data
    a= a.split(' ')
    context.user_data['O_ID']= a[1]
    cursor.execute(f'''SELECT * FROM "ORDERS" WHERE  "STATE" = 'W'  AND "O_ID" = {a[1]} ''')
    connect.commit()
    ords = cursor.fetchall()

    if not ords :
        return orders(update,context)

    d_ord = ords[0]

    if d_ord[3]:
        bot.send_message(chat_id=ch_id,text=f'admain {d_ord[3]} open order')
        return orders(update,context)

    cursor.execute(f'''UPDATE "ORDERS"
    SET "A_ID"='{A_ID}'
    WHERE "O_ID" = {a[1]} ''')
    connect.commit()

    cursor.execute(f'''SELECT * FROM "COUNTRY" WHERE  "COUNTR_ID" = {d_ord[15]} ''')
    connect.commit()
    c_n = cursor.fetchall()

    cursor.execute(f'''SELECT "FIELD_ID" FROM "FIELD_OR_LINE" WHERE  "O_ID" = {a[1]} ''')
    connect.commit()
    f_n = cursor.fetchall()

    p_n = ''
    for f in f_n :
        cursor.execute(f'''SELECT "FIELD_N" FROM "FIELD" WHERE  "FIELD_ID" = {f[0]} ''')
        connect.commit()
        p = cursor.fetchall()
        p_n += f'      -{p[0][0]}\n'

    now_y = datetime.date.today().year
    age =(now_y - datetime.date(int(d_ord[10]),1,1).year)
    w_y = (now_y - datetime.date(int(d_ord[14]),1,1).year)

    context.user_data['C_O_ID'] = d_ord[2]

    text = f'''num : {d_ord[0]}
date : {d_ord[4]}
client id : {d_ord[2]}
name : {d_ord[5]}
age : {age}
username : {d_ord[11]}
country : {c_n[0][1]}
phone : {d_ord[13]}
-----------------------------------
desc :
{d_ord[6]}
-----------------------------------
M_field : {d_ord[8]}
from : {w_y}
-----------------------------------
links of work :
{d_ord[7]}
-----------------------------------
feild :
{p_n}
-----------------------------------
soical links :
{d_ord[12]}


'''
    butt = [[InlineKeyboardButton(text='✅',callback_data='A'),
             InlineKeyboardButton(text='❌',callback_data='X'),
             InlineKeyboardButton(text='➡️',callback_data=back_o)]]
    keybo = InlineKeyboardMarkup(butt)
    img = d_ord[9]
    img = int(img, 2).to_bytes((len(img)) // 8, byteorder=sys.byteorder)
    img = io.BytesIO(img)
    photo_msg =bot.send_photo(chat_id=ch_id,photo=img)
    context.user_data['photo_id']= photo_msg.message_id
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id,message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id,text=text,reply_markup=keybo,disable_web_page_preview=True)
    context.user_data['msg'] = msg.message_id
    return a_ord

def back_s_o(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    A_ID = update.effective_user['id']
    O_ID =context.user_data['O_ID']
    photo_id = context.user_data['photo_id']
    bot.delete_message(chat_id=ch_id, message_id=photo_id)
    cursor.execute(f'''UPDATE "ORDERS"
    SET "A_ID" = NULL
    WHERE "O_ID" = {O_ID} ''')
    connect.commit()
    return orders(update,context)

def accept_ord(update: Update, context: CallbackContext) -> str:
    date = str(datetime.datetime.now().replace(microsecond=0))
    ch_id = update.effective_chat['id']
    A_ID = update.effective_user['id']
    O_ID =context.user_data['O_ID']
    photo_id = context.user_data['photo_id']
    C_O_ID = context.user_data['C_O_ID']
    user_id = update.effective_user['id']
    bot.delete_message(chat_id=ch_id, message_id=photo_id)

    if not (admin_check('A',user_id) or admin_check('O',user_id) ):
        msg_id = context.user_data['msg']
        bot.delete_message(chat_id=ch_id, message_id=msg_id)
        bot.send_message(chat_id=ch_id, text='you not admin \n send /start')
        return start(update,context)

    cursor.execute(f'''SELECT * FROM "ORDERS" WHERE "O_ID" = {O_ID}''')
    connect.commit()
    ord_f = cursor.fetchall()
    ord_d = ord_f[0]
    if ord_d[1] != 'W' :
        return orders(update, context)

    cursor.execute(f'''UPDATE "ORDERS"
SET "STATE" = 'A', "A_ID"='{A_ID}'
WHERE "O_ID" = {O_ID} ''')
    connect.commit()
    cursor.execute(f'''INSERT INTO "PROG" VALUES 
('{ord_d[2]}','{ord_d[5]}','{ord_d[6]}',{ord_d[15]},'{ord_d[7]}','{ord_d[8]}','{ord_d[9]}',{ord_d[10]},'{ord_d[11]}','{ord_d[12]}','{ord_d[13]}','{ord_d[14]}',1,'{date}') ''')
    connect.commit()

    cursor.execute(f'''SELECT "FIELD_ID" FROM "FIELD_OR_LINE" WHERE "O_ID" = {O_ID}''')
    connect.commit()
    f = cursor.fetchall()

    for i in f :
        cursor.execute(f'''INSERT INTO "FIELD_LINE"
VALUES ({ord_d[2]},{i[0]})''')

    connect.commit()
    text = f'''طلبك قد قبل  ✅'''
    bot.send_message(chat_id=C_O_ID, text=text)

    bot.send_message(chat_id=ch_id, text='DONE ✅')
    return orders(update, context)

def reject_ord(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    user_id = update.effective_user['id']
    A_ID = update.effective_user['id']
    O_ID =context.user_data['O_ID']
    photo_id = context.user_data['photo_id']
    bot.delete_message(chat_id=ch_id, message_id=photo_id)


    if not (admin_check('A',user_id) or admin_check('O',user_id) ):
        msg_id = context.user_data['msg']
        bot.delete_message(chat_id=ch_id, message_id=msg_id)
        bot.send_message(chat_id=ch_id, text='you not admin \n send /start')
        return start(update,context)


    cursor.execute(f'''SELECT * FROM "ORDERS" WHERE "O_ID" = {O_ID}''')
    connect.commit()
    ord_f = cursor.fetchall()
    ord_d = ord_f[0]
    if ord_d[1] != 'W' :
        return orders(update, context)

    cursor.execute(f'''UPDATE "ORDERS"
SET "STATE" = 'X', "A_ID" ='{A_ID}'
WHERE "O_ID" = {O_ID} ''')
    connect.commit()
    text = '''ما سبب الرفض ؟'''
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id, message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id, text=text, disable_web_page_preview=True)
    context.user_data['msg'] = msg.message_id
    return r_ord

def send_reason(update: Update, context: CallbackContext) -> str:
    reason = update.message.text
    C_O_ID = context.user_data['C_O_ID']
    text = f'''طلبك قد رفض ❌
بسبب :
{reason}'''
    bot.send_message(chat_id=C_O_ID,text=text)
    return orders(update, context)

def adman_f(update: Update, context: CallbackContext) -> str:
    ch_id = update.effective_chat['id']
    user_id = update.effective_user['id']

    if not admin_check('O', user_id):
        msg_id = context.user_data['msg']
        bot.delete_message(chat_id=ch_id, message_id=msg_id)
        bot.send_message(chat_id=ch_id, text='you not owner \n send /start')
        return start(update,context)


    cursor.execute(f'''SELECT * FROM "ADMIN" WHERE "A_TYPE" = 'A' ''')
    connect.commit()
    adms = cursor.fetchall()
    n_a = len(adms)

    text = 'admins number: n_a \n'
    butt = [
        [InlineKeyboardButton(text='🙍‍♂️ ADD 🙍‍♂️', callback_data='AD'),
        InlineKeyboardButton(text='➡ back ➡', callback_data='BK')]
    ]

    for i in adms :
        butt.append([InlineKeyboardButton(text = i[3],callback_data='A'+str(i[0]))])

    keybo = InlineKeyboardMarkup(butt)
    msg_id = context.user_data['msg']
    bot.delete_message(chat_id=ch_id, message_id=msg_id)
    msg = bot.send_message(chat_id=ch_id, text=text, reply_markup=keybo)
    context.user_data['msg'] = msg.message_id
    return cont


#-----------------------------