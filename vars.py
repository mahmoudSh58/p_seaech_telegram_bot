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