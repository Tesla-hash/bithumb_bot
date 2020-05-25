from datetime import datetime, timedelta
from commands.functions import *
from dbconnect.config import *
from config.config import *
from PIL import Image, ImageDraw, ImageFont
from api.BithumbGlobal import *
import telebot
from telebot import types
import requests
import datetime
import schedule
import threading
import time
import re
import os
import json
import mysql.connector

cwd = os.getcwd()

user_list = []

@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: message.text == 'Привет')
def welcome(message):
    text = 'Это бот для торговли на бирже Bithumb.\nДля работы в нем зарегиструйтесь введя команду /reg\nЗатем введите свой apiSecret и apiKey'

    username = get_username(message)
    chat_id = str(message.chat.id)
    if(user_exist(chat_id) == False):
        put_user(chat_id,username)

    bot.send_message(message.chat.id,text=text )

    #markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=False)
    #itembtn1 = types.KeyboardButton('Настроить Автопостинг')
    #markup.add(itembtn1)
    #bot.send_message(message.chat.id, "Команды:", reply_markup=markup)

@bot.message_handler(commands=['reg'])
def registation(message):
    text = 'Введите свой  API Ключ'
    message = bot.send_message(message.chat.id,text=text)
    bot.register_next_step_handler(message, process_api_secret_step)

def process_api_secret_step(message):
    apiKey = str(message.text)
    user_list.insert(0,apiKey)
    text = 'Введите свой Secret key'
    message = bot.send_message(message.chat.id,text=text)
    bot.register_next_step_handler(message, process_completion_registration)

def process_completion_registration(message):
    apiSecret = str(message.text)
    text = 'Отлично! Вы завершили регистрацию.\nТеперь у вас есть доступ к основным функциям бота'
    update_keys(user_list[0],apiSecret,str(message.chat.id))
    bot.send_message(message.chat.id,text=text)

@bot.message_handler(commands=['deposit'])
def deposit(message):
    chat_id = str(message.chat.id)
    breadcumb = get_user_keys(chat_id)
    bithumb = BithumbGlobalRestAPI(breadcumb[0],breadcumb[1])
    balance_btc = round(float(bithumb.balance('BTC')[0]['count']),4)
    balance_btc_frozen = round(float(bithumb.balance('BTC')[0]['frozen']),4)
    balance_eth = round(float(bithumb.balance('ETH')[0]['count']),4)
    balance_eth_frozen = round(float(bithumb.balance('ETH')[0]['frozen']),4)
    balance_usdt = round(float(bithumb.balance('USDT')[0]['count']),4)
    balance_usdt_frozen = round(float(bithumb.balance('USDT')[0]['frozen']),4)
    balance_bip = round(float(bithumb.balance('BIP')[0]['count']),4)
    balance_bip_frozen = round(float(bithumb.balance('BIP')[0]['frozen']),4)
    text = 'Ⓜ️ BIP: ' + str(balance_bip) + '\n❄️ Замороженный: ' + str(balance_bip_frozen)+'\n🅱️ BTC: ' + str(balance_btc) + '\n❄️ Замороженный: ' + str(balance_btc_frozen)+'\n💨 ETH: ' + str(balance_eth) + '\n❄️ Замороженный: ' + str(balance_eth_frozen)+ '\n💰 USDT: ' + str(balance_usdt) + '\n❄️ Замороженный: ' + str(balance_usdt_frozen)
    bot.send_message(message.chat.id,text=text)

@bot.message_handler(commands=['orders'])
def get_orders(message):
    bithumb = get_breadcumb(message.chat.id)
    orders = bithumb.openning_orders('BIP/USDT')
    bot.send_message(message.chat.id,text=str(orders))


@bot.message_handler(commands=['place'])
def place_order(message):
    bithumb = get_breadcumb(message.chat.id)
    bithumb.place_order('BIP/USDT','sell',0.01,700)
    text = 'Ордер успешно размещен'
    bot.send_message(message.chat.id,text=text)

@bot.message_handler(commands=['cancel'])
def cancel_order(message):
    bithumb = get_breadcumb(message.chat.id)
    bithumb.cancel_order('BIP/USDT','193328341685747712')
    text = 'Ордер успешно отменен'
    bot.send_message(message.chat.id,text=text)

@bot.message_handler(commands=['single'])
def get_single_order(message):
    bithumb = get_breadcumb(message.chat.id)
    print(bithumb.query_order('BIP/USDT','193328341685747712'))

@bot.message_handler(commands=['get'])
def orders(message):
    bithumb = get_breadcumb(message.chat.id)
    print(bithumb.orders('buy','BIP-USDT','trading'))






bot.polling(none_stop=True, interval=0)
