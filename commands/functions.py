import requests
from config.config import *
from dbconnect.config import *
from api.BithumbGlobal import *

mycursor = mydb.cursor(buffered=True)

def get_bithump_price():

    URL_BIP_COST_BITHUMP='https://global-openapi.bithumb.pro/market/data/ticker?symbol=BIP-USDT'
    bithump_url=requests.get(URL_BIP_COST_BITHUMP)
    sell_usdt=[]
    buy_usdt=[]
    data = bithump_url.json()['info'][0]

    return(data)

def send_price_bithumb(group_id):

    cost = get_bithump_price();
    price = round((float(cost['c'])),6)

    bot.send_message(chat_id="@"+str(group_id),text=str(price) + ' $')


def get_username(message):
    usr = bot.get_chat_member(message.chat.id, message.from_user.id)
    if not usr.user.username:
        return usr.user.first_name
    else:
        return usr.user.username

def user_exist(chat_id):
    mycursor.execute("SELECT chat_id FROM users LIMIT 1")
    result = mycursor.fetchone()
    mycursor.close()
    if result == None:
        return False

    else:
        mycursor.close()
        return True


def validate_time(post_time):
    time_value = post_time.split(':')
    if(int(time_value[0]) < 25):
        if(int(time_value[1]) < 61):
            return 1
        else:
            return 0
    else:
        return 0

def put_user(chat_id, name):
    sql = "INSERT INTO users (chat_id, username) VALUES (%s, %s)"
    val = (chat_id, name)
    mycursor.execute(sql, val)
    mycursor.close()
    mydb.commit()

def update_keys(apikey,apisecret,chat_id):
    sql = "UPDATE users set api_key = %s, api_secret = %s WHERE chat_id = %s"
    val = (apikey, apisecret, chat_id)
    mycursor.execute(sql, val)
    mycursor.close()
    mydb.commit()

def get_user_keys(chat_id):
    sql = "SELECT api_key, api_secret FROM users WHERE chat_id = "+chat_id
    #val = chat_id
    mycursor.execute(sql)
    result = mycursor.fetchone()
    mycursor.close()
    if result == None:
        return str('user not exists')
    else:
        return result

def get_breadcumb(chat_id):
    breadcumb = get_user_keys(str(chat_id))
    bithumb = BithumbGlobalRestAPI(breadcumb[0],breadcumb[1])

    return bithumb


#def get_balance(chat_id):
